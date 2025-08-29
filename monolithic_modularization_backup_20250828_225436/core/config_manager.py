from typing import Any, Dict

from __future__ import annotations


"""Placeholder configuration manager for testing purposes."""



class ConfigManager:
    def __init__(self, config: Dict[str, Any] | None = None) -> None:
        self.config = config or {}
