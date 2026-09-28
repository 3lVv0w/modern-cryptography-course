# ==============================================================================
# Crypto Chat Lab - Windows PowerShell Launcher
# Run with: powershell -ExecutionPolicy Bypass -File .\start.ps1
# ==============================================================================

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "    🔐 MODERN CRYPTOGRAPHY COURSE · CRYPTO CHAT & MITM LAB       " -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Verify Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] Node.js is not found in PATH!" -ForegroundColor Red
    Write-Host "Please install Node.js (v18 or higher) from https://nodejs.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit..."
    exit 1
}

$nodeVersion = node -v
Write-Host "[OK] Node.js $nodeVersion detected" -ForegroundColor Green

# 2. Verify NPM
if (-not (Get-Command npm -ErrorAction SilentlyContinue)) {
    Write-Host "[ERROR] npm is not found in PATH!" -ForegroundColor Red
    Read-Host "Press Enter to exit..."
    exit 1
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 3. Check and Install Dependencies
if (-not (Test-Path "node_modules")) {
    Write-Host "`n[INSTALL] Installing dependencies..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] npm install failed!" -ForegroundColor Red
        exit 1
    }
}

# 4. Check and Build Production Frontend
if (-not (Test-Path "dist")) {
    Write-Host "`n[BUILD] Compiling React frontend with Vite..." -ForegroundColor Yellow
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] npm run build failed!" -ForegroundColor Red
        exit 1
    }
}

# 5. Detect Local IPv4 LAN Address
$localIp = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias "Wi-Fi*", "Ethernet*" -ErrorAction SilentlyContinue | Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } | Select-Object -First 1).IPAddress

$port = 3005

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "🚀 STARTING CENTRALIZED CRYPTO SERVER ON PORT $port" -ForegroundColor Green
Write-Host "   • Local Host URL:   http://localhost:$port" -ForegroundColor White
if ($localIp) {
    Write-Host "   • Classroom LAN IP: http://${localIp}:$port" -ForegroundColor Yellow
    Write-Host "     (Share this URL with workshop participants on your Wi-Fi!)" -ForegroundColor Gray
}
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Press Ctrl + C to stop the server.`n"

node server.js
