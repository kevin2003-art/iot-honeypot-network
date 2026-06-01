import os
import json
import hashlib
import sys

DOWNLOADS_DIR = "cowrie/downloads"
LOG_FILE = "cowrie/logs/cowrie.json"

def hash_file(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_downloaded_files():
    files = []
    if not os.path.exists(DOWNLOADS_DIR):
        return files
    for fname in os.listdir(DOWNLOADS_DIR):
        fpath = os.path.join(DOWNLOADS_DIR, fname)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            sha256 = hash_file(fpath)
            files.append({
                "filename": fname,
                "size_bytes": size,
                "sha256": sha256
            })
    return files

def get_download_events():
    events = []
    if not os.path.exists(LOG_FILE):
        return events
    with open(LOG_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
                if event.get("eventid") in [
                    "cowrie.session.file_download",
                    "cowrie.session.file_upload"
                ]:
                    events.append(event)
            except json.JSONDecodeError:
                continue
    return events

def report():
    print("=" * 60)
    print("   PAYLOAD CAPTURE REPORT")
    print("=" * 60)

    files = get_downloaded_files()
    print(f"\n[*] Files captured in downloads folder: {len(files)}")
    for f in files:
        print(f"    File: {f['filename']}")
        print(f"    Size: {f['size_bytes']} bytes")
        print(f"    SHA256: {f['sha256']}")
        print()

    events = get_download_events()
    print(f"[*] Download/upload events in logs: {len(events)}")
    for e in events:
        print(f"    IP: {e.get('src_ip','?')} | File: {e.get('url', e.get('filename','?'))} | Time: {e.get('timestamp','?')}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    report()
