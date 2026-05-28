#!/bin/bash

LOG="cowrie/logs/cowrie.json"

if [ ! -f "$LOG" ]; then
    echo "Log file not found. Is Cowrie running?"
    exit 1
fi

echo "Watching honeypot logs..."
echo "Press Ctrl+C to stop"
echo "----------------------------"

tail -f "$LOG" | while read line; do
    EVENT=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('eventid','unknown'))" 2>/dev/null)
    SRC=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('src_ip','?'))" 2>/dev/null)
    MSG=$(echo "$line" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('message',''))" 2>/dev/null)
    echo "[$(date '+%H:%M:%S')] EVENT=$EVENT | SRC=$SRC | $MSG"
done
