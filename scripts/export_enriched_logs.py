import json
import os
import sys

LOG_FILE = "cowrie/logs/cowrie.json"
GEO_FILE = "cowrie/logs/geo_enriched.json"
OUTPUT_FILE = "cowrie/logs/enriched_events.json"

def load_geo(geo_file):
    if not os.path.exists(geo_file):
        print(f"[!] Geo file not found. Run geolocate_ips.py first.")
        sys.exit(1)
    with open(geo_file, "r") as f:
        return json.load(f)

def enrich_events(log_file, geo_data):
    enriched = []
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                src = event.get("src_ip", "")
                if src and src in geo_data:
                    event["geo"] = geo_data[src]
                enriched.append(event)
            except json.JSONDecodeError:
                continue
    return enriched

def export(log_file, geo_file, output_file):
    geo_data = load_geo(geo_file)
    events = enrich_events(log_file, geo_data)

    with open(output_file, "w") as f:
        json.dump(events, f, indent=4)

    print(f"[+] Exported {len(events)} enriched events to {output_file}")

if __name__ == "__main__":
    export(LOG_FILE, GEO_FILE, OUTPUT_FILE)
