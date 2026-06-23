#!/usr/bin/env python3
"""
MQEL local launcher — connecte le jeu au serveur local (127.0.0.1:13432).

Fonctionnement :
  1. Appelle POST /auth sur notre serveur local → obtient access_token + user_id
  2. Lance MightyQuest_mqel.exe (exe patché : ca.pem au lieu de /usr/local/ssl/cert.pem)
     avec les arguments -server_url / -steamticket / -steamid / etc.
  3. Le jeu se connecte à 127.0.0.1:13432 (Localnetworking DLL hardcodée)

Usage :  python launch_game.py
"""
import json, os, ssl, subprocess, sys, time, urllib.request

SERVER     = "https://127.0.0.1:13432"
GAME_DIR   = r"C:\Program Files (x86)\Steam\steamapps\common\The Mighty Quest For Epic Loot\GameData\Bin"
PATCHED_EXE = os.path.join(GAME_DIR, "MightyQuest_mqel.exe")
ORIG_EXE    = os.path.join(GAME_DIR, "MightyQuest.exe")

CTX = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode    = ssl.CERT_NONE


def call(path, body=None, token=None):
    h = {"Content-Type": "application/json"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(f"{SERVER}{path}",
          data=json.dumps(body or {}).encode(), headers=h, method="POST")
    return json.loads(urllib.request.urlopen(req, context=CTX, timeout=10).read())


def main():
    # ---- choisir l'exe à lancer
    if os.path.exists(PATCHED_EXE):
        exe = PATCHED_EXE
        print(f"[+] Utilise l'exe patché : {os.path.basename(exe)}")
    elif os.path.exists(ORIG_EXE):
        exe = ORIG_EXE
        print(f"[!] Exe patché absent, utilise l'original (TLS peut échouer) : {os.path.basename(exe)}")
    else:
        print(f"[ERR] MightyQuest.exe introuvable dans {GAME_DIR}"); sys.exit(1)

    # ---- copier notre ca.pem à côté de l'exe (l'exe patché cherche 'ca.pem' relatif)
    here = os.path.dirname(os.path.abspath(__file__))
    ca_src = os.path.join(here, ".mqel_certs", "ca.pem")
    ca_dst = os.path.join(GAME_DIR, "ca.pem")
    if os.path.exists(ca_src):
        import shutil; shutil.copy2(ca_src, ca_dst)
        print(f"[+] ca.pem copié dans {GAME_DIR}")
    else:
        print("[!] .mqel_certs/ca.pem absent — TLS peut échouer")

    # ---- authentification sur le serveur local
    print("[*] Authentification sur le serveur local...")
    try:
        auth = call("/auth")
    except Exception as e:
        print(f"[ERR] Impossible de contacter le serveur ({e})")
        print("      Lance d'abord start_server.bat (port 13432).")
        sys.exit(1)

    access_token  = auth["access_token"]
    user_id       = auth["user_id"]
    # steamid doit être un entier ≥ 76561100000000000 (format Steam64)
    numeric_id    = str(abs(hash(user_id)) % (10**17) + 76561100000000000)

    print(f"[+] Session créée — user_id: {user_id}")
    print(f"[+] Lancement de {os.path.basename(exe)}...")
    print()

    cmd = [
        exe,
        "-server_url",      SERVER,
        "-token",           "",           # vide = déclenche le login flow
        "-steamticket",     user_id,      # non-vide = déclenche le login flow
        "-steamid",         numeric_id,
        "-environmentName", "mqel-live",
        "-branchName",      "mqel",
    ]

    env = os.environ.copy()
    # Ne pas laisser un proxy système intercepter les connexions localhost
    for v in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY", "all_proxy"):
        env.pop(v, None)
    # Pointer libcurl/OpenSSL vers notre CA (belt-and-suspenders avec le binaire patché)
    env["CURL_CA_BUNDLE"] = ca_dst
    env["SSL_CERT_FILE"]  = ca_dst

    proc = subprocess.Popen(cmd, cwd=GAME_DIR, env=env)
    print(f"[+] Jeu lancé (PID {proc.pid})")
    print(f"[+] Le serveur proxy doit rester ouvert (fenêtre start_server).")
    print(f"    Ctrl+C ici pour arrêter le monitoring.")
    print()

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n[*] Fermeture.")


if __name__ == "__main__":
    main()
