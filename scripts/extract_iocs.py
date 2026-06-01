import json
import os
import sys
import re

LOG_FILE = "cowrie/logs/cowrie.json"

def extract_iocs(log_file):
    if not os.path.exists(log_file):
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    ips = set()
    urls = set()
    hashes = set()
    commands = set()
    usernames = set()
    passwords = set()

    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    url_pattern = re.compile(r'https?://[^\s]+')

    with open(log_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue

            eid = event.get("eventid", "")

            src = event.get("src_ip", "")
            if src:
                ips.add(src)

            if eid in ["cowrie.login.failed", "cowrie.login.success"]:
                u = event.get("username", "")
                p = event.get("password", "")
                if u:
                    usernames.add(u)
                if p:
                    passwords.add(p)

            if eid == "cowrie.command.input":
                cmd = event.get("input", "")
                if cmd:
                    commands.add(cmd)
                found_urls = url_pattern.findall(cmd)
                for url in found_urls:
                    urls.add(url)

            if eid == "cowrie.session.file_download":
                url = event.get("url", "")
                sha256 = event.get("shasum", "")
                if url:
                    urls.add(url)
                if sha256:
                    hashes.add(sha256)

    return ips, urls, hashes, commands, usernames, passwords

def report(ips, urls, hashes, commands, usernames, passwords):
    print("=" * 60)
    print("   INDICATORS OF COMPROMISE (IoC) REPORT")
    print("=" * 60)

    print(f"\n[*] Attacker IPs ({len(ips)}):")
    for ip in sorted(ips):
        print(f"    {ip}")

    print(f"\n[*] Malicious URLs ({len(urls)}):")
    for url in sorted(urls):
        print(f"    {url}")

    print(f"\n[*] File Hashes ({len(hashes)}):")
    for h in sorted(hashes):
        print(f"    {h}")

    print(f"\n[*] Usernames tried ({len(usernames)}):")
    for u in sorted(usernames):
        print(f"    {u}")

    print(f"\n[*] Passwords tried ({len(passwords)}):")
    for p in sorted(passwords):
        print(f"    {p}")

    print(f"\n[*] Commands executed ({len(commands)}):")
    for cmd in sorted(commands):
        print(f"    $ {cmd}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    ips, urls, hashes, commands, usernames, passwords = extract_iocs(LOG_FILE)
    report(ips, urls, hashes, commands, usernames, passwords)
