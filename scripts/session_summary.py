import json
import os
import sys
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"

def parse_sessions(log_file):
    if not os.path.exists(log_file):
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    sessions = defaultdict(lambda: {
        "src_ip": "",
        "start": "",
        "end": "",
        "login_attempts": 0,
        "login_success": False,
        "commands": [],
        "files_downloaded": []
    })

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            sid = event.get("session", "unknown")
            eid = event.get("eventid", "")
            src = event.get("src_ip", "")
            ts = event.get("timestamp", "")

            sessions[sid]["src_ip"] = src

            if eid == "cowrie.session.connect":
                sessions[sid]["start"] = ts

            if eid == "cowrie.session.closed":
                sessions[sid]["end"] = ts

            if eid == "cowrie.login.failed":
                sessions[sid]["login_attempts"] += 1

            if eid == "cowrie.login.success":
                sessions[sid]["login_success"] = True
                sessions[sid]["login_attempts"] += 1

            if eid == "cowrie.command.input":
                sessions[sid]["commands"].append(event.get("input", ""))

            if eid == "cowrie.session.file_download":
                sessions[sid]["files_downloaded"].append(event.get("url", ""))

    return sessions

def report(sessions):
    print("=" * 60)
    print("   ATTACKER SESSION SUMMARY")
    print("=" * 60)
    print(f"\n[*] Total sessions: {len(sessions)}")

    for sid, s in sessions.items():
        print(f"\n--- Session: {sid} ---")
        print(f"    IP: {s['src_ip']}")
        print(f"    Start: {s['start']}")
        print(f"    End: {s['end']}")
        print(f"    Login attempts: {s['login_attempts']}")
        print(f"    Login success: {s['login_success']}")
        print(f"    Commands run: {len(s['commands'])}")
        for cmd in s["commands"]:
            print(f"      $ {cmd}")
        if s["files_downloaded"]:
            print(f"    Files downloaded:")
            for f in s["files_downloaded"]:
                print(f"      {f}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    sessions = parse_sessions(LOG_FILE)
    report(sessions)
