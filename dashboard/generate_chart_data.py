import json
import os
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"
OUTPUT_FILE = "dashboard/chart_data.json"

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

def generate_chart_data(events):
    hourly = defaultdict(int)
    event_types = defaultdict(int)
    login_results = {"success": 0, "failed": 0}

    for e in events:
        eid = e.get("eventid", "unknown")
        ts = e.get("timestamp", "")

        event_types[eid] += 1

        if ts:
            try:
                hour = ts[11:13] + ":00"
                hourly[hour] += 1
            except:
                pass

        if eid == "cowrie.login.success":
            login_results["success"] += 1
        if eid == "cowrie.login.failed":
            login_results["failed"] += 1

    chart_data = {
        "hourly_attacks": [
            {"hour": h, "count": c}
            for h, c in sorted(hourly.items())
        ],
        "event_type_breakdown": [
            {"type": t.replace("cowrie.", ""), "count": c}
            for t, c in sorted(event_types.items(), key=lambda x: x[1], reverse=True)
        ],
        "login_results": login_results
    }

    os.makedirs("dashboard", exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(chart_data, f, indent=4)

    print(f"[+] Chart data saved to {OUTPUT_FILE}")
    print(f"[*] Hourly buckets: {len(chart_data['hourly_attacks'])}")
    print(f"[*] Event types: {len(chart_data['event_type_breakdown'])}")
    print(f"[*] Login success: {login_results['success']} | Failed: {login_results['failed']}")

if __name__ == "__main__":
    events = load_events(LOG_FILE)
    generate_chart_data(events)
