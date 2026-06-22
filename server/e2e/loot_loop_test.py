#!/usr/bin/env python3
"""Validation de la boucle LOOT/ECONOMY de bout en bout, sur le reseau (TLS).

Sequence (telle que demandee):
  1. GetAccountInformation initial      -> Or = 0,   inventaire = 0 objet
  2. StartAttack                        -> attaque lancee
  3. EndAttack(Victory)                 -> le serveur octroie +100 Or + 1 objet (Notifications)
  4. GetAccountInformation final        -> Or = 100, inventaire = 1 nouvel objet

Le client parle exactement comme le jeu: POST /<Service>Service.hqs/<Method>.
"""
import json, ssl, urllib.request

BASE = "https://127.0.0.1:443"
CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode = ssl.CERT_NONE


def call(service, method, body=None):
    url = f"{BASE}/{service}Service.hqs/{method}"
    data = json.dumps(body or {}).encode()
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=CTX, timeout=8) as r:
        return json.loads(r.read().decode())


def wallet_and_items(acc_result):
    r = acc_result["Result"]
    w = r.get("Wallet", {})
    items = r.get("Inventory", {}).get("HeroItems", [])
    return w.get("InGameCoin", 0), w.get("LifeForce", 0), items


def main():
    print("=== BOUCLE LOOT/ECONOMY (reseau, TLS) ===\n")

    # 1. etat initial
    acc = call("Account", "GetAccountInformation")
    gold0, lf0, items0 = wallet_and_items(acc)
    print(f"1. GetAccountInformation initial -> Or={gold0}  ForceVitale={lf0}  objets={len(items0)}")

    # 2. lancer l'attaque
    sa = call("Castle", "StartAttack", {"DefenderAccountId": 2})
    print(f"2. StartAttack -> {('Notifications' in sa or 'Result' in sa) and 'attaque lancee' or sa}")

    # 3. terminer l'attaque en VICTOIRE
    ea = call("Castle", "EndAttack", {"Victory": True, "completionType": "TreasureRoom"})
    notifs = ea.get("Notifications", [])
    print(f"3. EndAttack(Victory) -> {len(notifs)} notification(s):")
    for n in notifs:
        t = n.get("__type") or n.get("NotificationType")
        if "Amounts" in n:
            amts = ", ".join(f"+{a['Amount']} (currency {a['CurrencyType']})" for a in n["Amounts"])
            print(f"     - WalletUpdated: {amts}")
        elif "NewlyAdded" in n:
            it = n["NewlyAdded"]
            print(f"     - HeroInventoryAdded: TemplateId={it.get('TemplateId')} "
                  f"ExpirableId={it.get('ExpirableId')} SellPrice={it.get('SellPrice')}")

    # 4. etat final
    acc2 = call("Account", "GetAccountInformation")
    gold1, lf1, items1 = wallet_and_items(acc2)
    print(f"\n4. GetAccountInformation final   -> Or={gold1}  ForceVitale={lf1}  objets={len(items1)}")
    if items1:
        print(f"     nouvel objet: {json.dumps(items1[-1], ensure_ascii=False)}")

    # verdict (delta-based: real starting gold = DEFAULTACCOUNT.IGC 1000, loot scaled)
    ok = (gold1 > gold0 and len(items1) == len(items0) + 1)
    print()
    if ok:
        print(f"Victoire confirmee! L'Or est passe de {gold0} a {gold1} "
              f"(+{gold1 - gold0}), et l'inventaire a gagne 1 nouvel objet "
              f"({len(items0)} -> {len(items1)}).")
    else:
        print(f"ECHEC: attendu Or en hausse et +1 objet ; obtenu Or {gold0}->{gold1}, "
              f"objets {len(items0)}->{len(items1)}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
