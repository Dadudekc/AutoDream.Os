# Force Delete Corrupted Files Script
# Uses Windows API to force delete stubborn files

Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.ComponentModel;

public static class Kernel32
{
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool DeleteFile(string lpFileName);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool RemoveDirectory(string lpPathName);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern bool MoveFileEx(string lpExistingFileName, string lpNewFileName, uint dwFlags);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    public static extern IntPtr CreateFile(
        string lpFileName,
        uint dwDesiredAccess,
        uint dwShareMode,
        IntPtr lpSecurityAttributes,
        uint dwCreationDisposition,
        uint dwFlagsAndAttributes,
        IntPtr hTemplateFile);

    [DllImport("kernel32.dll", SetLastError = true)]
    public static extern bool CloseHandle(IntPtr hObject);

    public const uint GENERIC_ALL = 0x10000000;
    public const uint FILE_SHARE_READ = 0x00000001;
    public const uint FILE_SHARE_WRITE = 0x00000002;
    public const uint FILE_SHARE_DELETE = 0x00000004;
    public const uint OPEN_EXISTING = 3;
    public const uint FILE_ATTRIBUTE_NORMAL = 0x00000080;
    public const uint MOVEFILE_DELAY_UNTIL_REBOOT = 0x00000004;
    public const uint INVALID_HANDLE_VALUE = 0xFFFFFFFF;
}

public static class FileDeleter
{
    public static bool ForceDeleteFile(string filePath)
    {
        try
        {
            // Try normal delete first
            if (Kernel32.DeleteFile(filePath))
                return true;

            // Get last error
            int lastError = Marshal.GetLastWin32Error();
            
            // Try to open file with all access
            IntPtr handle = Kernel32.CreateFile(
                filePath,
                Kernel32.GENERIC_ALL,
                Kernel32.FILE_SHARE_READ | Kernel32.FILE_SHARE_WRITE | Kernel32.FILE_SHARE_DELETE,
                IntPtr.Zero,
                Kernel32.OPEN_EXISTING,
                Kernel32.FILE_ATTRIBUTE_NORMAL,
                IntPtr.Zero);

            if (handle != new IntPtr(Kernel32.INVALID_HANDLE_VALUE))
            {
                Kernel32.CloseHandle(handle);
                // Try delete again after opening
                return Kernel32.DeleteFile(filePath);
            }

            // Last resort: schedule for deletion on reboot
            return Kernel32.MoveFileEx(filePath, null, Kernel32.MOVEFILE_DELAY_UNTIL_REBOOT);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error deleting file " + filePath + ": " + ex.Message);
            return false;
        }
    }

    public static bool ForceDeleteDirectory(string dirPath)
    {
        try
        {
            // Try normal delete first
            if (Kernel32.RemoveDirectory(dirPath))
                return true;

            // Schedule for deletion on reboot
            return Kernel32.MoveFileEx(dirPath, null, Kernel32.MOVEFILE_DELAY_UNTIL_REBOOT);
        }
        catch (Exception ex)
        {
            Console.WriteLine("Error deleting directory " + dirPath + ": " + ex.Message);
            return false;
        }
    }
}
"@

# Function to recursively delete directory contents
function Remove-CorruptedDirectory {
    param([string]$Path)
    
    Write-Host "Attempting to delete: $Path" -ForegroundColor Yellow
    
    if (Test-Path $Path) {
        # Get all items in the directory
        $items = Get-ChildItem -Path $Path -Force -ErrorAction SilentlyContinue
        
        foreach ($item in $items) {
            if ($item.PSIsContainer) {
                # Recursively delete subdirectories
                Remove-CorruptedDirectory -Path $item.FullName
            } else {
                # Delete files using our custom deleter
                Write-Host "Deleting file: $($item.FullName)" -ForegroundColor Red
                $result = [FileDeleter]::ForceDeleteFile($item.FullName)
                if ($result) {
                    Write-Host "Successfully deleted: $($item.FullName)" -ForegroundColor Green
                } else {
                    Write-Host "Failed to delete: $($item.FullName)" -ForegroundColor Red
                }
            }
        }
        
        # Try to delete the directory itself
        Write-Host "Deleting directory: $Path" -ForegroundColor Red
        $result = [FileDeleter]::ForceDeleteDirectory($Path)
        if ($result) {
            Write-Host "Successfully deleted directory: $Path" -ForegroundColor Green
        } else {
            Write-Host "Failed to delete directory: $Path" -ForegroundColor Red
        }
    } else {
        Write-Host "Path does not exist: $Path" -ForegroundColor Yellow
    }
}

# Main execution
Write-Host "=== Force Delete Corrupted Files Tool ===" -ForegroundColor Cyan
Write-Host "Target: temp_dir_old" -ForegroundColor Yellow

# Change to the repository directory
Set-Location "D:\Agent_Cellphone_V2_Repository"

# Delete the corrupted directory
Remove-CorruptedDirectory -Path "temp_dir_old"

Write-Host "=== Operation Complete ===" -ForegroundColor Cyan
