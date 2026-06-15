#!/usr/bin/env python3
"""
stub_server.py — community-server stub for The Mighty Quest for Epic Loot.

Iteration 2: a *stateful* backend. It answers the boot/login sequence, keeps
accounts / sessions / profiles (persisted to server/state.json), and logs every
request so pointing the real client here reveals the exact Argo routing.

Zero dependencies (Python 3 stdlib). Run it on the game machine or a VPS:
    python3 server/stub_server.py --host 0.0.0.0 --port 8080

Responses are shaped from the reversed schema catalog
(re/catalog/network/generated/examples.json, 1,325 contracts). Boot/login/profile
get real stateful values; everything else returns its example payload + a log
line so we can fill it in from observed traffic.
"""
from __future__ import annotations
import argparse, datetime, json, os, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
EXAMPLES_PATH = os.path.join(ROOT, "re/catalog/network/generated/examples.json")
STATE_PATH = os.path.join(HERE, "state.json")
LOG_PATH = os.path.join(HERE, "requests.log")

EXAMPLES = json.load(open(EXAMPLES_PATH)) if os.path.exists(EXAMPLES_PATH) else {}


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def example(contract, **overrides):
    obj = dict(EXAMPLES.get(contract, {}))
    obj.update(overrides)
    return obj


# --- persistent state -------------------------------------------------------
class State:
    def __init__(self, path):
        self.path = path
        self.lock = threading.Lock()
        self.data = {"accounts": {}, "sessions": {}, "profiles": {}, "next_id": 1}
        if os.path.exists(path):
            try:
                self.data.update(json.load(open(path)))
            except Exception:
                pass

    def save(self):
        tmp = self.path + ".tmp"
        json.dump(self.data, open(tmp, "w"), indent=1)
        os.replace(tmp, self.path)

    def login(self, identity):
        """find-or-create an account for `identity` (e.g. a Steam ticket); return
        (account_id, profile_id, token)."""
        with self.lock:
            acc = self.data["accounts"].get(identity)
            if not acc:
                aid = self.data["next_id"]; self.data["next_id"] += 1
                acc = {"AccountId": aid, "ProfileId": str(aid),
                       "DisplayName": f"Player{aid}", "Email": "", "Privileges": 0}
                self.data["accounts"][identity] = acc
                self.data["profiles"][str(aid)] = example(
                    "ProfileInfo", AccountId=aid, DisplayName=acc["DisplayName"]) \
                    if "ProfileInfo" in EXAMPLES else {"AccountId": aid}
            token = f"tok-{acc['AccountId']}-{os.urandom(4).hex()}"
            self.data["sessions"][token] = acc["AccountId"]
            self.save()
            return acc, token

    def account_by_token(self, token):
        with self.lock:
            aid = self.data["sessions"].get(token)
            if aid is None:
                return None
            for acc in self.data["accounts"].values():
                if acc["AccountId"] == aid:
                    return acc
        return None


STATE = State(STATE_PATH)


# --- request handlers (keyword-routed until exact routes are observed) -------
def h_boot(req):
    return example("BootConfig", DistributionServiceUrl=req.base, GameWebsiteUrl=req.base,
                   EnvironmentName="community", WorldName="community")


def h_serverdefs(req):
    return example("ServerDefinitions",
                   ServerInfos=[example("ServerInfo", ApplicationID="hyperquest",
                                        DeploymentServiceID="community",
                                        RelativePathToApplication="/", ServerName="community")])


def h_connection(req):
    return example("GameServerConnectionConfig", GameServerUrl=req.base,
                   AccountName="player", AccountPassword="", HttpCompression=False)


def h_login(req):
    identity = (req.json.get("steamticket") or req.json.get("Ticket")
                or req.headers.get("X-Steam-Ticket") or "anonymous")
    acc, token = STATE.login(identity)
    return example("LoginResult", AccountId=acc["AccountId"],
                   ConnectionToken=token, ProfileId=acc["ProfileId"])


def h_account(req):
    token = req.token()
    acc = STATE.account_by_token(token) if token else None
    if not acc:
        acc, token = STATE.login(req.json.get("steamticket", "anonymous"))
    return example("AccountLite", AccountId=acc["AccountId"], DisplayName=acc["DisplayName"],
                   Email=acc.get("Email", ""), Privileges=acc.get("Privileges", 0),
                   ActivationStatus=1, Password="")


def h_profile(req):
    acc = STATE.account_by_token(req.token())
    pid = acc["ProfileId"] if acc else "1"
    return STATE.data["profiles"].get(pid, example("ProfileInfo"))


ROUTES = [
    ("bootconfig", h_boot),
    ("serverdefinitions", h_serverdefs), ("serverinfo", h_serverdefs),
    ("gameserverconnectionconfig", h_connection),
    ("accountcreation", h_account), ("login", h_login), ("account", h_account),
    ("profile", h_profile),
]


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    # convenience accessors used by handlers
    @property
    def base(self):
        host = self.headers.get("Host") or \
            f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        return f"http://{host}"

    def token(self):
        auth = self.headers.get("Authorization", "")
        if auth.lower().startswith("bearer "):
            return auth[7:]
        return self.headers.get("X-Connection-Token") or self._json.get("ConnectionToken")

    @property
    def json(self):
        return self._json

    def _read(self):
        n = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(n) if n else b""
        try:
            self._json = json.loads(body) if body else {}
        except Exception:
            self._json = {}
        return body

    def _log(self, body):
        line = f"{now()} {self.command} {self.path} ct={self.headers.get('Content-Type','')} len={len(body)}"
        print(line)
        with open(LOG_PATH, "a") as f:
            f.write(line + "\n")
            if body:
                f.write("    " + body[:2000].decode("latin1", "replace") + "\n")

    def _respond(self, obj, code=200):
        payload = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _handle(self):
        body = self._read()
        self._log(body)
        path = self.path.lower()
        for key, fn in ROUTES:
            if key in path:
                return self._respond(fn(self))
        seg = os.path.splitext(self.path.rstrip("/").split("/")[-1].split("?")[0])[0]
        for name, ex in EXAMPLES.items():
            if name.lower() == seg.lower():
                return self._respond(ex)
        self._respond({})

    do_GET = _handle
    do_POST = _handle
    do_PUT = _handle

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args()
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[+] Mighty Quest stub server on http://{args.host}:{args.port}")
    print(f"[+] {len(EXAMPLES)} contract examples; state -> {STATE_PATH}; log -> {LOG_PATH}")
    print("[+] stateful: accounts / sessions / profiles persist across restarts")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] stopped")


if __name__ == "__main__":
    main()
