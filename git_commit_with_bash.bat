@echo off
echo ====================================
echo  Git Bash Commit Workflow
echo ====================================
echo.

echo Checking for Git Bash...
where git-bash.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Git Bash found in PATH
    set GIT_BASH=git-bash.exe
) else (
    REM Check common Git installation paths
    if exist "C:\Program Files\Git\bin\bash.exe" (
        echo ✅ Git Bash found at C:\Program Files\Git\bin\bash.exe
        set GIT_BASH="C:\Program Files\Git\bin\bash.exe"
    ) else (
        if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
            echo ✅ Git Bash found at C:\Program Files (x86)\Git\bin\bash.exe
            set GIT_BASH="C:\Program Files (x86)\Git\bin\bash.exe"
        ) else (
            echo ❌ Git Bash not found
            echo Please install Git from https://git-scm.com/
            echo Make sure to select "Git Bash Here" during installation
            pause
            exit /b 1
        )
    )
)
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
start "" %GIT_BASH% --cd="%~dp0"

echo Git Bash opened! Use the commands above to commit.
pause
