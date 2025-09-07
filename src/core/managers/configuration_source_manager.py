"""Manager for loading and saving configurations from various sources."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


class ConfigurationSourceManager:
    """Handles IO for configuration data."""

    def load_from_file(self, path: str) -> Dict[str, Any]:
        file_path = Path(path)
        if not file_path.exists():
            return {}
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_to_file(self, path: str, data: Dict[str, Any]) -> bool:
        file_path = Path(path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        return True

    def load_from_env(self, prefix: str) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for key, value in os.environ.items():
            if key.startswith(prefix):
                result[key[len(prefix) :].lower()] = value
        return result
