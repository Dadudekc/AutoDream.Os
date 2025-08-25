from __future__ import annotations

from typing import Any, Callable, Dict

from .backup_storage import BackupStorage


class BackupRecovery:
    """Load backups and hand data back to consumers."""

    def __init__(self, storage: BackupStorage) -> None:
        self.storage = storage

    def restore(self, name: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        """Load backup *name* and pass to ``handler`` for processing."""
        data = self.storage.load_backup(name)
        handler(data)
