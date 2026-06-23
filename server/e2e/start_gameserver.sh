#!/bin/bash
pkill -f 'proxy.py' 2>/dev/null || true
pkill -f 'gameserver.py' 2>/dev/null || true
sleep 1
cd /tmp
nohup python3 -u /tmp/gameserver.py >/tmp/gameserver.log 2>&1 &
disown
sleep 3
echo "=== log ==="; cat /tmp/gameserver.log
echo "=== 443 ==="; (ss -ltn 2>/dev/null || netstat -ltn 2>/dev/null) | grep ':443' || echo none
