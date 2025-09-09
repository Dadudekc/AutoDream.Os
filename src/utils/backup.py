#!/usr/bin/env python3
"""
Backup Utilities - V2 Compliant Module
=====================================

Simple backup management utilities.
V2 Compliance: < 200 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime


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

    def create_backup(self, agents: Optional[List[str]] = None) -> str:
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

    def list_backups(self) -> List[str]:
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
            reverse=True
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
