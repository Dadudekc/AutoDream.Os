"""High level coordination for persistent storage operations."""

import json
import time
from typing import Any, Dict

from .persistent_storage_config import (
    StoragePaths,
    StorageType,
    DataIntegrityLevel,
    StorageMetadata,
)
from .persistent_storage_persistence import PersistentStoragePersistence
from .persistent_storage_validator import PersistentStorageValidator


class PersistentStorageManager:
    """Combines persistence and validation layers."""

    def __init__(self, paths: StoragePaths, storage_type: StorageType):
        self.paths = paths
        self.persistence = PersistentStoragePersistence(paths, storage_type)
        self.validator = PersistentStorageValidator()
        self.metadata: Dict[str, StorageMetadata] = {}
        self._metadata_file = self.paths.metadata_path / "metadata.json"
        self._load_metadata()

    # ------------------------------------------------------------------
    # Metadata handling
    def _load_metadata(self) -> None:
        if not self._metadata_file.exists():
            return
        with open(self._metadata_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
        for data_id, info in raw.items():
            self.metadata[data_id] = StorageMetadata(
                data_id=data_id,
                checksum=info["checksum"],
                timestamp=info["timestamp"],
                integrity_level=DataIntegrityLevel(info["integrity_level"]),
            )

    def _save_metadata(self) -> None:
        raw = {
            data_id: {
                "checksum": meta.checksum,
                "timestamp": meta.timestamp,
                "integrity_level": meta.integrity_level.value,
            }
            for data_id, meta in self.metadata.items()
        }
        with open(self._metadata_file, "w", encoding="utf-8") as f:
            json.dump(raw, f, indent=2)

    # ------------------------------------------------------------------
    # Public API
    def store(
        self,
        data_id: str,
        data: Any,
        data_type: str,
        integrity_level: DataIntegrityLevel,
    ) -> bool:
        checksum = self.validator.calculate_checksum(data)
        self.persistence.store(data_id, data, data_type)
        self.metadata[data_id] = StorageMetadata(
            data_id=data_id,
            checksum=checksum,
            timestamp=time.time(),
            integrity_level=integrity_level,
        )
        self._save_metadata()
        return True

    def retrieve(self, data_id: str) -> Any:
        data = self.persistence.retrieve(data_id)
        meta = self.metadata.get(data_id)
        if data is None or meta is None:
            return None
        if not self.validator.validate(data, meta.checksum):
            return None
        return data

    def status(self) -> Dict[str, Any]:
        return {
            "total_items": len(self.metadata),
            **self.persistence.status(),
        }


__all__ = ["PersistentStorageManager"]
