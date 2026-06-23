import sys, os, time, shutil, threading
sys.path.insert(0, "/home/user/mightyquest-drop/server")
import mqel_launcher as L
L.EXAMPLES, L.PKG_VERSIONS = L.load_catalog("/home/user/mightyquest-drop/re/catalog/network/generated")
L.PROXY_PORT = 443                       # game curl hits https://gs.themightyquest.com:443
cert, key, ca = L.ensure_certs()
os.makedirs("/usr/local/ssl", exist_ok=True)
shutil.copy(ca, "/usr/local/ssl/cert.pem")   # game's CURL_CA_BUNDLE trusts this
L.add_hosts()                                  # 127.0.0.1 gs.themightyquest.com
L.start_proxy(cert, key)
print("GAMESERVER_READY catalog=%d port=443" % len(L.EXAMPLES), flush=True)
while True: time.sleep(5)
