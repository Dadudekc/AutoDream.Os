# Launch Cursor with CDP debugging enabled for headless agent messaging
# Windows PowerShell script

$cursor = "$Env:LOCALAPPDATA\Programs\Cursor\Cursor.exe"

if (Test-Path $cursor) {
    Write-Host "🚀 Launching Cursor with CDP debugging enabled..." -ForegroundColor Green
    Write-Host "📡 CDP endpoint will be available at: http://127.0.0.1:9222" -ForegroundColor Yellow
    Write-Host "🛰️ Use cdp_send_message.py to send messages without mouse movement" -ForegroundColor Cyan

    Start-Process -FilePath $cursor -ArgumentList "--remote-debugging-port=9222"

    Write-Host "✅ Cursor launched with CDP debugging!" -ForegroundColor Green
    Write-Host "⏳ Wait for Cursor to fully load, then use the CDP messenger tool." -ForegroundColor Yellow
} else {
    Write-Host "❌ Cursor not found at: $cursor" -ForegroundColor Red
    Write-Host "💡 Make sure Cursor is installed in the default location." -ForegroundColor Yellow
}
