#!/usr/bin/env python3
"""
Backup Operations Module
========================

Handles backup, restore, and file copy operations.
Part of the unified file utilities system.

Author: Agent-8 (Operations & Support Specialist)
License: MIT
"""

import logging
import os
import shutil
from datetime import datetime
from pathlib import Path

from .file_metadata import FileMetadataOperations
from .file_serialization import DataSerializationOperations

logger = logging.getLogger(__name__)


class BackupOperations:
    """Handles backup and restore operations for individual files."""

    @staticmethod
    def create_backup(file_path: str, backup_suffix: str = ".backup") -> str | None:
        """
        Create a backup of a file.

        Args:
            file_path: Path to the file to backup
            backup_suffix: Suffix to add to backup file (default: .backup)

        Returns:
            str: Path to backup file if successful, None otherwise
        """
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
        """
        Restore a file from backup.

        Args:
            backup_path: Path to the backup file
            target_path: Path where the file should be restored

        Returns:
            bool: True if restore successful, False otherwise
        """
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
        """
        Copy file from source to destination.

        Args:
            source: Source file path
            destination: Destination file path

        Returns:
            bool: True if copy successful, False otherwise
        """
        try:
            DataSerializationOperations.ensure_directory(os.path.dirname(destination))
            shutil.copy2(source, destination)
            return True
        except Exception as e:
            logger.error(f"Failed to copy file from {source} to {destination}: {e}")
            return False

    @staticmethod
    def safe_delete_file(file_path: str) -> bool:
        """
        Safely delete a file with automatic backup.

        Args:
            file_path: Path to the file to delete

        Returns:
            bool: True if deletion successful, False otherwise
        """
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
    """
    Manages backups for agent state and configuration.

    Provides functionality for creating, listing, restoring, and cleaning up
    backups of agent workspaces and configuration files.
    """

    def __init__(self, root: str, dest: str):
        """
        Initialize backup manager.

        Args:
            root: Root directory to backup
            dest: Destination directory for backups
        """
        self.root = Path(root)
        self.dest = Path(dest)
        self.dest.mkdir(parents=True, exist_ok=True)

    def create_backup(self, agents: list[str] | None = None) -> str:
        """
        Create backup of agent state.

        Args:
            agents: List of specific agents to backup (None = backup all)

        Returns:
            str: Path to created backup directory

        Raises:
            FileNotFoundError: If root directory doesn't exist
        """
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
        """
        List all available backups.

        Returns:
            list[str]: List of backup directory paths
        """
        if not self.dest.exists():
            return []
        return [str(p) for p in self.dest.iterdir() if p.is_dir()]

    def restore_backup(self, backup_path: str) -> bool:
        """
        Restore from backup.

        Args:
            backup_path: Path to backup directory to restore from

        Returns:
            bool: True if restore successful, False otherwise
        """
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
        """
        Clean up old backups, keeping only the most recent ones.

        Args:
            keep_count: Number of recent backups to keep (default: 5)

        Returns:
            int: Number of backups deleted
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


def create_backup_manager(root: str, dest: str) -> BackupManager:
    """
    Factory function to create backup manager.

    Args:
        root: Root directory to backup
        dest: Destination directory for backups

    Returns:
        BackupManager: Configured backup manager instance
    """
    return BackupManager(root, dest)


__all__ = [
    "BackupOperations",
    "BackupManager",
    "create_backup_manager",
]
