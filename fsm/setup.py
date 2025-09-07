"""FSM package configuration and initialization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional

DEFAULT_CONFIG_PATH = Path(__file__).with_suffix(".json")


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Load FSM configuration from a JSON file."""
    path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def initialize(config_path: Optional[str] = None) -> Dict[str, Any]:
    """Initialize the FSM package and return configuration data."""
    return load_config(config_path)
