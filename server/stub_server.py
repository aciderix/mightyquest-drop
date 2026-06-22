#!/usr/bin/env python3
"""
stub_server.py — community-server stub for The Mighty Quest for Epic Loot.

Iteration 3: routes on the REAL endpoint pattern observed in live traffic
(`/<Service>Service.hqs/<Method>`, see re/catalog/network/endpoints_observed.txt)
and answers with COMPLETE, correctly-typed responses generated from the reversed
catalog (re/catalog/network/generated/examples.json — full field sets, real enum
values, `$type` discriminators). Stateful accounts/sessions, persisted. Logs
every request so unknown calls are easy to fill in.

Zero dependencies (Python 3 stdlib). Run on the game machine or a VPS:
    python3 server/stub_server.py --host 0.0.0.0 --port 8080
"""
from __future__ import annotations
import argparse, copy, datetime, json, os, re, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from completeness_gate import Gate
from command_notifications import CommandBus
from gameplay_catalog import catalog
import catalog_economy as ECO

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
NET = os.path.join(ROOT, "re/catalog/network")
EXAMPLES = json.load(open(os.path.join(NET, "generated/examples.json"))) \
    if os.path.exists(os.path.join(NET, "generated/examples.json")) else {}
GATE = Gate()            # schema-completeness for every response we emit
BUS = CommandBus(GATE)   # SendCommands -> correct notifications
PKG_VERSIONS = json.load(open(os.path.join(NET, "package_versions.json"))) \
    if os.path.exists(os.path.join(NET, "package_versions.json")) else {}
STATE_PATH = os.path.join(HERE, "state.json")
LOG_PATH = os.path.join(HERE, "requests.log")


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def envelope(payload):
    """Wrap a contract in the game's real response envelope. Confirmed against our
    captured real traffic (real_traffic.log): reads -> {"Result": <contract>};
    things that emit notifications -> {"Notifications": [...]} (and EndAttack uses
    both). Already-enveloped or empty payloads pass through untouched."""
    if not payload:
        return {}
    if isinstance(payload, dict) and (
            payload.keys() & {"Result", "Notifications", "GlobalNotifications"}):
        return payload
    return {"Result": payload}


UNCERTAIN_PATH = os.path.join(HERE, "uncertain.log")


def contract(name, **overrides):
    """A SCHEMA-COMPLETE `name`: starts from the catalog example, applies overrides,
    then runs the completeness gate so every field the client expects is present and
    nested contracts are filled (not left as {} -> silent client defaults).

    Any value we are NOT certain about (an enum resolved only by heuristic, or an
    enum name we could not resolve) is appended to uncertain.log with the contract
    and field — so if something misbehaves in game, you can grep this for the
    suspect field instead of hunting blind."""
    seed = copy.deepcopy(EXAMPLES.get(name, {}))
    seed.update(overrides)
    if name not in GATE.schemas:
        return seed
    uncertain = []
    obj = GATE.complete(name, seed, uncertain=uncertain)
    if uncertain:
        ts = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(UNCERTAIN_PATH, "a") as f:
            for u in uncertain:
                f.write(f"{ts} {name}: {u}\n")
    return obj


