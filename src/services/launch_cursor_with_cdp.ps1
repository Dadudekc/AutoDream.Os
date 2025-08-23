# Launch Cursor with CDP (Chrome DevTools Protocol) Enabled
# This allows headless messaging to Cursor agent chats without mouse movement

param(
    [int]$Port = 9222,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
🚀 Cursor CDP Launcher
======================

Launches Cursor with Chrome DevTools Protocol enabled for headless messaging.

Usage:
    .\launch_cursor_with_cdp.ps1                    # Use default port 9222
    .\launch_cursor_with_cdp.ps1 -Port 9223        # Use custom port
    .\launch_cursor_with_cdp.ps1 -Help             # Show this help

Features:
    ✅ Launches Cursor with --remote-debugging-port
    ✅ Enables CDP for headless messaging
    ✅ No mouse movement required
    ✅ Works with V1-V2 Message Queue System

After launching:
    python cdp_send_message.py "Your message" --target "Agent-3"
"@
    exit 0
}

Write-Host "🚀 Launching Cursor with CDP enabled..." -ForegroundColor Green
Write-Host "🔌 CDP Port: $Port" -ForegroundColor Cyan
Write-Host "⏳ Please wait..." -ForegroundColor Yellow

# Find Cursor installation paths
$cursorPaths = @(
    "$env:LOCALAPPDATA\Programs\Cursor\Cursor.exe",
    "$env:APPDATA\Cursor\Cursor.exe",
    "$env:PROGRAMFILES\Cursor\Cursor.exe",
    "$env:PROGRAMFILES(X86)\Cursor\Cursor.exe"
)

$cursorExe = $null
foreach ($path in $cursorPaths) {
    if (Test-Path $path) {
        $cursorExe = $path
        break
    }
}

if (-not $cursorExe) {
    Write-Host "❌ Cursor not found in standard locations" -ForegroundColor Red
    Write-Host "💡 Please install Cursor or provide the correct path" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Found Cursor at: $cursorExe" -ForegroundColor Green

# Check if port is already in use
try {
    $tcpClient = New-Object System.Net.Sockets.TcpClient
    $tcpClient.Connect("127.0.0.1", $Port)
    $tcpClient.Close()
    Write-Host "⚠️  Port $Port is already in use" -ForegroundColor Yellow
    Write-Host "💡 Another instance of Cursor with CDP might be running" -ForegroundColor Cyan
} catch {
    Write-Host "✅ Port $Port is available" -ForegroundColor Green
}

# Launch Cursor with CDP
try {
    $arguments = @(
        "--remote-debugging-port=$Port",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor"
    )

    Write-Host "🚀 Starting Cursor with CDP..." -ForegroundColor Green
    $process = Start-Process -FilePath $cursorExe -ArgumentList $arguments -PassThru

    if ($process) {
        Write-Host "✅ Cursor launched successfully (PID: $($process.Id))" -ForegroundColor Green
        Write-Host "🔌 CDP endpoint: http://127.0.0.1:$Port/json" -ForegroundColor Cyan

        # Wait a moment for Cursor to start
        Start-Sleep -Seconds 3

        # Test CDP connection
        try {
            $response = Invoke-RestMethod -Uri "http://127.0.0.1:$Port/json" -TimeoutSec 5
            Write-Host "✅ CDP connection successful!" -ForegroundColor Green
            Write-Host "📊 Found $($response.Count) targets" -ForegroundColor Cyan

            # Show available targets
            foreach ($target in $response) {
                if ($target.type -eq "page") {
                    Write-Host "   📄 $($target.title) ($($target.url))" -ForegroundColor White
                }
            }

        } catch {
            Write-Host "⚠️  CDP connection test failed" -ForegroundColor Yellow
            Write-Host "💡 Cursor may still be starting up" -ForegroundColor Cyan
        }

        Write-Host "`n🎯 Ready for headless messaging!" -ForegroundColor Green
        Write-Host "💡 Test with: python cdp_send_message.py 'Hello Agent-3!' --target 'Agent-3'" -ForegroundColor Cyan

    } else {
        Write-Host "❌ Failed to launch Cursor" -ForegroundColor Red
        exit 1
    }

} catch {
    Write-Host "❌ Error launching Cursor: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "`n📚 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Wait for Cursor to fully load" -ForegroundColor White
Write-Host "2. Open your agent chats" -ForegroundColor White
Write-Host "3. Test messaging: python cdp_send_message.py 'Test message' --target 'Agent-3'" -ForegroundColor White
Write-Host "4. Use with V1-V2 Message Queue System for automated messaging" -ForegroundColor White
