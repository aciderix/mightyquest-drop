#!/usr/bin/env python3
"""
monitor_server.py — instrumented local backend for MQEL end-to-end testing.

Listens on several ports at once (plain HTTP + HTTPS) so we capture whatever
the unmodified client actually does, and logs EVERY exchange in full (method,
path, headers, request body, response body) to a JSONL trace for automatic
validation. Routing/response generation reuses the reversed catalog
(examples.json) exactly like server/stub_server.py / mqel_launcher.py.

    python3 monitor_server.py
"""
from __future__ import annotations
import copy, json, os, re, ssl, threading, time, socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_HOST = "gs.themightyquest.com"
HTTP_PORTS  = [80, 8080]
HTTPS_PORTS = [443, 13432]
TRACE = os.path.join(HERE, "trace.jsonl")

def _find(name):
    for p in (os.path.join(HERE, name),
              os.path.join(HERE, "..", "mqel_data", name),
              os.path.join(HERE, "..", "..", "re", "catalog", "network", "generated", name)):
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)

EXAMPLES = json.load(open(_find("examples.json"), encoding="utf-8"))
PKG = json.load(open(_find("package_versions.json"), encoding="utf-8"))

_lock = threading.Lock()
_seq = 0


def contract(name, **ov):
    o = copy.deepcopy(EXAMPLES.get(name, {})); o.update(ov); return o


# method -> response builder (mirrors stub_server.py + a stateful command bus)
def endpoints():
    return {
        "GetAccountInformation":  lambda b: contract("AccountInformation", Privileges=9),
        "ChooseDisplayName":      lambda b: contract("AccountSummary",
                                     DisplayName=(b or {}).get("displayName", "Player")),
        "GetAttackSelectionList": lambda b: contract("AttackSelectionResult"),
        "GetCastleInfo":          lambda b: contract("CastleInfo"),
        "StartAttack":            lambda b: contract("AttackInfo"),
        "EndAttack":              lambda b: {},
        "GetCastlesForSale":      lambda b: contract("CastlesForSaleSelectionResult"),
        "GetCastleForSaleBuildInfo": lambda b: contract("CastleBuildInfo"),
        "ChooseFirstHero":        lambda b: {},
        "SendCommands":           lambda b: [],
        "KeepAlive":              lambda b: {},
        "CheckSeasonalCompetitionRewards": lambda b: {},
        "CheckNotifications":     lambda b: [],
        "GetRMPackagesVersion":   lambda b: PKG,
    }


def route(path, body):
    p = path.split("?")[0]
    m = re.match(r"/([A-Za-z]+)Service\.hqs/([A-Za-z]+)", p)
    matched = "unmatched"
    if m:
        svc, meth = m.group(1), m.group(2)
        h = endpoints().get(meth)
        if h:
            return h(body), f"endpoint:{svc}.{meth}"
        for c in EXAMPLES:
            if c.lower() in meth.lower():
                return EXAMPLES[c], f"fallback-example:{c}"
        return {}, f"hqs-empty:{svc}.{meth}"
    low = p.lower()
    if "package" in low or "distribution" in low or "version" in low:
        return PKG, "pkg-versions"
    seg = os.path.splitext(p.rstrip("/").split("/")[-1])[0]
    if seg in EXAMPLES:
        return EXAMPLES[seg], f"example:{seg}"
    return {}, matched


def log_exchange(rec):
    global _seq
    with _lock:
        _seq += 1
        rec["seq"] = _seq
        with open(TRACE, "a") as f:
            f.write(json.dumps(rec) + "\n")
        # human-friendly stderr line
        print(f"[{_seq:04d}] {rec['scheme']}:{rec['port']} {rec['method']} {rec['path']} "
              f"req={rec['req_len']}b -> {rec['resp_len']}b ({rec['route']})", flush=True)
    return _seq


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "MQEL-Monitor/1.0"

    def _read_body(self):
        n = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(n) if n else b""
        try:
            jb = json.loads(raw) if raw else {}
        except Exception:
            jb = None
        return raw, jb

    def _handle(self):
        raw, jb = self._read_body()
        try:
            resp, rt = route(self.path, jb if jb is not None else {})
        except Exception as e:
            resp, rt = {}, f"error:{e}"
        payload = json.dumps(resp).encode()
        try:
            body_txt = raw.decode("utf-8", "replace")
        except Exception:
            body_txt = repr(raw)
        log_exchange({
            "ts": time.time(),
            "scheme": self.server.scheme,
            "port": self.server.server_address[1],
            "method": self.command,
            "path": self.path,
            "host": self.headers.get("Host", ""),
            "ua": self.headers.get("User-Agent", ""),
            "headers": dict(self.headers),
            "req_len": len(raw),
            "req_body": body_txt[:4000],
            "route": rt,
            "resp_len": len(payload),
            "resp_body": payload.decode()[:2000],
        })
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception:
            pass

    do_GET = do_POST = do_PUT = do_DELETE = do_PATCH = do_HEAD = _handle

    def log_message(self, *a):
        pass


class ThreadingHTTPServer(socketserver.ThreadingMixIn, HTTPServer):
    daemon_threads = True
    scheme = "http"


def make_ssl_ctx():
    cdir = os.path.join(HERE, "certs")
    cert = os.path.join(cdir, "server.pem")
    key = os.path.join(cdir, "server.key")
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    # the 2013/2014 client supports old TLS; allow the widest range
    try:
        ctx.minimum_version = ssl.TLSVersion.TLSv1
    except Exception:
        pass
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    try:
        ctx.set_ciphers("ALL:@SECLEVEL=0")
    except Exception:
        pass
    return ctx


def serve(port, https):
    try:
        srv = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    except PermissionError:
        print(f"[!] cannot bind port {port} (permission)"); return
    except OSError as e:
        print(f"[!] port {port} unavailable: {e}"); return
    if https:
        try:
            ctx = make_ssl_ctx()
        except FileNotFoundError:
            srv.server_close()
            print(f"[!] skip https :{port} — run gen_certs.sh first (certs/ missing)")
            return
        srv.scheme = "https"
        srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    print(f"[ok] listening {'https' if https else 'http'}://0.0.0.0:{port}")
    threading.Thread(target=srv.serve_forever, daemon=True).start()


def main():
    open(TRACE, "w").close()
    for p in HTTP_PORTS:
        serve(p, https=False)
    for p in HTTPS_PORTS:
        serve(p, https=True)
    print(f"[ok] {len(EXAMPLES)} contracts loaded; tracing to {TRACE}")
    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
