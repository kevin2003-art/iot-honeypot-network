import json
import os
from collections import defaultdict
from datetime import datetime

LOG_FILE = "cowrie/logs/cowrie.json"
OUTPUT_FILE = "dashboard/dashboard_data.json"

def load_events(log_file):
    if not os.path.exists(log_file):
        return []
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

def generate(events):
    data = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_events": len(events),
        "total_sessions": 0,
        "total_login_attempts": 0,
        "total_login_success": 0,
        "total_commands": 0,
        "unique_ips": [],
        "top_passwords": [],
        "top_usernames": [],
        "top_commands": [],
        "events_over_time": [],
        "ip_event_counts": []
    }

    sessions = set()
    ips = defaultdict(int)
    passwords = defaultdict(int)
    usernames = defaultdict(int)
    commands = defaultdict(int)
    time_buckets = defaultdict(int)

    for e in events:
        eid = e.get("eventid", "")
        sid = e.get("session", "")
        src = e.get("src_ip", "")
        ts = e.get("timestamp", "")

        if sid:
            sessions.add(sid)
        if src:
            ips[src] += 1

        if ts:
            try:
                hour = ts[:13]
                time_buckets[hour] += 1
            except:
                pass

        if eid in ["cowrie.login.failed", "cowrie.login.success"]:
            data["total_login_attempts"] += 1
            p = e.get("password", "")
            u = e.get("username", "")
            if p:
                passwords[p] += 1
            if u:
                usernames[u] += 1

        if eid == "cowrie.login.success":
            data["total_login_success"] += 1

        if eid == "cowrie.command.input":
            data["total_commands"] += 1
            cmd = e.get("input", "")
            if cmd:
                commands[cmd] += 1

    data["total_sessions"] = len(sessions)
    data["unique_ips"] = sorted(list(ips.keys()))

    data["top_passwords"] = [
        {"password": p, "count": c}
        for p, c in sorted(passwords.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    data["top_usernames"] = [
        {"username": u, "count": c}
        for u, c in sorted(usernames.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    data["top_commands"] = [
        {"command": cmd, "count": c}
        for cmd, c in sorted(commands.items(), key=lambda x: x[1], reverse=True)[:10]
    ]

    data["events_over_time"] = [
        {"time": t, "count": c}
        for t, c in sorted(time_buckets.items())
    ]

    data["ip_event_counts"] = [
        {"ip": ip, "count": c}
        for ip, c in sorted(ips.items(), key=lambda x: x[1], reverse=True)
    ]

    os.makedirs("dashboard", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=4)

    print(f"[+] Dashboard data saved to {OUTPUT_FILE}")
    print(f"[*] Total events: {data['total_events']}")
    print(f"[*] Total sessions: {data['total_sessions']}")
    print(f"[*] Unique IPs: {len(data['unique_ips'])}")

import shutil

if __name__ == "__main__":
    events = load_events(LOG_FILE)
    generate(events)
    if os.path.exists("cowrie/logs/geo_enriched.json"):
        shutil.copy("cowrie/logs/geo_enriched.json", "dashboard/geo_enriched.json")
        print("[+] Geo data copied to dashboard folder")
