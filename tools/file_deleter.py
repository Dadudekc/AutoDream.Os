#!/usr/bin/env python3
"""
Advanced File Deletion Tool

This tool provides multiple methods to delete corrupted or stubborn files
that cannot be removed through normal Windows commands.

Usage:
    python tools/file_deleter.py <file_path>
    python tools/file_deleter.py <directory_path> --recursive
"""

import os
import sys
import ctypes
import shutil
import stat
import time
from pathlib import Path
from typing import Optional, List
import argparse


class FileDeleter:
    """Advanced file deletion tool with multiple deletion strategies."""
    
    def __init__(self, verbose: bool = True):
        self.verbose = verbose
        self.deletion_methods = [
            self._delete_normal,
            self._delete_force_attributes,
            self._delete_with_retry,
            self._delete_low_level,
            self._delete_with_permissions,
            self._delete_rename_first,
            self._delete_directory_workaround
        ]
    
    def log(self, message: str) -> None:
        """Log messages if verbose mode is enabled."""
        if self.verbose:
            print(f"[FileDeleter] {message}")
    
    def delete_file(self, file_path: str) -> bool:
        """
        Attempt to delete a file using multiple strategies.
        
        Args:
            file_path: Path to the file to delete
            
        Returns:
            True if file was successfully deleted, False otherwise
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            self.log(f"File does not exist: {file_path}")
            return True
        
        self.log(f"Attempting to delete: {file_path}")
        
        for i, method in enumerate(self.deletion_methods, 1):
            self.log(f"Trying method {i}/{len(self.deletion_methods)}: {method.__name__}")
            
            try:
                if method(file_path):
                    self.log(f"Successfully deleted using method: {method.__name__}")
                    return True
            except Exception as e:
                self.log(f"Method {method.__name__} failed: {e}")
            
            # Small delay between attempts
            time.sleep(0.1)
        
        self.log(f"Failed to delete file: {file_path}")
        return False
    
    def delete_directory(self, dir_path: str, recursive: bool = True) -> bool:
        """
        Attempt to delete a directory and its contents.
        
        Args:
            dir_path: Path to the directory to delete
            recursive: Whether to delete contents recursively
            
        Returns:
            True if directory was successfully deleted, False otherwise
        """
        dir_path = Path(dir_path)
        
        if not dir_path.exists():
            self.log(f"Directory does not exist: {dir_path}")
            return True
        
        self.log(f"Attempting to delete directory: {dir_path}")
        
        # First, try to delete all files in the directory
        if recursive:
            try:
                for root, dirs, files in os.walk(dir_path, topdown=False):
                    for file in files:
                        file_path = Path(root) / file
                        self.delete_file(str(file_path))
                    
                    for dir_name in dirs:
                        dir_path_to_remove = Path(root) / dir_name
                        try:
                            os.rmdir(dir_path_to_remove)
                        except:
                            pass
            except Exception as e:
                self.log(f"Error during recursive deletion: {e}")
        
        # Try to delete the directory itself
        for i, method in enumerate(self.deletion_methods, 1):
            self.log(f"Trying directory deletion method {i}: {method.__name__}")
            
            try:
                if method(dir_path):
                    self.log(f"Successfully deleted directory using method: {method.__name__}")
                    return True
            except Exception as e:
                self.log(f"Directory method {method.__name__} failed: {e}")
            
            time.sleep(0.1)
        
        self.log(f"Failed to delete directory: {dir_path}")
        return False
    
    def _delete_normal(self, path: Path) -> bool:
        """Standard file deletion."""
        try:
            if path.is_file():
                os.remove(path)
            else:
                os.rmdir(path)
            return True
        except:
            return False
    
    def _delete_force_attributes(self, path: Path) -> bool:
        """Remove all attributes and delete."""
        try:
            # Remove all attributes
            os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
            
            if path.is_file():
                os.remove(path)
            else:
                os.rmdir(path)
            return True
        except:
            return False
    
    def _delete_with_retry(self, path: Path) -> bool:
        """Delete with multiple retry attempts."""
        for attempt in range(5):
            try:
                if path.is_file():
                    os.remove(path)
                else:
                    os.rmdir(path)
                return True
            except:
                time.sleep(0.2)
        return False
    
    def _delete_low_level(self, path: Path) -> bool:
        """Use low-level Windows API calls."""
        try:
            if sys.platform == "win32":
                # Use Windows API to delete file
                kernel32 = ctypes.windll.kernel32
                file_handle = kernel32.CreateFileW(
                    str(path),
                    0x10000000,  # GENERIC_ALL
                    0,           # No sharing
                    None,
                    3,           # OPEN_EXISTING
                    0x02000000,  # FILE_FLAG_DELETE_ON_CLOSE
                    None
                )
                
                if file_handle != -1:
                    kernel32.CloseHandle(file_handle)
                    return True
        except:
            pass
        return False
    
    def _delete_with_permissions(self, path: Path) -> bool:
        """Take ownership and grant full permissions before deleting."""
        try:
            if sys.platform == "win32":
                # Use Windows API to take ownership
                advapi32 = ctypes.windll.advapi32
                kernel32 = ctypes.windll.kernel32
                
                # Get current process token
                token_handle = ctypes.c_void_p()
                advapi32.OpenProcessToken(
                    kernel32.GetCurrentProcess(),
                    0x0008 | 0x0020,  # TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY
                    ctypes.byref(token_handle)
                )
                
                # Enable SE_TAKE_OWNERSHIP_NAME privilege
                luid = ctypes.c_void_p()
                advapi32.LookupPrivilegeValueW(None, "SeTakeOwnershipPrivilege", ctypes.byref(luid))
                
                # Take ownership
                advapi32.SetFileSecurityW(
                    str(path),
                    0x00080000,  # OWNER_SECURITY_INFORMATION
                    None
                )
                
                kernel32.CloseHandle(token_handle)
            
            # Now try to delete
            if path.is_file():
                os.remove(path)
            else:
                os.rmdir(path)
            return True
        except:
            return False
    
    def _delete_rename_first(self, path: Path) -> bool:
        """Rename the file first, then delete it."""
        try:
            # Generate a temporary name
            temp_name = path.with_suffix('.tmp')
            counter = 0
            while temp_name.exists():
                temp_name = path.with_suffix(f'.tmp{counter}')
                counter += 1
            
            # Rename first
            path.rename(temp_name)
            
            # Now delete the renamed file
            if temp_name.is_file():
                os.remove(temp_name)
            else:
                os.rmdir(temp_name)
            return True
        except:
            return False
    
    def _delete_directory_workaround(self, path: Path) -> bool:
        """Special workaround for stubborn directories."""
        try:
            if path.is_dir():
                # Try to create an empty directory and replace
                temp_dir = path.parent / f"{path.name}_temp"
                temp_dir.mkdir(exist_ok=True)
                
                # Move contents to temp directory
                for item in path.iterdir():
                    try:
                        shutil.move(str(item), str(temp_dir))
                    except:
                        pass
                
                # Remove temp directory
                shutil.rmtree(temp_dir, ignore_errors=True)
                
                # Now try to remove the original directory
                os.rmdir(path)
                return True
        except:
            pass
        return False
    
    def _delete_corrupted_file(self, file_path: str) -> bool:
        """Special method for deleting corrupted files that can't be accessed normally."""
        try:
            # Method 1: Use Windows API directly
            if sys.platform == "win32":
                kernel32 = ctypes.windll.kernel32
                
                # Try to open the file with minimal access
                file_handle = kernel32.CreateFileW(
                    file_path,
                    0x10000000,  # GENERIC_ALL
                    0,           # No sharing
                    None,
                    3,           # OPEN_EXISTING
                    0x02000000,  # FILE_FLAG_DELETE_ON_CLOSE
                    None
                )
                
                if file_handle != -1:
                    kernel32.CloseHandle(file_handle)
                    return True
            
            # Method 2: Use subprocess to call Windows commands
            import subprocess
            try:
                result = subprocess.run(
                    ['cmd', '/c', 'del', '/f', '/q', file_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    return True
            except:
                pass
            
            # Method 3: Try to rename and delete
            try:
                temp_path = file_path + '.tmp'
                subprocess.run(['cmd', '/c', 'ren', file_path, os.path.basename(temp_path)], 
                             capture_output=True, timeout=5)
                subprocess.run(['cmd', '/c', 'del', '/f', '/q', temp_path], 
                             capture_output=True, timeout=5)
                return True
            except:
                pass
            
            # Method 4: Use robocopy to mirror empty directory
            try:
                parent_dir = os.path.dirname(file_path)
                temp_dir = parent_dir + '_empty'
                os.makedirs(temp_dir, exist_ok=True)
                
                subprocess.run(['robocopy', temp_dir, parent_dir, '/mir'], 
                             capture_output=True, timeout=10)
                shutil.rmtree(temp_dir, ignore_errors=True)
                return True
            except:
                pass
                
        except Exception as e:
            self.log(f"Corrupted file deletion failed: {e}")
        
        return False


def main():
    """Main function for command-line usage."""
    parser = argparse.ArgumentParser(description="Advanced File Deletion Tool")
    parser.add_argument("path", help="Path to file or directory to delete")
    parser.add_argument("--recursive", "-r", action="store_true", 
                       help="Delete directories recursively")
    parser.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress verbose output")
    
    args = parser.parse_args()
    
    deleter = FileDeleter(verbose=not args.quiet)
    path_str = args.path
    path = Path(path_str)
    
    # Check if path exists, handling corrupted files
    path_exists = False
    is_file = False
    is_dir = False
    
    try:
        path_exists = path.exists()
        if path_exists:
            is_file = path.is_file()
            is_dir = path.is_dir()
    except OSError as e:
        if "corrupted and unreadable" in str(e):
            print(f"Detected corrupted file: {path}")
            print("Attempting to delete corrupted file...")
            # Try to delete as a corrupted file
            success = deleter._delete_corrupted_file(path_str)
            if success:
                print(f"Successfully deleted corrupted file: {path}")
                sys.exit(0)
            else:
                print(f"Failed to delete corrupted file: {path}")
                sys.exit(1)
        else:
            print(f"Error accessing path: {e}")
            sys.exit(1)
    
    if not path_exists:
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)
    
    success = False
    if is_file:
        success = deleter.delete_file(str(path))
    elif is_dir:
        success = deleter.delete_directory(str(path), recursive=args.recursive)
    else:
        print(f"Error: Unknown path type: {path}")
        sys.exit(1)
    
    if success:
        print(f"Successfully deleted: {path}")
        sys.exit(0)
    else:
        print(f"Failed to delete: {path}")
        sys.exit(1)


if __name__ == "__main__":
    main()
