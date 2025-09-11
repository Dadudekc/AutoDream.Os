@echo off
echo 🐝 SWARM Daily Maintenance - 2025-09-11
cd /d "D:\Agent_Cellphone_V2_Repository"

REM Run maintenance orchestrator
python automation/swarm_maintenance_orchestrator.py --run-once

REM Run size monitoring
python automation/file_size_monitor.py

REM Generate daily report
echo Maintenance complete at %date% %time% >> automation_logs/daily_maintenance.log

echo 🐝 Daily maintenance complete!
pause
