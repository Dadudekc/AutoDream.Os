#!/usr/bin/env python3
"""
File Backup Operations Module - V2 Compliant
===========================================

File backup functionality extracted from consolidated_file_operations.py
for V2 compliance (≤400 lines).

Provides:
- File and directory backup operations
- Backup management and restoration
- Backup validation and verification
- Incremental and full backup support

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
import shutil
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class BackupResult:
    """Result of backup operation."""

    success: bool
    backup_path: Path | None
    files_backed_up: int
    total_size: int
    duration_seconds: float
    errors: list[str] = field(default_factory=list)


@dataclass
class ScanResult:
    """Result of file scanning operation."""

    directory: Path
    files_found: list[Path]
    total_size: int
    scan_duration: float
    filters_applied: dict[str, Any] = field(default_factory=dict)


class FileBackupOperations:
    """Handles file backup and restore operations."""

    def __init__(self):
        self.backup_history = []
        self.default_backup_dir = Path("backups")

    def create_backup(
        self,
        source: Path,
        backup_dir: Path = None,
        backup_name: str = None,
        incremental: bool = False,
    ) -> BackupResult:
        """Create a backup of a file or directory."""
        start_time = time.time()

        try:
            if backup_dir is None:
                backup_dir = self.default_backup_dir

            if backup_name is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                backup_name = f"{source.name}_{timestamp}"

            backup_path = backup_dir / backup_name

            # Ensure backup directory exists
            backup_dir.mkdir(parents=True, exist_ok=True)

            files_backed_up = 0
            total_size = 0
            errors = []

            if source.is_file():
                # Backup single file
                result = self._backup_file(source, backup_path)
                files_backed_up = 1 if result else 0
                total_size = source.stat().st_size if result else 0
                if not result:
                    errors.append(f"Failed to backup file {source}")

            elif source.is_dir():
                # Backup directory
                if incremental:
                    result = self._backup_directory_incremental(source, backup_path)
                else:
                    result = self._backup_directory_full(source, backup_path)

                if result:
                    files_backed_up, total_size = self._count_backup_contents(backup_path)
                else:
                    errors.append(f"Failed to backup directory {source}")
            else:
                errors.append(f"Source path {source} does not exist")
                result = False

            duration = time.time() - start_time

            backup_result = BackupResult(
                success=result,
                backup_path=backup_path if result else None,
                files_backed_up=files_backed_up,
                total_size=total_size,
                duration_seconds=duration,
                errors=errors,
            )

            if result:
                self.backup_history.append(backup_result)
                logger.info(
                    f"Backup completed: {backup_path} ({files_backed_up} files, {total_size} bytes)"
                )
            else:
                logger.error(f"Backup failed: {errors}")

            return backup_result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Backup operation failed: {e}")
            return BackupResult(
                success=False,
                backup_path=None,
                files_backed_up=0,
                total_size=0,
                duration_seconds=duration,
                errors=[str(e)],
            )

    def _backup_file(self, source_file: Path, backup_path: Path) -> bool:
        """Backup a single file."""
        try:
            shutil.copy2(source_file, backup_path)
            return True
        except Exception as e:
            logger.error(f"Failed to backup file {source_file}: {e}")
            return False

    def _backup_directory_full(self, source_dir: Path, backup_path: Path) -> bool:
        """Create a full directory backup."""
        try:
            shutil.copytree(source_dir, backup_path, dirs_exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"Failed to backup directory {source_dir}: {e}")
            return False

    def _backup_directory_incremental(self, source_dir: Path, backup_path: Path) -> bool:
        """Create an incremental directory backup."""
        try:
            # For incremental backup, we'll use rsync-like behavior
            # Copy only files that are newer or don't exist in backup
            backup_path.mkdir(parents=True, exist_ok=True)

            for item in source_dir.rglob("*"):
                if item.is_file():
                    relative_path = item.relative_to(source_dir)
                    backup_item = backup_path / relative_path

                    # Create parent directories if needed
                    backup_item.parent.mkdir(parents=True, exist_ok=True)

                    # Copy if file doesn't exist in backup or is newer
                    if (
                        not backup_item.exists()
                        or item.stat().st_mtime > backup_item.stat().st_mtime
                    ):
                        shutil.copy2(item, backup_item)

            return True
        except Exception as e:
            logger.error(f"Failed to create incremental backup {source_dir}: {e}")
            return False

    def _count_backup_contents(self, backup_path: Path) -> tuple[int, int]:
        """Count files and total size in backup."""
        try:
            files_count = 0
            total_size = 0

            for item in backup_path.rglob("*"):
                if item.is_file():
                    files_count += 1
                    total_size += item.stat().st_size

            return files_count, total_size
        except Exception as e:
            logger.error(f"Failed to count backup contents {backup_path}: {e}")
            return 0, 0

    def restore_backup(
        self, backup_path: Path, restore_path: Path, overwrite: bool = False
    ) -> bool:
        """Restore a backup to a target location."""
        try:
            if not backup_path.exists():
                logger.error(f"Backup path {backup_path} does not exist")
                return False

            if restore_path.exists() and not overwrite:
                logger.error(f"Restore path {restore_path} already exists and overwrite is False")
                return False

            if backup_path.is_file():
                # Restore single file
                if restore_path.exists() and overwrite:
                    restore_path.unlink()
                shutil.copy2(backup_path, restore_path)
            else:
                # Restore directory
                if restore_path.exists() and overwrite:
                    shutil.rmtree(restore_path)
                shutil.copytree(backup_path, restore_path)

            logger.info(f"Successfully restored backup {backup_path} to {restore_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to restore backup {backup_path}: {e}")
            return False

    def list_backups(self, backup_dir: Path = None) -> list[Path]:
        """List all available backups."""
        try:
            if backup_dir is None:
                backup_dir = self.default_backup_dir

            if not backup_dir.exists():
                return []

            backups = []
            for item in backup_dir.iterdir():
                if item.is_dir() or item.is_file():
                    backups.append(item)

            # Sort by modification time (newest first)
            backups.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            return backups

        except Exception as e:
            logger.error(f"Failed to list backups in {backup_dir}: {e}")
            return []

    def delete_backup(self, backup_path: Path) -> bool:
        """Delete a backup."""
        try:
            if backup_path.is_file():
                backup_path.unlink()
            else:
                shutil.rmtree(backup_path)

            logger.info(f"Successfully deleted backup {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete backup {backup_path}: {e}")
            return False

    def cleanup_old_backups(self, backup_dir: Path = None, keep_count: int = 5) -> int:
        """Clean up old backups, keeping only the most recent ones."""
        try:
            if backup_dir is None:
                backup_dir = self.default_backup_dir

            backups = self.list_backups(backup_dir)

            if len(backups) <= keep_count:
                return 0

            deleted_count = 0
            for backup in backups[keep_count:]:
                if self.delete_backup(backup):
                    deleted_count += 1

            logger.info(f"Cleaned up {deleted_count} old backups")
            return deleted_count

        except Exception as e:
            logger.error(f"Failed to cleanup old backups: {e}")
            return 0

    def verify_backup(self, backup_path: Path) -> bool:
        """Verify backup integrity."""
        try:
            if not backup_path.exists():
                return False

            # Basic verification - check if we can read the backup
            if backup_path.is_file():
                with open(backup_path, "rb") as f:
                    f.read(1)  # Try to read at least 1 byte
            else:
                # For directories, check if we can list contents
                list(backup_path.iterdir())

            logger.info(f"Backup verification successful: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"Backup verification failed {backup_path}: {e}")
            return False

    def get_backup_info(self, backup_path: Path) -> dict[str, Any]:
        """Get information about a backup."""
        try:
            if not backup_path.exists():
                return {"error": "Backup does not exist"}

            stat = backup_path.stat()
            files_count, total_size = self._count_backup_contents(backup_path)

            info = {
                "path": str(backup_path),
                "type": "file" if backup_path.is_file() else "directory",
                "size": stat.st_size,
                "files_count": files_count,
                "total_size": total_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "permissions": oct(stat.st_mode)[-3:],
            }

            return info

        except Exception as e:
            logger.error(f"Failed to get backup info {backup_path}: {e}")
            return {"error": str(e)}

    def get_backup_history(self) -> list[BackupResult]:
        """Get backup operation history."""
        return self.backup_history.copy()

    def clear_backup_history(self):
        """Clear backup operation history."""
        self.backup_history.clear()
        logger.info("Backup history cleared")


if __name__ == "__main__":
    # Example usage
    backup_ops = FileBackupOperations()

    # Test with current directory
    current_dir = Path(".")
    backup_dir = Path("test_backups")

    # Create backup
    result = backup_ops.create_backup(current_dir, backup_dir, "test_backup")
    print(f"Backup result: {result.success}")
    print(f"Files backed up: {result.files_backed_up}")
    print(f"Total size: {result.total_size} bytes")
    print(f"Duration: {result.duration_seconds:.2f} seconds")

    # List backups
    backups = backup_ops.list_backups(backup_dir)
    print(f"Available backups: {len(backups)}")

    # Get backup info
    if backups:
        info = backup_ops.get_backup_info(backups[0])
        print(f"Backup info: {info}")

    # Cleanup
    if backup_dir.exists():
        shutil.rmtree(backup_dir)

