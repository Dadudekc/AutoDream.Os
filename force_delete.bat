@echo off
echo === Force Delete Corrupted Files ===
echo Target: temp_dir_old_to_delete
echo.

REM Try multiple deletion methods
echo Method 1: Standard delete
rmdir /s /q "temp_dir_old_to_delete" 2>nul
if not exist "temp_dir_old_to_delete" (
    echo SUCCESS: Directory deleted with standard method
    goto :end
)

echo Method 2: Force delete with del command
del /f /q "temp_dir_old_to_delete\framework_disabled\system-integration-test-core.js" 2>nul
if not exist "temp_dir_old_to_delete\framework_disabled\system-integration-test-core.js" (
    rmdir /s /q "temp_dir_old_to_delete" 2>nul
    if not exist "temp_dir_old_to_delete" (
        echo SUCCESS: Directory deleted after removing corrupted file
        goto :end
    )
)

echo Method 3: Using robocopy to mirror empty directory
mkdir empty_temp_delete 2>nul
robocopy empty_temp_delete "temp_dir_old_to_delete" /MIR /R:1 /W:1 >nul 2>nul
rmdir empty_temp_delete 2>nul
rmdir "temp_dir_old_to_delete" 2>nul
if not exist "temp_dir_old_to_delete" (
    echo SUCCESS: Directory deleted with robocopy method
    goto :end
)

echo Method 4: Using subst virtual drive
subst Z: . 2>nul
cd /d Z:\temp_dir_old_to_delete\framework_disabled 2>nul
del /f /q system-integration-test-core.js 2>nul
cd /d Z:\ 2>nul
rmdir /s /q temp_dir_old_to_delete 2>nul
subst Z: /d 2>nul
if not exist "temp_dir_old_to_delete" (
    echo SUCCESS: Directory deleted with subst method
    goto :end
)

echo Method 5: Using PowerShell with .NET methods
powershell -Command "try { [System.IO.Directory]::Delete('temp_dir_old_to_delete', $true) } catch { Write-Host 'PowerShell method failed' }" 2>nul
if not exist "temp_dir_old_to_delete" (
    echo SUCCESS: Directory deleted with PowerShell method
    goto :end
)

echo Method 6: Schedule for deletion on reboot
powershell -Command "Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class Kernel32 { [DllImport(\"kernel32.dll\", SetLastError = true, CharSet = CharSet.Unicode)] public static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, uint dwFlags); public const uint MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004; }'; [Kernel32]::MoveFileEx('temp_dir_old_to_delete', $null, [Kernel32]::MOVEFILE_DELAY_UNTIL_REBOOT)" 2>nul
echo Scheduled for deletion on reboot

:end
echo.
echo === Operation Complete ===
if exist "temp_dir_old_to_delete" (
    echo WARNING: Directory still exists - may need manual intervention or reboot
) else (
    echo SUCCESS: Directory successfully deleted
)
pause
