#!/usr/bin/env python3
"""catalog_economy.py — REAL economy/loot/stats, sourced from the decrypted catalog.

Replaces the earlier guessed numbers (sell=50, loot=template 1001) with the
game's own formulas, read from GameplaySettings:
  - sell price       : HEROITEMSELLSETTINGS (base[category] x quality x rarity)
  - drop quality     : ATTACKERREWARDSETTINGS.ItemDropByType (frequencies + level gates)
  - reward type      : UNIVERSALDROPSETTINGS.RewardTypeTable
  - item stat bonuses: EQUIPMENTGENERATIONSETTINGS.MagicalProperties
                       (BaseValue + ValuePerLevel*itemLevel, gated by MinItemQuality)
  - hero stats       : sum of equipped items' magical properties

Where the catalog fully specifies a formula it is implemented exactly; the only
approximations are noted inline (e.g. gold from creature count, since the
SpecContainerId->creature-spec map is not in the reversed catalog).
"""
from __future__ import annotations
import random
from gameplay_catalog import catalog

CAT = catalog()


def _g(cat, key):
    d = CAT.get(cat, key)
    return d.get("GAMEPLAY", d) if isinstance(d, dict) else d


def _first_list(d):
    if isinstance(d, list):
        return d
    if isinstance(d, dict):
        for v in d.values():
            if isinstance(v, list):
                return v
    return []


_SELL = _g("HeroItems", "HEROITEMSELLSETTINGS")
_GEN = _g("HeroItems", "EQUIPMENTGENERATIONSETTINGS")
_REWARD = _g("GeneralSettings", "ATTACKERREWARDSETTINGS")
_UNIVERSAL = _g("GeneralSettings", "UNIVERSALDROPSETTINGS")
_TYPES = {t["Id"]: t.get("HeroItemCategoryType")
          for t in _g("HeroItems", "HEROITEMTYPES").get("ItemTypeList", [])}
_TEMPLATES = {it["Id"]: it for it in _first_list(_g("HeroItems", "HEROITEMTEMPLATES"))}

_QORDER = {"Basic": 0, "Magic": 1, "Exceptional": 2, "Legendary": 3, "Epic": 4}


# ── sell price (fully catalog-specified) ────────────────────────────────────
def category_of(template_id):
    return _TYPES.get(_TEMPLATES.get(template_id, {}).get("HeroItemTypeId"))


def sell_price(template_id, quality="Basic", rarity="Common"):
    base = _SELL.get("SellBasePrices", {}).get(category_of(template_id), 1)
    qm = _SELL.get("SellQualityModifiers", {}).get(quality, 1)
    rm = _SELL.get("SellRarityModifiers", {}).get(rarity, 1)
    return max(1, round(base * qm * rm))


# ── quality roll (ATTACKERREWARDSETTINGS frequencies, level-gated) ───────────
def _quality_freq(level):
    for band in _REWARD.get("ItemDropByType", {}).get("User", []):
        if band.get("LevelFrom", 1) <= level <= band.get("LevelTo", 999):
            freq = dict(band.get("ItemQualityFrequency", {}))
            # zero-out qualities whose level-range modifier is 0 at this level
            for r in band.get("ItemQualityStepModifiersByLevelRanges", []):
                if r.get("Min", 1) <= level <= r.get("Max", 999):
                    for q, m in r.get("QualityStepModifier", {}).items():
                        if m == 0:
                            freq.pop(q, None)
                    break
            return freq
    return {}


def roll_quality(level, rng=random):
    freq = _quality_freq(level)
    for q in ("Epic", "Legendary", "Exceptional", "Magic"):   # rarest first
        n = freq.get(q)
        if n and rng.random() < 1.0 / n:
            return q
    return "Basic"


def roll_rarity(quality, rng=random):
    table = _GEN.get("RarityLootTable", {}).get(quality, {"Common": 1})
    roll = rng.random(); acc = 0.0
    for rar, p in table.items():
        acc += p
        if roll <= acc:
            return rar
    return "Common"


