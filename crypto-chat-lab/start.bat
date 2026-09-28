@echo off
rem ==============================================================================
rem Crypto Chat Lab - Windows Batch Launcher (CMD)
rem ==============================================================================
title Crypto Chat Lab - Modern Cryptography Course
cls

echo ================================================================
echo     🔐 MODERN CRYPTOGRAPHY COURSE · CRYPTO CHAT & MITM LAB
echo ================================================================
echo.

rem 1. Check Node.js
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH!
    echo Please download and install Node.js (v18+) from https://nodejs.org
    pause
    exit /b 1
)

echo [OK] Node.js detected:
node -v

rem 2. Check NPM
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed or not in PATH!
    pause
    exit /b 1
)
echo [OK] npm detected.
echo.

rem Navigate to script directory
cd /d "%~dp0"

rem 3. Check and Install Dependencies
if not exist "node_modules\" (
    echo [INSTALL] Installing dependencies (Express, Socket.IO, React, Vite)...
    call npm install
    if %errorlevel% neq 0 (
        echo [ERROR] npm install failed!
        pause
        exit /b 1
    )
)

rem 4. Check and Build Production Frontend
if not exist "dist\" (
    echo [BUILD] Compiling React frontend with Vite...
    call npm run build
    if %errorlevel% neq 0 (
        echo [ERROR] npm run build failed!
        pause
        exit /b 1
    )
)

echo.
echo ================================================================
echo 🚀 STARTING CENTRALIZED CRYPTO SERVER ON PORT 3005
echo    • Local Browser: http://localhost:3005
echo    • Find your LAN IP by running "ipconfig" in another terminal
echo    • Participants on your Wi-Fi can join at http://[YOUR-IP]:3005
echo ================================================================
echo Press Ctrl + C to stop the server.
echo.

node server.js
pause
