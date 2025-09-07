"""Specialized manager for processing and retrieving results."""

from __future__ import annotations

import uuid
from typing import Any, Dict

from .contracts import Manager, ManagerContext, ManagerResult


class CoreResultsManager(Manager):
    """Handles result processing operations."""

    def __init__(self) -> None:
        self._results: Dict[str, Dict[str, Any]] = {}
        self._v2_compliant = True

    def initialize(self, context: ManagerContext) -> bool:
        context.logger("CoreResultsManager initialized")
        return True

    def execute(
        self, context: ManagerContext, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        handlers = {
            "process_results": self.process_results,
            "get_results": self.get_results,
        }
        handler = handlers.get(operation)
        if not handler:
            return ManagerResult(False, {}, {}, f"Unknown operation: {operation}")
        return handler(context, payload)

    def cleanup(self, context: ManagerContext) -> bool:
        self._results.clear()
        context.logger("CoreResultsManager cleaned up")
        return True

    def get_status(self) -> Dict[str, Any]:
        return {
            "active_results": len(self._results),
            "v2_compliant": self._v2_compliant,
        }

    # Handlers -----------------------------------------------------------------
    def process_results(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        result_id = payload.get("result_id") or str(uuid.uuid4())
        self._results[result_id] = {
            "result_type": payload.get("result_type", "general"),
            "data": payload.get("data", {}),
            "metadata": payload.get("metadata", {}),
        }
        context.logger(f"Result processed: {result_id}")
        return ManagerResult(True, {"result_id": result_id}, {})

    def get_results(
        self, context: ManagerContext, payload: Dict[str, Any]
    ) -> ManagerResult:
        return ManagerResult(True, {"results": self._results}, {})
