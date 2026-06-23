#!/bin/bash
# Generate the local CA + gs.themightyquest.com server cert used by monitor_server.py
set -e; cd "$(dirname "$0")"; mkdir -p certs; cd certs
cat > ext.cnf <<'X'
subjectAltName=DNS:gs.themightyquest.com,DNS:*.themightyquest.com,DNS:*.ubisoft.org,DNS:localhost,IP:127.0.0.1
basicConstraints=critical,CA:FALSE
keyUsage=critical,digitalSignature,keyEncipherment
extendedKeyUsage=serverAuth
X
openssl req -x509 -newkey rsa:2048 -nodes -keyout ca.key -out ca.pem -sha256 -days 3650 \
  -subj "/CN=MQEL-CA/O=MQEL" -addext "basicConstraints=critical,CA:TRUE" \
  -addext "keyUsage=critical,keyCertSign,cRLSign"
openssl req -newkey rsa:2048 -nodes -keyout server.key -out server.csr -subj "/CN=gs.themightyquest.com/O=MQEL"
openssl x509 -req -in server.csr -CA ca.pem -CAkey ca.key -CAcreateserial -out server.pem -days 3650 -sha256 -extfile ext.cnf
echo "certs/ generated"
