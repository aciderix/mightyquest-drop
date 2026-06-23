#!/usr/bin/env python3
"""Generate the local PKI (CA + server cert) using Git's openssl on Windows,
or the system openssl on Linux. Called by setup_windows.bat."""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CDIR = os.path.join(HERE, ".mqel_certs")
os.makedirs(CDIR, exist_ok=True)

# find openssl: system PATH first, then Git for Windows
openssl = "openssl"
for candidate in [r"C:\Program Files\Git\usr\bin\openssl.exe",
                  r"C:\Program Files (x86)\Git\usr\bin\openssl.exe"]:
    if os.path.exists(candidate):
        openssl = candidate
        break

def run(*args):
    subprocess.run([openssl] + list(args), check=True, capture_output=True)

ca_key = os.path.join(CDIR, "ca.key")
ca_pem = os.path.join(CDIR, "ca.pem")
sk     = os.path.join(CDIR, "server.key")
sc     = os.path.join(CDIR, "server.pem")
csr    = os.path.join(CDIR, "server.csr")
ext    = os.path.join(CDIR, "ext.cnf")

if all(os.path.exists(x) for x in (ca_pem, sk, sc)):
    print("[=] certs already present"); sys.exit(0)

with open(ext, "w") as f:
    f.write("subjectAltName=DNS:gs.themightyquest.com,IP:127.0.0.1,DNS:localhost\n"
            "basicConstraints=critical,CA:FALSE\n"
            "keyUsage=critical,digitalSignature,keyEncipherment\n"
            "extendedKeyUsage=serverAuth\n")

run("req", "-x509", "-newkey", "rsa:2048", "-nodes", "-keyout", ca_key,
    "-out", ca_pem, "-sha256", "-days", "3650", "-subj", "/CN=MQEL-CA/O=MQEL",
    "-addext", "basicConstraints=critical,CA:TRUE",
    "-addext", "keyUsage=critical,keyCertSign,cRLSign")
run("req", "-newkey", "rsa:2048", "-nodes", "-keyout", sk, "-out", csr,
    "-subj", "/CN=gs.themightyquest.com/O=MQEL")
run("x509", "-req", "-in", csr, "-CA", ca_pem, "-CAkey", ca_key,
    "-CAcreateserial", "-out", sc, "-days", "3650", "-sha256", "-extfile", ext)
print("[+] PKI generated:", CDIR)
