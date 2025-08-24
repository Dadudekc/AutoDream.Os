"""Orchestrator facade for the persistent storage subsystem."""

from pathlib import Path
from typing import Any, Dict

from .persistent_storage_config import (
    StorageType,
    DataIntegrityLevel,
    StoragePaths,
)
from .persistent_storage_manager import PersistentStorageManager


class PersistentDataStorage:
    """Facade used by the rest of the code base."""

    def __init__(
        self,
        storage_type: StorageType = StorageType.FILE_BASED,
        base_path: str = "persistent_data",
    ):
        paths = StoragePaths.create(base_path)
        self.manager = PersistentStorageManager(paths, storage_type)

    def store_data(
        self,
        data_id: str,
        data: Any,
        data_type: str = "general",
        integrity_level: DataIntegrityLevel = DataIntegrityLevel.ADVANCED,
    ) -> bool:
        """Store data with integrity metadata."""
        return self.manager.store(data_id, data, data_type, integrity_level)

    def retrieve_data(self, data_id: str) -> Any:
        """Retrieve data by identifier if it passes validation."""
        return self.manager.retrieve(data_id)

    def get_storage_status(self) -> Dict[str, Any]:
        """Return high level storage statistics."""
        return self.manager.status()


__all__ = ["PersistentDataStorage", "StorageType", "DataIntegrityLevel"]
