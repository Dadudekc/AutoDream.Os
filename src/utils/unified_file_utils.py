#!/usr/bin/env python3
"""
Unified File Utilities - V2 Compliance Module
===========================================

Consolidated file management utilities following SOLID principles.
Combines functionality from:
- file_utils.py (JSON/YAML, metadata, directory operations)
- file_scanner.py (file scanning operations)
- backup.py (backup management)

SOLID Implementation:
- SRP: Each utility class has single responsibility
- OCP: Extensible operation system
- DIP: Dependencies injected via constructor

Author: Agent-3 (DevOps Specialist)
License: MIT
"""

import hashlib
import json
import logging
import os
import shutil
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


class FileOperation(ABC):
    """Abstract base class for file operations."""

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute the file operation."""
        pass


class FileMetadataOperations:
    """Handles file metadata operations."""

    @staticmethod
    def file_exists(file_path: str) -> bool:
        """Check if a file exists."""
        return Path(file_path).exists()

    @staticmethod
    def is_file_readable(file_path: str) -> bool:
        """Check if a file is readable."""
        try:
            with open(file_path, encoding="utf-8") as f:
                f.read(1)
            return True
        except Exception:
            return False

    @staticmethod
    def is_file_writable(file_path: str) -> bool:
        """Check if a file is writable."""
        try:
            with open(file_path, "a", encoding="utf-8") as f:
                pass
            return True
        except Exception:
            return False

    @staticmethod
    def get_file_size(file_path: str) -> int | None:
        """Get file size in bytes."""
        try:
            return Path(file_path).stat().st_size
        except Exception as e:
            logger.error(f"Failed to get file size for {file_path}: {e}")
            return None

    @staticmethod
    def get_file_modified_time(file_path: str) -> datetime | None:
        """Get file last modified time."""
        try:
            timestamp = Path(file_path).stat().st_mtime
            return datetime.fromtimestamp(timestamp)
        except Exception:
            return None

    @staticmethod
    def get_file_hash(file_path: str) -> str | None:
        """Get SHA256 hash of file."""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Failed to get hash for {file_path}: {e}")
            return None

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        """Get file extension."""
        return Path(file_path).suffix.lower()

    @staticmethod
    def is_json_file(file_path: str) -> bool:
        """Check if file has JSON extension."""
        return FileMetadataOperations.get_file_extension(file_path) == ".json"


class DataSerializationOperations:
    """Handles data serialization operations (JSON/YAML)."""

    @staticmethod
    def ensure_directory(path: str) -> bool:
        """Ensure directory exists, create if not."""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to create directory {path}: {e}")
            return False

    @staticmethod
    def read_json(file_path: str) -> dict[str, Any] | None:
        """Read JSON file and return data."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"JSON file not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {e}")
            return None

    @staticmethod
    def write_json(file_path: str, data: dict[str, Any]) -> bool:
        """Write data to JSON file."""
        try:
            DataSerializationOperations.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Failed to write JSON {file_path}: {e}")
            return False

    @staticmethod
    def read_yaml(file_path: str) -> dict[str, Any] | None:
        """Read YAML file and return data."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to read YAML {file_path}: {e}")
            return None

    @staticmethod
    def write_yaml(file_path: str, data: dict[str, Any]) -> bool:
        """Write data to YAML file."""
        try:
            DataSerializationOperations.ensure_directory(os.path.dirname(file_path))
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
            return True
        except Exception as e:
            logger.error(f"Failed to write YAML {file_path}: {e}")
            return False


class DirectoryOperations:
    """Handles directory and file listing operations."""

    @staticmethod
    def list_files(directory: str, pattern: str = "*") -> list[str]:
        """List files in directory matching pattern."""
        try:
            path = Path(directory)
            if not path.exists() or not path.is_dir():
                return []
            return [str(f) for f in path.glob(pattern) if f.is_file()]
        except Exception as e:
            logger.error(f"Failed to list files in {directory}: {e}")
            return []

    @staticmethod
    def get_directory_size(directory_path: str) -> int:
        """Get total size of directory in bytes."""
        try:
            total = 0
            directory = Path(directory_path)
            if not directory.exists() or not directory.is_dir():
                return 0
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total += file_path.stat().st_size
            return total
        except Exception:
            return 0


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
                FileMetadataOperations.create_backup(target_path, ".pre_restore_backup")
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
        """Initialize backup manager.

        Args:
            root: Root directory to backup
            dest: Destination directory for backups
        """
        self.root = Path(root)
        self.dest = Path(dest)
        self.dest.mkdir(parents=True, exist_ok=True)

    def create_backup(self, agents: list[str] | None = None) -> str:
        """Create backup of agent state.

        Args:
            agents: List of specific agents to backup (None for all)

        Returns:
            Path to backup directory
        """
        if not self.root.exists():
            raise FileNotFoundError(f"Root directory {self.root} does not exist")

        # Create backup directory name with timestamp
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_dir = self.dest / f"backup_{timestamp}"
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Backup agent data
        if agents:
            # Backup specific agents
            for agent in agents:
                agent_dir = self.root / agent
                if agent_dir.exists():
                    shutil.copytree(agent_dir, backup_dir / agent, dirs_exist_ok=True)
        else:
            # Backup entire root directory
            if self.root.is_file():
                shutil.copy2(self.root, backup_dir / self.root.name)
            else:
                shutil.copytree(self.root, backup_dir / self.root.name, dirs_exist_ok=True)

        return str(backup_dir)

    def list_backups(self) -> list[str]:
        """List all available backups.

        Returns:
            List of backup directory paths
        """
        if not self.dest.exists():
            return []

        return [str(p) for p in self.dest.iterdir() if p.is_dir()]

    def restore_backup(self, backup_path: str) -> bool:
        """Restore from backup.

        Args:
            backup_path: Path to backup directory

        Returns:
            True if successful, False otherwise
        """
        backup = Path(backup_path)
        if not backup.exists():
            return False

        try:
            # Copy backup contents back to root
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
        """Clean up old backups, keeping only the most recent ones.

        Args:
            keep_count: Number of recent backups to keep

        Returns:
            Number of backups deleted
        """
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
        result = FileValidationResult(
            path=file_path,
            exists=False,
            is_file=False,
            is_directory=False,
            readable=False,
            writable=False,
            size_bytes=0,
            modified_time=None,
            errors=[],
        )

        try:
            path_obj = Path(file_path)
            result.exists = path_obj.exists()
            if result.exists:
                result.is_file = path_obj.is_file()
                result.is_directory = path_obj.is_dir()
                result.readable = FileMetadataOperations.is_file_readable(file_path)
                result.writable = FileMetadataOperations.is_file_writable(file_path)
                size = FileMetadataOperations.get_file_size(file_path)
                result.size_bytes = size or 0
                result.modified_time = FileMetadataOperations.get_file_modified_time(file_path)
        except Exception as e:
            result.errors.append(str(e))

        return result


class UnifiedFileScanner:
    """Unified file scanner combining scanning operations."""

    def __init__(self, skip_patterns: set[str] | None = None):
        """Initialize file scanner with skip patterns."""
        self.skip_patterns = skip_patterns or self._get_default_skip_patterns()

    def _get_default_skip_patterns(self) -> set[str]:
        """Get default patterns for files that should be skipped."""
        return {
            "__pycache__",
            ".git",
            "venv",
            "env",
            "node_modules",
            "*.pyc",
            "unified_file_utils.py",
        }

    def should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during scanning."""
        file_str = str(file_path)
        return any(pattern in file_str for pattern in self.skip_patterns)

    def scan_directory(self, root_dir: Path, pattern: str = "*.py") -> list[Path]:
        """Scan directory for files matching pattern."""
        matching_files = []
        for file_path in root_dir.rglob(pattern):
            if not self.should_skip_file(file_path):
                matching_files.append(file_path)
        return matching_files

    def get_directory_stats(self, root_dir: Path) -> dict[str, Any]:
        """Get comprehensive directory statistics."""
        stats = {
            "total_files": 0,
            "total_directories": 0,
            "total_size": 0,
            "file_types": {},
            "largest_files": [],
            "recently_modified": [],
        }

        for item in root_dir.rglob("*"):
            if item.is_file():
                stats["total_files"] += 1
                size = item.stat().st_size
                stats["total_size"] += size

                # Track file types
                ext = item.suffix.lower()
                if ext in stats["file_types"]:
                    stats["file_types"][ext] += 1
                else:
                    stats["file_types"][ext] = 1

                # Track largest files
                if len(stats["largest_files"]) < 10:
                    stats["largest_files"].append((str(item), size))
                else:
                    stats["largest_files"].sort(key=lambda x: x[1], reverse=True)
                    if size > stats["largest_files"][-1][1]:
                        stats["largest_files"][-1] = (str(item), size)

                # Track recently modified
                mtime = datetime.fromtimestamp(item.stat().st_mtime)
                if len(stats["recently_modified"]) < 10:
                    stats["recently_modified"].append((str(item), mtime))
                else:
                    stats["recently_modified"].sort(key=lambda x: x[1], reverse=True)
                    if mtime > stats["recently_modified"][-1][1]:
                        stats["recently_modified"][-1] = (str(item), mtime)

            elif item.is_dir():
                stats["total_directories"] += 1

        # Sort the lists
        stats["largest_files"].sort(key=lambda x: x[1], reverse=True)
        stats["recently_modified"].sort(key=lambda x: x[1], reverse=True)

        return stats


