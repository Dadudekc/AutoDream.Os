
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration management for communication workflow automation.

This module isolates configuration concerns.  It provides a simple dataclass
with default options and a manager that can load, update and expose those
settings.  Keeping configuration code separate makes future maintenance and
feature work easier.
"""
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class AutomationConfig:
    """Default configuration flags for automation features."""
    auto_channel_creation: bool = True
    intelligent_routing: bool = True
    batch_processing: bool = True
    auto_error_recovery: bool = True
    performance_monitoring: bool = True


class ConfigManager:
    """Handle loading and updating automation configuration."""

    def __init__(self, config: AutomationConfig | None = None) -> None:
        self._config = config or AutomationConfig()

    def update(self, **kwargs) -> None:
        """Update known configuration options."""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

    def as_dict(self) -> Dict[str, bool]:
        """Return the configuration as a plain dictionary."""
        return asdict(self._config).copy()
