@echo off
echo 🚀 Status.json Generator for All Agents
echo ======================================
echo.

echo 📋 Available Contracts from Recent Onboarding:
echo ✅ Agent-1: SSOT Violation Analysis & Resolution (400 pts)
echo ✅ Agent-2: Code Duplication Detection & Consolidation (350 pts)
echo ✅ Agent-3: Monolithic File Modularization (500 pts)
echo ✅ Agent-5: Data Source Consolidation (450 pts)
echo ✅ Agent-6: Function Duplication Elimination (300 pts)
echo ✅ Agent-7: Class Hierarchy Refactoring (400 pts)
echo ✅ Agent-8: Configuration Management Consolidation (350 pts)
echo.

echo 🔧 Generating status files for all agents...
echo.

REM Agent-1
echo 🚀 Generating status for Agent-1...
python generate_status.py --agent Agent-1 --contract-id SSOT-001 --title "SSOT Violation Analysis & Resolution" --points 400 --category "SSOT_Resolution" --difficulty "HIGH" --estimated-time "3-4 hours"
echo.

REM Agent-2
echo 🚀 Generating status for Agent-2...
python generate_status.py --agent Agent-2 --contract-id DEDUP-001 --title "Code Duplication Detection & Consolidation" --points 350 --category "Deduplication" --difficulty "MEDIUM" --estimated-time "2-3 hours"
echo.

REM Agent-3
echo 🚀 Generating status for Agent-3...
python generate_status.py --agent Agent-3 --contract-id MODULAR-001 --title "Monolithic File Modularization" --points 500 --category "Modularization" --difficulty "HIGH" --estimated-time "4-5 hours"
echo.

REM Agent-5
echo 🚀 Generating status for Agent-5...
python generate_status.py --agent Agent-5 --contract-id SSOT-002 --title "Data Source Consolidation" --points 450 --category "SSOT_Resolution" --difficulty "MEDIUM" --estimated-time "2-3 hours"
echo.

REM Agent-6
echo 🚀 Generating status for Agent-6...
python generate_status.py --agent Agent-6 --contract-id DEDUP-002 --title "Function Duplication Elimination" --points 300 --category "Deduplication" --difficulty "MEDIUM" --estimated-time "2-3 hours"
echo.

REM Agent-7
echo 🚀 Generating status for Agent-7...
python generate_status.py --agent Agent-7 --contract-id MODULAR-002 --title "Class Hierarchy Refactoring" --points 400 --category "Modularization" --difficulty "MEDIUM" --estimated-time "3-4 hours"
echo.

REM Agent-8
echo 🚀 Generating status for Agent-8...
python generate_status.py --agent Agent-8 --contract-id SSOT-003 --title "Configuration Management Consolidation" --points 350 --category "SSOT_Resolution" --difficulty "MEDIUM" --estimated-time "2-3 hours"
echo.

echo 🎉 All status files generated successfully!
echo.
echo 📁 Status files are now in each agent's workspace:
echo    agent_workspaces\Agent-1\status.json
echo    agent_workspaces\Agent-2\status.json
echo    agent_workspaces\Agent-3\status.json
echo    agent_workspaces\Agent-5\status.json
echo    agent_workspaces\Agent-6\status.json
echo    agent_workspaces\Agent-7\status.json
echo    agent_workspaces\Agent-8\status.json
echo.
echo 🔧 Next steps for agents:
echo    1. Review your status.json file
echo    2. Update progress as you work
echo    3. Use devlog system for updates
echo    4. Keep workspace clean and organized
echo.
echo 🚀 Good luck with your contracts!
pause
