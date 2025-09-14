"""In-memory storage for configuration values."""

from __future__ import annotations

from typing import Any


class ConfigurationStore:
    """Provides SSOT for configuration data."""

    def __init__(self) -> None:
        self._configs: dict[str, dict[str, Any]] = {}

    def set_config(self, name: str, data: dict[str, Any]) -> None:
        self._configs[name] = data

    def get_config(self, name: str) -> dict[str, Any] | None:
        return self._configs.get(name)

    def delete_config(self, name: str) -> None:
        self._configs.pop(name, None)

    def get_all_configs(self) -> dict[str, dict[str, Any]]:
        return dict(self._configs)

    def clear(self) -> None:
        self._configs.clear()
