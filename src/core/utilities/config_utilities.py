"""
Configuration Utilities - Configuration Manager
================================================

Manages configuration for manager components.
Part of shared_utilities.py modular refactoring.

Author: Agent-1 (Integration & Core Systems Specialist) - V2 Refactor
Original: Agent-6 (Coordination & Communication Specialist)
License: MIT
"""

from typing import Any

from .base_utilities import BaseUtility


class ConfigurationManager(BaseUtility):
    """Manages configuration for managers."""

    def __init__(self):
        super().__init__()
        self.config = {}

    def initialize(self) -> bool:
        """Initialize configuration manager."""
        self.logger.info("ConfigurationManager initialized")
        return True

    def cleanup(self) -> bool:
        """Clean up configuration resources."""
        self.config.clear()
        return True

    def set_config(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)


def create_configuration_manager() -> ConfigurationManager:
    """Create a new configuration manager instance."""
    return ConfigurationManager()


__all__ = ["ConfigurationManager", "create_configuration_manager"]
