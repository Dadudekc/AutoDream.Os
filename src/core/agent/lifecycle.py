"""Agent lifecycle management submodule."""

from dataclasses import dataclass
from typing import Dict, List, Optional

from .utils import current_time, ensure_list


@dataclass
class AgentInfo:
    """Basic information about an agent."""

    agent_id: str
    name: str
    capabilities: List[str]
    active: bool = True
    created_at: Optional[str] = None

    def __post_init__(self) -> None:
        if self.created_at is None:
            self.created_at = current_time().isoformat()
        self.capabilities = ensure_list(self.capabilities)


class AgentLifecycle:
    """Handles registration and availability of agents."""

    def __init__(self) -> None:
        self._agents: Dict[str, AgentInfo] = {}

    # ------------------------------------------------------------------
    # Registration utilities
    # ------------------------------------------------------------------
    def register(self, agent_id: str, name: str, capabilities=None) -> bool:
        if agent_id in self._agents:
            return False
        self._agents[agent_id] = AgentInfo(agent_id, name, capabilities or [])
        return True

    def unregister(self, agent_id: str) -> bool:
        return self._agents.pop(agent_id, None) is not None

    # ------------------------------------------------------------------
    # Query helpers
    # ------------------------------------------------------------------
    def get(self, agent_id: str) -> Optional[AgentInfo]:
        return self._agents.get(agent_id)

    def all_agents(self) -> List[AgentInfo]:
        return list(self._agents.values())

    def available_agents(self) -> List[AgentInfo]:
        return [a for a in self._agents.values() if a.active]
