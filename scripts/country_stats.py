import json
import os
import sys
from collections import defaultdict

GEO_FILE = "cowrie/logs/geo_enriched.json"
LOG_FILE = "cowrie/logs/cowrie.json"

def get_ip_event_counts(log_file):
    counts = defaultdict(int)
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                src = event.get("src_ip", "")
                if src:
                    counts[src] += 1
            except json.JSONDecodeError:
                continue
    return counts

def country_stats(geo_file, log_file):
    if not os.path.exists(geo_file):
        print(f"[!] Geo file not found. Run geolocate_ips.py first.")
        sys.exit(1)

    with open(geo_file, "r") as f:
        geo_data = json.load(f)

    ip_counts = get_ip_event_counts(log_file)

    country_events = defaultdict(int)
    country_ips = defaultdict(set)

    for ip, info in geo_data.items():
        country = info.get("country", "Unknown")
        country_events[country] += ip_counts.get(ip, 0)
        country_ips[country].add(ip)

    print("=" * 60)
    print("   ATTACKS BY COUNTRY")
    print("=" * 60)
    print(f"\n{'Country':<25} {'Unique IPs':<15} {'Total Events'}")
    print(f"{'-'*55}")

    for country, events in sorted(country_events.items(), key=lambda x: x[1], reverse=True):
        ips = len(country_ips[country])
        print(f"{country:<25} {ips:<15} {events}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    country_stats(GEO_FILE, LOG_FILE)
