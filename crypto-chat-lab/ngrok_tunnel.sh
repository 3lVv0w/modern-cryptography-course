#!/usr/bin/env bash
# ==============================================================================
# Modern Cryptography Course - Ngrok Secure Tunnel Launcher
# Exposes Centralized Crypto Chat Server (Port 3005) to Remote Participants
# Provides instant HTTPS and WSS (WebSocket Secure) Public URL
# ==============================================================================

set -e

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
BOLD='\033[1m'
NC='\033[0m' # No Color

PORT="${PORT:-3005}"

echo -e "${CYAN}${BOLD}"
echo "=================================================================="
echo "    🌐 NGROK SECURE TUNNEL LAUNCHER · CRYPTO CHAT LAB"
echo "=================================================================="
echo -e "${NC}"

# Find ngrok executable
NGROK_BIN=""
if command -v ngrok &> /dev/null; then
  NGROK_BIN="ngrok"
elif [ -f "/opt/homebrew/bin/ngrok" ]; then
  NGROK_BIN="/opt/homebrew/bin/ngrok"
elif [ -f "/usr/local/bin/ngrok" ]; then
  NGROK_BIN="/usr/local/bin/ngrok"
fi

if [ -z "$NGROK_BIN" ]; then
  echo -e "${RED}[ERROR] ngrok is not installed or not found in PATH!${NC}\n"
  echo -e "To install ngrok on your system:"
  echo -e "  • ${BOLD}macOS (Homebrew):${NC}  brew install ngrok/ngrok/ngrok"
  echo -e "  • ${BOLD}Windows (Winget):${NC}  winget install ngrok.ngrok"
  echo -e "  • ${BOLD}Linux (Snap/Apt):${NC}  curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo 'deb https://ngrok-agent.s3.amazonaws.com buster main' | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok"
  echo -e "  • ${BOLD}Official Website:${NC}  https://ngrok.com/download\n"
  echo -e "${YELLOW}After installing, register your free account authtoken:${NC}"
  echo -e "  ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>\n"
  exit 1
fi

echo -e "${GREEN}✓ ngrok found:${NC} $($NGROK_BIN version)"
echo -e "${BLUE}Targeting local server on port:${NC} ${BOLD}$PORT${NC}"
echo ""
echo -e "${YELLOW}${BOLD}INSTRUCTOR SETUP & CLIENT CONNECTION INSTRUCTIONS:${NC}"
echo -e "1. Make sure your Crypto Lab server is running in another terminal:"
echo -e "   ${CYAN}./start.sh${NC} (or ${CYAN}npm start${NC})"
echo -e "2. Once ngrok starts below, copy the ${BOLD}Forwarding HTTPS URL${NC}:"
echo -e "   Example: ${GREEN}https://xxxx-xx-xx.ngrok-free.app${NC}"
echo -e "3. Share this HTTPS URL with your workshop / remote participants:"
echo -e "   • They can open the URL in their browser to access the complete Web UI."
echo -e "   • Or in their local Crypto Lab UI, click ${BOLD}'Server: Localhost:3005'${NC} and paste this URL."
echo -e "4. ${BOLD}WSS & MQTT Access:${NC}"
echo -e "   • Socket.IO auto-connects over ${GREEN}wss://xxxx.ngrok-free.app${NC}"
echo -e "   • MQTT over WebSockets is accessible at: ${GREEN}wss://xxxx.ngrok-free.app/mqtt${NC}"
echo -e "5. View real-time tunnel inspection traffic at: ${CYAN}http://127.0.0.1:4040${NC}"
echo ""
echo -e "${BOLD}Launching ngrok tunnel on port $PORT... (Press Ctrl+C to terminate)${NC}"
echo "------------------------------------------------------------------"

exec "$NGROK_BIN" http "$PORT"
