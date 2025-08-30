"""Configuration and metadata definitions for persistent storage."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class StorageType(Enum):
    """Supported storage backends."""

    FILE_BASED = "file_based"
    DATABASE = "database"
    HYBRID = "hybrid"


class DataIntegrityLevel(Enum):
    """Integrity verification levels for stored data."""

    BASIC = "basic"
    ADVANCED = "advanced"
    CRITICAL = "critical"


@dataclass
class StoragePaths:
    """Convenience container for storage paths."""

    base_path: Path
    data_path: Path
    metadata_path: Path

    @classmethod
    def create(cls, base: str = "persistent_data") -> "StoragePaths":
        base_path = Path(base)
        paths = cls(
            base_path=base_path,
            data_path=base_path / "data",
            metadata_path=base_path / "metadata",
        )
        paths.ensure()
        return paths

    def ensure(self) -> None:
        for path in (self.base_path, self.data_path, self.metadata_path):
            path.mkdir(parents=True, exist_ok=True)


@dataclass
class StorageMetadata:
    """Metadata describing a stored data item."""

    data_id: str
    checksum: str
    timestamp: float
    integrity_level: DataIntegrityLevel


__all__ = [
    "StorageType",
    "DataIntegrityLevel",
    "StoragePaths",
    "StorageMetadata",
]
