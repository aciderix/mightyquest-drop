#!/usr/bin/env python3
"""Pilote la boucle LOOT/ECONOMY a travers le VRAI framework hyperquest du
client (CEF/Chromium-28 sous Wine), via CDP.

Chaque appel part du transport JS `hyperquest.client` dans le renderer, transite
par notre stub TLS (:443), et la reponse est re-injectee dans le framework. On
prouve donc la boucle de bout en bout cote *client live*, pas seulement reseau:

  1. GetAccountInformation -> Or = 0,   0 objet
  2. StartAttack           -> attaque lancee
  3. EndAttack(Victory)    -> Notifications (WalletUpdated + HeroInventoryAdded)
  4. GetAccountInformation -> Or = 100, 1 objet

Pre-requis: client lance avec --remote-debugging-port=9222, stub sur :443 avec
un etat frais (state.json supprime). Un SEUL /json (gere par Agent).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from agent import Agent


def wallet_items(acc):
    if not isinstance(acc, dict):
        return None, None
    w = acc.get("Wallet", {}) or {}
    items = (acc.get("Inventory", {}) or {}).get("HeroItems", []) or []
    return w.get("InGameCoin", 0), items


def main():
    a = Agent()                      # un seul /json, auto-pick du renderer vivant
    print("renderer attache:", a.page.get("url"))
    if not a.has_native_bridge():
        info = a.bootstrap_local()
        print("framework injecte: ok=%d fail=%d" % (info["ok"], info["fail"]))

    print("\n=== BOUCLE LOOT/ECONOMY pilotee via le framework JS live (CDP) ===\n")

    acc, _, je = a.invoke("GetAccountInformation", {})
    g0, it0 = wallet_items(acc)
    print(f"1. GetAccountInformation -> Or={g0}  objets={len(it0)}")

    sa, _, _ = a.invoke("StartAttack", {"DefenderAccountId": 2})
    print(f"2. StartAttack           -> {'AttackId' in (sa or {}) and 'attaque lancee' or 'ok'}")

    ea, _, je = a.invoke("EndAttack", {"Victory": True, "completionType": "TreasureRoom"})
    notifs = (ea or {}).get("Notifications", []) if isinstance(ea, dict) else []
    print(f"3. EndAttack(Victory)    -> {len(notifs)} notification(s) recues par le framework JS")
    for n in notifs:
        if "Amounts" in n:
            print("     - WalletUpdated:", ", ".join(
                f"+{x['Amount']} (currency {x['CurrencyType']})" for x in n["Amounts"]))
        elif "NewlyAdded" in n:
            it = n["NewlyAdded"]
            print(f"     - HeroInventoryAdded: TemplateId={it.get('TemplateId')} "
                  f"ExpirableId={it.get('ExpirableId')}")
    if je:
        print("     ! le framework JS a leve:", je)

    acc2, _, _ = a.invoke("GetAccountInformation", {})
    g1, it1 = wallet_items(acc2)
    print(f"4. GetAccountInformation -> Or={g1}  objets={len(it1)}")
    if it1:
        print("     nouvel objet vu par le client:", it1[-1])

    a.ws.close()
    ok = (g1 > g0 and len(it1) == len(it0) + 1)
    print()
    if ok:
        print("Victoire confirmee! Pilotee depuis le framework JS du client live: "
              f"l'Or est passe de {g0} a {g1} (+{g1 - g0}) et l'inventaire a gagne "
              f"1 nouvel objet ({len(it0)} -> {len(it1)}).")
    else:
        print(f"ECHEC via CDP: Or {g0}->{g1}, objets {len(it0)}->{len(it1)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
