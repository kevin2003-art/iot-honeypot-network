# Docker Build and Test Notes

## Build
- Image: iot-honeypot-network-cowrie
- Base: python:3.11-slim
- Cowrie cloned from official repo and installed via pip install .

## Device Simulation
- Hostname: MedDevice-IoT-001
- SSH Banner: SSH-2.0-OpenSSH_7.4p1 MedOS
- Fake filesystem mounted at honeyfs/
- Device: Patient Vitals Monitor PVM-2000X
- Firmware: v2.4.1-stable

## Test Results
- Connected via SSH on port 2222
- Credentials used: root / admin
- Cowrie accepted and presented fake medical device shell
- Commands tested: ls, cat /etc/hostname, cat /opt/meddevice/device_info.txt
- All commands captured in cowrie.log and cowrie.json

## Ports
- 2222: SSH honeypot
- 2223: Telnet honeypot

## Status
Honeypot fully running and simulating a medical IoT device successfully.
