# MCP Server Restart Script
# This script helps restart MCP servers after configuration changes

Write-Host "🔄 MCP Server Restart Script" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

Write-Host "`n📋 MCP Configuration Updated:" -ForegroundColor Yellow
Write-Host "✅ Added filesystem server with workspace root: D:\Agent_Cellphone_V2_Repository" -ForegroundColor Green
Write-Host "✅ Added sqlite server with database path" -ForegroundColor Green
Write-Host "✅ Added memory server with store path" -ForegroundColor Green
Write-Host "✅ Added git server with repository path" -ForegroundColor Green
Write-Host "✅ Added github server configuration" -ForegroundColor Green
Write-Host "✅ Added web-search server configuration" -ForegroundColor Green

Write-Host "`n🚨 IMPORTANT: To apply the MCP configuration changes:" -ForegroundColor Red
Write-Host "1. Close all Cursor IDE windows" -ForegroundColor White
Write-Host "2. Restart Cursor IDE" -ForegroundColor White
Write-Host "3. Open the project: D:\Agent_Cellphone_V2_Repository" -ForegroundColor White
Write-Host "4. Go to Cursor Settings → MCP" -ForegroundColor White
Write-Host "5. Verify all servers show 'running' status" -ForegroundColor White

Write-Host "`n🔧 MCP Servers Configured:" -ForegroundColor Yellow
Write-Host "• orchestrator" -ForegroundColor White
Write-Host "• messaging" -ForegroundColor White
Write-Host "• project-scanner" -ForegroundColor White
Write-Host "• debate-coordinator" -ForegroundColor White
Write-Host "• swarm-onboarding" -ForegroundColor White
Write-Host "• performance-monitor" -ForegroundColor White
Write-Host "• filesystem (NEW - with workspace root)" -ForegroundColor Green
Write-Host "• pieces-memory" -ForegroundColor White
Write-Host "• prometheus" -ForegroundColor White
Write-Host "• slack" -ForegroundColor White
Write-Host "• discord" -ForegroundColor White
Write-Host "• sqlite (NEW)" -ForegroundColor Green
Write-Host "• memory (NEW)" -ForegroundColor Green
Write-Host "• git (NEW)" -ForegroundColor Green
Write-Host "• github (NEW)" -ForegroundColor Green
Write-Host "• web-search (NEW)" -ForegroundColor Green

Write-Host "`n🎯 Expected Fix:" -ForegroundColor Yellow
Write-Host "The filesystem server should now resolve relative paths correctly to:" -ForegroundColor White
Write-Host "D:\Agent_Cellphone_V2_Repository" -ForegroundColor Cyan

Write-Host "`n✅ Configuration backup created at:" -ForegroundColor Green
Write-Host ".cursor\mcp.json.backup.*" -ForegroundColor White

Write-Host "`n🐝 WE ARE SWARM - MCP Configuration Updated!" -ForegroundColor Magenta
Write-Host "Ready to restart Cursor IDE and test the fix! 🚀" -ForegroundColor Magenta
