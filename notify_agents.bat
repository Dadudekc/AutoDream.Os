@echo off
echo 🐝 SWARM DEBATE NOTIFICATION SYSTEM
echo ====================================
echo.

echo 📊 Checking debate participation status...
python simple_debate_monitor.py --check
echo.

echo 🚨 Sending urgent notifications to agents with low participation...
python simple_debate_monitor.py --notify-pending
echo.

echo 📋 Notification complete!
echo.
echo 🎯 Next steps:
echo    - Monitor agent responses in cursor_agent_coords.json
echo    - Check debate_participation_tool.py for new arguments
echo    - Run notifications again if needed
echo.
echo 🐝 WE ARE SWARM - Active coordination in progress!
echo.
pause
