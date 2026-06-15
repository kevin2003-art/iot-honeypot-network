# IoT Honeypot Network — Healthcare Medical Device Deception

A fully functional Cowrie-based SSH/Telnet honeypot that simulates a hospital Patient Vitals Monitor (PVM-2000X) to capture, analyze and visualize attacker behavior targeting medical IoT devices.

## Team

- Kevin — Infrastructure, Docker, Git workflow, dashboard server, deployment
- Shalwin — Honeypot configuration, log analysis scripts, dashboard visualizations, reporting

## What This Project Does

1. Deploys a Cowrie honeypot in an isolated Docker network disguised as MedDevice-IoT-001, a medical Patient Vitals Monitor
2. Captures every login attempt, command and file download from attackers in JSON and text logs
3. Analyzes logs with 15+ Python and Bash scripts for brute force detection, IoC extraction, session profiling and geolocation
4. Visualizes everything on a military-style real-time dashboard with 7 tabs including a world map of attack origins
5. Generates a comprehensive final report with security recommendations

## Quick Start

    git clone git@github.com:kevin2003-art/iot-honeypot-network.git
    cd iot-honeypot-network
    bash scripts/setup_firewall.sh
    bash scripts/start_honeypot.sh
    bash scripts/launch_dashboard.sh

Open http://localhost:8080 to view the dashboard.

See [docs/deployment-guide.md](docs/deployment-guide.md) for full instructions.

## Project Structure

    iot-honeypot-network/
    ├── cowrie/              # Honeypot Dockerfile, config, fake filesystem
    ├── dashboard/           # HTML dashboard and data generators
    ├── docs/                # Architecture, deployment guide, reports
    ├── scripts/             # Analysis, monitoring and automation scripts
    └── docker-compose.yml   # Container orchestration

## Documentation

- [Architecture Diagram](docs/architecture-diagram.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Network Exposure Strategy](docs/network-exposure.md)
- [Week 2 Analysis](docs/week2-analysis.md)
- [Weekly Summary](docs/weekly_summary.md)
- [Final Report](docs/final_report.md)

## Tech Stack

- Cowrie 3.0.0 (SSH/Telnet honeypot)
- Docker + Docker Compose
- Python 3.11 (analysis and dashboard data)
- HTML/CSS/JavaScript (dashboard)
- ip-api.com (geolocation)

## Branch Strategy

- main: stable, protected, no direct commits
- feat/*: new features developed via pull request and squash merge
- fix/*: bug fixes developed via pull request and squash merge

## Disclaimer

This honeypot is for research, education and internal threat intelligence only. It runs in an isolated Docker network and must never be exposed without proper firewall controls.
