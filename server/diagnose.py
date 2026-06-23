#!/usr/bin/env python3
"""diagnose.py — turn trace.jsonl into an AI-readable diagnosis.

When a problem is reported in-game, run this. With NO prior context an AI can read
the output and know where to look. It surfaces, from the trace:
  - errors/exceptions (with the failing Service.Method),
  - requests served by the FALLBACK (static example) -> the usual cause of
    "this screen/feature looks empty or does nothing",
  - rejected commands (e.g. an equip refused: wrong slot / level too low),
  - heuristic/unknown command routing (notification edges not byte-confirmed),
  - a timeline of the last N requests.

Usage:
  python3 diagnose.py                      # full summary of trace.jsonl
  python3 diagnose.py --grep Guild         # only requests mentioning "Guild"
  python3 diagnose.py --method StartAttack # only that method
  python3 diagnose.py --tail 40            # last 40 requests timeline
  python3 diagnose.py --symptom            # symptom -> cause cheat-sheet

Each finding tells you which file/handler to look at, so a fix is local.
"""
import argparse, json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
TRACE = os.environ.get("MQ_TRACE", os.path.join(HERE, "trace.jsonl"))

# where each "source" / flag is implemented -> point the AI straight at the code
WHERE = {
    "fallback_example": "stub_server.py: _guess()/_handle (no dedicated handler). "
                        "To make it live: add a handler in ENDPOINTS or ep_social.",
    "ep_social": "stub_server.py: ep_social() (guild/friends/news/shop/leaderboard/battlelog).",
    "command_rejected": "command_notifications.py: CommandBus._apply (e.g. can_equip in "
                        "catalog_economy.py rejected a slot/level mismatch).",
    "command_unknown": "command_notifications.py: CURATED / notifications_for (edge not mapped).",
    "command_heuristic": "command_notifications.py: notification edge inferred, not byte-confirmed.",
    "exception": "a handler raised — see the 'error'/'traceback' record; fix that handler.",
}

SYMPTOMS = [
    ("Un écran/onglet est vide ou ne fait rien",
     "Cherche les requêtes 'fallback_example' de ce service (diagnose.py --grep <Service>). "
     "Ça veut dire: pas de handler dédié -> données statiques. Câbler dans ep_social/ENDPOINTS."),
    ("Une action (achat/équip/construction) n'a aucun effet",
     "Cherche 'command_rejected' ou la commande dans diagnose.py --method SendCommands. "
     "Rejet d'équip = mauvais slot/niveau (catalog_economy.can_equip). Sinon vérifier _apply."),
    ("Un objet équipé ne donne pas ses bonus",
     "Vérifier HeroStatModifier après HeroEquipmentEquip (command_notifications _apply + "
     "catalog_economy.hero_equipped_stats)."),
    ("Mauvais montant d'or/xp/loot",
     "Économie sourcée catalogue (catalog_economy.py). loot/xp = somme par créature "
     "(creature_loot/creature_xp). 2 valeurs sont dérivées (force-vitale par kill, perte trophée)."),
    ("Créatures niveau aberrant / combat cassé",
     "C'est la SIM 3D (moteur natif) — non couverte par le serveur. Vérifier que StartAttack "
     "renvoie un Castle avec CreatureTiers non vide (combat_inspect.py)."),
    ("Le client plante / réponse rejetée",
     "Chercher 'exception' (diagnose.py) et vérifier la complétude via completeness_gate."),
]


def load():
    if not os.path.exists(TRACE):
        print(f"(pas de trace: {TRACE} — lance le serveur et reproduis le problème)")
        sys.exit(0)
    out = []
    for ln in open(TRACE, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grep"); ap.add_argument("--method")
    ap.add_argument("--tail", type=int, default=0)
    ap.add_argument("--symptom", action="store_true")
    a = ap.parse_args()

    if a.symptom:
        print("=== SYMPTÔME → OÙ CHERCHER ===")
        for s, w in SYMPTOMS:
            print(f"\n• {s}\n  → {w}")
        return 0

    rows = load()
    rpc = [r for r in rows if r.get("kind") == "rpc"]
    errs = [r for r in rows if r.get("kind") == "error"]
    if a.grep:
        g = a.grep.lower()
        rpc = [r for r in rpc if g in json.dumps(r, default=str).lower()]
    if a.method:
        rpc = [r for r in rpc if r.get("method") == a.method]

    if a.tail:
        print(f"=== {min(a.tail, len(rpc))} dernières requêtes ===")
        for r in rpc[-a.tail:]:
            fl = (" FLAGS=" + ",".join(r.get("flags", []))) if r.get("flags") else ""
            print(f"  #{r['seq']} {r['method']:28} <- {r.get('source','-'):24}{fl}")
        return 0

    print(f"=== DIAGNOSE  ({len(rpc)} requêtes, {len(errs)} erreurs) — trace: {TRACE} ===")

    if errs:
        print("\n!!! ERREURS (à corriger en priorité) :")
        for e in errs[-8:]:
            print(f"  #{e['seq']} {e.get('service')}.{e.get('method')}: {e.get('error')}")
        print("   →", WHERE["exception"])

    # group flagged requests by flag prefix
    flagged = [r for r in rpc if r.get("flags")]
    by = Counter()
    for r in flagged:
        for f in r["flags"]:
            by[f.split(":")[0]] += 1
    if by:
        print("\n⚠ POINTS D'ATTENTION (par type) :")
        for k, n in by.most_common():
            print(f"  {n:4}x {k}")
            print(f"        → {WHERE.get(k, '(voir code)')}")

    # which services hit the fallback (the usual 'inert feature' cause)
    fb = Counter(r["method"] for r in rpc if "fallback_example" in (r.get("flags") or []))
    if fb:
        print("\n○ Méthodes servies par FALLBACK statique (candidates à câbler) :")
        for m, n in fb.most_common(15):
            print(f"  {n:4}x {m}")

    rej = [r for r in rpc for f in (r.get("flags") or []) if f.startswith("command_rejected")]
    if rej:
        print("\n✗ Commandes REJETÉES :")
        for r in rej[-10:]:
            cmds = [f for f in r["flags"] if f.startswith("command_rejected")]
            print(f"  #{r['seq']} {cmds}")

    if not (errs or by):
        print("\n✓ Rien d'anormal dans la trace (aucune erreur, aucun fallback/rejet).")
    print("\nAstuce: `diagnose.py --grep <Service>`, `--method <X>`, `--tail 40`, `--symptom`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
