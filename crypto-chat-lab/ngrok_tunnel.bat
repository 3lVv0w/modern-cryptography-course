@echo off
REM ==============================================================================
REM Modern Cryptography Course - Ngrok Secure Tunnel Launcher (Windows)
REM Exposes Centralized Crypto Chat Server (Port 3005) to Remote Participants
REM Provides instant HTTPS and WSS (WebSocket Secure) Public URL
REM ==============================================================================

echo ==================================================================
echo     NGROK SECURE TUNNEL LAUNCHER - CRYPTO CHAT LAB
echo ==================================================================
echo.

where ngrok >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] ngrok is not found in your system PATH!
    echo.
    echo To install ngrok on Windows:
    echo   winget install ngrok.ngrok
    echo   or download from: https://ngrok.com/download
    echo.
    echo After installing, add your auth token:
    echo   ngrok config add-authtoken YOUR_AUTH_TOKEN
    echo.
    pause
    exit /b 1
)

echo [OK] ngrok detected.
echo Target local server port: 3005
echo.
echo INSTRUCTIONS:
echo 1. Ensure your server is running (start.bat or npm start)
echo 2. Copy the Forwarding URL (e.g. https://xxxx.ngrok-free.app)
echo 3. Remote clients can visit that URL in any browser or enter it into the app
echo 4. WSS and MQTT over WebSockets (wss://xxxx.ngrok-free.app/mqtt) are enabled
echo 5. View ngrok web dashboard at http://127.0.0.1:4040
echo.
echo Launching tunnel...
ngrok http 3005
pause
