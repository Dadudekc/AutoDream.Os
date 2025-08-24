"""Core functionality for the configuration manager.

This module provides in-memory operations for configuration data such as
value access, summaries and a minimal file watching stub.  Loading and
validation are delegated to dedicated modules to keep this core small and
maintainable.
"""

from __future__ import annotations

from typing import Any, Dict, Callable, Type
import time


class ConfigManagerCore:
    """Encapsulates configuration storage and basic operations."""

    def __init__(
        self,
        config_dir: str,
        loader_cls: Type,
        validator_cls: Type,
    ):
        loader = loader_cls(config_dir)
        self.configs, validator_map = loader.load()
        self.validator = validator_cls(validator_map)
        self.validators = validator_map
        self.config_dir = config_dir
        self._watching = False

    # ------------------------------------------------------------------
    # value access helpers
    # ------------------------------------------------------------------
    def set_config_value(self, section: str, key: str, value: Any) -> None:
        self.configs.setdefault(section, {})[key] = value

    def get_config_value(self, section: str, key: str, default: Any | None = None) -> Any:
        return self.configs.get(section, {}).get(key, default)

    # ------------------------------------------------------------------
    # diagnostics
    # ------------------------------------------------------------------
    def get_config_summary(self) -> Dict[str, Any]:
        return {
            "config_dir": self.config_dir,
            "sections": list(self.configs.keys()),
            "timestamp": time.time(),
        }

    # ------------------------------------------------------------------
    # file watching stubs
    # ------------------------------------------------------------------
    def start_file_watching(self) -> None:
        self._watching = True

    def stop_file_watching(self) -> None:
        self._watching = False

    def cleanup(self) -> None:
        self.stop_file_watching()
