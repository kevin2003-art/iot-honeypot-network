import json
import os
import sys
from datetime import datetime
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"
REPORT_FILE = "cowrie/logs/threat_intel_report.txt"

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

def generate_report(events):
    lines = []
    now = datetime.utcnow().isoformat() + "Z"

    lines.append("=" * 60)
    lines.append("   THREAT INTELLIGENCE REPORT")
    lines.append(f"   Generated: {now}")
    lines.append("=" * 60)

    ip_events = defaultdict(list)
    for e in events:
        src = e.get("src_ip", "")
        if src:
            ip_events[src].append(e)

    lines.append(f"\n[1] ATTACK OVERVIEW")
    lines.append(f"    Total events logged : {len(events)}")
    lines.append(f"    Unique attacker IPs : {len(ip_events)}")

    total_fails = sum(1 for e in events if e.get("eventid") == "cowrie.login.failed")
    total_success = sum(1 for e in events if e.get("eventid") == "cowrie.login.success")
    total_cmds = sum(1 for e in events if e.get("eventid") == "cowrie.command.input")

    lines.append(f"    Failed logins       : {total_fails}")
    lines.append(f"    Successful logins   : {total_success}")
    lines.append(f"    Commands executed   : {total_cmds}")

    lines.append(f"\n[2] TOP ATTACKER IPs")
    sorted_ips = sorted(ip_events.items(), key=lambda x: len(x[1]), reverse=True)
    for ip, evts in sorted_ips[:10]:
        lines.append(f"    {ip} — {len(evts)} events")

    lines.append(f"\n[3] MOST USED PASSWORDS")
    passwords = defaultdict(int)
    for e in events:
        if e.get("eventid") in ["cowrie.login.failed", "cowrie.login.success"]:
            p = e.get("password", "")
            if p:
                passwords[p] += 1
    for p, count in sorted(passwords.items(), key=lambda x: x[1], reverse=True)[:10]:
        lines.append(f"    {p} — tried {count} times")

    lines.append(f"\n[4] MOST USED USERNAMES")
    usernames = defaultdict(int)
    for e in events:
        if e.get("eventid") in ["cowrie.login.failed", "cowrie.login.success"]:
            u = e.get("username", "")
            if u:
                usernames[u] += 1
    for u, count in sorted(usernames.items(), key=lambda x: x[1], reverse=True)[:10]:
        lines.append(f"    {u} — tried {count} times")

    lines.append(f"\n[5] COMMANDS EXECUTED BY ATTACKERS")
    commands = defaultdict(int)
    for e in events:
        if e.get("eventid") == "cowrie.command.input":
            cmd = e.get("input", "")
            if cmd:
                commands[cmd] += 1
    for cmd, count in sorted(commands.items(), key=lambda x: x[1], reverse=True)[:10]:
        lines.append(f"    $ {cmd} — {count} times")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

if __name__ == "__main__":
    events = load_events(LOG_FILE)
    report = generate_report(events)
    print(report)
    with open(REPORT_FILE, "w") as f:
        f.write(report)
    print(f"\n[+] Report saved to {REPORT_FILE}")
