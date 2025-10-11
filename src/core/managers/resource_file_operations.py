"""
Resource File Operations - Helper Module
========================================

Handles file operations for CoreResourceManager.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from __future__ import annotations

import os
import shutil
from typing import Any

from .contracts import ManagerContext, ManagerResult


class FileOperations:
    """Handles file operations for resource manager."""

    def __init__(self):
        """Initialize file operations handler."""
        self.operations_count = 0

    def handle_operation(
        self, context: ManagerContext, payload: dict[str, Any]
    ) -> ManagerResult:
        """Handle file operations."""
        operation = payload.get("file_operation", "")
        file_path = payload.get("file_path", "")

        try:
            if operation == "read":
                return self._read_operation(file_path)
            elif operation == "write":
                return self._write_operation(file_path, payload.get("content", ""))
            elif operation == "copy":
                return self._copy_operation(file_path, payload.get("destination", ""))
            elif operation == "move":
                return self._move_operation(file_path, payload.get("destination", ""))
            elif operation == "delete":
                return self._delete_operation(file_path)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown file operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _read_operation(self, file_path: str) -> ManagerResult:
        """Read file operation."""
        content = self.read_file(file_path)
        self.operations_count += 1
        return ManagerResult(
            success=True,
            data={"content": content, "path": file_path},
            metrics={"file_size": len(content)},
        )

    def _write_operation(self, file_path: str, content: str) -> ManagerResult:
        """Write file operation."""
        self.write_file(file_path, content)
        self.operations_count += 1
        return ManagerResult(
            success=True,
            data={"path": file_path, "written": True},
            metrics={"file_size": len(content)},
        )

    def _copy_operation(self, source: str, destination: str) -> ManagerResult:
        """Copy file operation."""
        shutil.copy2(source, destination)
        self.operations_count += 1
        return ManagerResult(
            success=True,
            data={"source": source, "destination": destination, "copied": True},
            metrics={},
        )

    def _move_operation(self, source: str, destination: str) -> ManagerResult:
        """Move file operation."""
        shutil.move(source, destination)
        self.operations_count += 1
        return ManagerResult(
            success=True,
            data={"source": source, "destination": destination, "moved": True},
            metrics={},
        )

    def _delete_operation(self, file_path: str) -> ManagerResult:
        """Delete file operation."""
        os.remove(file_path)
        self.operations_count += 1
        return ManagerResult(
            success=True, data={"path": file_path, "deleted": True}, metrics={}
        )

    def create_file(
        self, context: ManagerContext, file_path: str, content: str
    ) -> ManagerResult:
        """Create a file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            self.write_file(file_path, content)
            self.operations_count += 1
            return ManagerResult(
                success=True,
                data={"type": "file", "path": file_path, "created": True},
                metrics={"file_size": len(content)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def create_directory(self, context: ManagerContext, dir_path: str) -> ManagerResult:
        """Create a directory."""
        try:
            os.makedirs(dir_path, exist_ok=True)
            self.operations_count += 1
            return ManagerResult(
                success=True,
                data={"type": "directory", "path": dir_path, "created": True},
                metrics={},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    @staticmethod
    def read_file(file_path: str) -> str:
        """Read file content."""
        with open(file_path, encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def write_file(file_path: str, content: str) -> None:
        """Write file content."""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

