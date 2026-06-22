#!/usr/bin/env python3
"""
command_notifications.py — make /ServerCommandService.hqs/SendCommands answer
with the RIGHT notifications instead of `{}`.

The command bus is the #1 suspect for "bad in-game calculations": the client
posts a batch of `*Command`s and applies the `*Notification`s the server returns
to mutate its local state (wallet, inventory, hero xp, buildings...). If the
server returns `{}` for a command that should emit a notification, the client's
state silently desyncs from the server — gold not deducted, item not added, xp
not updated, building stuck — and every later calc is wrong.

This module maps each command to the notification(s) it must produce, builds them
schema-complete (via completeness_gate, with `$type` polymorphic discriminators),
and assembles the SendCommands response. Fire-and-forget commands (tracking,
idle, *viewed, set*) correctly produce nothing.

    from command_notifications import CommandBus
    bus = CommandBus()
    response = bus.handle(request_json)   # request_json = {"commands":[{...}]}

IMPORTANT — confidence: the command->notification edges are derived from the
reversed contract names + game semantics, NOT yet byte-confirmed against a live
server for every command. Each edge carries a confidence flag; validate the
"heuristic" ones against a real session capture before trusting them in
production. The SHAPE of every notification is exact (from schemas_typed.json);
only the command->notification routing is the part to confirm.

CLI:
  command_notifications.py --table          # print the full mapping + coverage
  command_notifications.py --emit BuyCommand # show notifications for one command
  command_notifications.py --dump  > re/catalog/network/generated/command_notifications.json
"""
import argparse, json, os, re, sys
from completeness_gate import Gate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "re", "catalog", "network", "generated",
                   "command_notifications.json")

# Curated command -> notifications. "exact" = strongly implied by matching
# contract names; "heuristic" = inferred from gameplay semantics, confirm vs a
# live capture. Empty list = fire-and-forget (server returns nothing for it).
CURATED = {
    # ---- fire-and-forget (no state mutation the client must learn about) -----
    "TrackingCommand": ([], "exact"),
    "ClientIdleCommand": ([], "exact"),
    "ObjectiveViewedCommand": ([], "exact"),
    "SpellViewedCommand": ([], "exact"),
    "HeroFreeTrialInfoViewedCommand": ([], "exact"),
    "SetCastleInventoryItemViewedCommand": ([], "exact"),
    "SetLastViewedDateCommand": ([], "exact"),
    "SetLastViewedDefendLogCommand": ([], "exact"),
    "SetLastViewedNewsCommand": ([], "exact"),
    "SetProfanityFilteringCommand": ([], "exact"),

    # ---- economy / shop ------------------------------------------------------
    "BuyCommand": (["WalletUpdatedNotification", "HeroInventoryAddedNotification"], "heuristic"),
    "BuyHeroItemCommand": (["WalletUpdatedNotification", "HeroInventoryAddedNotification"], "heuristic"),
    "BuyConsumableCommand": (["WalletUpdatedNotification"], "heuristic"),
    "BuyBackCommand": (["WalletUpdatedNotification", "HeroInventoryAddedNotification",
                        "BuyBackUpdatedNotification"], "heuristic"),
    "SellHeroItemCommand": (["WalletUpdatedNotification", "HeroInventoryRemovedNotification",
                             "BuyBackUpdatedNotification"], "heuristic"),
    "SellDefenseIngredientCommand": (["WalletUpdatedNotification",
                                      "CastleInventoryChangedNotification"], "heuristic"),

    # ---- hero equipment / inventory -----------------------------------------
    "HeroEquipmentEquipCommand": (["HeroEquipmentEquipNotification"], "exact"),
    "HeroEquipmentUnequipCommand": (["HeroEquipmentUnequipNotification"], "exact"),
    "HeroEquipConsumableCommand": (["HeroConsumableEquipNotification"], "exact"),
    "HeroEquipSpellCommand": (["HeroConsumableEquipNotification"], "heuristic"),
    "HeroUnequipSpellCommand": (["HeroConsumableUnequipNotification"], "heuristic"),
    "InventoryMoveItemCommand": (["HeroInventoryUpdatedNotification"], "heuristic"),
    "InventorySwapItemCommand": (["HeroInventoryUpdatedNotification"], "heuristic"),

    # ---- consumables ---------------------------------------------------------
    "ActivateConsumableCommand": (["ConsumableActivatedNotification"], "exact"),
    "ActivateConsumableOnItemCommand": (["ConsumableActivatedNotification",
                                         "HeroInventoryUpdatedNotification"], "heuristic"),
    "ExpireExpirableCommand": (["ExpirableRemovedNotification"], "heuristic"),

    # ---- forge ---------------------------------------------------------------
    "ForgeCraftCommand": (["ForgeStartedNotification", "WalletUpdatedNotification"], "heuristic"),
    "ForgeUpgradeCommand": (["ForgeStartedNotification", "WalletUpdatedNotification"], "heuristic"),
    "ForgeReforgeCommand": (["HeroInventoryUpdatedNotification", "WalletUpdatedNotification"], "heuristic"),

    # ---- castle / buildings --------------------------------------------------
    "BuildCommand": (["BuildingUpgradeStartedNotification", "BuildInfoUpdatedNotification"], "heuristic"),
    "UpgradeBuildingCommand": (["BuildingUpgradeStartedNotification"], "exact"),
    "UpgradeProductionMineBuildingCommand": (["BuildingUpgradeStartedNotification"], "heuristic"),
    "RestoreMinesBuildingCommand": (["MineEnabledNotification"], "heuristic"),
    "HarvestMineBuildingCommand": (["MineProductionCompletedNotification",
                                    "WalletUpdatedNotification"], "heuristic"),
    "AddCastleInventoryItemCommand": (["CastleInventoryChangedNotification"], "heuristic"),
    "BoostCastleInventoryItemCommand": (["CastleInventoryChangedNotification"], "heuristic"),
    "RemoveCastleRoomCommand": (["BuildInfoUpdatedNotification"], "heuristic"),

    # ---- progression ---------------------------------------------------------
    "SelectHeroCommand": (["HeroSelectedNotification"], "exact"),
    "SetAvatarCommand": (["AttackerAvatarUpdatedNotification"], "heuristic"),
    "CompleteAssignmentCommand": (["AssignmentCompletedNotification",
                                   "WalletUpdatedNotification"], "heuristic"),
    "HarvestHeroCorpseCommand": (["HarvestingCompletedNotification",
                                  "HeroInventoryAddedNotification"], "heuristic"),

    # ---- inbox ---------------------------------------------------------------
    "InboxCollectCommand": (["InboxItemsAddedNotification"], "heuristic"),
    "InboxCollectToHeroInventoryCommand": (["HeroInventoryAddedNotification"], "heuristic"),
    "InboxCollectToHeroEquipmentCommand": (["HeroEquipmentEquipNotification"], "heuristic"),
    "InboxCollectToBuyBackCommand": (["BuyBackUpdatedNotification"], "heuristic"),
}


