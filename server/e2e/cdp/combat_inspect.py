#!/usr/bin/env python3
"""Lire, sans rendu graphique, la composition exacte d'un combat depuis la
reponse StartAttack (AttackInfo) du serveur:

  - niveau du chateau (AttackInfo.Level / CastleHeartRank / AdjustedHeroLevel)
  - chaque creature placee: salle, type (SpecContainerId), position (RoomZoneId),
    endormie ?, et son Tier (via Castle.CreatureTiers) -> niveau affiche.

Chaine de donnees (100% lisible cote serveur):
  AttackInfo.Castle.Rooms[]  = CastleRoom{Id, Creatures[]}
    Creatures[]              = CastleCreature{SpecContainerId, RoomZoneId, ...}
  AttackInfo.Castle.CreatureTiers[] = {SpecContainerId, Tier}

NB: le niveau *affiche* final est calcule par le moteur natif a partir du Tier
+ des gamedata; le HUD le stocke en `uint` (HudEnemyTargettedEventArgs.Level),
donc un Tier manquant -> niveau -1 -> 4294967295 ("creature niveau 1 milliard").
On lit ici les ENTREES (tier, spec) qui le determinent.

Usage: combat_inspect.py [https://127.0.0.1:443] [DefenderAccountId]
"""
import sys, json, ssl, urllib.request

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://127.0.0.1:443"
DEF = int(sys.argv[2]) if len(sys.argv) > 2 else 2
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def start_attack():
    req = urllib.request.Request(BASE + "/AttackService.hqs/StartAttack",
                                 data=json.dumps({"DefenderAccountId": DEF}).encode(),
                                 method="POST", headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, context=CTX, timeout=8).read()).get("Result", {})


def enumerate_combat(ai):
    print("Niveau chateau (AttackInfo.Level) :", ai.get("Level"))
    print("CastleHeartRank                   :", ai.get("CastleHeartRank"))
    print("AdjustedHeroLevel                 :", ai.get("AdjustedHeroLevel"))
    castle = ai.get("Castle") or {}
    traw = castle.get("CreatureTiers")
    tiers = {t.get("SpecContainerId"): t.get("Tier") for t in traw} if isinstance(traw, list) else {}
    rooms = castle.get("Rooms") if isinstance(castle.get("Rooms"), list) else []
    total = 0
    for room in rooms:
        creatures = room.get("Creatures") if isinstance(room.get("Creatures"), list) else []
        for c in creatures:
            total += 1
            spec = c.get("SpecContainerId")
            tier = tiers.get(spec)
            flag = "" if tier is not None else "  <-- TIER MANQUANT -> underflow uint (niveau 1 milliard)"
            print("  salle %s | spec=%s zone=%s sleeping=%s | tier=%s%s"
                  % (room.get("Id"), spec, c.get("RoomZoneId"), c.get("IsSleeping"), tier, flag))
    print("Total creatures placees           :", total)
    if total == 0:
        print("(0 -> notre stub ne peuple pas encore le contenu de combat; "
              "structure correcte, contenu vide.)")


if __name__ == "__main__":
    enumerate_combat(start_attack())