# Main unified interface class
class UnifiedFileUtils:
    """Main unified interface for all file utilities."""

    def __init__(self):
        """Initialize unified file utilities."""
        self.metadata = FileMetadataOperations()
        self.serialization = DataSerializationOperations()
        self.directories = DirectoryOperations()
        self.backup = BackupOperations()
        self.validator = FileValidator()
        self.scanner = UnifiedFileScanner()

    # Convenience methods that delegate to appropriate operation classes
    def file_exists(self, file_path: str) -> bool:
        return self.metadata.file_exists(file_path)

    def read_json(self, file_path: str) -> dict[str, Any] | None:
        return self.serialization.read_json(file_path)

    def write_json(self, file_path: str, data: dict[str, Any]) -> bool:
        return self.serialization.write_json(file_path, data)

    def read_yaml(self, file_path: str) -> dict[str, Any] | None:
        return self.serialization.read_yaml(file_path)

    def write_yaml(self, file_path: str, data: dict[str, Any]) -> bool:
        return self.serialization.write_yaml(file_path, data)

    def list_files(self, directory: str, pattern: str = "*") -> list[str]:
        return self.directories.list_files(directory, pattern)

    def copy_file(self, source: str, destination: str) -> bool:
        return self.backup.copy_file(source, destination)

    def create_backup(self, file_path: str, backup_suffix: str = ".backup") -> str | None:
        return self.backup.create_backup(file_path, backup_suffix)

    def validate_file(self, file_path: str) -> FileValidationResult:
        return self.validator.validate_file_path(file_path)

    def scan_directory(self, root_dir: Path, pattern: str = "*.py") -> list[Path]:
        return self.scanner.scan_directory(root_dir, pattern)

    def get_directory_stats(self, root_dir: Path) -> dict[str, Any]:
        return self.scanner.get_directory_stats(root_dir)


def create_backup_manager(root: str, dest: str) -> BackupManager:
    """Factory function to create backup manager."""
    return BackupManager(root, dest)


if __name__ == "__main__":
    # Example usage
    utils = UnifiedFileUtils()

    # Test basic operations
    test_file = "test.json"
    test_data = {"message": "Unified File Utils Test", "timestamp": datetime.now().isoformat()}

    success = utils.write_json(test_file, test_data)
    if success:
        read_data = utils.read_json(test_file)
        print(f"✅ JSON round-trip successful: {read_data}")

    # Clean up
    if utils.file_exists(test_file):
        utils.backup.safe_delete_file(test_file)

    print("🎉 Unified File Utils test complete!")
