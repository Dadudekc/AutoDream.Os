@echo off
echo 🐝 SWARM Weekly Archiving - 2025-09-11
cd /d "D:\Agent_Cellphone_V2_Repository"

REM Run archiving cycle
python automation/auto_archiver.py

REM Clean up old archives
python automation/auto_archiver.py --cleanup-only

REM Run comprehensive maintenance
python automation/swarm_maintenance_orchestrator.py --run-once

echo 🐝 Weekly archiving complete!
pause
