# Schedule files for deletion on reboot using Windows API

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public static class Kernel32
{
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, uint dwFlags);

    public const uint MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004;
}
"@

Write-Host "=== Scheduling Files for Deletion on Reboot ===" -ForegroundColor Cyan

# Schedule the corrupted file for deletion
$corruptedFile = "temp_dir_old\framework_disabled\system-integration-test-core.js"
Write-Host "Scheduling file for deletion: $corruptedFile" -ForegroundColor Yellow

$result = [Kernel32]::MoveFileEx($corruptedFile, $null, [Kernel32]::MOVEFILE_DELAY_UNTIL_REBOOT)
if ($result) {
    Write-Host "Successfully scheduled file for deletion on reboot" -ForegroundColor Green
} else {
    Write-Host "Failed to schedule file for deletion" -ForegroundColor Red
    Write-Host "Error code: $([System.Runtime.InteropServices.Marshal]::GetLastWin32Error())" -ForegroundColor Red
}

# Schedule the directories for deletion
$directories = @(
    "temp_dir_old\framework_disabled",
    "temp_dir_old"
)

foreach ($dir in $directories) {
    Write-Host "Scheduling directory for deletion: $dir" -ForegroundColor Yellow
    $result = [Kernel32]::MoveFileEx($dir, $null, [Kernel32]::MOVEFILE_DELAY_UNTIL_REBOOT)
    if ($result) {
        Write-Host "Successfully scheduled directory for deletion on reboot" -ForegroundColor Green
    } else {
        Write-Host "Failed to schedule directory for deletion" -ForegroundColor Red
        Write-Host "Error code: $([System.Runtime.InteropServices.Marshal]::GetLastWin32Error())" -ForegroundColor Red
    }
}

Write-Host "=== Operation Complete ===" -ForegroundColor Cyan
Write-Host "Files will be deleted on the next system reboot" -ForegroundColor Yellow
