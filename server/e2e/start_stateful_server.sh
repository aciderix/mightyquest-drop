#!/bin/bash
pkill -f 'gameserver.py' 2>/dev/null || true
pkill -f 'stub_server.py' 2>/dev/null || true
pkill -f 'proxy.py' 2>/dev/null || true
sleep 1
rm -f /home/user/mightyquest-drop/server/state.json   # fresh account each session
cd /home/user/mightyquest-drop/server
nohup python3 -u stub_server.py --host 127.0.0.1 --port 443 --tls >/tmp/stateful.log 2>&1 &
disown
sleep 3
echo "=== log ==="; cat /tmp/stateful.log
