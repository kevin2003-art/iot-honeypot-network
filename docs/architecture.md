# System Architecture

## Overview

The IoT Honeypot Network is a multi-layer deception system designed to capture and analyze attacker behavior targeting healthcare IoT devices.

## Architecture Layers

### Layer 1 — Deception Layer
- Cowrie SSH and Telnet honeypot running in Docker
- Simulates a Patient Vitals Monitor (PVM-2000X)
- Custom hostname: MedDevice-IoT-001
- Fake filesystem with medical device files
- SSH banner mimicking MedOS 2.4.1

### Layer 2 — Isolation Layer
- Docker network: 172.20.0.0/24
- UFW firewall allowing only ports 2222 and 2223
- Container cannot reach host system
- All attacker activity sandboxed

### Layer 3 — Capture Layer
- cowrie.log: human readable event log
- cowrie.json: machine readable JSON events
- TTY recordings of every session
- Downloaded payload capture

### Layer 4 — Analysis Layer
- parse_logs.py: basic log parsing
- detect_bruteforce.py: brute force detection
- extract_iocs.py: indicator of compromise extraction
- session_summary.py: per session analysis
- attacker_profile.py: per IP profiling
- threat_intel_report.py: full threat report
- geolocate_ips.py: IP geolocation enrichment

### Layer 5 — Visualization Layer
- Military style HTML dashboard
- 7 tabbed views of attack data
- Auto refreshes every 30 seconds
- World map showing attack origins

## Data Flow

Attacker connects → Cowrie captures → JSON logs → Python scripts → Dashboard JSON → Browser dashboard

## Technology Stack

| Component | Technology |
|---|---|
| Honeypot | Cowrie 3.0.0 |
| Container | Docker + Docker Compose |
| Analysis | Python 3.11 |
| Dashboard | HTML + CSS + JavaScript |
| Geolocation | ip-api.com |
| Version Control | Git + GitHub |