# ---- persistent state ------------------------------------------------------
class State:
    def __init__(self, path):
        self.path = path; self.lock = threading.Lock()
        self.data = {"accounts": {}, "sessions": {}, "next_id": 1}
        if os.path.exists(path):
            try: self.data.update(json.load(open(path)))
            except Exception: pass

    def save(self):
        json.dump(self.data, open(self.path + ".tmp", "w"), indent=1)
        os.replace(self.path + ".tmp", self.path)

    def login(self, identity):
        with self.lock:
            acc = self.data["accounts"].get(identity)
            if not acc:
                aid = self.data["next_id"]; self.data["next_id"] += 1
                acc = {"AccountId": aid, "DisplayName": "", "Privileges": 9,
                       # the loot economy lives here, persisted across requests.
                       # starting gold = DEFAULTACCOUNT.IGC (1000) from the catalog
                       "wallet": {"InGameCoin": 1000, "LifeForce": 0, "PremiumCash": 0,
                                  "InGameCoinStorageCapacity": 100000,
                                  "LifeForceStorageCapacity": 100000},
                       "items": [], "next_item": 1,
                       "heroes": [], "selected_hero": 0,
                       # social / level-3 state
                       "friends": [], "guild": None, "guild_invitations": [],
                       "inbox": [], "messages": [],
                       "defend_log": [], "trophy": 0}
                self.data["accounts"][identity] = acc
            token = f"tok-{acc['AccountId']}-{os.urandom(4).hex()}"
            self.data["sessions"][token] = acc["AccountId"]
            self.save(); return acc, token

    def account(self, token):
        aid = self.data["sessions"].get(token)
        return next((a for a in self.data["accounts"].values() if a["AccountId"] == aid), None)

    def award(self, acc, gold=0, lifeforce=0, item_template=None):
        """Apply attack rewards to an account and persist them."""
        with self.lock:
            acc.setdefault("wallet", {"InGameCoin": 0, "LifeForce": 0, "PremiumCash": 0,
                                      "InGameCoinStorageCapacity": 100000,
                                      "LifeForceStorageCapacity": 100000})
            acc["wallet"]["InGameCoin"] += gold
            acc["wallet"]["LifeForce"] += lifeforce
            new_item = None
            if item_template is not None:
                iid = acc.get("next_item", 1); acc["next_item"] = iid + 1
                new_item = {"ExpirableId": f"item-{iid}", "TemplateId": item_template,
                            "AcquisitionDate": now(), "SellPrice": 50}
                acc.setdefault("items", []).append(new_item)
            self.save(); return new_item


STATE = State(STATE_PATH)


# ---- game endpoints (/<Service>Service.hqs/<Method>) ------------------------
def ep_account_information(req, acc):
    # Privileges must be 9 for a new account or hero-selection never shows.
    acc = acc or {}
    wallet = acc.get("wallet", {"InGameCoin": 1000, "LifeForce": 0, "PremiumCash": 0,
                                "InGameCoinStorageCapacity": 100000,
                                "LifeForceStorageCapacity": 100000})
    inv = contract("AccountInventory")
    inv["HeroItems"] = acc.get("items", [])      # reflect looted items
    inv["InventoryTabCount"] = DEFAULT_ACCOUNT.get("Inventory", {}).get("InventoryTabCount", 2)
    ai = contract("AccountInformation", AccountId=acc.get("AccountId", 1),
                  DisplayName=acc.get("DisplayName", ""), Privileges=9,
                  # real new-player state from AccountTemplates/DEFAULTACCOUNT
                  AvatarId=acc.get("AvatarId", DEFAULT_ACCOUNT.get("AvatarId", 10)),
                  CountryCode=DEFAULT_ACCOUNT.get("CountryCode", "CA"),
                  ProfanityFiltering=DEFAULT_ACCOUNT.get("ProfanityFiltering", True),
                  CastleRenovationLevel=DEFAULT_ACCOUNT.get("CastleRenovationLevel",
                                                            "RenovationLevel0"),
                  Wallet=wallet, Inventory=inv,
                  CompletedAssignments=len(acc.get("completed_assignments", [])),
                  SelectedHeroId=acc.get("selected_hero", 0))
    ai["Heroes"] = acc.get("heroes", [])         # the player's real hero(es)
    if acc.get("castle"):                        # reflect the player's built castle
        ai["BuildInfo"] = BUS.build_info(acc)
    # reflect the live social state (confirmed delivery channel for level-3 data)
    ai["Friends"] = acc.get("friends", [])
    ai["GuildInvitations"] = acc.get("guild_invitations", [])
    ai["Inbox"] = acc.get("inbox", [])
    ai["Guild"] = acc.get("guild") or {}        # cleared when the player has no guild
    return ai


