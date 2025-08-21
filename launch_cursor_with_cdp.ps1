# Launch Cursor with Chrome DevTools Protocol (CDP) enabled
# This enables headless message delivery without mouse movement

param(
    [string]$CursorPath = "$Env:LOCALAPPDATA\Programs\Cursor\Cursor.exe",
    [int]$CDPPort = 9222,
    [switch]$Force,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
Cursor CDP Launcher
===================

Launches Cursor with Chrome DevTools Protocol enabled for headless messaging.

Usage:
    .\launch_cursor_with_cdp.ps1 [options]

Options:
    -CursorPath <path>    Path to Cursor executable (default: auto-detect)
    -CDPPort <port>       CDP port number (default: 9222)
    -Force                Force launch even if Cursor is already running
    -Help                 Show this help message

Examples:
    .\launch_cursor_with_cdp.ps1
    .\launch_cursor_with_cdp.ps1 -CDPPort 9223
    .\launch_cursor_with_cdp.ps1 -Force

"@
    exit 0
}

# Function to check if Cursor is already running
function Test-CursorRunning {
    $processes = Get-Process -Name "Cursor" -ErrorAction SilentlyContinue
    return $processes.Count -gt 0
}

# Function to check if CDP port is available
function Test-CDPPortAvailable {
    param([int]$Port)
    
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("127.0.0.1", $Port)
        $connection.Close()
        return $false  # Port is in use
    }
    catch {
        return $true   # Port is available
    }
}

# Function to find Cursor installation
function Find-CursorInstallation {
    $possiblePaths = @(
        "$Env:LOCALAPPDATA\Programs\Cursor\Cursor.exe",
        "$Env:PROGRAMFILES\Cursor\Cursor.exe",
        "$Env:PROGRAMFILES(X86)\Cursor\Cursor.exe",
        "$Env:USERPROFILE\AppData\Local\Programs\Cursor\Cursor.exe"
    )
    
    foreach ($path in $possiblePaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    return $null
}

# Main execution
Write-Host "Cursor CDP Launcher" -ForegroundColor Green
Write-Host "===================" -ForegroundColor Green
Write-Host ""

# Check if Cursor is already running
if (Test-CursorRunning) {
    Write-Host "Cursor is already running." -ForegroundColor Yellow
    
    if (-not $Force) {
        Write-Host "Use -Force to launch another instance." -ForegroundColor Yellow
        Write-Host ""
        
        $response = Read-Host "Do you want to launch another instance? (y/N)"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Host "Launch cancelled." -ForegroundColor Red
            exit 1
        }
    }
    
    Write-Host "Launching additional Cursor instance..." -ForegroundColor Yellow
}

# Check if CDP port is available
if (-not (Test-CDPPortAvailable -Port $CDPPort)) {
    Write-Host "Warning: CDP port $CDPPort is already in use." -ForegroundColor Yellow
    Write-Host "This might cause conflicts with existing Cursor instances." -ForegroundColor Yellow
    Write-Host ""
    
    $response = Read-Host "Do you want to continue? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Launch cancelled." -ForegroundColor Red
        exit 1
    }
}

# Find Cursor installation if not specified
if (-not (Test-Path $CursorPath)) {
    Write-Host "Cursor path not found: $CursorPath" -ForegroundColor Yellow
    Write-Host "Searching for Cursor installation..." -ForegroundColor Yellow
    
    $foundPath = Find-CursorInstallation
    if ($foundPath) {
        $CursorPath = $foundPath
        Write-Host "Found Cursor at: $CursorPath" -ForegroundColor Green
    } else {
        Write-Host "Error: Cursor not found in standard locations." -ForegroundColor Red
        Write-Host "Please specify the correct path with -CursorPath parameter." -ForegroundColor Red
        exit 1
    }
}

# Verify Cursor executable exists
if (-not (Test-Path $CursorPath)) {
    Write-Host "Error: Cursor executable not found at: $CursorPath" -ForegroundColor Red
    exit 1
}

# Prepare launch arguments
$arguments = @(
    "--remote-debugging-port=$CDPPort",
    "--disable-web-security",
    "--disable-features=VizDisplayCompositor"
)

$argumentsString = $arguments -join " "

Write-Host "Launching Cursor with CDP enabled..." -ForegroundColor Green
Write-Host "Executable: $CursorPath" -ForegroundColor Cyan
Write-Host "CDP Port: $CDPPort" -ForegroundColor Cyan
Write-Host "Arguments: $argumentsString" -ForegroundColor Cyan
Write-Host ""

try {
    # Launch Cursor with CDP
    $process = Start-Process -FilePath $CursorPath -ArgumentList $arguments -PassThru
    
    if ($process) {
        Write-Host "Cursor launched successfully!" -ForegroundColor Green
        Write-Host "Process ID: $($process.Id)" -ForegroundColor Cyan
        Write-Host "CDP endpoint: http://127.0.0.1:$CDPPort/json" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "You can now use the message queue system to send messages without mouse movement." -ForegroundColor Green
        Write-Host ""
        Write-Host "Test CDP connection:" -ForegroundColor Yellow
        Write-Host "  python src/services/cdp_message_delivery.py" -ForegroundColor White
        Write-Host ""
        Write-Host "Send test message:" -ForegroundColor Yellow
        Write-Host "  python -c \"from src.services.cdp_message_delivery import send_message_to_cursor; print(send_message_to_cursor('Test message via CDP'))\"" -ForegroundColor White
    } else {
        Write-Host "Error: Failed to launch Cursor." -ForegroundColor Red
        exit 1
    }
}
catch {
    Write-Host "Error launching Cursor: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Wait a moment for Cursor to start
Write-Host "Waiting for Cursor to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test CDP connection
Write-Host "Testing CDP connection..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:$CDPPort/json" -TimeoutSec 5 -ErrorAction Stop
    $targets = $response.Content | ConvertFrom-Json
    
    Write-Host "CDP connection successful!" -ForegroundColor Green
    Write-Host "Found $($targets.Count) targets:" -ForegroundColor Cyan
    
    foreach ($target in $targets) {
        if ($target.type -eq "page") {
            Write-Host "  - $($target.title) ($($target.url))" -ForegroundColor White
        }
    }
}
catch {
    Write-Host "Warning: CDP connection test failed. Cursor may still be initializing." -ForegroundColor Yellow
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "You can manually test the connection later with:" -ForegroundColor Yellow
    Write-Host "  python src/services/cdp_message_delivery.py" -ForegroundColor White
}

Write-Host ""
Write-Host "Cursor CDP launcher completed successfully!" -ForegroundColor Green
Write-Host "The message queue system is now ready to use." -ForegroundColor Green
