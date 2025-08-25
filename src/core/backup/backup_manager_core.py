from __future__ import annotations

from typing import Any, Callable, Dict, List

from .backup_recovery import BackupRecovery
from .backup_storage import BackupStorage


class BackupManagerCore:
    """Core backup management operations."""

    def __init__(self, storage: BackupStorage, recovery: BackupRecovery) -> None:
        self.storage = storage
        self.recovery = recovery

    def create_backup(self, data: Dict[str, Any], name: str) -> None:
        """Create a named backup."""
        self.storage.save_backup(data, name)

    def list_backups(self) -> List[str]:
        """Return all available backups."""
        return self.storage.list_backups()

    def restore_backup(self, name: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Restore backup *name* using the provided ``handler``."""
        self.recovery.restore(name, handler)