def ep_choose_display_name(req, acc):
    name = (req.json.get("displayName") or req.json.get("DisplayName") or "Player")
    if acc:
        acc["DisplayName"] = name; STATE.save()
    return contract("AccountSummary", AccountId=(acc or {}).get("AccountId", 1), DisplayName=name)


def ep_choose_first_hero(req, acc):
    """Create the player's first hero from the real HeroTemplate (Knight=2,
    Archer=3, Mage=4, Runaway=5) so the hero has a real loadout, not an empty one."""
    body = req.json or {}
    tid = body.get("heroTemplateId") or body.get("HeroTemplateId") or 2
    hero = build_hero(tid)
    if acc:
        acc["heroes"] = [hero]
        acc["selected_hero"] = hero.get("HeroSpecContainerId", tid)
        STATE.save()
    return {}


CAT = catalog()
DEFAULT_ACCOUNT = CAT.get("AccountTemplates", CAT.find_one("AccountTemplates", "DEFAULTACCOUNT"))
_LVL_RE = re.compile(r"PVE_(\d+)_")


def _find_key(o, key):
    if isinstance(o, dict):
        for k, v in o.items():
            if k == key:
                return v
            r = _find_key(v, key)
            if r is not None:
                return r
    elif isinstance(o, list):
        for x in o:
            r = _find_key(x, key)
            if r is not None:
                return r
    return None


# real hero XP curve (cumulative thresholds) from GeneralSettings/HEROSETTINGS
XP_PER_LEVEL = _find_key(CAT.get("GeneralSettings", "HEROSETTINGS"), "XpPerLevel") or [0]


def level_for_xp(total):
    return max(1, sum(1 for th in XP_PER_LEVEL if total >= th))


def build_hero(template_id):
    """Build a Hero from the real HeroTemplate. Real lists/objects (Equipment,
    EquippedSpells, EquippedConsumables) are set after the gate so they survive."""
    if not CAT.has("HeroTemplates", template_id):
        template_id = 2  # default Knight
    t = CAT.get("HeroTemplates", template_id)
    h = contract("Hero",
                 HeroSpecContainerId=t.get("HeroSpecContainerId", template_id),
                 Level=t.get("Level", 1), XP=t.get("XP", 0))
    h["Equipment"] = t.get("Equipment", {})
    h["EquippedSpells"] = t.get("EquippedSpells", [])
    h["EquippedConsumables"] = t.get("EquippedConsumables", [])
    return h


def _castle_level(name):
    m = _LVL_RE.search(name or "")
    return max(1, int(m.group(1))) if m else 1


def _castle_from_player(rival):
    """Build an AttackInfo.Castle from another player's BUILT, published castle (PvP)."""
    pc = rival.get("castle") or {}
    creatures = pc.get("creatures", [])
    specs = sorted({cr.get("SpecContainerId") for cr in creatures if cr.get("SpecContainerId")})
    c = contract("Castle", AccountId=rival.get("AccountId", 0),
                 AccountDisplayName=rival.get("DisplayName") or "Rival",
                 LayoutId=1, ThemeId=0)
    c["Rooms"] = [{"Id": 1, "Creatures": creatures}]
    c["CreatureTiers"] = [{"SpecContainerId": s} for s in specs]
    c["TrapTiers"] = []
    return c, pc.get("Level", 1)


