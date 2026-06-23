#!/usr/bin/env python3
"""Jouer le VRAI jeu dans l'ordre, piloté via le framework JS du client live (CDP).

Séquence d'onboarding réelle, chaque étape sur du contenu de catalogue authentique:
  1. GetAccountInformation   -> nouveau joueur (Or = DEFAULTACCOUNT.IGC 1000)
  2. ChooseDisplayName       -> pseudo
  3. ChooseFirstHero(Knight) -> loadout héros réel
  4. GetAttackSelectionList  -> vrai roster PvE par niveau
  5. GetCastleInfo(tuto1)    -> vrai château
  6. StartAttack(tuto1)      -> vraies créatures + Hero peuplé
  7. EndAttack(Victory)      -> loot scripté du tuto
  8. GetAccountInformation   -> Or en hausse, +1 objet

Chaque réponse passe par la completeness gate, est reçue par le vrai framework
hyperquest, et on vérifie les invariants (pas d'underflow, loadout présent, loot).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from agent import Agent

TUTO1 = 2  # CastleId de PVE_00_TUTORIAL_01


def gold_items(acc):
    if not isinstance(acc, dict):
        return 0, []
    w = acc.get("Wallet", {}) or {}
    items = (acc.get("Inventory", {}) or {}).get("HeroItems", []) or []
    return w.get("InGameCoin", 0), items


def creatures(ai):
    castle = (ai or {}).get("Castle", {}) or {}
    tiers = {t.get("SpecContainerId") for t in (castle.get("CreatureTiers") or [])}
    placed = unresolved = 0
    for room in castle.get("Rooms") or []:
        for c in room.get("Creatures") or []:
            placed += 1
            if c.get("SpecContainerId") not in tiers:
                unresolved += 1
    return placed, unresolved


def main():
    a = Agent()
    a.bootstrap_local()
    print("=== PLAYTHROUGH (client live via CDP) — jeu réel dans l'ordre ===\n")
    checks = []

    acc, _, _ = a.invoke("GetAccountInformation", {})
    g0, it0 = gold_items(acc)
    print(f"1. Nouveau compte           -> Or={g0}  objets={len(it0)}")
    checks.append(("compte de départ Or=1000", g0 == 1000))

    a.invoke("ChooseDisplayName", {"displayName": "ClaudeHero"})
    print("2. ChooseDisplayName        -> ClaudeHero")

    a.invoke("ChooseFirstHero", {"heroTemplateId": 2})
    acc, _, _ = a.invoke("GetAccountInformation", {})
    heroes = acc.get("Heroes") if isinstance(acc, dict) else []
    sel = acc.get("SelectedHeroId") if isinstance(acc, dict) else 0
    print(f"3. ChooseFirstHero(Knight)  -> heroes={len(heroes)} SelectedHeroId={sel}")
    checks.append(("héros créé + sélectionné", len(heroes) == 1 and sel == 2))

    sel_list, _, _ = a.invoke("GetAttackSelectionList", {})
    by_level = (sel_list or {}).get("CastlesByLevel", []) if isinstance(sel_list, dict) else []
    total = sum(len(x.get("Castles", [])) for x in by_level)
    print(f"4. GetAttackSelectionList   -> {len(by_level)} niveaux, {total} châteaux PvE réels")
    checks.append(("roster PvE non vide", total > 50))

    ci, _, _ = a.invoke("GetCastleInfo", {"CastleId": TUTO1})
    print(f"5. GetCastleInfo(tuto1)     -> Level={ci.get('Level')} RoomCount={ci.get('RoomCount')}")
    checks.append(("castle info réel", isinstance(ci, dict) and ci.get("RoomCount", 0) > 0))

    ai, _, jserr = a.invoke("StartAttack", {"CastleId": TUTO1})
    placed, unresolved = creatures(ai)
    hero = (ai or {}).get("Hero", {}) if isinstance(ai, dict) else {}
    print(f"6. StartAttack(tuto1)       -> {placed} créatures placées ({unresolved} non résolues), "
          f"Hero SpecContainer={hero.get('HeroSpecContainerId')} Level={hero.get('Level')}")
    checks.append(("créatures réelles, 0 underflow", placed > 0 and unresolved == 0))
    checks.append(("Hero peuplé (skill bar non vide)", bool(hero.get("HeroSpecContainerId"))))
    if jserr:
        print("     ! framework JS a levé:", jserr)

    ea, _, _ = a.invoke("EndAttack", {"Victory": True})
    notifs = (ea or {}).get("Notifications", []) if isinstance(ea, dict) else []
    print(f"7. EndAttack(Victory)       -> {len(notifs)} notification(s) (loot)")

    acc, _, _ = a.invoke("GetAccountInformation", {})
    g1, it1 = gold_items(acc)
    print(f"8. Compte final             -> Or={g1}  objets={len(it1)}")
    checks.append(("Or en hausse + 1 objet looté", g1 > g0 and len(it1) == len(it0) + 1))

    a.ws.close()
    print("\n=== INVARIANTS ===")
    allok = True
    for label, ok in checks:
        print(f"  [{'OK ' if ok else 'KO!'}] {label}")
        allok = allok and ok
    print("\n" + ("TOUT VERT: le jeu se déroule dans l'ordre sur du contenu réel, "
                  "via le client live." if allok else "DES CHECKS ONT ÉCHOUÉ."))
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
