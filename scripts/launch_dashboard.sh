#!/bin/bash

echo "[*] Launching IoT Honeypot Dashboard..."

if ! docker ps | grep -q "cowrie-honeypot"; then
    echo "[*] Starting honeypot first..."
    bash scripts/start_honeypot.sh
    sleep 5
fi

echo "[*] Generating dashboard data..."
python3 dashboard/generate_dashboard_data.py
python3 dashboard/generate_chart_data.py

echo "[+] Dashboard available at http://localhost:8080/index.html"
echo "[+] Press Ctrl+C to stop"
python3 dashboard/serve_dashboard.py
