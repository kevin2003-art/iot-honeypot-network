import json
import os
import sys
import time
import requests
from collections import defaultdict

LOG_FILE = "cowrie/logs/cowrie.json"
OUTPUT_FILE = "cowrie/logs/geo_enriched.json"

def get_unique_ips(log_file):
    ips = set()
    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                src = event.get("src_ip", "")
                if src:
                    ips.add(src)
            except json.JSONDecodeError:
                continue
    return list(ips)

def lookup_ip(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return {
                    "ip": ip,
                    "country": data.get("country", "Unknown"),
                    "country_code": data.get("countryCode", "??"),
                    "region": data.get("regionName", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown"),
                    "lat": data.get("lat", 0),
                    "lon": data.get("lon", 0)
                }
    except requests.RequestException:
        pass
    return {
        "ip": ip,
        "country": "Unknown",
        "country_code": "??",
        "region": "Unknown",
        "city": "Unknown",
        "isp": "Unknown",
        "lat": 0,
        "lon": 0
    }

def enrich(log_file):
    if not os.path.exists(log_file):
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    ips = get_unique_ips(log_file)
    print(f"[*] Found {len(ips)} unique attacker IPs")
    print(f"[*] Looking up geolocation for each IP...")

    geo_data = {}
    for ip in ips:
        print(f"    Checking {ip}...")
        geo_data[ip] = lookup_ip(ip)
        time.sleep(1)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(geo_data, f, indent=4)

    print(f"\n[+] Geo enriched data saved to {OUTPUT_FILE}")
    print("\n[*] Attacker Locations:")
    print(f"    {'IP':<18} {'Country':<20} {'City':<20} {'ISP'}")
    print(f"    {'-'*80}")
    for ip, info in geo_data.items():
        print(f"    {ip:<18} {info['country']:<20} {info['city']:<20} {info['isp']}")

if __name__ == "__main__":
    enrich(LOG_FILE)
