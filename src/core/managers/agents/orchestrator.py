"""High-level coordination for agent management."""

from __future__ import annotations

from typing import Any, Dict

from .config import load_config
from .lifecycle import LifecycleManager
from .metrics import collect_metrics


class AgentOrchestrator:
    """Coordinate configuration, lifecycle and metrics for agents."""

    def __init__(self, config_path: str | None = None) -> None:
        self.config = load_config(config_path)
        self.lifecycle = LifecycleManager()

    # Lifecycle operations delegated to LifecycleManager
    def register_agent(self, agent_id: str, payload: Dict[str, Any]) -> None:
        self.lifecycle.register(agent_id, payload)

    def unregister_agent(self, agent_id: str) -> bool:
        return self.lifecycle.unregister(agent_id)

    # Metrics collection
    def metrics(self) -> Dict[str, Any]:
        return collect_metrics(self.lifecycle)
