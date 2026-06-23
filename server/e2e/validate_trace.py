#!/usr/bin/env python3
"""
validate_trace.py — validate a captured client<->server session.

Reads the monitor's trace.jsonl (every exchange the unmodified game made against
our local backend) and checks, per request:
  * the method routed to a real catalog contract,
  * the response we returned is schema-complete (all fields the client's typed
    schema expects are present — the "emit every field" rule that the prior
    community server violated),
  * cross-references the methods seen against endpoints_observed.txt.

Usage: python3 validate_trace.py [trace.jsonl] [schemas_typed.json]
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRACE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "trace.jsonl")
SCHEMAS = sys.argv[2] if len(sys.argv) > 2 else \
    "/home/user/mightyquest-drop/re/catalog/network/schemas_typed.json"
OBSERVED = "/home/user/mightyquest-drop/re/catalog/network/endpoints_observed.txt"

schemas = json.load(open(SCHEMAS, encoding="utf-8"))
# map response contract -> set of expected field names
def fields_of(name):
    s = schemas.get(name)
    if not s:
        return None
    return {f[0] for f in s.get("fields", [])}

observed = set()
for ln in open(OBSERVED, encoding="utf-8"):
    m = re.search(r"/(\w+)Service\.hqs/(\w+)", ln)
    if m:
        observed.add(m.group(2))

# the response builder maps method -> contract (mirror of monitor_server)
METHOD_CONTRACT = {
    "GetAccountInformation": "AccountInformation",
    "ChooseDisplayName": "AccountSummary",
    "GetAttackSelectionList": "AttackSelectionResult",
    "GetCastleInfo": "CastleInfo",
    "StartAttack": "AttackInfo",
    "GetCastlesForSale": "CastlesForSaleSelectionResult",
    "GetCastleForSaleBuildInfo": "CastleBuildInfo",
}

rows = []
seen_methods = set()
if os.path.exists(TRACE):
    for ln in open(TRACE, encoding="utf-8"):
        ln = ln.strip()
        if not ln:
            continue
        rec = json.loads(ln)
        if "curl/8" in rec.get("ua", ""):
            continue  # skip our own probes
        m = re.search(r"/(\w+)Service\.hqs/(\w+)", rec.get("path", ""))
        method = m.group(2) if m else rec.get("path")
        seen_methods.add(method)
        contract = METHOD_CONTRACT.get(method)
        verdict = "—"
        if contract:
            exp = fields_of(contract)
            try:
                resp = json.loads(rec.get("resp_body", "{}"))
            except Exception:
                resp = {}
            if exp is None:
                verdict = "no-schema"
            else:
                missing = exp - set(resp)
                verdict = "COMPLETE" if not missing else f"missing {len(missing)}: {sorted(missing)[:5]}"
        rows.append((rec.get("seq"), rec.get("scheme"), method, rec.get("req_len"),
                     rec.get("resp_len"), rec.get("route"), verdict))

print("=" * 78)
print("CAPTURED CLIENT<->SERVER EXCHANGES (game traffic only)")
print("=" * 78)
if not rows:
    print("(no game exchanges captured yet)")
else:
    for seq, scheme, method, rq, rs, route, verdict in rows:
        print(f"  #{seq} {scheme:5s} {method:30s} req={rq}b resp={rs}b  [{verdict}]")

print()
print("ENDPOINT COVERAGE vs endpoints_observed.txt")
print(f"  observed-in-RE methods : {len(observed)}")
print(f"  hit-in-this-session    : {sorted(seen_methods) if seen_methods else '(none)'}")
both = seen_methods & observed
print(f"  matched real endpoints : {sorted(both) if both else '(none)'}")
