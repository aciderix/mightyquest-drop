#!/bin/bash
export XDG_RUNTIME_DIR=/tmp/xdgrt WINEPREFIX=/home/user/wpC WINEARCH=win32 WINEDEBUG=-all DISPLAY=:107
for s in TERM KILL; do pkill -$s -f MightyQuest 2>/dev/null; pkill -$s -f winedevice 2>/dev/null; pkill -$s wineserver 2>/dev/null; pkill -$s Xvfb 2>/dev/null; pkill -$s -f 'http.server' 2>/dev/null; pkill -$s -f uiserver.py 2>/dev/null; done
sleep 5; rm -rf /tmp/.wine-* /tmp/.X*-lock /tmp/.X11-unix/* 2>/dev/null
# UI http server on :80 (gamedata -> GameData/Data)
nohup python3 /tmp/uiserver.py >/tmp/uihttp.log 2>&1 & disown
sleep 1; echo "UI http: $(curl -s -o /dev/null -w '%{http_code}' http://localhost/gamedata/UI/Html/en/Index.html 2>/dev/null)"
cp /home/user/dxvk-1.10.3/x32/d3d9.dll "$WINEPREFIX/drive_c/windows/system32/d3d9.dll"
grep -q gs.themightyquest.com /etc/hosts 2>/dev/null || echo "127.0.0.1 gs.themightyquest.com" >> /etc/hosts
pgrep -f gameserver.py >/dev/null || bash /tmp/start_gs.sh >/dev/null 2>&1
Xvfb :107 -screen 0 1280x1024x24 >/tmp/xvfb.log 2>&1 & sleep 3
cd /home/user/port/GameData/Bin; rm -f MQLog.txt; rm -f /tmp/binkpatch_ok.txt
rm -rf /home/user/port/GameData/Bin/CefCache/* 2>/dev/null
cp /home/user/binkstub/bink2w32.dll bink2w32.dll
export LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 DXVK_FRAME_RATE=30
export VK_ICD_FILENAMES=/usr/share/vulkan/icd.d/lvp_icd.json DXVK_LOG_LEVEL=none
export WINEDLLOVERRIDES="winhttp=n,b;bink2w32=n;d3d9=n"
# game's OpenSSL uses its compiled-in default CA path; honor SSL_CERT_FILE (Z:=/)
export CURL_CA_BUNDLE='Z:\usr\local\ssl\cert.pem' SSL_CERT_FILE='Z:\usr\local\ssl\cert.pem' SSL_CERT_DIR='Z:\usr\local\ssl\certs'
# also drop CA where Wine resolves the compiled default "/usr/local/ssl/cert.pem" (C: drive root)
mkdir -p "$WINEPREFIX/drive_c/usr/local/ssl/certs"
cp /usr/local/ssl/cert.pem "$WINEPREFIX/drive_c/usr/local/ssl/cert.pem" 2>/dev/null || true
nohup wine MightyQuest.exe --no-sandbox --disable-gpu --disable-software-rasterizer --disable-3d-apis --disable-web-security --ignore-certificate-errors --allow-file-access-from-files --remote-debugging-port=9222 --remote-allow-origins=* -server_url https://127.0.0.1 -environmentName mqel-live -branchName mqel -steamid 76561201696194782 -steamticket "" -token "" >/tmp/wine_lobby.log 2>&1 & disown
echo "launched lobby test pid $!; baseline crash=$(ls /home/user/port/CrashReport/*.breport 2>/dev/null|wc -l)"
