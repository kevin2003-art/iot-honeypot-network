import json
import os
import sys
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"

def load_events(log_file):
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
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return events

def profile_attackers(events):
    profiles = defaultdict(lambda: {
        "total_events": 0,
        "sessions": set(),
        "failed_logins": 0,
        "successful_logins": 0,
        "commands": [],
        "passwords_tried": set(),
        "usernames_tried": set(),
        "files_downloaded": []
    })

    for e in events:
        src = e.get("src_ip", "")
        if not src:
            continue

        eid = e.get("eventid", "")
        sid = e.get("session", "")

        profiles[src]["total_events"] += 1
        if sid:
            profiles[src]["sessions"].add(sid)

        if eid == "cowrie.login.failed":
            profiles[src]["failed_logins"] += 1
            profiles[src]["passwords_tried"].add(e.get("password", ""))
            profiles[src]["usernames_tried"].add(e.get("username", ""))

        if eid == "cowrie.login.success":
            profiles[src]["successful_logins"] += 1

        if eid == "cowrie.command.input":
            profiles[src]["commands"].append(e.get("input", ""))

        if eid == "cowrie.session.file_download":
            profiles[src]["files_downloaded"].append(e.get("url", ""))

    return profiles

def print_profiles(profiles):
    print("=" * 60)
    print("   ATTACKER PROFILES")
    print("=" * 60)

    sorted_profiles = sorted(
        profiles.items(),
        key=lambda x: x[1]["total_events"],
        reverse=True
    )

    for ip, p in sorted_profiles:
        print(f"\n IP: {ip}")
        print(f"    Total events      : {p['total_events']}")
        print(f"    Sessions          : {len(p['sessions'])}")
        print(f"    Failed logins     : {p['failed_logins']}")
        print(f"    Successful logins : {p['successful_logins']}")
        print(f"    Usernames tried   : {', '.join(sorted(p['usernames_tried']))}")
        print(f"    Passwords tried   : {', '.join(sorted(p['passwords_tried']))}")
        print(f"    Commands run      : {len(p['commands'])}")
        for cmd in p["commands"][:5]:
            print(f"      $ {cmd}")
        if p["files_downloaded"]:
            print(f"    Files downloaded  :")
            for f in p["files_downloaded"]:
                print(f"      {f}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    events = load_events(LOG_FILE)
    profiles = profile_attackers(events)
    print_profiles(profiles)
