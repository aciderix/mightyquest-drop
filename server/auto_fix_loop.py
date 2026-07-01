#!/usr/bin/env python3
"""
auto_fix_loop.py - boucle autonome : lance le jeu, surveille via CDP,
lit le MQLog, corrige array_fields.json, recommence jusqu'a succes.

Usage: python auto_fix_loop.py [--max-iterations N]
"""
import json, os, re, subprocess, sys, time, ssl, urllib.request
import ctypes, threading

HERE = os.path.dirname(os.path.abspath(__file__))
GAME_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\The Mighty Quest For Epic Loot\GameData\Bin"
MQLOG    = os.path.join(GAME_DIR, "MQLog.txt")
ARRAY_FIELDS_PATH = os.path.normpath(os.path.join(HERE, "..", "re", "catalog", "network", "gamedata", "array_fields.json"))
SERVER_CMD = [sys.executable, os.path.join(HERE, "stub_server.py"),
              "--host", "0.0.0.0", "--port", "443", "--tls",
              "--cert", os.path.join(HERE, ".mqel_certs", "server.pem"),
              "--key",  os.path.join(HERE, ".mqel_certs", "server.key")]
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE

# ── websocket (stdlib only) ───────────────────────────────────────────────
try:
    import websocket
    HAS_WS = True
except ImportError:
    HAS_WS = False
    print("[WARN] websocket-client not installed - DOM monitoring disabled")
    print("       pip install websocket-client")


def kill_game():
    subprocess.run(["taskkill", "/F", "/IM", "MightyQuest.exe"], capture_output=True)
    time.sleep(1)


def kill_server():
    subprocess.run(["taskkill", "/F", "/IM", "python.exe", "/FI", "WINDOWTITLE eq MQEL*"],
                   capture_output=True)
    # Also kill by port
    subprocess.run(r'for /f "tokens=5" %a in (\'netstat -aon ^| find ":443 "\') do taskkill /F /PID %a',
                   shell=True, capture_output=True)
    time.sleep(2)


def start_server():
    kill_server()
    # Remove state/trace for clean run
    for f in ("state.json", "trace.jsonl"):
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            os.remove(p)
    proc = subprocess.Popen(SERVER_CMD, cwd=HERE, creationflags=subprocess.CREATE_NEW_CONSOLE)
    time.sleep(4)
    # Verify it's up
    for _ in range(10):
        try:
            urllib.request.urlopen(
                urllib.request.Request("https://127.0.0.1:443/AccountService.hqs/GetAccountInformation",
                    data=b"{}", method="POST"), context=CTX, timeout=3)
            print("[+] Serveur pret")
            return proc
        except:
            time.sleep(1)
    raise RuntimeError("Serveur ne repond pas")


def get_session():
    """Get auth token from server."""
    r = urllib.request.Request("https://127.0.0.1:443/auth",
        data=b"{}", method="POST", headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, context=CTX, timeout=5).read())


def launch_game(user_id):
    """Deploy CA and launch MightyQuest.exe with CDP enabled."""
    import shutil
    ca_src = os.path.join(HERE, ".mqel_certs", "ca.pem")
    shutil.copy2(ca_src, os.path.join(GAME_DIR, "ca.pem"))
    os.makedirs(r"C:\usr\local\ssl", exist_ok=True)
    shutil.copy2(ca_src, r"C:\usr\local\ssl\cert.pem")

    numeric_id = str(abs(hash(user_id)) % (10**17) + 76561100000000000)
    env = os.environ.copy()
    for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY"):
        env.pop(v, None)
    env["CURL_CA_BUNDLE"] = r"C:\usr\local\ssl\cert.pem"
    env["SSL_CERT_FILE"]  = r"C:\usr\local\ssl\cert.pem"
    env["OPENSSL_CONF"]   = ""

    cmd = [os.path.join(GAME_DIR, "MightyQuest.exe"),
           "-server_url", "https://127.0.0.1:443",
           "-token", "", "-steamticket", user_id,
           "-steamid", numeric_id,
           "-environmentName", "mqel-live", "-branchName", "mqel",
           "--remote-debugging-port=9222", "--remote-allow-origins=*"]
    proc = subprocess.Popen(cmd, cwd=GAME_DIR, env=env)
    print(f"[+] Jeu lance PID {proc.pid}")

    # SSL memory patch in background
    def _patch():
        from launch_game import _patch_ssl
        _patch_ssl(proc.pid, delay=20.0)
    threading.Thread(target=_patch, daemon=True).start()
    return proc


