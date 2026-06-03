# Week 2 Analysis Report

## Overview
Week 2 focused on exposing the Cowrie honeypot in a controlled environment and capturing attacker behavior for analysis.

## What Was Deployed
- Cowrie SSH and Telnet honeypot running on ports 2222 and 2223
- Docker isolated network subnet 172.20.0.0/24
- UFW firewall allowing only honeypot ports to external traffic
- Download and TTY session capture volumes mounted

## Scripts Developed
| Script | Purpose |
|---|---|
| start_honeypot.sh | Start and verify honeypot container |
| stop_honeypot.sh | Cleanly shut down honeypot |
| verify_ports.sh | Confirm SSH and Telnet ports are listening |
| connection_alert.sh | Real-time alert for new attacker connections |
| detect_bruteforce.py | Detect IPs exceeding failed login threshold |
| parse_logs.py | Parse Cowrie JSON logs into readable summary |
| session_summary.py | Group all attacker activity by session ID |
| extract_iocs.py | Extract indicators of compromise from logs |
| aggregate_logs.py | Produce structured JSON summary of all events |
| attack_timeline.py | Display chronological view of attacker activity |
| threat_intel_report.py | Generate full threat intelligence report |
| attacker_profile.py | Build detailed profile per attacking IP |
| geolocate_ips.py | Enrich attacker IPs with geolocation data |
| export_enriched_logs.py | Merge geo data into cowrie events |
| country_stats.py | Count attacks grouped by country |

## Key Findings (Sample Data)
- Attackers immediately attempt brute force on SSH port 2222
- Most common usernames: root, admin, user
- Most common passwords: 123456, password, admin, admin123
- Attackers run reconnaissance commands after login: ls, cat /etc/passwd, id, uname -a
- All activity is fully captured in cowrie.log and cowrie.json

## Next Steps - Week 3
- Build a visual dashboard to display attack data
- Add world map showing attack origins by country
- Visualize most targeted commands and credentials
