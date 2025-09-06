@echo off
echo ====================================
echo  Git Bash Setup for Pre-commit Hooks
echo ====================================
echo.

echo Checking for Git Bash...
where git-bash.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✅ Git Bash found in PATH
    goto :setup
) else (
    echo Checking common Git Bash locations...
    if exist "C:\Program Files\Git\bin\bash.exe" (
        echo ✅ Git Bash found at C:\Program Files\Git\bin\bash.exe
        goto :setup
    ) else if exist "C:\Program Files (x86)\Git\bin\bash.exe" (
        echo ✅ Git Bash found at C:\Program Files (x86)\Git\bin\bash.exe
        goto :setup
    ) else (
        echo ❌ Git Bash not found. Please install Git from https://git-scm.com/
        echo Make sure to select "Git Bash Here" during installation
        goto :end
    )
)

:setup
echo.
echo ====================================
echo  Git Bash Setup Complete!
echo ====================================
echo.
echo 🎯 Your new workflow:
echo.
echo 1. Right-click in project folder
echo 2. Select "Git Bash Here"
echo 3. Make your changes
echo 4. Test: pre-commit run --all-files
echo 5. Commit: git commit -m "message"
echo 6. Push: git push
echo.
echo ✅ No more --no-verify needed!
echo.
echo ====================================
pause
:end
