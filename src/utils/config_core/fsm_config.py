"""Compatibility wrapper for FSM configuration utilities.

This module preserves the previous import path while delegating to the
centralized configuration implementation in :mod:`utils.config_core`.
"""

from typing import Any


# Create a simple FSMConfig class for compatibility
class FSMConfig:
    """FSM configuration compatibility class."""

    def __init__(self):
        self._configs = {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get FSM configuration value."""
        return self._configs.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set FSM configuration value."""
        self._configs[key] = value


# Also provide FSMConfiguration alias for compatibility
FSMConfiguration = FSMConfig

__all__ = ["FSMConfig", "FSMConfiguration"]
