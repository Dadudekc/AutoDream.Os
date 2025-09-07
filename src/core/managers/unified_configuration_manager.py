"""Unified configuration manager composed of smaller components."""

from __future__ import annotations

from typing import Any, Dict

from .base_manager import BaseManager, ManagerType
from .configuration_source_manager import ConfigurationSourceManager
from .configuration_store import ConfigurationStore
from .contracts import ManagerContext, ManagerResult


class UnifiedConfigurationManager(BaseManager):
    """Aggregates configuration loading, validation and storage."""

    def __init__(self) -> None:
        super().__init__(ManagerType.CONFIGURATION, "unified_configuration")
        self.store = ConfigurationStore()
        self.sources = ConfigurationSourceManager()

    def initialize(self, context: ManagerContext) -> bool:
        context.logger("UnifiedConfigurationManager initialized")
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        handlers = {
            "load_config": self._load_config,
            "save_config": self._save_config,
            "get_all_configs": self._get_all_configs,
        }
        handler = handlers.get(operation)
        if not handler:
            return ManagerResult(False, {}, {}, f"Unknown operation: {operation}")
        return handler(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        self.store.clear()
        context.logger("UnifiedConfigurationManager cleaned up")
        return True

    def get_status(self) -> Dict[str, Any]:
        return {"config_count": len(self.store.get_all_configs())}

    # Handlers -----------------------------------------------------------------
    def _load_config(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        name = payload["name"]
        source = payload.get("path")
        data = self.sources.load_from_file(source) if source else {}
        env_prefix = payload.get("env_prefix")
        if env_prefix:
            data.update(self.sources.load_from_env(env_prefix))
        self.store.set_config(name, data)
        return ManagerResult(True, {"config": data}, {})

    def _save_config(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        name = payload["name"]
        data = payload.get("data", {})
        path = payload.get("path")
        self.store.set_config(name, data)
        if path:
            self.sources.save_to_file(path, data)
        return ManagerResult(True, {"config": name}, {})

    def _get_all_configs(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        return ManagerResult(True, {"configs": self.store.get_all_configs()}, {})
