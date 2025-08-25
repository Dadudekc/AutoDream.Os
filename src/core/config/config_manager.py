"""Configuration manager orchestrator.

This thin facade wires together the parser, validator and core
implementation. It exposes the same public interface as the original
monolithic module but delegates the heavy lifting to specialised
components created during initialization.
"""

from __future__ import annotations

from .config_manager_core import ConfigManagerCore
from .config_parser import ConfigParser
from .config_validator import ConfigValidator
from ..config_manager_config import ConfigEntry, ConfigMetadata

__all__ = [
    "ConfigManager",
    "ConfigParser",
    "ConfigValidator",
    "ConfigEntry",
    "ConfigMetadata",
]


class ConfigManager(ConfigManagerCore):
    """Orchestrates configuration loading and validation."""

    def __init__(self, config_dir: str | None = None):
        config_dir = config_dir or "config"
        super().__init__(config_dir, ConfigParser, ConfigValidator)
