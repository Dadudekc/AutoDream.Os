# Git Bash Commit Script for Agent Cellphone V2 Project
# This script uses Git Bash to commit with pre-commit hooks

Write-Host "🚀 Committing with Git Bash and pre-commit hooks..." -ForegroundColor Green

# Check if Git Bash exists
if (-not (Test-Path "C:\Program Files\Git\bin\bash.exe")) {
    Write-Host "❌ Git Bash not found! Please install Git for Windows first." -ForegroundColor Red
    exit 1
}

# Get commit message from parameter or prompt
if ($args.Count -gt 0) {
    $commit_msg = $args -join " "
} else {
    $commit_msg = Read-Host "Enter commit message"
}

Write-Host "📝 Commit message: $commit_msg" -ForegroundColor Cyan

# Use Git Bash to commit with pre-commit hooks
$bash_cmd = "cd /d/Agent_Cellphone_V2_Repository && git add . && git commit -m `"$commit_msg`""
& "C:\Program Files\Git\bin\bash.exe" -c $bash_cmd

Write-Host "✅ Commit completed with Git Bash!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 No more --no-verify flag needed!" -ForegroundColor Yellow
Write-Host ""
Write-Host "WE. ARE. SWARM. ⚡️🔥🏆" -ForegroundColor Magenta
