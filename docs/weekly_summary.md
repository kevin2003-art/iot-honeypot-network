# Weekly Honeypot Summary Report

Generated: 2026-06-13T18:23:29.189466Z

## Overview
- Total events captured: 132
- Unique attacker IPs: 1
- Total sessions: 11
- Successful logins: 8
- Failed login attempts: 8
- Commands executed: 7

## Top 5 Passwords Used by Attackers
- `` — 8 times
- `admin` — 8 times

## Top 5 Usernames Used by Attackers
- `root` — 16 times

## Top 5 Commands Executed
- `exit` — 8 times
- `cat /opt/meddevice/device_info.txt` — 5 times
- `ls /opt` — 5 times
- `cat /etc/hostname` — 3 times
- `ls /` — 1 times

## Attacker IPs
- 172.20.0.1

## Recommendations
- Block all attacker IPs at the network firewall
- Rotate default credentials on all IoT devices
- Monitor for commands indicating lateral movement
- Review downloaded payloads for malware signatures