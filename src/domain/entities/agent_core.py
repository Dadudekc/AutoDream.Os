"""
Agent Entity Core - V2 Compliant
=================================

Core agent entity functionality.
V2 Compliance: ≤400 lines, single responsibility, KISS principle
"""

import logging
from datetime import datetime, timedelta

from .agent_models import AgentCapability, AgentConfig, AgentMetrics, AgentStatus, AgentType

logger = logging.getLogger(__name__)


class AgentCore:
    """Core agent functionality."""

    def __init__(self, config: AgentConfig):
        """Initialize agent core."""
        self.config = config
        self.status = config.status
        self.start_time = datetime.now()
        logger.info(f"Agent {config.agent_id} initialized")

    def activate(self) -> bool:
        """Activate the agent."""
        try:
            if self.status == AgentStatus.INACTIVE:
                self.status = AgentStatus.ACTIVE
                self.config.updated_at = datetime.now()
                logger.info(f"Agent {self.config.agent_id} activated")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to activate agent {self.config.agent_id}: {e}")
            return False

    def deactivate(self) -> bool:
        """Deactivate the agent."""
        try:
            if self.status == AgentStatus.ACTIVE:
                self.status = AgentStatus.INACTIVE
                self.config.updated_at = datetime.now()
                logger.info(f"Agent {self.config.agent_id} deactivated")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to deactivate agent {self.config.agent_id}: {e}")
            return False

    def set_busy(self) -> bool:
        """Set agent to busy status."""
        try:
            if self.status == AgentStatus.ACTIVE:
                self.status = AgentStatus.BUSY
                self.config.updated_at = datetime.now()
                logger.info(f"Agent {self.config.agent_id} set to busy")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to set agent {self.config.agent_id} to busy: {e}")
            return False

    def set_error(self, error_message: str) -> bool:
        """Set agent to error status."""
        try:
            self.status = AgentStatus.ERROR
            self.config.updated_at = datetime.now()
            self.config.metadata["last_error"] = error_message
            logger.error(f"Agent {self.config.agent_id} set to error: {error_message}")
            return True
        except Exception as e:
            logger.error(f"Failed to set agent {self.config.agent_id} to error: {e}")
            return False

    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has specific capability."""
        return capability in self.config.capabilities

    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        return self.status

    def get_uptime(self) -> float:
        """Get agent uptime in seconds."""
        return (datetime.now() - self.start_time).total_seconds()

    def update_metrics(self, metrics: AgentMetrics):
        """Update agent metrics."""
        self.config.metrics = metrics
        self.config.updated_at = datetime.now()
        logger.debug(f"Updated metrics for agent {self.config.agent_id}")


class AgentManager:
    """Agent management system."""

    def __init__(self):
        """Initialize agent manager."""
        self.agents: dict[str, AgentCore] = {}
        logger.info("AgentManager initialized")

    def register_agent(self, config: AgentConfig) -> bool:
        """Register a new agent."""
        try:
            if config.agent_id in self.agents:
                logger.warning(f"Agent {config.agent_id} already registered")
                return False

            agent_core = AgentCore(config)
            self.agents[config.agent_id] = agent_core
            logger.info(f"Registered agent {config.agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to register agent {config.agent_id}: {e}")
            return False

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        try:
            if agent_id in self.agents:
                del self.agents[agent_id]
                logger.info(f"Unregistered agent {agent_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to unregister agent {agent_id}: {e}")
            return False

    def get_agent(self, agent_id: str) -> AgentCore | None:
        """Get agent by ID."""
        return self.agents.get(agent_id)

    def get_all_agents(self) -> dict[str, AgentCore]:
        """Get all registered agents."""
        return self.agents.copy()

    def get_agents_by_status(self, status: AgentStatus) -> list[AgentCore]:
        """Get agents by status."""
        return [agent for agent in self.agents.values() if agent.get_status() == status]

    def get_agents_by_type(self, agent_type: AgentType) -> list[AgentCore]:
        """Get agents by type."""
        return [agent for agent in self.agents.values() if agent.config.agent_type == agent_type]

    def get_agents_by_capability(self, capability: AgentCapability) -> list[AgentCore]:
        """Get agents by capability."""
        return [agent for agent in self.agents.values() if agent.has_capability(capability)]

    def get_active_agents(self) -> list[AgentCore]:
        """Get all active agents."""
        return self.get_agents_by_status(AgentStatus.ACTIVE)

    def get_busy_agents(self) -> list[AgentCore]:
        """Get all busy agents."""
        return self.get_agents_by_status(AgentStatus.BUSY)

    def get_error_agents(self) -> list[AgentCore]:
        """Get all agents in error status."""
        return self.get_agents_by_status(AgentStatus.ERROR)

    def get_agent_count(self) -> int:
        """Get total number of registered agents."""
        return len(self.agents)

    def get_status_summary(self) -> dict[str, int]:
        """Get status summary of all agents."""
        summary = {}
        for status in AgentStatus:
            summary[status.value] = len(self.get_agents_by_status(status))
        return summary

    def cleanup_inactive_agents(self, max_age_hours: int = 24) -> int:
        """Clean up inactive agents older than specified hours."""
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        cleaned_count = 0

        for agent_id, agent in list(self.agents.items()):
            if agent.get_status() == AgentStatus.INACTIVE and agent.config.updated_at < cutoff_time:
                self.unregister_agent(agent_id)
                cleaned_count += 1

        logger.info(f"Cleaned up {cleaned_count} inactive agents")
        return cleaned_count
