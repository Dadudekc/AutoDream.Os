"""Data loading utilities for error reports."""

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple


class ErrorDataLoader:
    """Load pattern, trend, and correlation data from JSON files."""

    def load(self, patterns_path: Path, trends_path: Path, correlations_path: Path) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Load data from the given file paths."""
        return (
            self._load_json_list(patterns_path),
            self._load_json_list(trends_path),
            self._load_json_list(correlations_path),
        )

    def _load_json_list(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, list) else []
