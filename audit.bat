@echo off
REM Windows batch file for audit commands
REM Usage: audit.bat [audit|audit-force|audit-ci|hooks]

if "%1"=="audit" (
    python tools/audit_cleanup.py
) else if "%1"=="audit-force" (
    python tools/audit_cleanup.py --force
) else if "%1"=="audit-ci" (
    python tools/audit_cleanup.py
) else if "%1"=="hooks" (
    bash tools/install_hooks.sh
) else (
    echo Usage: audit.bat [audit^|audit-force^|audit-ci^|hooks]
    echo.
    echo audit       - Run audit (safe)
    echo audit-force - Force report even if risky
    echo audit-ci    - Run audit for CI
    echo hooks       - Install pre-commit hooks
)
