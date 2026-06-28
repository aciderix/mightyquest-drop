#!/usr/bin/env python3
"""
MQEL local launcher — même mécanique que l'ancien launcher.py qui fonctionnait.

Fonctionnement (doc §2-4) :
  1. POST /auth → session (access_token + user_id)
  2. Deploie ca.pem dans C:/usr/local/ssl/cert.pem  (OpenSSL OPENSSLDIR compile)
     + a cote de l'exe (relatif 'ca.pem' pour le binaire patche)
  3. Lance MightyQuest.exe (original) avec args:
       -server_url https://gs.themightyquest.com  (le hosts redirige vers 127.0.0.1)
       -token ""  -steamticket <user_id>  -steamid <int64>
       -environmentName mqel-live  -branchName mqel
  4. Après 20 secondes : patch mémoire SSL libcurl (bypass verifypeer/verifyresult)
     — même patterns que MQELOffline.dll, doc §3.2 Approche B
"""
import ctypes, json, os, shutil, ssl, subprocess, sys, threading, time, urllib.request

GAME_DIR = r"C:\Program Files (x86)\Steam\steamapps\common\The Mighty Quest For Epic Loot\GameData\Bin"
ORIG_EXE  = os.path.join(GAME_DIR, "MightyQuest.exe")

# Le serveur local écoute sur 443, le hosts redirige gs.themightyquest.com → 127.0.0.1
SERVER_LOCAL = "https://127.0.0.1:443"
SERVER_URL   = "https://127.0.0.1:443"  # direct — pas de dépendance DNS/hosts

CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE


def call(path, body=None):
    req = urllib.request.Request(f"{SERVER_LOCAL}{path}",
          data=json.dumps(body or {}).encode(),
          headers={"Content-Type": "application/json"}, method="POST")
    return json.loads(urllib.request.urlopen(req, context=CTX, timeout=10).read())


def deploy_ca(ca_src):
    """Déploie le CA aux emplacements qu'OpenSSL 1.0.1e cherche sur Windows."""
    # OpenSSL OPENSSLDIR compilé = /usr/local/ssl → C:\usr\local\ssl sur Windows
    openssl_dir = r"C:\usr\local\ssl"
    openssl_cert = os.path.join(openssl_dir, "cert.pem")
    os.makedirs(openssl_dir, exist_ok=True)
    shutil.copy2(ca_src, openssl_cert)
    print(f"[+] CA -> {openssl_cert}")
    # Aussi à côté de l'exe (relatif 'ca.pem' pour le binaire patché si présent)
    shutil.copy2(ca_src, os.path.join(GAME_DIR, "ca.pem"))
    print(f"[+] CA -> {GAME_DIR}\\ca.pem")
    return openssl_cert


