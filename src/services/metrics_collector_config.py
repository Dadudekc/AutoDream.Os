
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration helpers for metrics collectors."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict
import platform


@dataclass
class CollectorConfig:
    """Basic configuration for metrics collectors."""

    collection_interval: int = 60
    enabled: bool = True
    tags: Dict[str, str] = field(
        default_factory=lambda: {"host": platform.node(), "collector": "core"}
    )
