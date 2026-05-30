#!/bin/bash

echo "[*] Starting IoT Honeypot Network..."

if ! docker info > /dev/null 2>&1; then
    echo "[!] Docker is not running. Start Docker first."
    exit 1
fi

docker-compose down > /dev/null 2>&1

docker-compose up -d

sleep 5

STATUS=$(docker ps --filter "name=cowrie-honeypot" --format "{{.Status}}")

if [[ "$STATUS" == Up* ]]; then
    echo "[+] Honeypot is running."
    echo "[+] SSH honeypot listening on port 2222"
    echo "[+] Telnet honeypot listening on port 2223"
    echo "[+] Logs are being written to cowrie/logs/"
else
    echo "[!] Honeypot failed to start. Check logs:"
    docker logs cowrie-honeypot
    exit 1
fi
