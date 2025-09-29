#!/usr/bin/env python3
"""
Backup Manager
==============

Manages database backups for migration operations.
"""

import hashlib
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class BackupManager:
    """Manages database backups for migration operations."""

    def __init__(self, db_path: Path, backup_dir: Path):
        """Initialize backup manager."""
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def create_migration_backup(self) -> dict[str, Any]:
        """Create a backup before migration."""
        try:
            if not self.db_path.exists():
                logger.info("No existing database found, skipping backup")
                return {"success": True, "message": "No existing database to backup"}

            # Create timestamped backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_filename = f"agent_system_backup_{timestamp}.db"
            backup_path = self.backup_dir / backup_filename

            # Copy database file
            shutil.copy2(self.db_path, backup_path)

            # Calculate checksum
            checksum = self._calculate_checksum(backup_path)

            logger.info(f"Backup created: {backup_path}")
            logger.info(f"Backup checksum: {checksum}")

            return {
                "success": True,
                "backup_path": str(backup_path),
                "checksum": checksum,
                "size_bytes": backup_path.stat().st_size,
            }

        except Exception as e:
            logger.error(f"Backup creation failed: {e}")
            return {"success": False, "error": str(e)}

    def restore_from_backup(self, backup_path: str) -> dict[str, Any]:
        """Restore database from backup."""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                return {"success": False, "error": "Backup file not found"}

            # Create backup of current database if it exists
            if self.db_path.exists():
                current_backup = self.db_path.with_suffix(".db.current_backup")
                shutil.copy2(self.db_path, current_backup)

            # Restore from backup
            shutil.copy2(backup_file, self.db_path)

            logger.info(f"Database restored from: {backup_path}")

            return {"success": True, "restored_from": backup_path}

        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return {"success": False, "error": str(e)}

    def list_backups(self) -> dict[str, Any]:
        """List available backups."""
        try:
            backups = []
            for backup_file in self.backup_dir.glob("*.db"):
                if backup_file.is_file():
                    backups.append(
                        {
                            "filename": backup_file.name,
                            "path": str(backup_file),
                            "size_bytes": backup_file.stat().st_size,
                            "created": datetime.fromtimestamp(
                                backup_file.stat().st_ctime
                            ).isoformat(),
                        }
                    )

            return {
                "success": True,
                # SECURITY: Key placeholder - replace with environment variable
            }

        except Exception as e:
            logger.error(f"Failed to list backups: {e}")
            return {"success": False, "error": str(e)}

    def _calculate_checksum(self, file_path: Path) -> str:
        """Calculate SHA256 checksum of file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
