"""Simple integrity validation utilities for persistent storage."""

import hashlib
import json
from typing import Any


class PersistentStorageValidator:
    """Calculates and verifies checksums for stored data."""

    def calculate_checksum(self, data: Any) -> str:
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def validate(self, data: Any, checksum: str) -> bool:
        return self.calculate_checksum(data) == checksum


__all__ = ["PersistentStorageValidator"]