def _patch_ssl(pid, delay=20.0):
    """Patch mémoire SSL libcurl — doc §3.2 Approche B / patterns MQELOffline.dll.
    Attend `delay` secondes pour que UBX décompresse et que l'anti-tamper passe."""
    import ctypes
    k32 = ctypes.windll.kernel32
    PROCESS_VM_READ = 0x0010; PROCESS_VM_WRITE = 0x0020; PROCESS_VM_OPERATION = 0x0008
    MEM_COMMIT = 0x1000; PAGE_EXECUTE_READWRITE = 0x40

    # Setter verifypeer/verifyhost → return 1
    PATTERN1 = bytes.fromhex("8B442404" "8B4C2408" "8B54240C"
                              "8988C0000000" "8990E8000000" "C3")
    PATCH1   = b"\xB8\x01\x00\x00\x00\xC3" + b"\x90" * (len(PATTERN1) - 6)
    # Getter ssl.verifyresult → return 0
    PATTERN2 = bytes.fromhex("8B442404" "8B80EC000000" "C3")
    PATCH2   = b"\xB8\x00\x00\x00\x00\xC3" + b"\x90" * (len(PATTERN2) - 6)

    class MBI(ctypes.Structure):
        _fields_ = [("BaseAddress",ctypes.c_size_t),("AllocationBase",ctypes.c_size_t),
                    ("AllocationProtect",ctypes.c_uint32),("RegionSize",ctypes.c_size_t),
                    ("State",ctypes.c_uint32),("Protect",ctypes.c_uint32),("Type",ctypes.c_uint32)]

    print(f"[PATCH] Attente {delay:.0f}s (UBX unpack + anti-tamper)...")
    time.sleep(delay)

    h = k32.OpenProcess(PROCESS_VM_READ|PROCESS_VM_WRITE|PROCESS_VM_OPERATION, False, pid)
    if not h:
        print(f"[PATCH] Impossible d'ouvrir PID {pid}"); return

    def scan_patch(pattern, patch, label):
        mbi = MBI(); addr = 0; count = 0
        while k32.VirtualQueryEx(h, ctypes.c_size_t(addr), ctypes.byref(mbi), ctypes.sizeof(mbi)):
            next_addr = mbi.BaseAddress + mbi.RegionSize
            if mbi.State == MEM_COMMIT and mbi.Protect not in (0, 0x01):
                buf = ctypes.create_string_buffer(mbi.RegionSize)
                read = ctypes.c_size_t(0)
                if k32.ReadProcessMemory(h, ctypes.c_size_t(mbi.BaseAddress), buf, mbi.RegionSize, ctypes.byref(read)):
                    chunk = bytes(buf); idx = 0
                    while True:
                        pos = chunk.find(pattern, idx)
                        if pos < 0: break
                        target = mbi.BaseAddress + pos
                        old_p = ctypes.c_uint32(0)
                        k32.VirtualProtectEx(h, ctypes.c_size_t(target), len(patch), PAGE_EXECUTE_READWRITE, ctypes.byref(old_p))
                        k32.WriteProcessMemory(h, ctypes.c_size_t(target), patch, len(patch), None)
                        k32.VirtualProtectEx(h, ctypes.c_size_t(target), len(patch), old_p, ctypes.byref(old_p))
                        count += 1; idx = pos + len(patch)
            if next_addr <= addr: break
            addr = next_addr
        return count

    try:
        n1 = scan_patch(PATTERN1, PATCH1, "verifypeer setter")
        n2 = scan_patch(PATTERN2, PATCH2, "verifyresult getter")
        if n1 or n2:
            print(f"[PATCH] SSL bypass OK: {n1}x setter, {n2}x getter patchés")
        else:
            print(f"[PATCH] Patterns SSL non trouvés (déjà patchés ou version différente)")
    finally:
        k32.CloseHandle(h)


def main():
    if not os.path.exists(ORIG_EXE):
        print(f"[ERR] {ORIG_EXE} introuvable"); sys.exit(1)

    here = os.path.dirname(os.path.abspath(__file__))
    ca_src = os.path.join(here, ".mqel_certs", "ca.pem")
    if not os.path.exists(ca_src):
        print("[ERR] .mqel_certs/ca.pem absent — lance setup_windows.bat d'abord"); sys.exit(1)

    # 1. Déployer le CA
    deploy_ca(ca_src)

    # 2. /auth — fixed user_id so the SAME account is reused across launches
    # (otherwise /auth mints a random identity each time and you redo onboarding).
    print("[*] Authentification...")
    try:
        auth = call("/auth", {"user_id": os.environ.get("MQ_USER_ID", "player1")})
    except Exception as e:
        print(f"[ERR] Serveur inaccessible ({e})\n      Lance d'abord start_server.bat"); sys.exit(1)
    user_id    = auth["user_id"]
    numeric_id = str(abs(hash(user_id)) % (10**17) + 76561100000000000)
    print(f"[+] user_id: {user_id}")

    # 3. Lancer l'exe original avec les args du doc §2.3
    env = os.environ.copy()
    for v in ("http_proxy","https_proxy","HTTP_PROXY","HTTPS_PROXY","all_proxy"): env.pop(v,None)
    env["CURL_CA_BUNDLE"] = r"C:\usr\local\ssl\cert.pem"
    env["SSL_CERT_FILE"]  = r"C:\usr\local\ssl\cert.pem"
    env["OPENSSL_CONF"]   = ""

    cmd = [ORIG_EXE,
           "-server_url",      SERVER_URL,
           "-token",           "",
           "-steamticket",     user_id,
           "-steamid",         numeric_id,
           "-environmentName", "mqel-live",
           "-branchName",      "mqel",
           "--remote-debugging-port=9222",
           "--remote-allow-origins=*"]

    print(f"[+] Lancement de MightyQuest.exe...")
    proc = subprocess.Popen(cmd, cwd=GAME_DIR, env=env)
    print(f"[+] PID {proc.pid} — patch SSL dans 20s...")

    # 4. Patch mémoire SSL en thread daemon
    t = threading.Thread(target=_patch_ssl, args=(proc.pid,), daemon=True)
    t.start()

    try:
        proc.wait()
    except KeyboardInterrupt:
        print("\n[*] Fermeture.")


if __name__ == "__main__":
    main()