def wait_for_cdp(timeout=60):
    """Wait for CDP port 9222 to be ready."""
    print("[*] Attente CDP (port 9222)...")
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            resp = urllib.request.urlopen("http://localhost:9222/json/version", timeout=2)
            print("[+] CDP pret")
            return True
        except:
            time.sleep(2)
    return False


def cdp_get_dom_text():
    """Connect to CDP once, read DOM text, close. Returns text or None."""
    if not HAS_WS:
        return None
    try:
        pages = json.loads(urllib.request.urlopen("http://localhost:9222/json", timeout=5).read())
        page_ws = next((p["webSocketDebuggerUrl"] for p in pages
                        if p.get("type") == "page" and p.get("webSocketDebuggerUrl")), None)
        if not page_ws:
            return None
        ws = websocket.create_connection(page_ws, timeout=10, suppress_origin=True)
        ws.send(json.dumps({"id": 1, "method": "Runtime.evaluate",
                            "params": {"expression": "document.body && document.body.innerText || ''",
                                       "returnByValue": True}}))
        ws.settimeout(8)
        while True:
            m = json.loads(ws.recv())
            if m.get("id") == 1:
                ws.close()
                return m.get("result", {}).get("result", {}).get("value", "")
    except Exception as e:
        print(f"[CDP] {e}")
        return None


def read_mqlog_errors():
    """Return (position, expected_char) from MQLog JSON ERROR, or None."""
    if not os.path.exists(MQLOG):
        return None
    for line in open(MQLOG, encoding="utf-8", errors="replace"):
        m = re.search(r"JSON ERROR: Memory Stream\(\d+,(\d+)\): Expected character: '(.)'", line)
        if m:
            return int(m.group(1)), m.group(2)
    return None


def read_mqlog_shutdown():
    """Return the shutdown reason from MQLog, or None if still running."""
    if not os.path.exists(MQLOG):
        return None
    lines = open(MQLOG, encoding="utf-8", errors="replace").readlines()
    # Read all lines to get all shutdown reasons
    reasons = []
    for line in lines:
        m = re.search(r"Application shutdown.*?Reason\s*:\s*(.+)", line)
        if m:
            reasons.append(m.group(1).strip())
    return reasons[-1] if reasons else None


def read_mqlog_last_error():
    """Return last meaningful error/warning from MQLog."""
    if not os.path.exists(MQLOG):
        return None
    lines = list(open(MQLOG, encoding="utf-8", errors="replace"))
    for line in reversed(lines[-100:]):
        if any(t in line for t in ["ERROR", "FAIL", "failed", "error"]) and "WARNING" not in line and "IsVisible" not in line:
            return line.strip()
    return None


def get_field_at_pos(pos):
    """Find which field is at byte position `pos` in the AccountInformation response."""
    r = urllib.request.Request(
        "https://127.0.0.1:443/AccountService.hqs/GetAccountInformation",
        data=b"{}", method="POST", headers={"Content-Type": "application/json"})
    txt = urllib.request.urlopen(r, context=CTX, timeout=5).read().decode("utf-8")
    # pos is 1-based in the game's stream (full JSON from byte 1)
    byte = pos - 1
    context = txt[max(0, byte-60):byte+10]
    # find the last "fieldname": before this position
    m = re.findall(r'"([A-Za-z][A-Za-z0-9_]*)":\s*$|"([A-Za-z][A-Za-z0-9_]*)":\s+[^{[]', context)
    keys = re.findall(r'"([A-Za-z][A-Za-z0-9_]*)"\s*:', context)
    print(f"  Contexte byte {pos}: {repr(context)}")
    return keys[-1] if keys else None, txt


def fix_array_fields(field_name, expected_char):
    """Add or remove field from array_fields.json based on what game expects."""
    fields = json.load(open(ARRAY_FIELDS_PATH))
    changed = False
    if expected_char == "[" and field_name not in fields:
        fields.append(field_name)
        print(f"  [FIX] {field_name} -> [] (ajoute a array_fields)")
        changed = True
    elif expected_char == "{" and field_name in fields:
        fields = [f for f in fields if f != field_name]
        print(f"  [FIX] {field_name} -> {{}} (retire de array_fields)")
        changed = True
    if changed:
        json.dump(sorted(fields), open(ARRAY_FIELDS_PATH, "w"), indent=1)
    return changed


