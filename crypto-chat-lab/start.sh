#!/usr/bin/env bash
# ==============================================================================
# Crypto Chat Lab - Universal Local & Centralized Server Launcher (macOS & Linux)
# ==============================================================================

set -e

# Terminal Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
GOLD='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear 2>/dev/null || true

echo -e "${CYAN}================================================================${NC}"
echo -e "${CYAN}    🔐 MODERN CRYPTOGRAPHY COURSE · CRYPTO CHAT & MITM LAB       ${NC}"
echo -e "${CYAN}================================================================${NC}"
echo ""

# 1. Verify Node.js
if ! command -v node >/dev/null 2>&1; then
    echo -e "${RED}[ERROR] Node.js is not installed or not in PATH!${NC}"
    echo -e "Please install Node.js (v18 or higher) from https://nodejs.org"
    exit 1
fi

NODE_VER=$(node -v | sed 's/v//' | cut -d. -f1)
if [ "$NODE_VER" -lt 18 ]; then
    echo -e "${GOLD}[WARNING] Detected Node.js $(node -v). Version 18+ is recommended.${NC}"
fi

echo -e "${GREEN}✓ Node.js $(node -v) detected${NC}"

# 2. Verify NPM
if ! command -v npm >/dev/null 2>&1; then
    echo -e "${RED}[ERROR] npm is not installed or not in PATH!${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm $(npm -v) detected${NC}"

# Change to script directory
cd "$(dirname "$0")"

# 3. Check and Install Dependencies
if [ ! -d "node_modules" ]; then
    echo ""
    echo -e "${GOLD}[INSTALL] Installing dependencies (express, socket.io, react, vite)...${NC}"
    npm install
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
fi

# 4. Check and Build Production Frontend
if [ ! -d "dist" ] || [ ! -f "dist/index.html" ]; then
    echo ""
    echo -e "${GOLD}[BUILD] Compiling React frontend with Vite...${NC}"
    npm run build
    echo -e "${GREEN}✓ Frontend built successfully into dist/${NC}"
fi

# 5. Detect Local LAN IP Address
LAN_IP=""
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    LAN_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || scutil --nwi | grep -m1 'address' | awk '{print $3}' || echo "")
else
    # Linux
    LAN_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || ip -4 addr show scope global | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -n1 || echo "")
fi

PORT=${PORT:-3005}

echo ""
echo -e "${CYAN}----------------------------------------------------------------${NC}"
echo -e "${GREEN}🚀 STARTING CENTRALIZED CRYPTO SERVER ON PORT ${PORT}${NC}"
echo -e "   • Local Host URL:        ${CYAN}http://localhost:${PORT}${NC}"
if [ -n "$LAN_IP" ]; then
    echo -e "   • Classroom LAN IP:      ${GOLD}http://${LAN_IP}:${PORT}${NC}"
    echo -e "     (Share this link with students on your local Wi-Fi network!)"
fi
echo -e "${CYAN}----------------------------------------------------------------${NC}"
echo -e "Press ${GOLD}Ctrl + C${NC} to stop the server."
echo ""

# 6. Launch the server
exec node server.js
