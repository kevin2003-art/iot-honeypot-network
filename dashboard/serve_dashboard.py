import http.server
import socketserver
import os
import threading
import time
import json
import subprocess

PORT = 8080
DASHBOARD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))

def regenerate_data():
    while True:
        try:
            subprocess.run(["python3", "dashboard/generate_dashboard_data.py"], check=True)
            subprocess.run(["python3", "dashboard/generate_chart_data.py"], check=True)
            print("[*] Dashboard data refreshed")
        except Exception as e:
            print(f"[!] Data refresh error: {e}")
        time.sleep(30)

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

def start_server():
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + "/..")

    refresh_thread = threading.Thread(target=regenerate_data, daemon=True)
    refresh_thread.start()
    print(f"[+] Auto-refresh thread started (every 30 seconds)")

    subprocess.run(["python3", "dashboard/generate_dashboard_data.py"])
    subprocess.run(["python3", "dashboard/generate_chart_data.py"])

    with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
        print(f"[+] Dashboard server running at http://localhost:{PORT}")
        print(f"[+] Open your browser at http://localhost:{PORT}/index.html")
        print(f"[+] Press Ctrl+C to stop")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Dashboard server stopped")

if __name__ == "__main__":
    start_server()
