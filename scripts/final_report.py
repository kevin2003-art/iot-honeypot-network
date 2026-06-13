import json
import os
import sys
from datetime import datetime
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"
GEO_FILE = "cowrie/logs/geo_enriched.json"
OUTPUT_FILE = "docs/final_report.md"

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

def load_geo(geo_file):
    if not os.path.exists(geo_file):
        return {}
    with open(geo_file, "r") as f:
        return json.load(f)

def generate(events, geo_data):
    now = datetime.utcnow().isoformat() + "Z"

    ips = set()
    sessions = set()
    passwords = defaultdict(int)
    usernames = defaultdict(int)
    commands = defaultdict(int)
    login_success = 0
    login_fail = 0
    file_downloads = 0

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
        if eid == "cowrie.session.file_download":
            file_downloads += 1

    top_passwords = sorted(passwords.items(), key=lambda x: x[1], reverse=True)[:10]
    top_usernames = sorted(usernames.items(), key=lambda x: x[1], reverse=True)[:10]
    top_commands = sorted(commands.items(), key=lambda x: x[1], reverse=True)[:10]

    lines = []
    lines.append("# Final Honeypot Analysis Report")
    lines.append(f"\nGenerated: {now}")
    lines.append("\n---\n")

    lines.append("## Executive Summary")
    lines.append(f"\nThe IoT Honeypot Network successfully captured and analyzed attacker behavior targeting a simulated healthcare medical device. The honeypot ran as a Patient Vitals Monitor (PVM-2000X) on ports 2222 (SSH) and 2223 (Telnet) inside an isolated Docker environment.\n")

    lines.append("## Key Statistics")
    lines.append(f"\n| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total events captured | {len(events)} |")
    lines.append(f"| Unique attacker IPs | {len(ips)} |")
    lines.append(f"| Total sessions | {len(sessions)} |")
    lines.append(f"| Successful logins | {login_success} |")
    lines.append(f"| Failed login attempts | {login_fail} |")
    lines.append(f"| Commands executed | {sum(commands.values())} |")
    lines.append(f"| Files downloaded | {file_downloads} |")

    lines.append("\n## Top 10 Passwords Tried")
    lines.append("\n| Password | Count |")
    lines.append("|---|---|")
    for p, c in top_passwords:
        lines.append(f"| {p} | {c} |")

    lines.append("\n## Top 10 Usernames Tried")
    lines.append("\n| Username | Count |")
    lines.append("|---|---|")
    for u, c in top_usernames:
        lines.append(f"| {u} | {c} |")

    lines.append("\n## Top 10 Commands Executed")
    lines.append("\n| Command | Count |")
    lines.append("|---|---|")
    for cmd, c in top_commands:
        lines.append(f"| {cmd} | {c} |")

    lines.append("\n## Attacker IP Analysis")
    lines.append("\n| IP Address | Country | City | ISP |")
    lines.append("|---|---|---|---|")
    for ip in sorted(ips):
        geo = geo_data.get(ip, {})
        country = geo.get("country", "Unknown")
        city = geo.get("city", "Unknown")
        isp = geo.get("isp", "Unknown")
        lines.append(f"| {ip} | {country} | {city} | {isp} |")

    lines.append("\n## Security Recommendations")
    lines.append("\n1. Block all identified attacker IPs at the network perimeter firewall")
    lines.append("2. Never use default credentials on any IoT device")
    lines.append("3. Disable SSH and Telnet on medical IoT devices where not required")
    lines.append("4. Implement network segmentation to isolate medical devices")
    lines.append("5. Deploy honeypots as early warning systems across the hospital network")
    lines.append("6. Monitor for lateral movement commands like cat /etc/passwd and id")
    lines.append("7. Review all downloaded payloads for malware signatures using VirusTotal")

    lines.append("\n## Conclusion")
    lines.append("\nThe honeypot successfully deceived attackers into believing they had compromised a real hospital medical device. All attacker activity was captured, analyzed and visualized without any risk to real systems. This intelligence can now be used to harden the actual hospital network against these attack techniques.\n")

    os.makedirs("docs", exist_ok=True)
    report = "\n".join(lines)
    with open(OUTPUT_FILE, "w") as f:
        f.write(report)

    print(f"[+] Final report saved to {OUTPUT_FILE}")
    print(report)

if __name__ == "__main__":
    events = load_events(LOG_FILE)
    geo_data = load_geo(GEO_FILE)
    generate(events, geo_data)
