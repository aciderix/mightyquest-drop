#!/bin/bash
# snapshot_game.sh — capture an ARET "save-state" of the live game under Wine.
#
# The packed client self-unpacks + resolves its protector IAT in memory under
# Wine, then hangs at a stable init point (OpenBF PACKAGE_PRELOAD). We SIGSTOP it
# and dump the unpacked image (0x400000..0x1e00000) into game.snap (ARETSNP1).
# ARET then seeds this into lifted functions to run the real client code headless
# (no GUI / Direct3D) — see README "ARET save-state path".
#
#   bash snapshot_game.sh                 # -> game.snap
#
# Needs: wine (32-bit), Xvfb, the game at $GAME, retoolkit dump tool.
set -u
GAME=${GAME:-/home/user/port/GameData/Bin}
DUMP=${DUMP:-/home/user/retoolkit/tools/snapshot/dump_snapshot.py}
OUT=${1:-/home/user/e2e/game.snap}
DISP=:77

pkill -9 -f MightyQuest 2>/dev/null; pkill -9 Xvfb 2>/dev/null; sleep 1
rm -f /tmp/.X*-lock; rm -rf /tmp/.X11-unix/* 2>/dev/null
Xvfb "$DISP" -screen 0 1280x1024x24 >/tmp/xvfb_snap.log 2>&1 &
sleep 2

cd "$GAME"; rm -f MQLog.txt
export WINEPREFIX=${WINEPREFIX:-/home/user/wineprefix} WINEARCH=win32 WINEDEBUG=-all DISPLAY=$DISP
export WINEDLLOVERRIDES="winhttp=n,b" CURL_CA_BUNDLE='Z:\usr\local\ssl\cert.pem'
wine MightyQuest.exe -server_url https://gs.themightyquest.com >/tmp/wine_snap.log 2>&1 &

# wait for the image to be unpacked + initialized (engine + bigfile preload)
for i in $(seq 1 60); do
    grep -qiE 'PACKAGE_PRELOAD|LoadGameSettings' MQLog.txt 2>/dev/null && break
    pgrep -x MightyQuest.exe >/dev/null || { echo "game exited early"; exit 1; }
    sleep 2
done
PID=$(pgrep -x MightyQuest.exe | head -1)
echo "[*] snapshotting unpacked image of PID $PID"
python3 "$DUMP" "$PID" "$OUT" 0x400000 0x1e00000
pkill -9 -f MightyQuest 2>/dev/null; pkill -9 Xvfb 2>/dev/null
echo "[done] $OUT"
