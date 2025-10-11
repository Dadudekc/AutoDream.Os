#!/usr/bin/env python3
"""
Unified File Utilities - V2 Compliance Module
===========================================

Main interface for file operations.
Refactored to V2 compliance by splitting into modules.

Author: Agent-3 (DevOps Specialist), Refactored by Agent-5
License: MIT
"""

import logging
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .file_operations.directory_operations import DirectoryOperations
from .file_operations.file_metadata import FileMetadataOperations, FileOperation
from .file_operations.file_serialization import DataSerializationOperations

logger = logging.getLogger(__name__)


class BackupOperations:
    """Handles backup and restore operations."""

    @staticmethod
    def create_backup(file_path: str, backup_suffix: str = ".backup") -> str | None:
        """Create a backup of a file."""
        try:
            if not FileMetadataOperations.file_exists(file_path):
                return None
            backup_path = f"{file_path}{backup_suffix}"
            shutil.copy2(file_path, backup_path)
            return backup_path
        except Exception:
            return None

    @staticmethod
    def restore_from_backup(backup_path: str, target_path: str) -> bool:
        """Restore a file from backup."""
        try:
            if not FileMetadataOperations.file_exists(backup_path):
                return False
            if FileMetadataOperations.file_exists(target_path):
                BackupOperations.create_backup(target_path, ".pre_restore_backup")
            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    @staticmethod
    def copy_file(source: str, destination: str) -> bool:
        """Copy file from source to destination."""
        try:
            DataSerializationOperations.ensure_directory(os.path.dirname(destination))
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False

    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """Safely delete a file with backup."""
        try:
            if not FileMetadataOperations.file_exists(file_path):
                return True
            backup_path = BackupOperations.create_backup(file_path, ".pre_delete_backup")
            if not backup_path:
                return False
            Path(file_path).unlink()
            return True
        except Exception:
            return False


