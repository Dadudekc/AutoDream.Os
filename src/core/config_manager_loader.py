
# MIGRATED: This file has been migrated to the centralized configuration system
"""Simple configuration loader used by the ConfigManager.

The loader discovers JSON or YAML files in a directory and returns a
mapping of section names to data as well as a mapping of section names to
validator callables. Validation here is intentionally lightweight – each
loaded section receives a validator that always returns ``True``.  This
provides a predictable structure for the validator component while
keeping the loader focused solely on I/O concerns.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, Tuple
import json
import yaml


class ConfigLoader:
    """Load configuration files from a directory."""

    def __init__(self, config_dir: str):
        self.config_dir = Path(config_dir)

    def load(self) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, Callable[[Dict[str, Any]], bool]]]:
        configs: Dict[str, Dict[str, Any]] = {}
        validators: Dict[str, Callable[[Dict[str, Any]], bool]] = {}

        if self.config_dir.exists():
            for path in self.config_dir.iterdir():
                if path.suffix.lower() not in {".json", ".yaml", ".yml"}:
                    continue
                try:
                    with path.open("r", encoding="utf-8") as f:
                        data = json.load(f) if path.suffix.lower() == ".json" else yaml.safe_load(f)
                    configs[path.stem] = data or {}
                    validators[path.stem] = lambda d: True
                except Exception:
                    # Skip unreadable files but continue processing others
                    continue

        if not configs:
            configs["default"] = {}
            validators["default"] = lambda d: True

        return configs, validators
