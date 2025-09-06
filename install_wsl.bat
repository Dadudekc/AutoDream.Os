@echo off
REM WSL Installation Script for Windows
REM Run this script as Administrator

echo 🚀 Installing WSL for Agent Cellphone V2 Project...

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as Administrator
) else (
    echo ❌ This script must be run as Administrator!
    echo Right-click Command Prompt and select "Run as Administrator"
    pause
    exit /b 1
)

REM Enable WSL feature
echo 🔧 Enabling WSL feature...
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

REM Enable Virtual Machine Platform
echo 🔧 Enabling Virtual Machine Platform...
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

REM Install WSL
echo 📦 Installing WSL...
wsl --install

echo ✅ WSL installation initiated!
echo.
echo 🔄 Next steps:
echo 1. Restart your computer
echo 2. Open WSL (Ubuntu will be installed automatically)
echo 3. Set up username and password
echo 4. Navigate to your project: cd /mnt/d/Agent_Cellphone_V2_Repository
echo 5. Run the setup script: bash setup_wsl.sh
echo.
echo 🎯 After setup, you'll be able to use git without --no-verify flag!
echo.
echo WE. ARE. SWARM. ⚡️🔥🏆
pause
