from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class BackupStorage:
    """Handle persistence of backup data on disk."""

    def __init__(self, backup_dir: str | Path = "data/backups") -> None:
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def save_backup(self, data: Dict[str, Any], name: str) -> Path:
        """Persist *data* as JSON under ``name``.

        Returns the path to the created backup file.
        """
        path = self.backup_dir / f"{name}.json"
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, sort_keys=True)
        return path

    def load_backup(self, name: str) -> Dict[str, Any]:
        """Load backup ``name`` and return its data."""
        path = self.backup_dir / f"{name}.json"
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def list_backups(self) -> List[str]:
        """Return available backup names."""
        return [p.stem for p in self.backup_dir.glob("*.json")]
