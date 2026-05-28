# Docker Build and Test Notes

## Build
- Image: iot-honeypot-network_cowrie
- Base: python:3.11-slim
- Cowrie cloned from official repo

## Test
- Connected via SSH on port 2222
- Used credentials: root / admin
- Cowrie accepted connection and presented fake shell
- Commands logged: ls, whoami, cat /etc/passwd, id, uname -a

## Logs
- cowrie.log: human readable
- cowrie.json: machine readable for parsing

## Status
Honeypot running and capturing attacker interactions successfully.
