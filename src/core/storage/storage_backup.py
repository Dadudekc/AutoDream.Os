#!/usr/bin/env python3
"""
Storage Backup - Agent Cellphone V2
===================================

Backup and recovery functionality for persistent storage.
Follows Single Responsibility Principle with 150 LOC limit.
"""

import time
import json
import hashlib
import threading
import shutil
from typing import Dict, List, Optional, Any
import logging
from pathlib import Path
from datetime import datetime, timedelta

from .storage_types import BackupStrategy, StorageMetadata


class StorageBackupManager:
    """
    Manages backup and recovery operations

    Responsibilities:
    - Create and manage data backups
    - Implement recovery strategies
    - Maintain backup retention policies
    """

    def __init__(self, backup_path: Path, retention_days: int = 30):
        self.logger = logging.getLogger(f"{__name__}.StorageBackupManager")
        self.backup_path = backup_path
        self.retention_days = retention_days
        self.backup_history: List[Dict[str, Any]] = []

        # Ensure backup directory exists
        self.backup_path.mkdir(parents=True, exist_ok=True)

        # Load backup history
        self._load_backup_history()

    def create_backup(self, data_path: Path, backup_name: str = None) -> Optional[str]:
        """Create a backup of the data directory"""
        try:
            if not backup_name:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"backup_{timestamp}"
            backup_dir = self.backup_path / backup_name
            if backup_dir.exists():
                self.logger.warning(f"Backup directory already exists: {backup_dir}")
                return None
            shutil.copytree(data_path, backup_dir)
            backup_info = {
                "backup_name": backup_name,
                "timestamp": time.time(),
                "source_path": str(data_path),
                "backup_path": str(backup_dir),
                "size": self._calculate_directory_size(backup_dir),
                "file_count": self._count_files(backup_dir),
            }
            metadata_file = backup_dir / "backup_metadata.json"
            metadata_file.write_text(json.dumps(backup_info, indent=2))
            self.backup_history.append(backup_info)
            self._save_backup_history()
            self.logger.info(f"Backup created successfully: {backup_name}")
            return backup_name
        except Exception as e:
            self.logger.error(f"Failed to create backup: {e}")
            return None

    def restore_backup(self, backup_name: str, restore_path: Path) -> bool:
        """Restore data from a backup"""
        try:
            backup_dir = self.backup_path / backup_name

            if not backup_dir.exists():
                self.logger.error(f"Backup not found: {backup_name}")
                return False

            # Verify backup integrity
            metadata_file = backup_dir / "backup_metadata.json"
            if not metadata_file.exists():
                self.logger.error(f"Backup metadata not found: {backup_name}")
                return False

            # Read backup metadata
            backup_info = json.loads(metadata_file.read_text())

            # Clear restore path
            if restore_path.exists():
                shutil.rmtree(restore_path)

            # Restore from backup
            shutil.copytree(backup_dir, restore_path, dirs_exist_ok=True)

            # Remove backup metadata from restored data
            restored_metadata = restore_path / "backup_metadata.json"
            if restored_metadata.exists():
                restored_metadata.unlink()

            self.logger.info(
                f"Backup restored successfully: {backup_name} -> {restore_path}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Failed to restore backup {backup_name}: {e}")
            return False

    def list_backups(self) -> List[Dict[str, Any]]:
        """List all available backups"""
        return sorted(self.backup_history, key=lambda x: x["timestamp"], reverse=True)

    def get_backup_info(self, backup_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific backup"""
        for backup in self.backup_history:
            if backup["backup_name"] == backup_name:
                return backup
        return None

    def delete_backup(self, backup_name: str) -> bool:
        """Delete a backup"""
        try:
            backup_dir = self.backup_path / backup_name

            if not backup_dir.exists():
                self.logger.warning(f"Backup directory not found: {backup_name}")
                return False

            # Remove backup directory
            shutil.rmtree(backup_dir)

            # Remove from history
            self.backup_history = [
                b for b in self.backup_history if b["backup_name"] != backup_name
            ]
            self._save_backup_history()

            self.logger.info(f"Backup deleted successfully: {backup_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to delete backup {backup_name}: {e}")
            return False

    def cleanup_old_backups(self) -> int:
        """Remove backups older than retention period"""
        try:
            cutoff_time = time.time() - (self.retention_days * 24 * 3600)
            old_backups = [
                b for b in self.backup_history if b["timestamp"] < cutoff_time
            ]

            deleted_count = 0
            for backup in old_backups:
                if self.delete_backup(backup["backup_name"]):
                    deleted_count += 1

            self.logger.info(f"Cleaned up {deleted_count} old backups")
            return deleted_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup old backups: {e}")
            return 0

    def _calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory"""
        total_size = 0
        try:
            for file_path in directory.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception as e:
            self.logger.warning(f"Error calculating directory size: {e}")
        return total_size

    def _count_files(self, directory: Path) -> int:
        """Count total files in directory"""
        try:
            return len([f for f in directory.rglob("*") if f.is_file()])
        except Exception as e:
            self.logger.warning(f"Error counting files: {e}")
            return 0

    def _load_backup_history(self):
        """Load backup history from file"""
        try:
            history_file = self.backup_path / "backup_history.json"
            if history_file.exists():
                self.backup_history = json.loads(history_file.read_text())
        except Exception as e:
            self.logger.warning(f"Failed to load backup history: {e}")

    def _save_backup_history(self):
        """Save backup history to file"""
        try:
            history_file = self.backup_path / "backup_history.json"
            history_file.write_text(json.dumps(self.backup_history, indent=2))
        except Exception as e:
            self.logger.error(f"Failed to save backup history: {e}")
