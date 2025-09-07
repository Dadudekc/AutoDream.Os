from typing import Any, Dict, List

from .agent_utils import AgentCapability, AgentInfo
from __future__ import annotations


"""Agent registration module."""




class AgentRegistry:
    """Handles agent registration and metadata access."""

    def __init__(self, agents: Dict[str, AgentInfo] | None = None) -> None:
        self._agents: Dict[str, AgentInfo] = agents or {}

    def register_agent(
        self, agent_id: str, capabilities: List[AgentCapability]
    ) -> None:
        """Register a new agent with its capabilities."""
        self._agents[agent_id] = AgentInfo(capabilities)

    def get_agent_info(self, agent_id: str) -> Dict[str, Any] | None:
        """Retrieve information about a registered agent."""
        info = self._agents.get(agent_id)
        if not info:
            return None
        return {"capabilities": info.capabilities}

    def list_agents(self) -> Dict[str, Dict[str, Any]]:
        """List all registered agents and their capabilities."""
        return {
            agent_id: {"capabilities": info.capabilities}
            for agent_id, info in self._agents.items()
        }
