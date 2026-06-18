#!/usr/bin/env python3
"""
stub_server.py — community-server stub for The Mighty Quest for Epic Loot.

Iteration 3: routes on the REAL endpoint pattern observed in live traffic
(`/<Service>Service.hqs/<Method>`, see re/catalog/network/endpoints_observed.txt)
and answers with COMPLETE, correctly-typed responses generated from the reversed
catalog (re/catalog/network/generated/examples.json — full field sets, real enum
values, `$type` discriminators). Stateful accounts/sessions, persisted. Logs
every request so unknown calls are easy to fill in.

Zero dependencies (Python 3 stdlib). Run on the game machine or a VPS:
    python3 server/stub_server.py --host 0.0.0.0 --port 8080
"""
from __future__ import annotations
import argparse, copy, datetime, json, os, re, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
NET = os.path.join(ROOT, "re/catalog/network")
EXAMPLES = json.load(open(os.path.join(NET, "generated/examples.json"))) \
    if os.path.exists(os.path.join(NET, "generated/examples.json")) else {}
PKG_VERSIONS = json.load(open(os.path.join(NET, "package_versions.json"))) \
    if os.path.exists(os.path.join(NET, "package_versions.json")) else {}
STATE_PATH = os.path.join(HERE, "state.json")
LOG_PATH = os.path.join(HERE, "requests.log")


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def contract(name, **overrides):
    """a COMPLETE example of `name` (full fields / real enums / $type), overridden."""
    obj = copy.deepcopy(EXAMPLES.get(name, {}))
    obj.update(overrides)
    return obj


# ---- persistent state ------------------------------------------------------
class State:
    def __init__(self, path):
        self.path = path; self.lock = threading.Lock()
        self.data = {"accounts": {}, "sessions": {}, "next_id": 1}
        if os.path.exists(path):
            try: self.data.update(json.load(open(path)))
            except Exception: pass

    def save(self):
        json.dump(self.data, open(self.path + ".tmp", "w"), indent=1)
        os.replace(self.path + ".tmp", self.path)

    def login(self, identity):
        with self.lock:
            acc = self.data["accounts"].get(identity)
            if not acc:
                aid = self.data["next_id"]; self.data["next_id"] += 1
                acc = {"AccountId": aid, "DisplayName": "", "Privileges": 9}
                self.data["accounts"][identity] = acc
            token = f"tok-{acc['AccountId']}-{os.urandom(4).hex()}"
            self.data["sessions"][token] = acc["AccountId"]
            self.save(); return acc, token

    def account(self, token):
        aid = self.data["sessions"].get(token)
        return next((a for a in self.data["accounts"].values() if a["AccountId"] == aid), None)


STATE = State(STATE_PATH)


# ---- game endpoints (/<Service>Service.hqs/<Method>) ------------------------
def ep_account_information(req, acc):
    # Privileges must be 9 for a new account or hero-selection never shows.
    return contract("AccountInformation", AccountId=(acc or {}).get("AccountId", 1),
                    DisplayName=(acc or {}).get("DisplayName", ""), Privileges=9)


def ep_choose_display_name(req, acc):
    name = (req.json.get("displayName") or req.json.get("DisplayName") or "Player")
    if acc:
        acc["DisplayName"] = name; STATE.save()
    return contract("AccountSummary", AccountId=(acc or {}).get("AccountId", 1), DisplayName=name)


# method name -> handler(req, acc) ; default below serves a matching example
ENDPOINTS = {
    "GetAccountInformation": ep_account_information,
    "ChooseDisplayName":     ep_choose_display_name,
    "GetAttackSelectionList": lambda r, a: contract("AttackSelectionResult"),
    "GetCastleInfo":          lambda r, a: contract("CastleInfo"),
    "StartAttack":            lambda r, a: contract("AttackInfo"),
    "EndAttack":              lambda r, a: {},
    "GetCastlesForSale":      lambda r, a: contract("CastlesForSaleSelectionResult"),
    "ChooseFirstHero":        lambda r, a: {},          # response contract TBD
    "SendCommands":           lambda r, a: {},          # command bus -> notifications
    "CheckSeasonalCompetitionRewards": lambda r, a: {},
}

# boot / launcher-side endpoints (the local proxy / distribution layer)
def boot_config(req):
    return contract("BootConfig", DistributionServiceUrl=req.base, GameWebsiteUrl=req.base,
                    EnvironmentName="community", WorldName="community")


def distribution(req):
    # echo the client package versions so the patch-check passes
    return PKG_VERSIONS or {}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    @property
    def base(self):
        h = self.headers.get("Host") or f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        return f"http://{h}"

    def token(self):
        a = self.headers.get("Authorization", "")
        return a[7:] if a.lower().startswith("bearer ") else self.headers.get("X-Connection-Token")

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        try: self._json = json.loads(body) if body else {}
        except Exception: self._json = {}
        return body

    @property
    def json(self): return self._json

    def _log(self, body):
        line = f"{now()} {self.command} {self.path} len={len(body)}"
        print(line)
        with open(LOG_PATH, "a") as f:
            f.write(line + ("\n    " + body[:1500].decode("latin1", "replace") if body else "") + "\n")

    def _send(self, obj, code=200):
        p = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(p)))
        self.end_headers(); self.wfile.write(p)

    def _handle(self):
        body = self._read(); self._log(body)
        path = self.path.split("?")[0]
        # game RPC: /<Service>Service.hqs/<Method>
        m = re.match(r"/([A-Za-z]+)Service\.hqs/([A-Za-z]+)", path)
        if m:
            service, method = m.group(1), m.group(2)
            acc = STATE.account(self.token())
            if acc is None:
                acc, _ = STATE.login(self.headers.get("X-Steam-Ticket", "anonymous"))
            h = ENDPOINTS.get(method)
            return self._send(h(self, acc) if h else self._guess(method))
        low = path.lower()
        if "login" in low or "account" in low and "creation" in low:
            acc, token = STATE.login(self.json.get("steamticket", "anonymous"))
            return self._send(contract("LoginResult", AccountId=acc["AccountId"],
                                        ConnectionToken=token, ProfileId=str(acc["AccountId"])))
        if "bootconfig" in low:
            return self._send(boot_config(self))
        if "package" in low or "distribution" in low or "version" in low:
            return self._send(distribution(self))
        # fall back: serve an example matching the last path segment
        seg = os.path.splitext(path.rstrip("/").split("/")[-1])[0]
        return self._send(EXAMPLES.get(seg, {}))

    def _guess(self, method):
        """no handler: serve an example whose contract name appears in the method."""
        for c in EXAMPLES:
            if c.lower() in method.lower():
                return EXAMPLES[c]
        return {}

    do_GET = do_POST = do_PUT = _handle

    def log_message(self, *a): pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    a = ap.parse_args()
    srv = ThreadingHTTPServer((a.host, a.port), Handler)
    print(f"[+] MQEL stub on http://{a.host}:{a.port}  ({len(EXAMPLES)} contract examples)")
    print(f"[+] routing /<Service>Service.hqs/<Method>; state {STATE_PATH}; log {LOG_PATH}")
    try: srv.serve_forever()
    except KeyboardInterrupt: print("\n[+] stopped")


if __name__ == "__main__":
    main()
