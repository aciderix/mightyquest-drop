#!/bin/bash
# launch_controllable.sh — run the game under Wine + Xvfb with the CEF UI exposed
# over the Chrome DevTools Protocol (remote debugging), so it can be driven and
# inspected programmatically. The UI is HTML/JS in CEF 3.1453 (Chromium 28); the
# DevTools endpoint comes up at http://127.0.0.1:$PORT/json.
#
#   bash launch_controllable.sh            # launch + wait for CDP
#
# Needs: wine (32-bit), Xvfb, the game at $GAME.
set -u
GAME=${GAME:-/home/user/port/GameData/Bin}
EXE=${EXE:-MightyQuest.exe}
PORT=${PORT:-9222}
DISP=${DISP:-:77}
SERVER_URL=${SERVER_URL:-https://gs.themightyquest.com}

pkill -9 -f MightyQuest 2>/dev/null; pkill -9 Xvfb 2>/dev/null; sleep 1
rm -f /tmp/.X*-lock; rm -rf /tmp/.X11-unix/* 2>/dev/null
Xvfb "$DISP" -screen 0 1280x1024x24 >/tmp/xvfb_ctl.log 2>&1 &
sleep 2

cd "$GAME"; rm -f MQLog.txt
export WINEPREFIX=${WINEPREFIX:-/home/user/wineprefix} WINEARCH=win32 WINEDEBUG=-all DISPLAY=$DISP
export WINEDLLOVERRIDES="winhttp=n,b" CURL_CA_BUNDLE='Z:\usr\local\ssl\cert.pem'
echo "[*] launching $EXE --remote-debugging-port=$PORT (display $DISP, server $SERVER_URL)"
wine "$EXE" --remote-debugging-port=$PORT -server_url "$SERVER_URL" >/tmp/wine_ctl.log 2>&1 &
WPID=$!
echo "[*] wine pid $WPID; waiting for CEF DevTools on 127.0.0.1:$PORT ..."

for i in $(seq 1 90); do
    if curl -s --max-time 2 "http://127.0.0.1:$PORT/json/version" >/tmp/cdp_version.json 2>/dev/null \
       && [ -s /tmp/cdp_version.json ]; then
        echo "[+] CDP UP after ${i}x2s"
        echo "---- /json/version ----"; cat /tmp/cdp_version.json; echo
        echo "---- /json (pages) ----"; curl -s "http://127.0.0.1:$PORT/json"
        exit 0
    fi
    pgrep -x MightyQuest.exe >/dev/null || pgrep -f mightyquest-ui >/dev/null || {
        echo "[!] game process gone; tail of MQLog + wine log:"; tail -15 MQLog.txt 2>/dev/null
        tail -15 /tmp/wine_ctl.log; exit 1; }
    sleep 2
done
echo "[!] CDP did not come up in 180s. MQLog tail:"; tail -20 MQLog.txt 2>/dev/null
echo "wine log tail:"; tail -20 /tmp/wine_ctl.log
echo "listening ports:"; (ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | grep -E "$PORT|LISTEN" | head
exit 2
