#!/usr/bin/env python3
"""
mqel_launcher.py — turnkey local launcher for The Mighty Quest for Epic Loot.

Runs the WHOLE thing from one command, fully offline (no external backend):
  1. generates a local CA + server cert for the game-server hostname,
  2. starts a local HTTPS proxy on 127.0.0.1:13432 that answers the game's
     `/<Service>Service.hqs/<Method>` calls with COMPLETE responses from the
     reversed catalog (examples.json — full fields, real enum values, $type),
  3. deploys the winhttp shim + CA + (optionally) patches the exe for SSL,
  4. redirects the game-server hostname to localhost and launches the game.

Drop this next to MightyQuest.exe (GameData/Bin/) together with `mqel_data/`
(examples.json, package_versions.json) and `plumbing/` (winhttp.dll,
patch_binary.py). Then just run it.

    python mqel_launcher.py            # auto-detect exe, Windows or Wine
    python mqel_launcher.py --exe PATH --catalog DIR

Reuses the proven cert/proxy/SSL plumbing from the earlier community effort;
the only change is that responses are generated locally from our complete
catalog instead of being forwarded to a remote backend.
"""
from __future__ import annotations
import argparse, copy, json, os, re, ssl, subprocess, sys, threading, time
from http.server import HTTPServer, BaseHTTPRequestHandler

GAME_HOST = "gs.themightyquest.com"   # the game's hard-coded server hostname
PROXY_PORT = 13432                    # the winhttp shim connects here
HERE = os.path.dirname(os.path.abspath(__file__))

# ── response catalog ─────────────────────────────────────────────────────────
def load_catalog(catalog_dir):
    def j(name):
        for p in (os.path.join(catalog_dir, name), os.path.join(HERE, "mqel_data", name),
                  os.path.join(HERE, name)):
            if os.path.exists(p):
                return json.load(open(p, encoding="utf-8"))
        return {}
    return j("examples.json"), j("package_versions.json")


EXAMPLES, PKG_VERSIONS = {}, {}


def contract(name, **ov):
    o = copy.deepcopy(EXAMPLES.get(name, {})); o.update(ov); return o


# method -> response builder (mirrors server/stub_server.py)
def endpoints():
    return {
        "GetAccountInformation": lambda b: contract("AccountInformation", Privileges=9),
        "ChooseDisplayName":     lambda b: contract("AccountSummary",
                                    DisplayName=(b or {}).get("displayName", "Player")),
        "GetAttackSelectionList": lambda b: contract("AttackSelectionResult"),
        "GetCastleInfo":          lambda b: contract("CastleInfo"),
        "StartAttack":            lambda b: contract("AttackInfo"),
        "EndAttack":              lambda b: {},
        "GetCastlesForSale":      lambda b: contract("CastlesForSaleSelectionResult"),
        "ChooseFirstHero":        lambda b: {},
        "SendCommands":           lambda b: {},
        "CheckSeasonalCompetitionRewards": lambda b: {},
    }


def route(path, body):
    """produce a JSON-able response for a request path (+ parsed body)."""
    p = path.split("?")[0]
    m = re.match(r"/([A-Za-z]+)Service\.hqs/([A-Za-z]+)", p)
    if m:
        h = endpoints().get(m.group(2))
        if h:
            return h(body)
        for c in EXAMPLES:                      # fall back: example by method name
            if c.lower() in m.group(2).lower():
                return EXAMPLES[c]
        return {}
    low = p.lower()
    if "package" in low or "distribution" in low or "version" in low:
        return PKG_VERSIONS or {}
    seg = os.path.splitext(p.rstrip("/").split("/")[-1])[0]
    return EXAMPLES.get(seg, {})


# ── local HTTPS proxy ────────────────────────────────────────────────────────
LOG = os.path.join(HERE, "mqel_requests.log")


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def _body(self):
        n = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(n) if n else b""
        try: return raw, (json.loads(raw) if raw else {})
        except Exception: return raw, {}

    def _serve(self):
        raw, jb = self._body()
        try:
            resp = route(self.path, jb)
        except Exception as e:
            resp = {}
        with open(LOG, "a") as f:
            f.write(f"{self.command} {self.path} len={len(raw)} -> {len(json.dumps(resp))}b\n")
        payload = json.dumps(resp).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers(); self.wfile.write(payload)

    do_GET = do_POST = do_PUT = _serve

    def log_message(self, *a): pass


def ensure_certs():
    """two-level PKI (CA + CA-signed server cert) — satisfies the game's
    OpenSSL 1.0.1e. Returns (server_cert, server_key, ca_cert)."""
    cdir = os.path.join(HERE, ".mqel_certs"); os.makedirs(cdir, exist_ok=True)
    ca_key, ca = os.path.join(cdir, "ca.key"), os.path.join(cdir, "ca.pem")
    sk, sc = os.path.join(cdir, "server.key"), os.path.join(cdir, "server.pem")
    if all(os.path.exists(x) for x in (ca, sk, sc)):
        return sc, sk, ca
    san = f"subjectAltName=DNS:{GAME_HOST},IP:127.0.0.1,DNS:localhost\n"
    ext = os.path.join(cdir, "ext.cnf")
    open(ext, "w").write(san + "basicConstraints=critical,CA:FALSE\n"
                         "keyUsage=critical,digitalSignature,keyEncipherment\n"
                         "extendedKeyUsage=serverAuth\n")
    R = lambda *a: subprocess.run(a, check=True, capture_output=True)
    R("openssl", "req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", ca_key,
      "-out", ca, "-sha256", "-days", "3650", "-subj", "/CN=MQEL-CA/O=MQEL",
      "-addext", "basicConstraints=critical,CA:TRUE",
      "-addext", "keyUsage=critical,keyCertSign,cRLSign")
    csr = os.path.join(cdir, "server.csr")
    R("openssl", "req", "-newkey", "rsa:2048", "-nodes", "-keyout", sk, "-out", csr,
      "-subj", f"/CN={GAME_HOST}/O=MQEL")
    R("openssl", "x509", "-req", "-in", csr, "-CA", ca, "-CAkey", ca_key,
      "-CAcreateserial", "-out", sc, "-days", "3650", "-sha256", "-extfile", ext)
    print("[ok] generated local CA + server certificate")
    return sc, sk, ca


