from __future__ import annotations
import json
from pathlib import Path
from typing import Any


class FileAdapter:
    """File adapter for reading and writing JSON data."""

    def read_json(self, path: str) -> Any:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_json(self, path: str, data: Any) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
