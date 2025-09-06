# WSL Installation Script for Windows
# Run this script as Administrator in PowerShell

Write-Host "🚀 Installing WSL for Agent Cellphone V2 Project..." -ForegroundColor Green

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "❌ This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Enable WSL feature
Write-Host "🔧 Enabling WSL feature..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# Enable Virtual Machine Platform
Write-Host "🔧 Enabling Virtual Machine Platform..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Install WSL
Write-Host "📦 Installing WSL..." -ForegroundColor Yellow
wsl --install

Write-Host "✅ WSL installation initiated!" -ForegroundColor Green
Write-Host ""
Write-Host "🔄 Next steps:" -ForegroundColor Cyan
Write-Host "1. Restart your computer" -ForegroundColor White
Write-Host "2. Open WSL (Ubuntu will be installed automatically)" -ForegroundColor White
Write-Host "3. Set up username and password" -ForegroundColor White
Write-Host "4. Navigate to your project: cd /mnt/d/Agent_Cellphone_V2_Repository" -ForegroundColor White
Write-Host "5. Run the setup script: bash setup_wsl.sh" -ForegroundColor White
Write-Host ""
Write-Host "🎯 After setup, you'll be able to use git without --no-verify flag!" -ForegroundColor Green
Write-Host ""
Write-Host "WE. ARE. SWARM. ⚡️🔥🏆" -ForegroundColor Magenta