def ep_start_attack(req, acc):
    """Serve a REAL castle: PvP (another player's built+published castle) when a
    DefenderAccountId targets one, else a real catalog PvE castle (default: first
    tutorial castle). Real lists are set AFTER the gate so it cannot clobber them."""
    body = req.json or {}
    # --- PvP: attack another player's published castle -----------------------
    defid = body.get("DefenderAccountId") or body.get("defenderAccountId")
    if defid and defid != (acc or {}).get("AccountId"):
        rival = next((a for a in STATE.data["accounts"].values()
                      if a.get("AccountId") == defid and (a.get("castle") or {}).get("published")), None)
        if rival:
            castle, level = _castle_from_player(rival)
            ai = contract("AttackInfo", Level=level, CastleHeartRank=max(1, level // 5),
                          AdjustedHeroLevel=level, IsTutorial=False, AttackType=1)
            ai["Castle"] = castle
            hero = (acc.get("heroes") if acc else None) or []
            ai["Hero"] = hero[0] if hero else build_hero(2)
            if acc is not None:
                acc["current_attack"] = None
                acc["current_pvp"] = defid          # remember the PvP target
                STATE.save()
            return ai
    cid = body.get("CastleId") or body.get("castleId")
    if not (cid and CAT.has("Castles", cid)):
        cid = CAT.find_one("Castles", "PVE_00_TUTORIAL_01")
    cas = CAT.get("Castles", cid)
    name = CAT.name("Castles", cid)
    level = _castle_level(name)

    castle = contract("Castle",
                      AccountId=cas.get("AccountId", 2),
                      AccountDisplayName=name,
                      LayoutId=cas.get("LayoutId", 1),
                      ThemeId=cas.get("ThemeId", 0),
                      OasisNameId=cas.get("OasisName", 0))
    # real content, kept verbatim from the catalog (post-gate so it survives)
    castle["Rooms"] = cas.get("Rooms", [])
    castle["CreatureTiers"] = cas.get("CreatureTiers", [])
    castle["TrapTiers"] = cas.get("TrapTiers", [])

    ai = contract("AttackInfo",
                  Level=level,
                  CastleHeartRank=max(1, level // 5),
                  AdjustedHeroLevel=level,
                  IsTutorial=bool(cas.get("IsTutorialCastle")))
    ai["Castle"] = castle
    # the attacker's real hero loadout (skills/equipment), not an empty bar
    hero = (acc.get("heroes") if acc else None) or []
    ai["Hero"] = hero[0] if hero else build_hero(2)
    if acc is not None:
        acc["current_attack"] = cid          # remember target for EndAttack loot
        STATE.save()
    return ai


def _pve_castles():
    """All real PvE castles from the catalog: (id, name, level)."""
    out = []
    for cid in CAT.ids("Castles"):
        name = CAT.name("Castles", cid)
        if name.startswith("PVE_"):
            out.append((cid, name, _castle_level(name)))
    return out


def _castle_info(cid, name, level):
    cas = CAT.get("Castles", cid)
    rooms = cas.get("Rooms") if isinstance(cas.get("Rooms"), list) else []
    info = contract("CastleInfo",
                    Level=level, CastleType=1, Difficulty=max(1, level),
                    AttackabilityStatus=1, IsCastleAttackable=True,
                    RoomCount=len(rooms), VictoryConditionLevel=1)
    info["DefenderAccountSummary"] = contract("CastleSummary",
                                              AccountId=cas.get("AccountId", cid),
                                              AccountDisplayName=name, Level=level,
                                              IsPublished=True)
    return info


def ep_get_attack_selection_list(req, acc):
    """The real PvE castle roster, grouped by level (CastlesByLevel)."""
    by_level = {}
    for cid, name, level in _pve_castles():
        by_level.setdefault(level, []).append(_castle_info(cid, name, level))
    levels = [contract("AttackSelectionByLevelResult", Level=lvl) for lvl in sorted(by_level)]
    for entry, lvl in zip(levels, sorted(by_level)):
        entry["Castles"] = by_level[lvl]
    res = contract("AttackSelectionResult")
    res["CastlesByLevel"] = levels
    return res


def ep_get_castle_info(req, acc):
    body = req.json or {}
    cid = body.get("CastleId") or body.get("castleId")
    if not (cid and CAT.has("Castles", cid)):
        cid = CAT.find_one("Castles", "PVE_00_TUTORIAL_01")
    name = CAT.name("Castles", cid)
    return _castle_info(cid, name, _castle_level(name))


def _add_item(acc, src):
    """Append a real catalog-described item (e.g. a scripted CustomLoot equipment)
    to the account inventory and persist it."""
    iid = acc.get("next_item", 1); acc["next_item"] = iid + 1
    item = {"ExpirableId": f"item-{iid}", "TemplateId": src.get("TemplateId"),
            "ArchetypeId": src.get("ArchetypeId"), "ItemLevel": src.get("ItemLevel", 1),
            "PrimaryStatsModifiers": src.get("PrimaryStatsModifiers", []),
            "AcquisitionDate": now(), "SellPrice": 50}
    acc.setdefault("items", []).append(item); STATE.save()
    return item


def ep_get_castles_for_sale(req, acc):
    """The real purchasable starter castles (BUY_* in the catalog)."""
    sale = []
    for cid in CAT.ids("Castles"):
        name = CAT.name("Castles", cid)
        if name.startswith("BUY_"):
            sale.append(contract("CastleForSale", SaleId=cid, UbisoftCastleId=cid,
                                 DebugName=name, CanBePurchased=True, IsInteractive=True,
                                 IsStartupCastle=("BASIC_ROYAL_A" in name)))
    res = contract("CastlesForSaleSelectionResult")
    res["CastlesForSale"] = sale
    return res


# AttackCompletionType (client JS enum): TreasureRoom=0 Retry=1 Exit=2 Escape=3 Incomplete=4
COMPLETION = {"TreasureRoom": 0, "Retry": 1, "Exit": 2, "Escape": 3, "Incomplete": 4}


def ep_end_attack(req, acc):
    """End of attack. ALWAYS returns a real EndAttackInfo (so the client navigates
    correctly even on escape/defeat -- never the empty {} that broke the post-combat
    state). On a clean win it also pays the loot and emits the reward notifications,
    honoring the castle's scripted CustomAttackerReward."""
    body = req.json or {}
    completion = body.get("completionType", body.get("CompletionType", "TreasureRoom"))
    won = body.get("victory", body.get("Victory", True)) and \
          completion not in ("Escape", "Exit", "Incomplete")
    comp_int = COMPLETION.get(completion, 0 if won else COMPLETION["Escape"])

    # PvP: record the defend log on the rival + adjust trophies (server-authoritative)
    pvp = (acc or {}).get("current_pvp")
    pvp_rooms = None
    if acc and pvp and won:
        rival = next((a for a in STATE.data["accounts"].values()
                      if a.get("AccountId") == pvp), None)
        if rival:
            entry = contract("DefendLogEntry", AttackId=f"atk-{pvp}-{len(rival.get('defend_log', []))}",
                             CompletionType=COMPLETION.get(completion, 0),
                             HeroSpecContainerId=acc.get("selected_hero", 0))
            entry["AttackerAccountSummary"] = contract("AccountSummary",
                AccountId=acc["AccountId"], AccountDisplayName=acc.get("DisplayName") or "Player", Level=1)
            rival.setdefault("defend_log", []).insert(0, entry)
            pvp_rooms = [{"Creatures": (rival.get("castle") or {}).get("creatures", [])}]
            # real trophy gain: matchmaking difficulty -> TrophyGainBuckets
            atk_level = (((acc.get("heroes") or [{}])[0]) or {}).get("Level", 1)
            d_rating = ECO.castle_rating(pvp_rooms)
            gain = ECO.trophy_gain(atk_level, d_rating)
            acc["trophy"] = acc.get("trophy", 0) + gain
            rival["trophy"] = max(0, rival.get("trophy", 0) - max(1, gain // 3))
    if acc:
        acc["current_pvp"] = None

    cid = (acc or {}).get("current_attack")
    has_cas = bool(cid and CAT.has("Castles", cid))
    cas = CAT.get("Castles", cid) if has_cas else {}
    level = _castle_level(CAT.name("Castles", cid)) if has_cas else 1
    hero_level = (((acc or {}).get("heroes") or [{}])[0] or {}).get("Level", 1)

    if not (acc and won):
        # defeat / escape: no reward, but a complete EndAttackInfo for clean nav
        info = contract("EndAttackInfo", CompletionType=comp_int,
                        IsCompletionRewardMissed=True, EnterTreasureRoom=False,
                        TotalGold=0, TotalLifeForce=0, TotalXp=0,
                        DefenderCastleId=cid or 0,
                        DefenderCastleType=cas.get("CastleType", 1) if has_cas else 1,
                        HeroLevel=hero_level, VictoryConditionType=0)
        return {"Result": info}

    reward = cas.get("CustomAttackerReward") or {}
    # REAL loot: sum each killed creature's catalog loot/xp over the actual castle
    # (PvP -> rival's placed creatures, PvE -> the catalog castle). Server-summed,
    # so the player can never loot more than the castle contains (anti-cheat).
    rooms = pvp_rooms if pvp_rooms is not None else (cas.get("Rooms") if has_cas else [])
    g_sum, xp_sum = ECO.castle_rewards(rooms)
    gold = g_sum or 10 * max(1, level)        # fallback only if nothing summable
    xp = xp_sum or 10 * max(1, level)
    lifeforce = max(1, gold // 3)
    STATE.award(acc, gold=gold, lifeforce=lifeforce)
    notifs = [contract("WalletUpdatedNotification", Index=0, NotificationType=24, Amounts=[
        {"Amount": gold, "CurrencyType": 2},        # IGC (gold)
        {"Amount": lifeforce, "CurrencyType": 4}])]  # LifeForce

    idx = 1
    if not reward.get("DisableItemDrop"):
        item = None
        hero_key = str(acc.get("selected_hero", 2))
        for loot in reward.get("CustomLoots", []):
            phi = loot.get("PerHeroItem") or {}
            if phi.get(hero_key):
                item = _add_item(acc, phi[hero_key][0]); break
        if item is None:
            # real generated drop: catalog quality roll + catalog stat bonuses
            iid = acc.get("next_item", 1); acc["next_item"] = iid + 1
            item = ECO.generate_item(ECO.random_equipment_template(), level,
                                     f"item-{iid}", now=now())
            acc.setdefault("items", []).append(item); STATE.save()
        notifs.append(contract("HeroInventoryAddedNotification", Index=idx, NewlyAdded=item)); idx += 1

    # hero progression: the win grants XP; crossing a threshold levels the hero up
    hero = (acc.get("heroes") or [None])[0]
    if hero is not None:
        old_lvl = hero.get("Level", 1)
        hero["XP"] = hero.get("XP", 0) + xp
        hero["Level"] = level_for_xp(hero["XP"])
        STATE.save()
        notifs.append(contract("HeroXpChangedNotification", Index=idx,
                               HeroSpecContainerId=hero.get("HeroSpecContainerId", 0),
                               Level=hero["Level"], LevelChanged=(hero["Level"] > old_lvl),
                               TotalXp=hero["XP"], XpAdded=xp))

    info = contract("EndAttackInfo", CompletionType=comp_int, IsCompletionRewardMissed=False,
                    EnterTreasureRoom=True, DefenderCastleId=cid or 0,
                    DefenderCastleType=cas.get("CastleType", 1) if has_cas else 1,
                    HeroLevel=hero_level, VictoryConditionType=3, VictoryConditionLevel=1,
                    TotalGold=gold, KillsGold=gold, TotalLifeForce=lifeforce,
                    KillsLifeForce=lifeforce, TotalXp=xp, KillsXp=xp)
    return {"Result": info, "Notifications": notifs}


def ep_social(service, method, req, acc):
    """Stateful level-3 services (guild, friends, news, ...). Mutations are
    reflected in AccountInformation (the confirmed channel). Returns a response
    dict, or None to fall through to the schema-complete example fallback."""
    if acc is None:
        return None
    s, m = service.lower(), method.lower()
    body = req.json or {}

    if "friend" in s:                                  # ---- FRIENDS ----
        friends = acc.setdefault("friends", [])
        if any(k in m for k in ("add", "invite", "request", "send", "accept")):
            fid = body.get("FriendAccountId") or body.get("AccountId") or (200 + len(friends))
            friends.append({"FriendAccountId": fid,
                            "FriendDisplayName": body.get("DisplayName") or f"Friend{fid}",
                            "HasAccepted": True, "IsCastleAttackable": True})
            STATE.save(); return {}
        if any(k in m for k in ("remove", "delete", "decline", "cancel")):
            if friends:
                friends.pop()
            STATE.save(); return {}
        return None                                    # reads: AccountInformation carries it

    if "guild" in s:                                   # ---- GUILD ----
        if "create" in m or "join" in m:
            acc["guild"] = contract("Guild", Id=body.get("GuildId", 1), Rank=8,
                                    DisplayName=body.get("DisplayName") or body.get("GuildName")
                                    or "ClaudeGuild")
            STATE.save(); return {"Result": acc["guild"]}
        if "leave" in m or "quit" in m:
            acc["guild"] = None; STATE.save(); return {}
        if "search" in m:
            return contract("GuildSearchResult")
        if "get" in m and acc.get("guild"):
            return {"Result": acc["guild"]}
        return None

    if "news" in s:                                    # ---- NEWS ----
        return contract("NewsResult")

    if "shop" in s:                                    # ---- SHOP (real SKUs) ----
        res = contract("ShopResult") if "ShopResult" in GATE.schemas else {}
        skus = [contract("ShopSku", Code=str(k.get("Code")), ItemCount=k.get("ItemCount", 1),
                         InternalDescription=k.get("InternalDescription", ""), IsActive=True)
                for k in ECO.shop_skus()]
        if isinstance(res, dict):
            res["Skus"] = skus
            return {"Result": res}
        return {"Result": {"Skus": skus}}

    if "leaderboard" in s or "league" in s:            # ---- LEADERBOARD ----
        ranked = sorted(STATE.data["accounts"].values(),
                        key=lambda x: x.get("trophy", 0), reverse=True)
        entries = []
        for r in ranked[:100]:
            e = contract("LeaderboardEntry", Score=r.get("trophy", 0))
            e["AccountSummary"] = contract("AccountSummary", AccountId=r.get("AccountId", 0),
                                           AccountDisplayName=r.get("DisplayName") or "Player",
                                           Level=1)
            entries.append(e)
        return {"Result": {"Entries": entries}}

    if "battlelog" in s or "defendlog" in s or "defend" in s:   # ---- DEFEND LOG ----
        dl = contract("DefendLog")
        dl["DefendLogEntries"] = acc.get("defend_log", [])
        return {"Result": dl}

    if "inbox" in s:                                   # ---- INBOX (read) ----
        return {"Result": {"Items": acc.get("inbox", [])}}

    return None                                        # other reads -> example fallback


# method name -> handler(req, acc) ; default below serves a matching example
ENDPOINTS = {
    "GetAccountInformation": ep_account_information,
    "ChooseDisplayName":     ep_choose_display_name,
    "GetAttackSelectionList": ep_get_attack_selection_list,
    "GetCastleInfo":          ep_get_castle_info,
    "StartAttack":            ep_start_attack,
    "EndAttack":              ep_end_attack,
    "GetCastlesForSale":      lambda r, a: ep_get_castles_for_sale(r, a),
    "ChooseFirstHero":        ep_choose_first_hero,
    "SendCommands":           lambda r, a: BUS.handle(r.json, a, state=STATE),  # stateful bus
    "CheckSeasonalCompetitionRewards": lambda r, a: {},
}

# boot / launcher-side endpoints (the local proxy / distribution layer)
def boot_config(req):
    return contract("BootConfig", DistributionServiceUrl=req.base, GameWebsiteUrl=req.base,
                    EnvironmentName="community", WorldName="community")


def distribution(req):
    # echo the client package versions so the patch-check passes
    return PKG_VERSIONS or {}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    @property
    def base(self):
        h = self.headers.get("Host") or f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        return f"http://{h}"

    def token(self):
        a = self.headers.get("Authorization", "")
        return a[7:] if a.lower().startswith("bearer ") else self.headers.get("X-Connection-Token")

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        try: self._json = json.loads(body) if body else {}
        except Exception: self._json = {}
        return body

    @property
    def json(self): return self._json

    def _log(self, body):
        line = f"{now()} {self.command} {self.path} len={len(body)}"
        print(line)
        with open(LOG_PATH, "a") as f:
            f.write(line + ("\n    " + body[:1500].decode("latin1", "replace") if body else "") + "\n")

    def _send(self, obj, code=200):
        p = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(p)))
        self.end_headers(); self.wfile.write(p)

    def _handle(self):
        body = self._read(); self._log(body)
        path = self.path.split("?")[0]
        # game RPC: /<Service>Service.hqs/<Method>
        m = re.match(r"/([A-Za-z]+)Service\.hqs/([A-Za-z]+)", path)
        if m:
            service, method = m.group(1), m.group(2)
            acc = STATE.account(self.token())
            if acc is None:
                acc, _ = STATE.login(self.headers.get("X-Steam-Ticket", "anonymous"))
            h = ENDPOINTS.get(method)
            if h:
                return self._send(envelope(h(self, acc)))
            social = ep_social(service, method, self, acc)   # stateful level-3 services
            if social is not None:
                return self._send(envelope(social))
            return self._send(envelope(self._guess(method)))
        low = path.lower()
        if "login" in low or "account" in low and "creation" in low:
            acc, token = STATE.login(self.json.get("steamticket", "anonymous"))
            return self._send(contract("LoginResult", AccountId=acc["AccountId"],
                                        ConnectionToken=token, ProfileId=str(acc["AccountId"])))
        if "bootconfig" in low:
            return self._send(boot_config(self))
        if "package" in low or "distribution" in low or "version" in low:
            return self._send(distribution(self))
        # fall back: serve an example matching the last path segment
        seg = os.path.splitext(path.rstrip("/").split("/")[-1])[0]
        return self._send(EXAMPLES.get(seg, {}))

    def _guess(self, method):
        """no handler: serve an example whose contract name appears in the method."""
        for c in EXAMPLES:
            if c.lower() in method.lower():
                return EXAMPLES[c]
        return {}

    do_GET = do_POST = do_PUT = _handle

    def log_message(self, *a): pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--tls", action="store_true",
                    help="serve HTTPS using the MQEL CA/server cert (for the game's "
                         "curl, which needs TLS on :443 to gs.themightyquest.com)")
    ap.add_argument("--cert"); ap.add_argument("--key")
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    scheme = "http"
    if a.tls:
        import ssl
        cert, key = a.cert, a.key
        if not (cert and key):
            # reuse the launcher's two-level PKI so the game (and ca.pem) trust us
            import mqel_launcher as L
            cert, key, _ = L.ensure_certs()
        ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ctx.load_cert_chain(cert, key)
        ctx.minimum_version = ssl.TLSVersion.TLSv1     # 2013 client
        ctx.maximum_version = ssl.TLSVersion.TLSv1_2
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
        scheme = "https"
    print(f"[+] MQEL stub on {scheme}://{a.host}:{a.port}  ({len(EXAMPLES)} contract examples)")
    print(f"[+] stateful routing /<Service>Service.hqs/<Method>; state {STATE_PATH}; log {LOG_PATH}")
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\n[+] stopped")


if __name__ == "__main__":
    main()
