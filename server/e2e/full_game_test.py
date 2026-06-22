#!/usr/bin/env python3
"""Test complet reseau (TLS): exerce et verifie TOUT ce qui est cable sur le
contenu reel du catalogue. Un seul compte, joue dans l'ordre, asserts partout."""
import json, ssl, urllib.request, sys

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
B = "https://127.0.0.1:443"
CHECKS = []


def call(svc, meth, body=None):
    r = urllib.request.Request(f"{B}/{svc}Service.hqs/{meth}",
                               data=json.dumps(body or {}).encode(), method="POST",
                               headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, context=CTX, timeout=8).read())


def cmd(name, **f):
    return call("ServerCommand", "SendCommands", {"commands": [
        dict({"$type": f"HyperQuest.GameServer.Contracts.{name}, HyperQuest.GameServer.Contracts"}, **f)]})


def acc():
    return call("Account", "GetAccountInformation")["Result"]


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

    ok = sum(1 for _, c in CHECKS if c); tot = len(CHECKS)
    print(f"\n=== {ok}/{tot} checks OK ===")
    print("TOUT VERT" if ok == tot else "DES CHECKS ONT ECHOUE")
    return 0 if ok == tot else 1


if __name__ == "__main__":
    sys.exit(main())
