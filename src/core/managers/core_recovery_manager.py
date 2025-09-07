"""Specialized manager handling error recovery operations."""

from __future__ import annotations

import uuid
from typing import Any, Dict

from .contracts import Manager, ManagerContext, ManagerResult


class CoreRecoveryManager(Manager):
    """Provides recovery mechanisms for service operations."""

    def __init__(self) -> None:
        self._strategies: Dict[str, Dict[str, Any]] = {
            "default_retry": {
                "type": "retry",
                "conditions": {},
                "actions": ["retry"],
                "enabled": True,
            }
        }

    def initialize(self, context: ManagerContext) -> bool:
        context.logger("CoreRecoveryManager initialized")
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        handlers = {
            "register_recovery_strategy": self.register_recovery_strategy,
            "recover_from_error": self.recover_from_error,
            "get_recovery_strategies": self.get_recovery_strategies,
        }
        handler = handlers.get(operation)
        if not handler:
            return ManagerResult(False, {}, {}, f"Unknown operation: {operation}")
        return handler(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        self._strategies.clear()
        context.logger("CoreRecoveryManager cleaned up")
        return True

    def get_status(self) -> Dict[str, Any]:
        return {"strategies": list(self._strategies.keys())}

    # Handlers -----------------------------------------------------------------
    def register_recovery_strategy(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        name = payload["strategy_name"]
        self._strategies[name] = {
            "type": payload.get("strategy_type", "retry"),
            "conditions": payload.get("conditions", {}),
            "actions": payload.get("actions", []),
            "enabled": payload.get("enabled", True),
        }
        context.logger(f"Recovery strategy registered: {name}")
        return ManagerResult(True, {"strategy_name": name, "registered": True}, {})

    def recover_from_error(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        recovery_id = str(uuid.uuid4())
        error_type = payload.get("error_type", "unknown")
        context.logger(
            f"Recovery invoked for {error_type} with id {recovery_id}"
        )
        return ManagerResult(True, {"recovery_id": recovery_id}, {})

    def get_recovery_strategies(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        return ManagerResult(True, {"strategies": self._strategies}, {})