# ── main loop ─────────────────────────────────────────────────────────────
def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-iterations", type=int, default=20)
    args = ap.parse_args()

    print("=" * 60)
    print("MQEL auto-fix loop - detecte et corrige les erreurs JSON")
    print("=" * 60)

    for iteration in range(1, args.max_iterations + 1):
        print(f"\n{'='*50}")
        print(f"=== ITERATION {iteration} ===")
        print(f"{'='*50}")

        # 1. Start server
        print("[1] Demarrage du serveur...")
        srv_proc = start_server()

        # 2. Auth + launch game
        print("[2] Authentification + lancement du jeu...")
        auth = get_session()
        game_proc = launch_game(auth["user_id"])

        # 3. Wait for CDP
        cdp_ready = wait_for_cdp(timeout=90)

        # 4. Monitor: wait for error or success
        print("[3] Surveillance (max 60s)...")
        deadline = time.time() + 60
        error_found = False
        success = False

        while time.time() < deadline:
            time.sleep(3)

            # Check if game still running
            if game_proc.poll() is not None:
                print("[!] Jeu termine")
                break

            # Check DOM for error/success text
            if cdp_ready and HAS_WS:
                dom = cdp_get_dom_text()
                if dom:
                    if any(t in dom.lower() for t in ["network error", "erreur reseau",
                                                       "serveur en maintenance", "maintenance"]):
                        print(f"[DOM] Erreur detectee: {dom[:120]}")
                        error_found = True
                        break
                    if any(t in dom for t in ["Choose a display name", "Choisissez",
                                               "Select your hero", "Knight", "Archer",
                                               "Castle Level", "lobby"]):
                        print(f"[DOM] Succes ! UI chargee: {dom[:120]}")
                        success = True
                        break

            # Check MQLog regardless
            err = read_mqlog_errors()
            if err:
                pos, exp = err
                print(f"[MQLog] JSON ERROR a pos {pos}, Expected '{exp}'")
                error_found = True
                break

        # 5. Read MQLog for error details
        err = read_mqlog_errors()

        if success:
            # Kill game + server then report
            game_proc.terminate(); kill_game()
            srv_proc.terminate(); kill_server()
            print("\n" + "="*50)
            print("SUCCeS ! Le jeu charge l'interface correctement.")
            print("="*50)
            return 0

        if not err:
            err = read_mqlog_errors()

        # Analyse the error BEFORE killing the server
        field_name = None
        if err:
            pos, exp_char = err
            print(f"\n[5] Analyse: pos={pos} expected='{exp_char}'")
            try:
                field_name, _ = get_field_at_pos(pos)
                print(f"  Champ fautif: {field_name}")
            except Exception as e:
                print(f"  [!] get_field_at_pos failed: {e}")

        # Now kill game + server
        print("[4] Arret du jeu...")
        game_proc.terminate(); kill_game(); time.sleep(2)
        srv_proc.terminate(); kill_server()

        if not err:
            # Check what actually happened
            shutdown = read_mqlog_shutdown()
            last_err = read_mqlog_last_error()
            print(f"[?] Pas de JSON ERROR.")
            print(f"    Shutdown reason: {shutdown}")
            print(f"    Dernier log error: {last_err}")
            # Check trace for what endpoints were called
            trace_path = os.path.join(HERE, "trace.jsonl")
            if os.path.exists(trace_path):
                lines = open(trace_path).readlines()
                print(f"    Requetes recues ({len(lines)}):")
                for l in lines:
                    try:
                        j = json.loads(l)
                        print(f"      #{j.get('seq')} {j.get('method')} flags={j.get('flags')}")
                    except:
                        pass
            if shutdown and "AccountInformation" not in (shutdown or ""):
                print("[+] AccountInformation OK! Nouveau probleme detecte.")
                print("    Correction manuelle requise - voir shutdown + trace ci-dessus.")
            return 1

        if not field_name:
            print("[!] Impossible de determiner le champ. Arret.")
            return 1

        fixed = fix_array_fields(field_name, exp_char)
        if not fixed:
            print(f"[!] Aucune correction appliquee pour {field_name}. Arret.")
            return 1

        print(f"[6] Correction appliquee - iteration suivante")

    print("\n[!] Max iterations atteint sans succes.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
