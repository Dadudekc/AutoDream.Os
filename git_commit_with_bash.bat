@echo off
echo ====================================
echo  Git Bash Commit Workflow
echo ====================================
echo.

echo Checking for Git Bash...
where git-bash.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Git Bash not found in PATH
    echo Please install Git with Git Bash
    pause
    exit /b 1
)

echo ✅ Git Bash found
echo.

echo Opening Git Bash for commit...
echo.
echo In Git Bash, run these commands:
echo   cd /d/Agent_Cellphone_V2_Repository
echo   git status
echo   pre-commit run --all-files
echo   git add .
echo   git commit -m "your message"
echo   git push origin agent
echo.

REM Launch Git Bash in the project directory
start "" "C:\Program Files\Git\bin\bash.exe" --cd="%~dp0"

echo Git Bash opened! Use the commands above to commit.
pause
