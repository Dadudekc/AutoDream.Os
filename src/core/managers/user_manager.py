#!/usr/bin/env python3
"""User management module for agent registration and tracking."""

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional

from .manager_utils import current_timestamp


class AgentStatus(Enum):
    """Agent lifecycle states."""

    ONLINE = "online"
    OFFLINE = "offline"
    BUSY = "busy"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    ERROR = "error"


class AgentCapability(Enum):
    """Capability types an agent can possess."""

    REFACTORING = "refactoring"
    TESTING = "testing"
    INTEGRATION = "integration"
    DOCUMENTATION = "documentation"
    COORDINATION = "coordination"
    SECURITY = "security"
    PERFORMANCE = "performance"


@dataclass
class AgentInfo:
    """Information describing an agent."""

    agent_id: str
    name: str
    status: AgentStatus
    capabilities: List[AgentCapability]
    current_contract: Optional[str]
    last_heartbeat: str
    performance_score: float
    contracts_completed: int
    total_uptime: float
    resource_usage: Dict[str, Any]


class UserManager:
    """Manage registration and lifecycle of agents."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__ + ".UserManager")
        self.agents: Dict[str, AgentInfo] = {}

    # ------------------------------------------------------------------
    # Agent registration and lifecycle
    # ------------------------------------------------------------------
    def register_agent(self, agent_id: str, name: str, capabilities: List[str]) -> bool:
        """Register a new agent with provided capabilities."""
        try:
            agent_capabilities = [AgentCapability(cap) for cap in capabilities]
        except ValueError as exc:  # pragma: no cover - defensive
            self.logger.error("Invalid capability for agent %s: %s", agent_id, exc)
            return False

        info = AgentInfo(
            agent_id=agent_id,
            name=name,
            status=AgentStatus.OFFLINE,
            capabilities=agent_capabilities,
            current_contract=None,
            last_heartbeat=current_timestamp(),
            performance_score=0.0,
            contracts_completed=0,
            total_uptime=0.0,
            resource_usage={},
        )
        self.agents[agent_id] = info
        return True

    def unregister_agent(self, agent_id: str) -> bool:
        """Remove an agent from tracking."""
        return self.agents.pop(agent_id, None) is not None

    def update_agent_status(self, agent_id: str, status: AgentStatus) -> bool:
        """Update the status for a tracked agent."""
        agent = self.agents.get(agent_id)
        if not agent:
            return False
        agent.status = status
        agent.last_heartbeat = current_timestamp()
        return True

    # ------------------------------------------------------------------
    # Agent queries
    # ------------------------------------------------------------------
    def get_agent(self, agent_id: str) -> Optional[AgentInfo]:
        """Return information about a specific agent."""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> List[AgentInfo]:
        """Return all registered agents."""
        return list(self.agents.values())

    def get_agents_by_status(self, status: AgentStatus) -> List[AgentInfo]:
        """Return agents filtered by status."""
        return [a for a in self.agents.values() if a.status == status]

    def get_agents_by_capability(self, capability: AgentCapability) -> List[AgentInfo]:
        """Return agents that have a given capability."""
        return [a for a in self.agents.values() if capability in a.capabilities]

    # ------------------------------------------------------------------
    # Contract management
    # ------------------------------------------------------------------
    def assign_contract(self, agent_id: str, contract_id: str) -> bool:
        """Assign a contract to an agent."""
        agent = self.agents.get(agent_id)
        if not agent:
            return False
        agent.current_contract = contract_id
        agent.status = AgentStatus.BUSY
        return True

    def complete_contract(self, agent_id: str, contract_id: str) -> bool:
        """Mark a contract as completed for an agent."""
        agent = self.agents.get(agent_id)
        if not agent or agent.current_contract != contract_id:
            return False
        agent.current_contract = None
        agent.contracts_completed += 1
        agent.status = AgentStatus.IDLE
        return True

    # ------------------------------------------------------------------
    # Summary statistics
    # ------------------------------------------------------------------
    def get_summary(self) -> Dict[str, Any]:
        """Return aggregate statistics about all agents."""
        return {
            "total_agents": len(self.agents),
            "by_status": {
                status.value: len([a for a in self.agents.values() if a.status == status])
                for status in AgentStatus
            },
            "by_capability": {
                capability.value: len(
                    [a for a in self.agents.values() if capability in a.capabilities]
                )
                for capability in AgentCapability
            },
            "performance_stats": {
                "average_score": (
                    sum(a.performance_score for a in self.agents.values()) / len(self.agents)
                    if self.agents
                    else 0.0
                ),
                "total_contracts": sum(a.contracts_completed for a in self.agents.values()),
                "busy_agents": len([a for a in self.agents.values() if a.current_contract]),
            },
        }
