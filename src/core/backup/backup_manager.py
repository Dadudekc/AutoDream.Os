from __future__ import annotations

from typing import Any, Callable, Dict, List

from .backup_manager_core import BackupManagerCore
from .backup_recovery import BackupRecovery
from .backup_storage import BackupStorage


class BackupManager:
    """High-level orchestrator coordinating backup components."""

    def __init__(self, backup_dir: str | None = None) -> None:
        storage = BackupStorage(backup_dir or "data/backups")
        recovery = BackupRecovery(storage)
        self.core = BackupManagerCore(storage, recovery)

    def create_backup(self, data: Dict[str, Any], name: str) -> None:
        self.core.create_backup(data, name)

    def list_backups(self) -> List[str]:
        return self.core.list_backups()

    def restore_backup(self, name: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        self.core.restore_backup(name, handler)
