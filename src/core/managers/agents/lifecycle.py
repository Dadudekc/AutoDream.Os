"""Agent lifecycle management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Agent:
    """Represents a lightweight agent record."""

    agent_id: str
    payload: Dict[str, Any]


class LifecycleManager:
    """Manage registration and basic state of agents."""

    def __init__(self) -> None:
        self._agents: Dict[str, Agent] = {}

    def register(self, agent_id: str, payload: Dict[str, Any]) -> Agent:
        agent = Agent(agent_id=agent_id, payload=payload)
        self._agents[agent_id] = agent
        return agent

    def unregister(self, agent_id: str) -> bool:
        return self._agents.pop(agent_id, None) is not None

    def get(self, agent_id: str) -> Optional[Agent]:
        return self._agents.get(agent_id)

    def all(self) -> Dict[str, Agent]:
        return dict(self._agents)
