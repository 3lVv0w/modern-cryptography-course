#!/usr/bin/env python3
"""
Universal Cross-Platform Launcher for Crypto Chat Lab
Works on macOS, Windows, and Linux.
Usage: python3 start_lab.py
"""

import os
import sys
import shutil
import socket
import subprocess
from pathlib import Path

def get_lan_ip():
    """Detect local LAN IP address by querying routing table."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't actually send data, just connects to determine outbound interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'

def main():
    print("=" * 64)
    print("    🔐 MODERN CRYPTOGRAPHY COURSE · CRYPTO CHAT & MITM LAB")
    print("=" * 64)

    # 1. Verify Node.js
    node_path = shutil.which("node")
    if not node_path:
        print("\n[ERROR] Node.js is not found in your system PATH!")
        print("Please install Node.js (v18 or higher) from: https://nodejs.org")
        sys.exit(1)

    node_ver = subprocess.check_output([node_path, "-v"], text=True).strip()
    print(f"✓ Node.js detected: {node_ver}")

    # 2. Verify NPM
    npm_path = shutil.which("npm")
    if not npm_path:
        print("\n[ERROR] npm is not found in your system PATH!")
        sys.exit(1)
    
    # Switch to script directory
    script_dir = Path(__file__).resolve().parent
    os.chdir(script_dir)

    # 3. Check and Install Dependencies
    node_modules = script_dir / "node_modules"
    if not node_modules.exists():
        print("\n[INSTALL] Installing dependencies (Express, Socket.IO, React, Vite)...")
        res = subprocess.run([npm_path, "install"], shell=(sys.platform == 'win32'))
        if res.returncode != 0:
            print("[ERROR] npm install failed!")
            sys.exit(1)
        print("✓ Dependencies installed.")

    # 4. Check and Build Production Frontend
    dist_dir = script_dir / "dist"
    if not dist_dir.exists() or not (dist_dir / "index.html").exists():
        print("\n[BUILD] Compiling React frontend with Vite...")
        res = subprocess.run([npm_path, "run", "build"], shell=(sys.platform == 'win32'))
        if res.returncode != 0:
            print("[ERROR] npm run build failed!")
            sys.exit(1)
        print("✓ Production frontend compiled successfully into dist/")

    # 5. Network Discovery
    lan_ip = get_lan_ip()
    port = os.environ.get("PORT", "3005")

    print("\n" + "-" * 64)
    print(f"🚀 STARTING CENTRALIZED CRYPTO SERVER ON PORT {port}")
    print(f"   • Local Machine:    http://localhost:{port}")
    if lan_ip and lan_ip != '127.0.0.1':
        print(f"   • Classroom LAN IP: http://{lan_ip}:{port}")
        print("     (Share this URL with workshop participants on your Wi-Fi!)")
    print(f"   • MQTT TCP Broker:  mqtt://localhost:1883 (Topic: crypto/#)")
    print(f"   • MQTT WebSockets:  ws://localhost:{port}/mqtt")
    print(f"   • Remote Ngrok WSS: Run './ngrok_tunnel.sh' in another terminal")
    print("-" * 64)
    print("Press Ctrl + C to stop the server.\n")

    # 6. Execute node server.js
    try:
        subprocess.run([node_path, "server.js"])
    except KeyboardInterrupt:
        print("\nShutting down Crypto Chat Lab server. Goodbye!")

if __name__ == "__main__":
    main()
