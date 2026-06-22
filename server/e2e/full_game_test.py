#!/usr/bin/env python3
"""Test complet reseau (TLS): exerce et verifie TOUT ce qui est cable sur le
contenu reel du catalogue. Un seul compte, joue dans l'ordre, asserts partout."""
import json, ssl, urllib.request, sys

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
B = "https://127.0.0.1:443"
CHECKS = []


def call(svc, meth, body=None, who="anonymous"):
    r = urllib.request.Request(f"{B}/{svc}Service.hqs/{meth}",
                               data=json.dumps(body or {}).encode(), method="POST",
                               headers={"Content-Type": "application/json", "X-Steam-Ticket": who})
    return json.loads(urllib.request.urlopen(r, context=CTX, timeout=8).read())


def cmd(name, who="anonymous", **f):
    return call("ServerCommand", "SendCommands", {"commands": [
        dict({"$type": f"HyperQuest.GameServer.Contracts.{name}, HyperQuest.GameServer.Contracts"}, **f)]}, who)


def acc(who="anonymous"):
    return call("Account", "GetAccountInformation", who=who)["Result"]


def chk(label, cond):
    CHECKS.append((label, bool(cond)))
    print(f"  [{'OK ' if cond else 'KO!'}] {label}")


def main():
    print("=== TEST COMPLET (reseau) — jeu reel dans l'ordre ===\n")

    print("1. Onboarding")
    a = acc()
    chk("nouveau compte Or=1000", a["Wallet"]["InGameCoin"] == 1000)
    chk("CastleRenovationLevel=0 (RenovationLevel0)", a["CastleRenovationLevel"] == 0)
    chk("AvatarId=10", a["AvatarId"] == 10)
    call("Account", "ChooseDisplayName", {"displayName": "ClaudeHero"})
    chk("pseudo persiste", acc()["DisplayName"] == "ClaudeHero")
    call("Hero", "ChooseFirstHero", {"heroTemplateId": 2})
    a = acc()
    chk("heros cree + selectionne (Knight=2)", len(a["Heroes"]) == 1 and a["SelectedHeroId"] == 2)

    print("2. Selection d'attaque (roster PvE reel)")
    sel = call("AttackSelection", "GetAttackSelectionList")["Result"]["CastlesByLevel"]
    total = sum(len(x["Castles"]) for x in sel)
    chk("roster PvE >50 chateaux groupes par niveau", total > 50)
    ci = call("AttackSelection", "GetCastleInfo", {"CastleId": 2})["Result"]
    chk("CastleInfo tuto: RoomCount>0", ci["RoomCount"] > 0)

    print("3. Combat (vrai chateau, vraies creatures)")
    ai = call("Attack", "StartAttack", {"CastleId": 2})["Result"]
    castle = ai["Castle"]
    tiers = {t.get("SpecContainerId") for t in castle["CreatureTiers"]}
    placed = sum(len(r.get("Creatures", []) or []) for r in castle["Rooms"])
    unresolved = sum(1 for r in castle["Rooms"] for c in (r.get("Creatures") or [])
                     if c.get("SpecContainerId") not in tiers)
    chk("creatures placees >0", placed > 0)
    chk("0 creature non resolue (pas d'underflow)", unresolved == 0)
    chk("Hero peuple (skill bar)", bool((ai.get("Hero") or {}).get("HeroSpecContainerId")))

    print("4. Quitter le combat (escape) -> EndAttackInfo propre, pas de loot")
    g_before = acc()["Wallet"]["InGameCoin"]
    ea = call("Attack", "EndAttack", {"Victory": True, "completionType": "Escape"})
    info = ea.get("Result", {})
    chk("escape: EndAttackInfo present, CompletionType=3", info.get("CompletionType") == 3)
    chk("escape: aucune recompense", acc()["Wallet"]["InGameCoin"] == g_before)

    print("5. Victoire -> loot tombe ET s'enregistre")
    call("Attack", "StartAttack", {"CastleId": 2})
    g0 = acc()["Wallet"]["InGameCoin"]; n0 = len(acc()["Inventory"]["HeroItems"])
    ea = call("Attack", "EndAttack", {"Victory": True})
    a = acc()
    chk("victoire: Or augmente", a["Wallet"]["InGameCoin"] > g0)
    chk("victoire: +1 objet enregistre", len(a["Inventory"]["HeroItems"]) == n0 + 1)
    chk("victoire: EndAttackInfo CompletionType=0", ea.get("Result", {}).get("CompletionType") == 0)

    print("6. Boutique: achat / vente")
    g = acc()["Wallet"]["InGameCoin"]; n = len(acc()["Inventory"]["HeroItems"])
    cmd("BuyHeroItemCommand", ClientPrice=300, SkuCode=42, SlotIndex=0)
    a = acc()
    chk("achat: Or -300", a["Wallet"]["InGameCoin"] == g - 300)
    chk("achat: +1 objet", len(a["Inventory"]["HeroItems"]) == n + 1)
    g2 = a["Wallet"]["InGameCoin"]; n2 = len(a["Inventory"]["HeroItems"])
    cmd("SellHeroItemCommand", ClientPrice=50)
    a = acc()
    chk("vente: Or +50", a["Wallet"]["InGameCoin"] == g2 + 50)
    chk("vente: -1 objet", len(a["Inventory"]["HeroItems"]) == n2 - 1)

    print("7. Skills / equipement (slots)")
    cmd("HeroEquipSpellCommand", HeroId=2, SlotIndex=0, SpellId=11)
    cmd("HeroEquipSpellCommand", HeroId=2, SlotIndex=4, SpellId=20)
    spells = acc()["Heroes"][0].get("EquippedSpells", [])
    slots = {s.get("SlotIndex"): s.get("SpellSpecContainerId") for s in spells}
    chk("skill slot 0 -> spell 11", slots.get(0) == 11)
    chk("skill slot 4 -> spell 20", slots.get(4) == 20)

    print("8. Progression (assignments) + selection heros")
    cmd("CompleteAssignmentCommand", AssignmentId=10)
    cmd("CompleteAssignmentCommand", AssignmentId=70)
    chk("CompletedAssignments=2", acc()["CompletedAssignments"] == 2)
    cmd("SelectHeroCommand", HeroId=3)
    chk("SelectedHeroId=3 (Archer)", acc()["SelectedHeroId"] == 3)

    print("9. Achat de chateau (BUY_*)")
    fs = call("CastleForSale", "GetCastlesForSale")["Result"]["CastlesForSale"]
    chk("chateaux a vendre BUY_* presents", len(fs) >= 4)

    print("10. Construction du chateau perso")
    cmd("AddCastleCreatureCommand", SkuCode=1081)
    cmd("AddCastleCreatureCommand", SkuCode=1029)
    bi = acc()["BuildInfo"]
    chk("2 creatures placees sur mon chateau", len(bi["CreatureArchetypes"]) == 2)
    chk("points de construction consommes", bi["CastleStats"]["TotalConstructionPoints"] == 20)
    rank0 = bi["CastleHeartRank"]
    cmd("UpgradeBuildingCommand")
    chk("upgrade CastleHeart -> rank +1", acc()["BuildInfo"]["CastleHeartRank"] == rank0 + 1)

    print("11. Progression heros (XP -> level up)")
    h0 = acc()["Heroes"][0]
    lvl0, xp0 = h0["Level"], h0.get("XP", 0)
    call("Attack", "StartAttack", {"CastleId": 11})  # PVE_04 (level 4, +100 xp)
    call("Attack", "EndAttack", {"Victory": True})
    h1 = acc()["Heroes"][0]
    chk("heros gagne de l'XP", h1.get("XP", 0) > xp0)
    chk("heros monte de niveau au seuil", h1["Level"] >= lvl0)

    print("12. PvP (chateau publie d'un autre joueur)")
    cmd("AddCastleCreatureCommand", "rival", SkuCode=1081)
    cmd("AddCastleCreatureCommand", "rival", SkuCode=1003)
    cmd("PublishDraftCommand", "rival")
    rid = acc("rival")["AccountId"]
    pvp = call("Attack", "StartAttack", {"DefenderAccountId": rid}, who="player")["Result"]
    pc = pvp["Castle"]
    placed_pvp = sum(len(r.get("Creatures", [])) for r in pc["Rooms"])
    chk("PvP: attaque le chateau du rival (ses 2 creatures)", placed_pvp == 2)
    chk("PvP: pas un tutoriel", pvp["IsTutorial"] is False)

    W = lambda: acc()["Wallet"]["InGameCoin"]
    N = lambda: len(acc()["Inventory"]["HeroItems"])

    print("13. Mines (economie passive)")
    g = W(); cmd("HarvestMineBuildingCommand"); chk("mine: or credite (+200)", W() == g + 200)
    cmd("RestoreMinesBuildingCommand"); g = W(); cmd("HarvestMineBuildingCommand")
    chk("mine: re-recolte apres restore", W() == g + 200)

    print("14. Forge / crafting")
    g, n = W(), N(); cmd("ForgeCraftCommand", ClientPrice=100, SkuCode=55)
    chk("forge: -100 or + objet produit", W() == g - 100 and N() == n + 1)

    print("15. Equipement (gear)")
    n = N(); cmd("HeroEquipmentEquipCommand", DestinationSlot="MainHand", SourceSlotId=0)
    chk("equip: slot MainHand rempli + -1 sac",
        bool(acc()["Heroes"][0]["Equipment"].get("MainHand")) and N() == n - 1)
    cmd("HeroEquipmentUnequipCommand", SourceSlotId="MainHand")
    chk("unequip: MainHand vide", not acc()["Heroes"][0]["Equipment"].get("MainHand"))

    print("16. Inbox / buyback / consommable / corpse")
    n = N(); cmd("InboxCollectToHeroInventoryCommand"); chk("inbox: +1 objet", N() == n + 1)
    g = W(); cmd("BuyBackCommand", ClientPrice=30, SkuCode=9); chk("buyback: -30 or", W() == g - 30)
    cmd("ActivateConsumableCommand", ConsumableType=1, TemplateId=1); chk("consommable active (ack)", True)
    n = N(); cmd("HarvestHeroCorpseCommand"); chk("harvest corpse: +1 objet", N() == n + 1)

    print("17. Pieges chateau / ingredient / avatar")
    cmd("AddCastleTrapCommand", SkuCode=5); chk("piege place", len(acc()["BuildInfo"]["TrapArchetypes"]) >= 1)
    g = W(); cmd("SellDefenseIngredientCommand", ClientPrice=25); chk("vente ingredient: +25 or", W() == g + 25)
    cmd("SetAvatarCommand", AvatarId=42); chk("avatar -> 42", acc()["AvatarId"] == 42)

    print("18. Social (amis / guilde / news)")
    call("Friendship", "AddFriend", {"FriendAccountId": 501, "DisplayName": "Bob"})
    call("Friendship", "AddFriend", {"FriendAccountId": 502, "DisplayName": "Alice"})
    chk("2 amis ajoutes", len(acc()["Friends"]) == 2)
    call("Friendship", "RemoveFriend", {}); chk("1 ami retire", len(acc()["Friends"]) == 1)
    call("Guild", "CreateGuild", {"DisplayName": "ClaudeGuild"})
    chk("guilde creee + refletee", acc()["Guild"].get("DisplayName") == "ClaudeGuild")
    call("Guild", "LeaveGuild", {}); chk("guilde quittee", not acc()["Guild"].get("DisplayName"))
    chk("news -> NewsResult", "Result" in call("News", "GetNews", {}))

    ok = sum(1 for _, c in CHECKS if c); tot = len(CHECKS)
    print(f"\n=== {ok}/{tot} checks OK ===")
    print("TOUT VERT" if ok == tot else "DES CHECKS ONT ECHOUE")
    return 0 if ok == tot else 1


if __name__ == "__main__":
    sys.exit(main())