class CommandBus:
    TYPE_RE = re.compile(r"\.([A-Za-z0-9_]+),")   # "...Contracts.BuyCommand, ..." -> BuyCommand

    def __init__(self, gate=None):
        self.gate = gate or Gate()
        self.notif_types = {k for k in self.gate.schemas if k.endswith("Notification")}

    # ---- resolve a command's notifications, with a name-stem heuristic fallback
    def notifications_for(self, command_name):
        if command_name in CURATED:
            return CURATED[command_name]
        # heuristic: <Stem>Command -> a notification sharing the stem
        stem = command_name[:-7] if command_name.endswith("Command") else command_name
        for cand in (stem + "Notification",
                     stem.replace("Update", "Updated") + "Notification",
                     stem.replace("Add", "Added") + "Notification"):
            if cand in self.notif_types:
                return ([cand], "heuristic")
        return ([], "unknown")     # safe default: emit nothing, but flag it

    # ---- build one schema-complete notification with its $type + Index --------
    def build(self, notif_name, index, **over):
        obj = self.gate.complete(notif_name, {"Index": index}, add_type=True)
        for k, v in over.items():           # set after the gate so lists survive
            obj[k] = v
        return obj

    # ---- STATEFUL command handlers: mutate the account, emit REAL values -------
    @staticmethod
    def _hero(acc):
        heroes = acc.get("heroes") or []
        return heroes[0] if heroes else None

    @staticmethod
    def _set_slot(slots, index, key, value):
        for s in slots:
            if s.get("SlotIndex") == index:
                s[key] = value
                return
        slots.append({"SlotIndex": index, key: value})

    # ---- the player's own castle (construction) -------------------------------
    @staticmethod
    def _castle(acc):
        return acc.setdefault("castle", {
            "Level": 1, "CastleHeartRank": 1, "creatures": [], "traps": [], "rooms": [],
            "construction_used": 0, "construction_max": 1000, "next_index": 1})

    def build_info(self, acc):
        """A schema-complete BuildInfo reflecting the player's real castle state."""
        c = self._castle(acc)
        bi = self.gate.complete("BuildInfo", {
            "Level": c["Level"], "CastleHeartRank": c["CastleHeartRank"],
            "CreatureNextIndex": c["next_index"], "WorkersAvailable": c.get("workers", 2)})
        bi["CreatureArchetypes"] = c["creatures"]
        bi["TrapArchetypes"] = c["traps"]
        bi["InventoryRooms"] = c["rooms"]
        bi["CastleStats"] = self.gate.complete("CastleStats", {
            "MaxConstructionPoints": c["construction_max"],
            "TotalConstructionPoints": c["construction_used"]})
        return bi

    def _apply(self, name, cmd, acc, idx):
        """Mutate `acc` for a known command and return real notifications, or None
        if this command has no stateful handler (caller falls back to the shape)."""
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        w = acc.setdefault("wallet", {"InGameCoin": 0, "LifeForce": 0, "PremiumCash": 0,
                                      "InGameCoinStorageCapacity": 100000,
                                      "LifeForceStorageCapacity": 100000})

        if name in ("BuyCommand", "BuyHeroItemCommand"):
            price = int(cmd.get("ClientPrice") or 0)
            w["InGameCoin"] = max(0, w["InGameCoin"] - price)
            iid = acc.get("next_item", 1); acc["next_item"] = iid + 1
            item = {"ExpirableId": f"item-{iid}", "TemplateId": cmd.get("SkuCode"),
                    "AcquisitionDate": now, "SellPrice": price // 2}
            acc.setdefault("items", []).append(item)
            return [self.build("WalletUpdatedNotification", idx, NotificationType=24,
                               Amounts=[{"Amount": -price, "CurrencyType": 2}]),
                    self.build("HeroInventoryAddedNotification", idx + 1, NewlyAdded=item)]

        if name == "BuyConsumableCommand":
            price = int(cmd.get("ClientPrice") or 0)
            w["InGameCoin"] = max(0, w["InGameCoin"] - price)
            return [self.build("WalletUpdatedNotification", idx, NotificationType=24,
                               Amounts=[{"Amount": -price, "CurrencyType": 2}])]

        if name == "SellHeroItemCommand":
            gain = int(cmd.get("ClientPrice") or 0) or 50
            w["InGameCoin"] += gain
            items = acc.setdefault("items", [])
            if items:
                items.pop()
            return [self.build("WalletUpdatedNotification", idx, NotificationType=24,
                               Amounts=[{"Amount": gain, "CurrencyType": 2}]),
                    self.build("HeroInventoryRemovedNotification", idx + 1)]

        if name in ("HeroEquipSpellCommand",):
            hero = self._hero(acc)
            if hero is not None:
                self._set_slot(hero.setdefault("EquippedSpells", []),
                               int(cmd.get("SlotIndex", 0)),
                               "SpellSpecContainerId", cmd.get("SpellId"))
            return [self.build("HeroConsumableEquipNotification", idx)]

        if name == "HeroUnequipSpellCommand":
            hero = self._hero(acc)
            if hero is not None:
                hero["EquippedSpells"] = [s for s in hero.get("EquippedSpells", [])
                                          if s.get("SlotIndex") != int(cmd.get("SlotIndex", -1))]
            return [self.build("HeroConsumableUnequipNotification", idx)]

        if name == "SelectHeroCommand":
            acc["selected_hero"] = cmd.get("HeroId", acc.get("selected_hero", 0))
            return [self.build("HeroSelectedNotification", idx)]

        if name == "CompleteAssignmentCommand":
            done = acc.setdefault("completed_assignments", [])
            aid = cmd.get("AssignmentId")
            if aid is not None and aid not in done:
                done.append(aid)
            return [self.build("AssignmentCompletedNotification", idx)]

        # ---- castle construction: place / remove creatures on the player castle
        if name == "AddCastleCreatureCommand":
            c = self._castle(acc)
            cidx = c["next_index"]; c["next_index"] += 1
            c["creatures"].append({
                "Id": cidx, "SpecContainerId": cmd.get("SkuCode"),
                "AggroPropagationOffsetX": cmd.get("AggroPropagationOffsetX", 0),
                "AggroPropagationOffsetZ": cmd.get("AggroPropagationOffsetZ", 0),
                "TotemCastleBuildableId": cmd.get("TotemCastleBuildableId", 0)})
            c["construction_used"] = min(c["construction_max"], c["construction_used"] + 10)
            return [self.build("BuildInfoUpdatedNotification", idx, BuildInfo=self.build_info(acc))]

        if name in ("RemoveCastleRoomCommand", "UpdateCastleCreatureCommand"):
            c = self._castle(acc)
            if name == "RemoveCastleRoomCommand" and c["creatures"]:
                c["creatures"].pop(); c["construction_used"] = max(0, c["construction_used"] - 10)
            return [self.build("BuildInfoUpdatedNotification", idx, BuildInfo=self.build_info(acc))]

        if name in ("BuildCommand", "UpgradeBuildingCommand"):
            c = self._castle(acc)
            c["CastleHeartRank"] += 1
            c["construction_max"] += 500       # higher rank -> bigger build cap
            return [self.build("BuildingUpgradeStartedNotification", idx),
                    self.build("BuildInfoUpdatedNotification", idx + 1, BuildInfo=self.build_info(acc))]

        return None

    # ---- handle a full SendCommands request ----------------------------------
    def handle(self, request_json, acc=None, *, state=None, warn=None):
        commands = (request_json or {}).get("commands", []) or []
        notifications, idx, unknown = [], 0, []
        for cmd in commands:
            name = self._command_name(cmd)
            if not name:
                continue
            # stateful path: real mutation + real-valued notifications
            applied = self._apply(name, cmd, acc, idx) if acc is not None else None
            if applied is not None:
                notifications.extend(applied); idx += len(applied)
                continue
            # shape-only path (no stateful handler yet): emit the curated shapes
            notifs, conf = self.notifications_for(name)
            if conf == "unknown":
                unknown.append(name)
            for nname in notifs:
                notifications.append(self.build(nname, idx)); idx += 1
        if acc is not None and state is not None:
            state.save()
        if warn is not None and unknown:
            warn(unknown)
        # Real-traffic shape: {} when nothing happened, else {"Notifications": [...]}.
        return {"Notifications": notifications} if notifications else {}

    def _command_name(self, cmd):
        t = (cmd or {}).get("$type", "")
        m = self.TYPE_RE.search(t)
        if m:
            return m.group(1)
        # fallback: a bare {"Command":"X"} or {"type":"X"} form
        for k in ("Command", "command", "type", "Type"):
            if isinstance(cmd.get(k), str):
                return cmd[k]
        return None

    # ---- the full table, for inspection / handoff ----------------------------
    def table(self):
        cmds = sorted(k for k in self.gate.schemas if k.endswith("Command"))
        out = {}
        for c in cmds:
            notifs, conf = self.notifications_for(c)
            out[c] = {"notifications": notifs, "confidence": conf}
        return out


# --------------------------------------------------------------------------- CLI
def main():
    ap = argparse.ArgumentParser(description="SendCommands -> notifications")
    ap.add_argument("--table", action="store_true")
    ap.add_argument("--emit", help="show notifications a command would produce")
    ap.add_argument("--dump", action="store_true", help="write the JSON table to the catalog")
    a = ap.parse_args()
    bus = CommandBus()

    if a.emit:
        req = {"commands": [{"$type": f"HyperQuest.GameServer.Contracts.{a.emit}, "
                             "HyperQuest.GameServer.Contracts"}]}
        print(json.dumps(bus.handle(req), indent=2))
        return 0

    tbl = bus.table()
    by_conf = {}
    for c, v in tbl.items():
        by_conf.setdefault(v["confidence"], []).append(c)

    if a.dump:
        os.makedirs(os.path.dirname(OUT), exist_ok=True)
        json.dump(tbl, open(OUT, "w"), indent=1)
        print(f"[+] wrote {OUT} ({len(tbl)} commands)")
        return 0

    if a.table:
        for c in sorted(tbl):
            v = tbl[c]
            mark = {"exact": "  ", "heuristic": "~ ", "unknown": "? "}[v["confidence"]]
            print(f"{mark}{c:42s} -> {', '.join(v['notifications']) or '(none)'}")
        print(f"\ncoverage: exact={len(by_conf.get('exact',[]))}  "
              f"heuristic={len(by_conf.get('heuristic',[]))}  "
              f"unknown={len(by_conf.get('unknown',[]))}  / {len(tbl)} commands")
        if by_conf.get("unknown"):
            print("unknown (returns {} — confirm against a real capture):")
            for c in sorted(by_conf["unknown"]):
                print("   ", c)
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
