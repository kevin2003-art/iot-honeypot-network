# Security Policy

## Purpose
This project is a defensive security research tool. It is designed to capture and analyze attacker behavior in a fully isolated environment.

## Safe Usage
- Always run inside Docker — never run Cowrie directly on your host system
- Always configure UFW firewall before exposing honeypot ports
- Never expose port 22 (real SSH) alongside the honeypot ports
- Regularly rotate the Docker container to clear attacker SSH keys
- Store log data securely — it may contain real attacker credentials and malware

## Reporting Issues
If you find a security issue in this project open a GitHub issue marked SECURITY.

## Disclaimer
This tool is for educational and research purposes only. The authors are not responsible for any misuse.
