"""Low level persistence operations for persistent storage."""

import json
import sqlite3
from pathlib import Path
from typing import Any, Optional

from .persistent_storage_config import StoragePaths, StorageType


class PersistentStoragePersistence:
    """Handles reading and writing data to persistent storage."""

    def __init__(self, paths: StoragePaths, storage_type: StorageType):
        self.paths = paths
        self.storage_type = storage_type
        self.db_path = paths.base_path / "storage.db"
        if storage_type in (StorageType.DATABASE, StorageType.HYBRID):
            self._init_db()

    # ------------------------------------------------------------------
    # Database helpers
    def _init_db(self) -> None:
        self.conn = sqlite3.connect(str(self.db_path))
        cur = self.conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS data_entries (id TEXT PRIMARY KEY, data_type TEXT, content TEXT)"
        )
        self.conn.commit()

    def _store_db(self, data_id: str, data: Any, data_type: str) -> None:
        if not hasattr(self, "conn"):
            return
        cur = self.conn.cursor()
        cur.execute(
            "REPLACE INTO data_entries (id, data_type, content) VALUES (?, ?, ?)",
            (data_id, data_type, json.dumps(data)),
        )
        self.conn.commit()

    def _load_db(self, data_id: str) -> Optional[Any]:
        if not hasattr(self, "conn"):
            return None
        cur = self.conn.cursor()
        cur.execute("SELECT content FROM data_entries WHERE id = ?", (data_id,))
        row = cur.fetchone()
        return json.loads(row[0]) if row else None

    # ------------------------------------------------------------------
    # File helpers
    def _store_file(self, data_id: str, data: Any, data_type: str) -> None:
        target_dir = self.paths.data_path / data_type
        target_dir.mkdir(parents=True, exist_ok=True)
        with open(target_dir / f"{data_id}.json", "w", encoding="utf-8") as f:
            json.dump(data, f)

    def _load_file(self, data_id: str) -> Optional[Any]:
        for path in self.paths.data_path.rglob(f"{data_id}.json"):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    # ------------------------------------------------------------------
    # Public API
    def store(self, data_id: str, data: Any, data_type: str) -> None:
        if self.storage_type == StorageType.FILE_BASED:
            self._store_file(data_id, data, data_type)
        elif self.storage_type == StorageType.DATABASE:
            self._store_db(data_id, data, data_type)
        else:  # HYBRID
            self._store_file(data_id, data, data_type)
            self._store_db(data_id, data, data_type)

    def retrieve(self, data_id: str) -> Optional[Any]:
        if self.storage_type == StorageType.FILE_BASED:
            return self._load_file(data_id)
        if self.storage_type == StorageType.DATABASE:
            return self._load_db(data_id)
        # HYBRID
        data = self._load_file(data_id)
        return data if data is not None else self._load_db(data_id)

    def status(self) -> dict:
        return {"storage_type": self.storage_type.value}


__all__ = ["PersistentStoragePersistence"]
