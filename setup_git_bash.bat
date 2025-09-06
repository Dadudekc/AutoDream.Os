@echo off
REM Git Bash Setup for Agent Cellphone V2 Project
REM This script configures pre-commit to use Git Bash

echo 🚀 Setting up Git Bash for pre-commit hooks...

REM Check if Git Bash exists
if not exist "C:\Program Files\Git\bin\bash.exe" (
    echo ❌ Git Bash not found! Please install Git for Windows first.
    echo Download from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git Bash found!

REM Configure pre-commit to use Git Bash
echo 🔧 Configuring pre-commit to use Git Bash...

REM Set environment variable for pre-commit
setx PRE_COMMIT_USE_SYSTEM_GIT "1"
setx GIT_BASH_PATH "C:\Program Files\Git\bin\bash.exe"

echo ✅ Environment variables set!

REM Test pre-commit with Git Bash
echo 🧪 Testing pre-commit with Git Bash...
"C:\Program Files\Git\bin\bash.exe" -c "cd /d/Agent_Cellphone_V2_Repository && pre-commit run --all-files"

echo.
echo ✅ Git Bash setup complete!
echo.
echo 🎯 Next steps:
echo 1. Close and reopen your terminal
echo 2. Test: git commit -m "test: Git Bash setup"
echo 3. No more --no-verify flag needed! 🎉
echo.
echo WE. ARE. SWARM. ⚡️🔥🏆
pause
