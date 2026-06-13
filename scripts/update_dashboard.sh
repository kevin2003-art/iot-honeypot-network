#!/bin/bash

echo "[*] Updating dashboard data..."

python3 dashboard/generate_dashboard_data.py
python3 dashboard/generate_chart_data.py

if [ -f "cowrie/logs/geo_enriched.json" ]; then
    cp cowrie/logs/geo_enriched.json dashboard/geo_enriched.json
    echo "[+] Geo data updated"
fi

echo "[+] Dashboard data updated successfully"
echo "[+] Run 'bash scripts/launch_dashboard.sh' to view"
