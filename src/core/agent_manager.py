from __future__ import annotations

"""Minimal agent manager used for assignment optimisation tests."""

from dataclasses import dataclass
from typing import Dict, List, Any

AgentCapability = str


@dataclass
class AgentInfo:
    capabilities: List[AgentCapability]


class AgentManager:
    """Stores registered agents and their capabilities."""

    def __init__(self, agents: Dict[str, AgentInfo] | None = None) -> None:
        self._agents: Dict[str, AgentInfo] = agents or {}

    def register_agent(
        self, agent_id: str, capabilities: List[AgentCapability]
    ) -> None:
        self._agents[agent_id] = AgentInfo(capabilities)

    def get_agent_info(self, agent_id: str) -> Dict[str, Any] | None:
        info = self._agents.get(agent_id)
        if not info:
            return None
        return {"capabilities": info.capabilities}

    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        return {
            agent_id: {"capabilities": info.capabilities}
            for agent_id, info in self._agents.items()
        }
