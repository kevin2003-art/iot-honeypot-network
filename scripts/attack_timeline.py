import json
import os
import sys
from datetime import datetime

LOG_FILE = "cowrie/logs/cowrie.json"

EVENT_LABELS = {
    "cowrie.session.connect": "CONNECTION",
    "cowrie.login.failed": "LOGIN FAIL",
    "cowrie.login.success": "LOGIN SUCCESS",
    "cowrie.command.input": "COMMAND",
    "cowrie.session.file_download": "FILE DOWNLOAD",
    "cowrie.session.closed": "DISCONNECT"
}

def parse_timeline(log_file):
    if not os.path.exists(log_file):
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    events = []
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                events.append(event)
            except json.JSONDecodeError:
                continue

    events.sort(key=lambda x: x.get("timestamp", ""))
    return events

def print_timeline(events):
    print("=" * 70)
    print("   ATTACK TIMELINE")
    print("=" * 70)

    for e in events:
        eid = e.get("eventid", "")
        label = EVENT_LABELS.get(eid, eid)
        ts = e.get("timestamp", "?")
        src = e.get("src_ip", "?")

        detail = ""
        if eid == "cowrie.login.failed":
            detail = f"user={e.get('username','?')} pass={e.get('password','?')}"
        elif eid == "cowrie.login.success":
            detail = f"user={e.get('username','?')} pass={e.get('password','?')}"
        elif eid == "cowrie.command.input":
            detail = f"$ {e.get('input','')}"
        elif eid == "cowrie.session.file_download":
            detail = f"url={e.get('url','?')}"

        print(f"[{ts}] {label:<16} | {src:<16} | {detail}")

    print("=" * 70)

if __name__ == "__main__":
    events = parse_timeline(LOG_FILE)
    print_timeline(events)