# ── item stat generation (EQUIPMENTGENERATIONSETTINGS.MagicalProperties) ────
def generate_stats(level, quality, rng=random):
    out = []
    for mp in _GEN.get("MagicalProperties", []):
        if _QORDER.get(quality, 0) < _QORDER.get(mp.get("MinItemQuality", "Basic"), 0):
            continue
        if rng.random() < mp.get("RandomChance", 0):
            val = mp.get("BaseValue", 0) + mp.get("ValuePerLevel", 0) * level
            out.append({"Id": mp["Id"], "Value": round(val, 2),
                        "Name": mp.get("DebugName", str(mp["Id"]))})
    return out


def generate_item(template_id, level, item_id, quality=None, rng=random, now=""):
    """A real generated equipment item with catalog-sourced stats + sell price."""
    if quality is None:
        quality = roll_quality(level, rng)
    rarity = roll_rarity(quality, rng)
    stats = generate_stats(level, quality, rng)
    return {"ExpirableId": item_id, "TemplateId": template_id, "ItemLevel": level,
            "ArchetypeId": _TEMPLATES.get(template_id, {}).get("ArchetypeId", 0),
            "Quality": quality, "Rarity": rarity,
            "MagicalProperties": stats,
            "PrimaryStatsModifiers": [s["Value"] for s in stats[:3]],
            "SellPrice": sell_price(template_id, quality, rarity),
            "AcquisitionDate": now}


def random_equipment_template(rng=random):
    ids = list(_TEMPLATES)
    return rng.choice(ids) if ids else 1


# ── hero stats = sum of equipped items' magical properties ──────────────────
def hero_equipped_stats(hero):
    total = {}
    for item in (hero.get("Equipment") or {}).values():
        if isinstance(item, dict):
            for mp in item.get("MagicalProperties", []):
                total[mp["Id"]] = round(total.get(mp["Id"], 0) + mp.get("Value", 0), 2)
    return total


# ── trophies (matchmaking difficulty -> crown gain from TrophyGainBuckets) ──
_MM = _g("GeneralSettings", "MATCHMAKINGSETTINGS").get("MatchmakingTable", [])
_TROPHY_BUCKETS = _g("GeneralSettings", "ATTACKADVISORSETTINGS").get("TrophyGainBuckets", [])


def _mm_row(level):
    for r in _MM:
        if r.get("AttackerLevel") == level:
            return r
    return _MM[min(len(_MM) - 1, max(0, level - 1))] if _MM else {}


def castle_rating(rooms):
    """Defense rating ~= sum of the castle's creatures' construction points (strength)."""
    total = 0
    for room in (rooms or []):
        for cr in (room.get("Creatures") or []):
            total += creature_cp(cr.get("SpecContainerId"))
    return total


def difficulty(attacker_level, defender_rating):
    r = _mm_row(attacker_level)
    if defender_rating < r.get("MediumThreshold", 7):
        return "Easy"
    if defender_rating < r.get("HardThreshold", 12):
        return "Medium"
    return "Hard"


def _bucket_mid(i):
    b = _TROPHY_BUCKETS[max(0, min(i, len(_TROPHY_BUCKETS) - 1))] if _TROPHY_BUCKETS else {}
    lo = b.get("MinCrownGain", b.get("MaxCrownGain", 10))
    hi = b.get("MaxCrownGain", lo)
    return round((lo + hi) / 2)


def trophy_gain(attacker_level, defender_rating):
    """Crowns won, from TrophyGainBuckets, by matchmaking difficulty
    (Easy/Medium/Hard -> low/main/high bucket)."""
    diff = difficulty(attacker_level, defender_rating)
    return {"Easy": _bucket_mid(1), "Medium": _bucket_mid(2),
            "Hard": _bucket_mid(len(_TROPHY_BUCKETS) - 1)}.get(diff, _bucket_mid(2))


