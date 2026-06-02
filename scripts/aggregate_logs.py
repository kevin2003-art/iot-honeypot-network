import json
import os
import sys
from datetime import datetime

LOG_FILE = "cowrie/logs/cowrie.json"
OUTPUT_FILE = "cowrie/logs/aggregated_report.json"

def aggregate(log_file):
    if not os.path.exists(log_file):
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_events": 0,
        "unique_ips": [],
        "total_sessions": 0,
        "total_login_attempts": 0,
        "total_login_success": 0,
        "total_commands": 0,
        "total_file_downloads": 0,
        "events_by_type": {}
    }

    ips = set()
    sessions = set()

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            report["total_events"] += 1

            eid = event.get("eventid", "unknown")
            src = event.get("src_ip", "")
            sid = event.get("session", "")

            if src:
                ips.add(src)
            if sid:
                sessions.add(sid)

            report["events_by_type"][eid] = report["events_by_type"].get(eid, 0) + 1

            if eid == "cowrie.login.failed":
                report["total_login_attempts"] += 1
            if eid == "cowrie.login.success":
                report["total_login_success"] += 1
                report["total_login_attempts"] += 1
            if eid == "cowrie.command.input":
                report["total_commands"] += 1
            if eid == "cowrie.session.file_download":
                report["total_file_downloads"] += 1

    report["unique_ips"] = sorted(list(ips))
    report["total_sessions"] = len(sessions)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(report, f, indent=4)

    print(f"[+] Aggregated report saved to {OUTPUT_FILE}")
    print(f"[*] Total events: {report['total_events']}")
    print(f"[*] Unique IPs: {len(report['unique_ips'])}")
    print(f"[*] Total sessions: {report['total_sessions']}")
    print(f"[*] Login attempts: {report['total_login_attempts']}")
    print(f"[*] Successful logins: {report['total_login_success']}")
    print(f"[*] Commands executed: {report['total_commands']}")
    print(f"[*] Files downloaded: {report['total_file_downloads']}")

if __name__ == "__main__":
    aggregate(LOG_FILE)
