"""
File Manager - KISS Simplified
==============================

Simplified file manager for essential file operations.
KISS PRINCIPLE: Keep It Simple, Stupid - restored after deletion.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Restoration
License: MIT
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class FileManager:
    """KISS Simplified File Manager.

    Restored after deletion - focuses on essential file operations only.
    """

    def __init__(self):
        """Initialize simplified file manager."""
        self.operations_count = 0
        self.last_operation = None

    def read_file(self, file_path: str) -> str:
        """Read file content - simplified."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            self._record_operation("read", file_path)
            return content
        except Exception as e:
            raise Exception(f"Failed to read file {file_path}: {e}")

    def write_file(self, file_path: str, content: str) -> bool:
        """Write file content - simplified."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self._record_operation("write", file_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to write file {file_path}: {e}")

    def copy_file(self, source: str, destination: str) -> bool:
        """Copy file - simplified."""
        try:
            shutil.copy2(source, destination)
            self._record_operation("copy", f"{source} -> {destination}")
            return True
        except Exception as e:
            raise Exception(f"Failed to copy file {source} to {destination}: {e}")

    def move_file(self, source: str, destination: str) -> bool:
        """Move file - simplified."""
        try:
            shutil.move(source, destination)
            self._record_operation("move", f"{source} -> {destination}")
            return True
        except Exception as e:
            raise Exception(f"Failed to move file {source} to {destination}: {e}")

    def delete_file(self, file_path: str) -> bool:
        """Delete file - simplified."""
        try:
            os.remove(file_path)
            self._record_operation("delete", file_path)
            return True
        except Exception as e:
            raise Exception(f"Failed to delete file {file_path}: {e}")

    def file_exists(self, file_path: str) -> bool:
        """Check if file exists - simplified."""
        return os.path.exists(file_path)

    def list_directory(self, directory: str) -> List[str]:
        """List directory contents - simplified."""
        try:
            return os.listdir(directory)
        except Exception as e:
            raise Exception(f"Failed to list directory {directory}: {e}")

    def create_directory(self, directory: str) -> bool:
        """Create directory - simplified."""
        try:
            os.makedirs(directory, exist_ok=True)
            self._record_operation("create_dir", directory)
            return True
        except Exception as e:
            raise Exception(f"Failed to create directory {directory}: {e}")

    def get_file_size(self, file_path: str) -> int:
        """Get file size - simplified."""
        try:
            return os.path.getsize(file_path)
        except Exception as e:
            raise Exception(f"Failed to get file size {file_path}: {e}")

    def _record_operation(self, operation: str, file_path: str) -> None:
        """Record operation for tracking."""
        self.operations_count += 1
        self.last_operation = datetime.now()

    def get_status(self) -> Dict[str, Any]:
        """Get file manager status."""
        return {
            "operations_count": self.operations_count,
            "last_operation": (
                self.last_operation.isoformat() if self.last_operation else None
            ),
            "status": "active",
        }

    def cleanup(self) -> None:
        """Cleanup file manager resources."""
        try:
            self.operations_count = 0
            self.last_operation = None
        except Exception:
            pass


# Global instance for backward compatibility
_global_file_manager = None


def create_file_manager() -> FileManager:
    """Create a file manager instance."""
    return FileManager()


def get_file_manager() -> FileManager:
    """Get global file manager instance."""
    global _global_file_manager

    if _global_file_manager is None:
        _global_file_manager = FileManager()

    return _global_file_manager
