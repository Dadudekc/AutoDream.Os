"""
Resource Context Operations - Helper Module
===========================================

Handles context operations for CoreResourceManager.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .contracts import ManagerContext, ManagerResult


class ContextOperations:
    """Handles context operations for resource manager."""

    def __init__(self):
        """Initialize context operations handler."""
        self.operations_count = 0
        self._agent_contexts: dict[str, dict[str, Any]] = {}

    def handle_operation(self, context: ManagerContext, payload: dict[str, Any]) -> ManagerResult:
        """Handle context operations."""
        operation = payload.get("context_operation", "")
        agent_id = payload.get("agent_id", "")

        try:
            if operation == "set":
                return self._set_context(agent_id, payload.get("context_data", {}))
            elif operation == "get":
                return self._get_context(agent_id)
            elif operation == "update":
                return self._update_context(agent_id, payload.get("updates", {}))
            elif operation == "delete":
                return self._delete_context(agent_id)
            else:
                return ManagerResult(
                    success=False,
                    data={},
                    metrics={},
                    error=f"Unknown context operation: {operation}",
                )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def _set_context(self, agent_id: str, context_data: dict[str, Any]) -> ManagerResult:
        """Set agent context."""
        self._agent_contexts[agent_id] = {
            **context_data,
            "last_updated": datetime.now().isoformat(),
        }
        self.operations_count += 1
        return ManagerResult(
            success=True,
            data={"agent_id": agent_id, "context": self._agent_contexts[agent_id]},
            metrics={"context_keys": len(context_data)},
        )

    def _get_context(self, agent_id: str) -> ManagerResult:
        """Get agent context."""
        if agent_id in self._agent_contexts:
            return ManagerResult(
                success=True,
                data={"agent_id": agent_id, "context": self._agent_contexts[agent_id]},
                metrics={"context_keys": len(self._agent_contexts[agent_id])},
            )
        else:
            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Context not found for agent: {agent_id}",
            )

    def _update_context(self, agent_id: str, updates: dict[str, Any]) -> ManagerResult:
        """Update agent context."""
        if agent_id in self._agent_contexts:
            self._agent_contexts[agent_id].update(updates)
            self._agent_contexts[agent_id]["last_updated"] = datetime.now().isoformat()
            self.operations_count += 1
            return ManagerResult(
                success=True,
                data={"agent_id": agent_id, "context": self._agent_contexts[agent_id]},
                metrics={"context_keys": len(self._agent_contexts[agent_id])},
            )
        else:
            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Context not found for agent: {agent_id}",
            )

    def _delete_context(self, agent_id: str) -> ManagerResult:
        """Delete agent context."""
        if agent_id in self._agent_contexts:
            del self._agent_contexts[agent_id]
            self.operations_count += 1
            return ManagerResult(
                success=True,
                data={"agent_id": agent_id, "deleted": True},
                metrics={},
            )
        else:
            return ManagerResult(
                success=False,
                data={},
                metrics={},
                error=f"Context not found for agent: {agent_id}",
            )

    def create_context(
        self, context: ManagerContext, agent_id: str, context_data: dict[str, Any]
    ) -> ManagerResult:
        """Create an agent context."""
        try:
            self._agent_contexts[agent_id] = {
                **context_data,
                "last_updated": datetime.now().isoformat(),
            }
            self.operations_count += 1
            return ManagerResult(
                success=True,
                data={"type": "context", "agent_id": agent_id, "created": True},
                metrics={"context_keys": len(context_data)},
            )
        except Exception as e:
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    def get_context_if_exists(self, context_id: str) -> dict[str, Any] | None:
        """Get context if it exists."""
        return self._agent_contexts.get(context_id)

    def update_context_direct(
        self, context_id: str, updates: dict[str, Any]
    ) -> dict[str, Any] | None:
        """Update context directly if it exists."""
        if context_id in self._agent_contexts:
            self._agent_contexts[context_id].update(updates)
            self._agent_contexts[context_id]["last_updated"] = datetime.now().isoformat()
            return self._agent_contexts[context_id]
        return None

    def delete_context_if_exists(self, context_id: str) -> bool:
        """Delete context if it exists."""
        if context_id in self._agent_contexts:
            del self._agent_contexts[context_id]
            return True
        return False

    def clear_contexts(self) -> None:
        """Clear all contexts."""
        self._agent_contexts.clear()

    def get_context_count(self) -> int:
        """Get context count."""
        return len(self._agent_contexts)

    def get_context_ids(self) -> list[str]:
        """Get all context IDs."""
        return list(self._agent_contexts.keys())
