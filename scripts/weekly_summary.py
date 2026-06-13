import json
import os
from datetime import datetime
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"
OUTPUT_FILE = "docs/weekly_summary.md"

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

def generate_summary(events):
    now = datetime.utcnow().isoformat() + "Z"
    total = len(events)
    ips = set()
    sessions = set()
    passwords = defaultdict(int)
    usernames = defaultdict(int)
    commands = defaultdict(int)
    login_success = 0
    login_fail = 0

    for e in events:
        src = e.get("src_ip", "")
        sid = e.get("session", "")
        eid = e.get("eventid", "")

        if src:
            ips.add(src)
        if sid:
            sessions.add(sid)

        if eid == "cowrie.login.success":
            login_success += 1
            passwords[e.get("password", "")] += 1
            usernames[e.get("username", "")] += 1

        if eid == "cowrie.login.failed":
            login_fail += 1
            passwords[e.get("password", "")] += 1
            usernames[e.get("username", "")] += 1

        if eid == "cowrie.command.input":
            commands[e.get("input", "")] += 1

    top_passwords = sorted(passwords.items(), key=lambda x: x[1], reverse=True)[:5]
    top_usernames = sorted(usernames.items(), key=lambda x: x[1], reverse=True)[:5]
    top_commands = sorted(commands.items(), key=lambda x: x[1], reverse=True)[:5]

    lines = []
    lines.append("# Weekly Honeypot Summary Report")
    lines.append(f"\nGenerated: {now}\n")
    lines.append("## Overview")
    lines.append(f"- Total events captured: {total}")
    lines.append(f"- Unique attacker IPs: {len(ips)}")
    lines.append(f"- Total sessions: {len(sessions)}")
    lines.append(f"- Successful logins: {login_success}")
    lines.append(f"- Failed login attempts: {login_fail}")
    lines.append(f"- Commands executed: {len(commands)}")

    lines.append("\n## Top 5 Passwords Used by Attackers")
    for p, c in top_passwords:
        lines.append(f"- `{p}` — {c} times")

    lines.append("\n## Top 5 Usernames Used by Attackers")
    for u, c in top_usernames:
        lines.append(f"- `{u}` — {c} times")

    lines.append("\n## Top 5 Commands Executed")
    for cmd, c in top_commands:
        lines.append(f"- `{cmd}` — {c} times")

    lines.append("\n## Attacker IPs")
    for ip in sorted(ips):
        lines.append(f"- {ip}")

    lines.append("\n## Recommendations")
    lines.append("- Block all attacker IPs at the network firewall")
    lines.append("- Rotate default credentials on all IoT devices")
    lines.append("- Monitor for commands indicating lateral movement")
    lines.append("- Review downloaded payloads for malware signatures")

    os.makedirs("docs", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        f.write("\n".join(lines))

    print(f"[+] Weekly summary saved to {OUTPUT_FILE}")
    for line in lines:
        print(line)

if __name__ == "__main__":
    events = load_events(LOG_FILE)
    generate_summary(events)
