#!/bin/bash

LOG="cowrie/logs/cowrie.json"

echo "[*] Monitoring honeypot for new connections..."
echo "[*] Press Ctrl+C to stop"
echo "------------------------------------------------"

if [ ! -f "$LOG" ]; then
    echo "[!] Log file not found. Is the honeypot running?"
    exit 1
fi

tail -f "$LOG" | while read line; do
    EVENT=$(echo "$line" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('eventid',''))
except:
    print('')
" 2>/dev/null)

    SRC=$(echo "$line" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('src_ip','unknown'))
except:
    print('unknown')
" 2>/dev/null)

    TIME=$(date '+%Y-%m-%d %H:%M:%S')

    if [[ "$EVENT" == "cowrie.session.connect" ]]; then
        echo "[$TIME] ALERT: New connection from $SRC"
    fi

    if [[ "$EVENT" == "cowrie.login.success" ]]; then
        echo "[$TIME] WARNING: Successful login from $SRC"
    fi

    if [[ "$EVENT" == "cowrie.login.failed" ]]; then
        echo "[$TIME] INFO: Failed login attempt from $SRC"
    fi

    if [[ "$EVENT" == "cowrie.command.input" ]]; then
        CMD=$(echo "$line" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    print(d.get('input',''))
except:
    print('')
" 2>/dev/null)
        echo "[$TIME] COMMAND from $SRC: $CMD"
    fi
done