def start_proxy(cert, key):
    srv = HTTPServer(("127.0.0.1", PROXY_PORT), Handler)
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cert, key)
    ctx.minimum_version = ssl.TLSVersion.TLSv1      # the 2013 client needs TLS 1.0
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print(f"[ok] HTTPS proxy on 127.0.0.1:{PROXY_PORT} (serving local catalog)")
    return srv


# ── host / exe / launch plumbing ─────────────────────────────────────────────
def hosts_path():
    return (r"C:\Windows\System32\drivers\etc\hosts" if os.name == "nt" else "/etc/hosts")


def add_hosts():
    hp = hosts_path(); line = f"127.0.0.1 {GAME_HOST}"
    try:
        if line in open(hp, errors="ignore").read():
            return
        with open(hp, "a") as f:
            f.write(f"\n# MQEL\n{line}\n")
        print(f"[ok] redirected {GAME_HOST} -> 127.0.0.1 in {hp}")
    except PermissionError:
        print(f"[!] add this line to {hp} (admin/sudo):  {line}")


def find_exe(hint):
    cands = [hint] if hint else []
    cands += [os.path.join(HERE, n) for n in ("MightyQuest_mqel.exe", "MightyQuest.exe")]
    cands += [os.path.join(HERE, "..", "MightyQuest.exe")]
    for c in cands:
        if c and os.path.exists(c):
            return os.path.abspath(c)
    return None


def prepare_exe(exe, ca):
    """deploy winhttp shim + CA next to the exe; patch SSL path if needed."""
    gdir = os.path.dirname(exe)
    dll = os.path.join(HERE, "plumbing", "winhttp.dll")
    if os.path.exists(dll):
        import shutil; shutil.copy(dll, os.path.join(gdir, "winhttp.dll"))
        print("[ok] deployed winhttp shim next to the game")
    else:
        print("[!] plumbing/winhttp.dll missing — build it (plumbing/build.sh)")
    import shutil; shutil.copy(ca, os.path.join(gdir, "ca.pem"))         # relative cert path
    # if not already a *_mqel.exe, patch the OpenSSL cert path in place
    if not exe.endswith("_mqel.exe"):
        patch = os.path.join(HERE, "plumbing", "patch_binary.py")
        out = os.path.join(gdir, "MightyQuest_mqel.exe")
        if os.path.exists(patch) and not os.path.exists(out):
            try:
                subprocess.run([sys.executable, patch, exe, out], check=True)
                print("[ok] patched exe SSL cert path -> MightyQuest_mqel.exe")
                return out
            except Exception as e:
                print(f"[!] exe patch failed ({e}); will try the unpatched exe")
    return exe


def launch(exe):
    gdir = os.path.dirname(exe); env = dict(os.environ)
    if os.name != "nt":                               # Linux/macOS via Wine
        env["WINEDLLOVERRIDES"] = "winhttp=n"         # load our local winhttp shim
        cmd = ["wine", exe]
    else:
        cmd = [exe]
    print(f"[+] launching {os.path.basename(exe)} …")
    return subprocess.Popen(cmd, cwd=gdir, env=env)


def main():
    global EXAMPLES, PKG_VERSIONS
    ap = argparse.ArgumentParser()
    ap.add_argument("--exe")
    ap.add_argument("--catalog", default=os.path.join(HERE, "..", "re/catalog/network/generated"))
    a = ap.parse_args()

    EXAMPLES, PKG_VERSIONS = load_catalog(a.catalog)
    if not EXAMPLES:
        print("[!] examples.json not found — copy re/catalog/network/generated/examples.json "
              "and package_versions.json into mqel_data/ next to this launcher.")
    print(f"[ok] loaded {len(EXAMPLES)} contract responses")

    cert, key, ca = ensure_certs()
    start_proxy(cert, key)
    add_hosts()

    exe = find_exe(a.exe)
    if not exe:
        print("[!] MightyQuest.exe not found — place this launcher next to it, or pass --exe.")
        print("    Proxy is running; you can point a client at https://%s:%d" % (GAME_HOST, PROXY_PORT))
    else:
        exe = prepare_exe(exe, ca)
        proc = launch(exe)
        print("[+] playing — requests logged to mqel_requests.log. Ctrl-C to stop.")
        try:
            proc.wait()
        except KeyboardInterrupt:
            pass
    try:
        while not exe:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[+] stopped")


if __name__ == "__main__":
    main()
