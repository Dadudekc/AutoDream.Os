"""Agent lifecycle management utilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict

from ..agent_config import AgentConfig


@dataclass
class AgentState:
    """State container for a single agent."""

    status: str = AgentConfig.DEFAULT_LIFECYCLE_STATE
    metadata: Dict[str, str] = field(default_factory=dict)


class AgentLifecycleManager:
    """Tracks and mutates agent lifecycle states.

    The manager keeps a simple in-memory registry of agent states and
    exposes small helper methods to transition between common
    lifecycle phases. It intentionally avoids external side effects so
    it can be reused in tests or higher level orchestration layers.
    """

    def __init__(self) -> None:
        self._agents: Dict[str, AgentState] = {}

    def register(self, agent_id: str) -> None:
        """Register a new agent with default state."""

        self._agents[agent_id] = AgentState()

    def update_status(self, agent_id: str, status: str) -> None:
        """Update lifecycle status for an agent."""

        if agent_id not in self._agents:
            self.register(agent_id)
        self._agents[agent_id].status = status

    def get_status(self, agent_id: str) -> str:
        """Return current lifecycle status for an agent."""

        return self._agents.get(agent_id, AgentState()).status
