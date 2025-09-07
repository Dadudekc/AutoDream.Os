
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration utilities for extended AI/ML managers."""

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AIConfig:
    """Container for AI/ML configuration values."""

    api_keys: Dict[str, str]


def load_ai_config(config: Dict[str, Any]) -> AIConfig:
    """Load AI/ML specific configuration section."""
    return AIConfig(api_keys=config.get("api_keys", {}))
