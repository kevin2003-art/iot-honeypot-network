#!/bin/bash

echo "[*] Verifying honeypot port bindings..."

check_port() {
    PORT=$1
    NAME=$2
    if ss -tlnp | grep -q ":$PORT "; then
        echo "[+] Port $PORT ($NAME) is OPEN and listening"
    else
        echo "[!] Port $PORT ($NAME) is NOT listening"
    fi
}

check_port 2222 "SSH Honeypot"
check_port 2223 "Telnet Honeypot"

echo ""
echo "[*] Active Docker containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
