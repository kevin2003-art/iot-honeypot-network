import json
import os
import sys
from datetime import datetime

LOG_FILE = "cowrie/logs/cowrie.json"

def parse_logs(log_file):
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
    return events

def summarize(events):
    print("=" * 60)
    print("   HONEYPOT ATTACK SUMMARY")
    print("=" * 60)

    total = len(events)
    print(f"\n[*] Total events captured: {total}")

    ips = {}
    commands = []
    logins = []
    failed = []

    for e in events:
        src = e.get("src_ip", None)
        event_id = e.get("eventid", "")

        if src:
            ips[src] = ips.get(src, 0) + 1

        if event_id == "cowrie.command.input":
            commands.append(e.get("input", ""))

        if event_id == "cowrie.login.success":
            logins.append({
                "ip": src,
                "username": e.get("username", ""),
                "password": e.get("password", ""),
                "time": e.get("timestamp", "")
            })

        if event_id == "cowrie.login.failed":
            failed.append({
                "ip": src,
                "username": e.get("username", ""),
                "password": e.get("password", "")
            })

    print(f"\n[*] Unique attacker IPs: {len(ips)}")
    for ip, count in sorted(ips.items(), key=lambda x: x[1], reverse=True):
        print(f"    {ip} — {count} events")

    print(f"\n[*] Successful logins: {len(logins)}")
    for l in logins:
        print(f"    IP: {l['ip']} | User: {l['username']} | Pass: {l['password']} | Time: {l['time']}")

    print(f"\n[*] Failed login attempts: {len(failed)}")
    for f in failed[:10]:
        print(f"    IP: {f['ip']} | User: {f['username']} | Pass: {f['password']}")
    if len(failed) > 10:
        print(f"    ... and {len(failed) - 10} more")

    print(f"\n[*] Commands executed by attackers: {len(commands)}")
    for cmd in commands:
        print(f"    $ {cmd}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    events = parse_logs(LOG_FILE)
    summarize(events)
