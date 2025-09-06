# PowerShell script to properly launch Git Bash for git operations
param(
    [string]$ProjectPath = $PWD.Path
)

Write-Host "🚀 Launching Git Bash for Professional Git Workflow" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Yellow

# Check for Git Bash
$gitBashPaths = @(
    "C:\Program Files\Git\bin\bash.exe",
    "C:\Program Files (x86)\Git\bin\bash.exe",
    "$env:ProgramFiles\Git\bin\bash.exe"
)

$gitBashPath = $null
foreach ($path in $gitBashPaths) {
    if (Test-Path $path) {
        $gitBashPath = $path
        Write-Host "✅ Git Bash found at: $path" -ForegroundColor Green
        break
    }
}

if (-not $gitBashPath) {
    Write-Host "❌ Git Bash not found. Please install Git from https://git-scm.com/" -ForegroundColor Red
    Write-Host "Make sure to select 'Git Bash Here' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📋 Your Professional Git Bash Workflow:" -ForegroundColor Cyan
Write-Host "1. Make changes in your editor" -ForegroundColor White
Write-Host "2. Test: pre-commit run --all-files" -ForegroundColor White
Write-Host "3. Commit: git commit -m 'your message'" -ForegroundColor White
Write-Host "4. Push: git push origin agent" -ForegroundColor White
Write-Host ""

# Launch Git Bash with proper working directory
Write-Host "🔧 Launching Git Bash..." -ForegroundColor Green
try {
    Start-Process -FilePath $gitBashPath -ArgumentList "--cd=`"$ProjectPath`"" -WindowStyle Normal
    Write-Host "✅ Git Bash launched successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "💡 Tip: Use the commands shown above in Git Bash" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to launch Git Bash: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to close this window"
