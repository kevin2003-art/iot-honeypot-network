#!/bin/bash

echo "[*] Stopping IoT Honeypot Network..."

docker-compose down

echo "[+] Honeypot stopped."
echo "[+] Logs are saved in cowrie/logs/"
