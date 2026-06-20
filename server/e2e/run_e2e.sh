#!/bin/bash
# run_e2e.sh — turnkey headless end-to-end test for MQEL under Wine.
#
# Brings up the instrumented local backend, redirects the game's hostnames to it,
# deploys the SSL/HTTP plumbing, and launches the unmodified game headless under
# Xvfb+Wine while capturing BOTH sides of every exchange.
#
#   client (game, libcurl/OpenSSL + winhttp)  <-->  monitor_server.py (catalog)
#        |                                              |
#        |  /etc/hosts: gs.themightyquest.com->127.0.0.1
#        |  winhttp shim: ignore cert errors            |  trace.jsonl (full I/O)
#        |  /usr/local/ssl/cert.pem = our CA            |  tcpdump capture.pcap
#
# Prereqs (Ubuntu 24.04): wine + i386, xvfb, tcpdump, openssl, git-lfs (for game data).
set -u
E2E=/home/user/e2e
GAME=/home/user/port/GameData/Bin
DUR=${1:-150}

echo "[*] 1/6 CA where the game's static libcurl/OpenSSL looks for it"
mkdir -p /usr/local/ssl && cp "$E2E/certs/ca.pem" /usr/local/ssl/cert.pem

echo "[*] 2/6 hosts redirect"
grep -q gs.themightyquest.com /etc/hosts || cat >> /etc/hosts <<EOF
127.0.0.1 gs.themightyquest.com
127.0.0.1 distribution.themightyquest.com
127.0.0.1 hqbloomberg.ubisoft.org
EOF

echo "[*] 3/6 deploy plumbing next to the exe"
cp "/home/user/mightyquest-drop/server/plumbing/winhttp.dll" "$GAME/winhttp.dll"
cp "$E2E/certs/ca.pem" "$GAME/ca.pem"

echo "[*] 4/6 start instrumented backend (ports 80/443/8080/13432)"
pkill -f monitor_server.py 2>/dev/null; sleep 1
( cd "$E2E" && python3 monitor_server.py >server_stdout.log 2>&1 & )
sleep 2

echo "[*] 5/6 start packet capture on loopback"
pkill -f 'tcpdump -i lo' 2>/dev/null
rm -f "$E2E/capture.pcap"
tcpdump -i lo -n -s0 -w "$E2E/capture.pcap" tcp >/dev/null 2>&1 &

echo "[*] 6/6 launch game headless under Xvfb for ${DUR}s"
rm -f /tmp/.X*-lock; rm -rf /tmp/.X11-unix/X*
cd "$GAME"
rm -f MQLog.txt HQ_Bloomberg.log NetworkLog.Txt CEFLog.Txt winhttp_proxy.log
export WINEPREFIX=/home/user/wineprefix WINEARCH=win32 WINEDEBUG=-all
export WINEDLLOVERRIDES="winhttp=n,b"
export CURL_CA_BUNDLE='Z:\usr\local\ssl\cert.pem'
timeout "$DUR" xvfb-run -a -s "-screen 0 1280x1024x24" \
    wine MightyQuest.exe -server_url https://gs.themightyquest.com \
    > "$E2E/wine_run.log" 2>&1
echo "[done] game exited ($?). Analyse with: python3 $E2E/validate_trace.py"
