"""Persistence abstraction for data integrity management state."""

from __future__ import annotations

import json
import os
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class IntegrityDataPersistence:
    """Handles atomic, validated persistence of integrity data."""

    def __init__(self, base_path: str = "data/persistent/integrity") -> None:
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def save(self, data: Dict[str, Any]) -> bool:
        """Save integrity data atomically after validation."""
        try:
            checksum = hashlib.sha256(
                json.dumps(data, sort_keys=True).encode("utf-8")
            ).hexdigest()
            payload = {
                "data": data,
                "checksum": checksum,
                "timestamp": datetime.now().isoformat(),
                "version": "2.0.0",
            }

            tmp_path = self.base_path / "integrity_data.json.tmp"
            final_path = self.base_path / "integrity_data.json"

            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=2, default=str)

            with open(tmp_path, "r", encoding="utf-8") as f:
                written = json.load(f)

            verify_checksum = hashlib.sha256(
                json.dumps(written["data"], sort_keys=True).encode("utf-8")
            ).hexdigest()
            if verify_checksum != written["checksum"]:
                return False

            os.replace(tmp_path, final_path)
            return True
        except Exception:
            return False


__all__ = ["IntegrityDataPersistence"]
