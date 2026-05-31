#!/bin/bash

echo "[*] Setting up firewall rules for honeypot..."

sudo apt install -y ufw > /dev/null 2>&1

sudo ufw --force reset > /dev/null 2>&1

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow 22/tcp
sudo ufw allow 2222/tcp
sudo ufw allow 2223/tcp

sudo ufw --force enable

echo "[+] Firewall rules applied:"
sudo ufw status verbose
