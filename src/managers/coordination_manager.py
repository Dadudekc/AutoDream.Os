"""Basic agent coordination helper."""

from __future__ import annotations

from typing import Dict, List, Optional

from ..agent_config import AgentConfig


class AgentCoordinator:
    """Coordinates work distribution among agents.

    The coordinator implements a minimal round-robin scheduler using the
    strategy defined in :mod:`agent_config`. It can be expanded with more
    sophisticated logic as needed.
    """

    def __init__(self) -> None:
        self._agents: List[str] = []
        self._cursor: int = 0
        self.strategy = AgentConfig.DEFAULT_COORDINATION_STRATEGY

    def add_agent(self, agent_id: str) -> None:
        if agent_id not in self._agents:
            self._agents.append(agent_id)

    def remove_agent(self, agent_id: str) -> None:
        if agent_id in self._agents:
            self._agents.remove(agent_id)
            self._cursor %= len(self._agents) if self._agents else 1

    def next_agent(self) -> Optional[str]:
        """Return the next agent according to the active strategy."""

        if not self._agents:
            return None
        agent = self._agents[self._cursor]
        self._cursor = (self._cursor + 1) % len(self._agents)
        return agent