# ── shop (real SKUs from ShopSettings) ──────────────────────────────────────
try:
    _shop_names = CAT.names("ShopSettings")
    _SHOP = _g("ShopSettings", _shop_names[0]) if _shop_names else {}
except Exception:
    _SHOP = {}
_SKUS = {str(s.get("Code")): s for s in (_SHOP.get("Skus", []) if isinstance(_SHOP, dict) else [])}


def shop_skus():
    return list(_SKUS.values())


def sku(code):
    return _SKUS.get(str(code))


def sku_price(code, default=0):
    s = _SKUS.get(str(code))
    return int((s or {}).get("Price", {}).get("Amount", default)), \
           int((s or {}).get("Price", {}).get("CurrencyType", 2))


# ── per-creature values (SpecContainerId == Creatures catalog id, direct map) ─
def _creature_field(spec_id, key, default=0):
    if not CAT.has("Creatures", spec_id):
        return default
    g = CAT.get("Creatures", spec_id).get("GAMEPLAY", [])
    for comp in (g if isinstance(g, list) else []):
        if isinstance(comp, dict) and key in comp:
            return comp[key]
    return default


def creature_loot(spec_id):
    """Per-creature loot base (HealthOrbFragmentsLootBase) -- scales with strength."""
    return max(0, _creature_field(spec_id, "HealthOrbFragmentsLootBase", 0))


def creature_cp(spec_id):
    """Real construction-point cost to place this creature."""
    return max(1, _creature_field(spec_id, "ConstructionPoints", 1))


def creature_xp(spec_id):
    return max(0, _creature_field(spec_id, "BuildXp", 0))


def castle_rewards(rooms):
    """Sum the REAL per-creature loot/xp over a castle's placed creatures.
    Server-authoritative (the player can never get more than the castle contains)."""
    gold = xp = 0
    for room in (rooms or []):
        for cr in (room.get("Creatures") or []):
            sid = cr.get("SpecContainerId")
            gold += creature_loot(sid)
            xp += creature_xp(sid)
    return gold, xp


# ── buildings (CastleHeart construction cap, mine production) — real per rank ─
_BUILDINGS = {CAT.name("Buildings", i): _g("Buildings", i) for i in CAT.ids("Buildings")}


def _ranks(name):
    b = _BUILDINGS.get(name)
    if isinstance(b, list) and b and isinstance(b[0], dict):
        return b[0].get("Ranks", [])
    if isinstance(b, dict):
        return b.get("Ranks", [])
    return []


def castleheart_max(rank):
    """Real MaxConstructionPoints for a CastleHeart rank (rank 1 -> Ranks[0])."""
    r = _ranks("CastleHeart")
    if not r:
        return 20
    return r[max(0, min(rank - 1, len(r) - 1))].get("MaxConstructionPoints", 20)


def mine_capacity(mine, rank):
    """Real accumulated capacity for a mine rank (GoldMine/LifeForceMine/...)."""
    r = _ranks(mine)
    if not r:
        return 200
    return r[max(0, min(rank - 1, len(r) - 1))].get("Capacity", 200)


# ── reward type roll (UNIVERSALDROPSETTINGS) ────────────────────────────────
def roll_reward_type(rng=random):
    table = _UNIVERSAL.get("RewardTypeTable", {"InventoryItem": 1})
    roll = rng.random(); acc = 0.0
    for t, p in table.items():
        acc += p
        if roll <= acc:
            return t
    return "InventoryItem"


if __name__ == "__main__":
    rng = random.Random(42)
    print("sell Longsword(1) Epic/Named:", sell_price(1, "Epic", "Named"))
    print("sell Longsword(1) Basic/Common:", sell_price(1, "Basic", "Common"))
    for lvl in (1, 5, 20):
        it = generate_item(1, lvl, f"item-{lvl}", rng=rng)
        print(f"L{lvl}: quality={it['Quality']} rarity={it['Rarity']} "
              f"sell={it['SellPrice']} stats={[(s['Name'], s['Value']) for s in it['MagicalProperties']]}")
