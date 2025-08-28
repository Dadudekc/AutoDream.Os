from __future__ import annotations

"""Placeholder configuration manager for testing purposes."""

from typing import Any, Dict


class ConfigManager:
    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}
