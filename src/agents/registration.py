"""Agent registration module for coordinator.

Provides simple in-memory registry storing agent metadata.
"""
from __future__ import annotations
from typing import Dict, Any


class AgentRegistry:
    """Stores metadata for registered agents."""

    def __init__(self) -> None:
        self._agents: Dict[str, Dict[str, Any]] = {}

    def register(self, agent_id: str, info: Dict[str, Any] | None = None) -> None:
        if agent_id in self._agents:
            raise ValueError(f"Agent {agent_id} already registered")
        self._agents[agent_id] = info or {}

    def deregister(self, agent_id: str) -> None:
        self._agents.pop(agent_id, None)

    def get(self, agent_id: str) -> Dict[str, Any] | None:
        return self._agents.get(agent_id)

    def all_agents(self) -> Dict[str, Dict[str, Any]]:
        return dict(self._agents)
