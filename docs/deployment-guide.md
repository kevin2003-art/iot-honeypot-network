# Deployment Guide

## Prerequisites
- Kali Linux (or any Debian-based Linux)
- Docker and Docker Compose installed
- Git installed
- Python 3.11+

## Step 1 — Clone the repository

    git clone git@github.com:kevin2003-art/iot-honeypot-network.git
    cd iot-honeypot-network

## Step 2 — Configure firewall

    bash scripts/setup_firewall.sh

This opens only ports 2222 (SSH) and 2223 (Telnet) for the honeypot while keeping the rest of the system locked down.

## Step 3 — Build and start the honeypot

    bash scripts/start_honeypot.sh

## Step 4 — Verify it is running

    bash scripts/verify_ports.sh
    docker ps

## Step 5 — Generate the fake medical device filesystem (first time only)

    bash scripts/build_fake_fs.sh

## Step 6 — Launch the dashboard

    bash scripts/launch_dashboard.sh

Open a browser at http://localhost:8080

## Step 7 — Monitor live attacks

    bash scripts/connection_alert.sh

## Step 8 — Run analysis after capturing data

    python3 scripts/parse_logs.py
    python3 scripts/threat_intel_report.py
    python3 scripts/attacker_profile.py
    python3 scripts/detect_bruteforce.py
    python3 scripts/extract_iocs.py
    python3 scripts/geolocate_ips.py
    python3 scripts/final_report.py

## Step 9 — Stop the honeypot

    bash scripts/stop_honeypot.sh

## Safety Notes

- The honeypot runs in an isolated Docker network (172.20.0.0/24)
- The container cannot access the host filesystem outside mounted volumes
- Never run the honeypot with elevated privileges beyond what Docker requires
- Regularly back up cowrie/logs/ for evidence retention
- This deployment is for research, education and internal threat intelligence purposes only
