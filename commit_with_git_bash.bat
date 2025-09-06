@echo off
REM Git Bash Commit Script for Agent Cellphone V2 Project
REM This script uses Git Bash to commit with pre-commit hooks

echo 🚀 Committing with Git Bash and pre-commit hooks...

REM Check if Git Bash exists
if not exist "C:\Program Files\Git\bin\bash.exe" (
    echo ❌ Git Bash not found! Please install Git for Windows first.
    pause
    exit /b 1
)

REM Get commit message from user
if "%1"=="" (
    set /p commit_msg="Enter commit message: "
) else (
    set commit_msg=%*
)

echo 📝 Commit message: %commit_msg%

REM Use Git Bash to commit with pre-commit hooks
"C:\Program Files\Git\bin\bash.exe" -c "cd /d/Agent_Cellphone_V2_Repository && git add . && git commit -m \"%commit_msg%\""

echo ✅ Commit completed with Git Bash!
echo.
echo 🎯 No more --no-verify flag needed!
echo.
echo WE. ARE. SWARM. ⚡️🔥🏆
