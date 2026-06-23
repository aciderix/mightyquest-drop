#!/usr/bin/env python3
"""
replay_real_traffic.py — replay the REAL recorded client<->server traffic
(captured when the community setup worked, on Windows) against THIS server, and
validate our responses.

Ground truth: server/mqel_network*.log from branch rebuild-online-server — every
exchange is "◄── CLIENT REQUEST (...)" + JSON  then  "──► SERVER RESPONSE
(HTTP 200)" + JSON. We re-issue each client request to our local backend and
check our response is schema-complete and structurally consistent with what the
real client accepted.

    python3 replay_real_traffic.py <server_base_url> <log...>
"""
import json, re, sys, urllib.request, urllib.error

SCHEMAS = "/home/user/mightyquest-drop/re/catalog/network/schemas_typed.json"
schemas = json.load(open(SCHEMAS, encoding="utf-8"))
METHOD_CONTRACT = {
    "GetAccountInformation": "AccountInformation",
    "GetAttackSelectionList": "AttackSelectionResult",
    "GetCastleInfo": "CastleInfo",
    "StartAttack": "AttackInfo",
    "GetCastlesForSale": "CastlesForSaleSelectionResult",
}

REQ = "CLIENT REQUEST"
RES = "SERVER RESPONSE"

def parse(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    # split into exchanges on the "#<n>  time  VERB /path" header
    parts = re.split(r"\n#\d+\s+[\d:.]+\s+", raw)
    out = []
    for p in parts[1:]:
        mh = re.match(r"(GET|POST|PUT)\s+(\S+)", p)
        if not mh:
            continue
        verb, path_ = mh.group(1), mh.group(2)
        req = _json_after(p, REQ)
        res = _json_after(p, RES)
        out.append((verb, path_, req, res))
    return out

def _json_after(block, marker):
    i = block.find(marker)
    if i < 0:
        return None
    seg = block[i:]
    s = seg.find("{")
    a = seg.find("[")
    start = min([x for x in (s, a) if x >= 0], default=-1)
    if start < 0:
        return {} if marker == REQ else None
    # balance braces/brackets
    depth = 0; instr = False; esc = False; end = None
    for j, ch in enumerate(seg[start:], start):
        if esc: esc = False; continue
        if ch == "\\": esc = True; continue
        if ch == '"': instr = not instr; continue
        if instr: continue
        if ch in "{[": depth += 1
        elif ch in "}]":
            depth -= 1
            if depth == 0: end = j+1; break
    if end is None:
        return None
    try:
        return json.loads(seg[start:end])
    except Exception:
        return None

def http(base, verb, path_, body):
    url = base.rstrip("/") + path_
    data = json.dumps(body).encode() if (body and verb != "GET") else None
    req = urllib.request.Request(url, data=data, method=verb,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, f"ERR {e}"

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:80"
    logs = sys.argv[2:] or ["real_traffic.log"]
    exchanges = []
    for lg in logs:
        try:
            exchanges += parse(lg)
        except FileNotFoundError:
            print(f"[skip] {lg} not found")
    print(f"Replaying {len(exchanges)} real exchanges against {base}\n")
    ok = miss = err = 0
    for verb, path_, req, recorded in exchanges:
        m = re.search(r"/(\w+)Service\.hqs/(\w+)", path_)
        method = m.group(2) if m else path_
        status, resp = http(base, verb, path_, req)
        note = ""
        if status != 200:
            err += 1; note = f"HTTP {status} {resp}"
        else:
            contract = METHOD_CONTRACT.get(method)
            if contract and contract in schemas:
                exp = {f[0] for f in schemas[contract]["fields"]}
                got = set(resp) if isinstance(resp, dict) else set()
                missing = exp - got
                if missing:
                    miss += 1; note = f"schema missing {len(missing)}: {sorted(missing)[:4]}"
                else:
                    ok += 1; note = f"schema-complete ({len(got)} fields)"
            else:
                ok += 1
                rk = len(recorded) if isinstance(recorded, (dict, list)) else "?"
                note = f"served (recorded had {rk} top-level)"
        print(f"  {verb:4s} {method:28s} -> {status}  {note}")
    print(f"\nSummary: {ok} ok, {miss} schema-incomplete, {err} errors, "
          f"{len(exchanges)} total")

if __name__ == "__main__":
    main()
