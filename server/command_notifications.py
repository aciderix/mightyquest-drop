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
    def build(self, notif_name, index):
        obj = self.gate.complete(notif_name, {"Index": index}, add_type=True)
        return obj

    # ---- handle a full SendCommands request ----------------------------------
    def handle(self, request_json, *, warn=None):
        commands = (request_json or {}).get("commands", []) or []
        notifications, idx, unknown = [], 0, []
        for cmd in commands:
            name = self._command_name(cmd)
            if not name:
                continue
            notifs, conf = self.notifications_for(name)
            if conf == "unknown":
                unknown.append(name)
            for nname in notifs:
                notifications.append(self.build(nname, idx))
                idx += 1
        if warn is not None and unknown:
            warn(unknown)
        # the client accepts {} (no notifications) or a list of notifications
        return notifications if notifications else {}

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