class BackupManager:
    """Simple backup manager for agent state and configuration."""

    def __init__(self, root: str, dest: str):
        """Initialize backup manager."""
        self.root = Path(root)
        self.dest = Path(dest)
        self.dest.mkdir(parents=True, exist_ok=True)

    def create_backup(self, agents: list[str] | None = None) -> str:
        """Create backup of agent state."""
        if not self.root.exists():
            raise FileNotFoundError(f"Root directory {self.root} does not exist")

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = self.dest / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)

        if agents:
            for agent in agents:
                agent_dir = self.root / agent
                if agent_dir.exists():
                    shutil.copytree(agent_dir, backup_dir / agent, dirs_exist_ok=True)
        else:
            if self.root.is_file():
                shutil.copy2(self.root, backup_dir / self.root.name)
            else:
                shutil.copytree(self.root, backup_dir / self.root.name, dirs_exist_ok=True)

        return str(backup_dir)

    def list_backups(self) -> list[str]:
        """List all available backups."""
        if not self.dest.exists():
            return []
        return [str(p) for p in self.dest.iterdir() if p.is_dir()]

    def restore_backup(self, backup_path: str) -> bool:
        """Restore from backup."""
        backup = Path(backup_path)
        if not backup.exists():
            return False

        try:
            for item in backup.iterdir():
                dest_path = self.root / item.name
                if item.is_file():
                    shutil.copy2(item, dest_path)
                else:
                    shutil.copytree(item, dest_path, dirs_exist_ok=True)
            return True
        except Exception:
            return False

    def cleanup_old_backups(self, keep_count: int = 5) -> int:
        """Clean up old backups, keeping only the most recent ones."""
        backups = sorted(
            [p for p in self.dest.iterdir() if p.is_dir()],
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        if len(backups) <= keep_count:
            return 0

        deleted_count = 0
        for backup in backups[keep_count:]:
            try:
                shutil.rmtree(backup)
                deleted_count += 1
            except Exception:
                pass

        return deleted_count


@dataclass
class FileValidationResult:
    """Result of file validation."""

    path: str
    exists: bool
    is_file: bool
    is_directory: bool
    readable: bool
    writable: bool
    size_bytes: int
    modified_time: datetime | None
    errors: list[str]


class FileValidator:
    """Handles comprehensive file validation."""

    @staticmethod
    def validate_file_path(file_path: str) -> FileValidationResult:
        """Validate file path and return detailed information."""
        path = Path(file_path)
        errors = []

        return FileValidationResult(
            path=file_path,
            exists=path.exists(),
            is_file=path.is_file() if path.exists() else False,
            is_directory=path.is_dir() if path.exists() else False,
            readable=FileMetadataOperations.is_file_readable(file_path) if path.exists() else False,
            writable=FileMetadataOperations.is_file_writable(file_path) if path.exists() else False,
            size_bytes=FileMetadataOperations.get_file_size(file_path) or 0,
            modified_time=FileMetadataOperations.get_file_modified_time(file_path),
            errors=errors,
        )


class UnifiedFileScanner:
    """Unified file scanner with filtering and pattern matching."""

    def __init__(self, root_directory: str):
        """Initialize file scanner."""
        self.root = Path(root_directory)
        self.scanned_files: set[str] = set()

    def scan_directory(
        self, extensions: list[str] | None = None, exclude_patterns: list[str] | None = None
    ) -> list[str]:
        """Scan directory for files."""
        files = []
        exclude_patterns = exclude_patterns or []

        if not self.root.exists():
            return files

        for file_path in self.root.rglob("*"):
            if not file_path.is_file():
                continue

            if any(pattern in str(file_path) for pattern in exclude_patterns):
                continue

            if extensions and file_path.suffix.lower() not in extensions:
                continue

            files.append(str(file_path))
            self.scanned_files.add(str(file_path))

        return files

    def get_scanned_files(self) -> set[str]:
        """Get set of scanned files."""
        return self.scanned_files.copy()

    def reset_scan(self) -> None:
        """Reset scanned files."""
        self.scanned_files.clear()


class UnifiedFileUtils:
    """Main unified file utilities interface."""

    def __init__(self):
        """Initialize unified file utilities."""
        self.metadata = FileMetadataOperations()
        self.serialization = DataSerializationOperations()
        self.directory = DirectoryOperations()
        self.backup = BackupOperations()
        self.validator = FileValidator()

    # Metadata operations
    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        return self.metadata.file_exists(file_path)

    def get_file_size(self, file_path: str) -> int | None:
        """Get file size."""
        return self.metadata.get_file_size(file_path)

    def get_file_hash(self, file_path: str) -> str | None:
        """Get file hash."""
        return self.metadata.get_file_hash(file_path)

    # Serialization operations
    def read_json(self, file_path: str) -> dict[str, Any] | None:
        """Read JSON file."""
        return self.serialization.read_json(file_path)

    def write_json(self, file_path: str, data: dict[str, Any]) -> bool:
        """Write JSON file."""
        return self.serialization.write_json(file_path, data)

    def read_yaml(self, file_path: str) -> dict[str, Any] | None:
        """Read YAML file."""
        return self.serialization.read_yaml(file_path)

    def write_yaml(self, file_path: str, data: dict[str, Any]) -> bool:
        """Write YAML file."""
        return self.serialization.write_yaml(file_path, data)

    # Directory operations
    def list_files(self, directory: str, pattern: str = "*") -> list[str]:
        """List files in directory."""
        return self.directory.list_files(directory, pattern)

    def get_directory_size(self, directory_path: str) -> int:
        """Get directory size."""
        return self.directory.get_directory_size(directory_path)

    # Backup operations
    def create_backup(self, file_path: str) -> str | None:
        """Create file backup."""
        return self.backup.create_backup(file_path)

    def copy_file(self, source: str, destination: str) -> bool:
        """Copy file."""
        return self.backup.copy_file(source, destination)

    # Validation operations
    def validate_file(self, file_path: str) -> FileValidationResult:
        """Validate file."""
        return self.validator.validate_file_path(file_path)


def create_backup_manager(root: str, dest: str) -> BackupManager:
    """Factory function to create backup manager."""
    return BackupManager(root, dest)


# Backward compatibility exports
__all__ = [
    "FileOperation",
    "FileMetadataOperations",
    "DataSerializationOperations",
    "DirectoryOperations",
    "BackupOperations",
    "BackupManager",
    "FileValidationResult",
    "FileValidator",
    "UnifiedFileScanner",
    "UnifiedFileUtils",
    "create_backup_manager",
]
