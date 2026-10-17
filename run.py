"""
CypherSwarm (OrgBrain) — One-Click Launcher
Starts the FastAPI server and opens the interactive dashboard in your browser.
"""

import os
import sys
import webbrowser
import threading
import time

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(CURRENT_DIR, "backend")

if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

import uvicorn

def open_browser():
    time.sleep(1.8)
    url = "http://127.0.0.1:8000"
    print(f"\n[Browser] Opening CypherSwarm Dashboard at {url} ...")
    webbrowser.open(url)

if __name__ == "__main__":
    print("=" * 65)
    print("CypherSwarm: Company Brain Co-Pilot (FalkorDB Edition)")
    print("Built for Graph Hacks: Tracks 01, 02, and 03")
    print("=" * 65)

    threading.Thread(target=open_browser, daemon=True).start()

    os.chdir(BACKEND_DIR)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
