import json
import os
import sys
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"
THRESHOLD = 5

def detect_bruteforce(log_file):
    if not os.path.exists(log_file):
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    failed_attempts = defaultdict(list)

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            if event.get("eventid") == "cowrie.login.failed":
                src_ip = event.get("src_ip", "unknown")
                username = event.get("username", "")
                password = event.get("password", "")
                timestamp = event.get("timestamp", "")
                failed_attempts[src_ip].append({
                    "username": username,
                    "password": password,
                    "timestamp": timestamp
                })

    print("=" * 60)
    print("   BRUTE FORCE DETECTION REPORT")
    print("=" * 60)

    found = False
    for ip, attempts in failed_attempts.items():
        if len(attempts) >= THRESHOLD:
            found = True
            print(f"\n[!] BRUTE FORCE DETECTED: {ip}")
            print(f"    Total failed attempts: {len(attempts)}")
            print(f"    Sample credentials tried:")
            for a in attempts[:5]:
                print(f"      User: {a['username']} | Pass: {a['password']} | Time: {a['timestamp']}")
            if len(attempts) > 5:
                print(f"      ... and {len(attempts) - 5} more attempts")

    if not found:
        print(f"\n[*] No brute force detected (threshold: {THRESHOLD} failed attempts per IP)")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    detect_bruteforce(LOG_FILE)
