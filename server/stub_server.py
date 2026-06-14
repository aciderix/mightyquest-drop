#!/usr/bin/env python3
"""
stub_server.py — minimal community-server stub for The Mighty Quest for Epic Loot.

Goal of this first iteration: stand up an HTTP endpoint that (a) answers the
boot / login sequence with correctly-shaped JSON, and (b) LOGS every request the
client makes — so when the real client (on a Windows box) is pointed here, we
discover the exact Argo routing empirically.

Zero dependencies: Python 3 standard library only. Run it anywhere, including
the machine that runs the game.

    python3 server/stub_server.py --host 0.0.0.0 --port 8080

Then point the client's DistributionServiceUrl / GameServerUrl at
http://<this-host>:8080  (see server/README.md).

Responses are shaped from the reversed schema catalog
(re/catalog/network/generated/examples.json). Boot/login messages get sensible
values; everything else returns its example payload (or {} + a log line).
"""
from __future__ import annotations
import argparse, datetime, json, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES_PATH = os.path.join(ROOT, "re/catalog/network/generated/examples.json")
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "requests.log")

EXAMPLES = {}
if os.path.exists(EXAMPLES_PATH):
    EXAMPLES = json.load(open(EXAMPLES_PATH))


def now():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def example(contract, **overrides):
    """example payload for a contract, with field overrides."""
    obj = dict(EXAMPLES.get(contract, {}))
    obj.update(overrides)
    return obj


# --- boot / login flow, shaped with values that let the client progress -------
def boot_config(base_url):
    return example("BootConfig",
                   DistributionServiceUrl=base_url,
                   GameWebsiteUrl=base_url,
                   EnvironmentName="community",
                   WorldName="community")


def server_definitions(base_url):
    return example("ServerDefinitions",
                   ServerInfos=[example("ServerInfo",
                                        ApplicationID="hyperquest",
                                        DeploymentServiceID="community",
                                        RelativePathToApplication="/",
                                        ServerName="community")])


def game_server_connection_config(base_url):
    return example("GameServerConnectionConfig",
                   GameServerUrl=base_url,
                   AccountName="player",
                   AccountPassword="",
                   HttpCompression=False)


def login_result():
    return example("LoginResult",
                   AccountId=1,
                   ConnectionToken="community-token",
                   ProfileId="1")


# path keyword -> handler producing a response dict
ROUTES = {
    "bootconfig": lambda u: boot_config(u),
    "serverdefinitions": lambda u: server_definitions(u),
    "serverinfo": lambda u: server_definitions(u),
    "gameserverconnectionconfig": lambda u: game_server_connection_config(u),
    "login": lambda u: login_result(),
    "account": lambda u: login_result(),
}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _base_url(self):
        host = self.headers.get("Host") or f"{self.server.server_address[0]}:{self.server.server_address[1]}"
        return f"http://{host}"

    def _log_request(self, body):
        line = (f"{now()} {self.command} {self.path} "
                f"ct={self.headers.get('Content-Type','')} "
                f"len={len(body)}")
        print(line)
        if body:
            print("    body:", body[:600].decode("latin1", "replace"))
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
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        self._log_request(body)
        path = self.path.lower()
        for key, fn in ROUTES.items():
            if key in path:
                return self._respond(fn(self._base_url()))
        # exact match on the last path segment (e.g. /api/CastleInfo -> CastleInfo)
        seg = self.path.rstrip("/").split("/")[-1].split("?")[0]
        seg = os.path.splitext(seg)[0]
        for name, ex in EXAMPLES.items():
            if name.lower() == seg.lower():
                return self._respond(ex)
        # loose fallback: a known contract name appears in the path
        for name, ex in EXAMPLES.items():
            if name.lower() in path:
                return self._respond(ex)
        # unknown -> empty 200 so the client keeps talking; the log captures it
        self._respond({})

    do_GET = _handle
    do_POST = _handle
    do_PUT = _handle

    def log_message(self, *a):  # silence default noisy logging
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8080)
    args = ap.parse_args()
    if not EXAMPLES:
        print(f"[!] {EXAMPLES_PATH} missing — run re/tools/gen_examples.py", file=sys.stderr)
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"[+] Mighty Quest stub server on http://{args.host}:{args.port}")
    print(f"[+] {len(EXAMPLES)} contract examples loaded; requests logged to {LOG_PATH}")
    print("[+] point the client's DistributionServiceUrl/GameServerUrl here")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n[+] stopped")


if __name__ == "__main__":
    main()
