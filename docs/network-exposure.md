# Network Exposure Strategy

## Overview
The honeypot is exposed in a controlled and sandboxed manner. Only the honeypot ports are opened to the network. The real system remains protected.

## Exposed Ports
| Port | Protocol | Purpose |
|------|----------|---------|
| 2222 | TCP | SSH Honeypot |
| 2223 | TCP | Telnet Honeypot |

## Firewall Rules
- Default: deny all incoming
- Allow: port 22 (admin SSH access to host)
- Allow: port 2222 (SSH honeypot)
- Allow: port 2223 (Telnet honeypot)

## Safety Measures
- Cowrie runs inside Docker container
- Docker network is isolated subnet 172.20.0.0/24
- Attacker cannot reach host system from inside Cowrie
- All attacker activity is logged to cowrie/logs/

## Testing
- Use scripts/start_honeypot.sh to start
- Use scripts/verify_ports.sh to confirm ports are open
- Use scripts/watch_logs.sh to monitor live attacks
- Use scripts/parse_logs.py to analyze captured data
