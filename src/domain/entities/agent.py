"""
Agent Entity - V2 Compliant (Simplified)
========================================

Core Agent entity with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent status enumeration."""

    INACTIVE = "inactive"
    ACTIVE = "active"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


class AgentType(Enum):
    """Agent type enumeration."""

    CORE = "core"
    SERVICE = "service"
    INTEGRATION = "integration"
    UTILITY = "utility"


class AgentCapability(Enum):
    """Agent capability enumeration."""

    MESSAGING = "messaging"
    COMMAND_EXECUTION = "command_execution"
    DATA_PROCESSING = "data_processing"
    COORDINATION = "coordination"
    USER_INTERFACE = "user_interface"
    SECURITY = "security"
    SYSTEM_INTEGRATION = "system_integration"


@dataclass
class AgentMetrics:
    """Agent performance metrics."""

    time_created: datetime = field(default_factory=datetime.now)
    time_last_active: datetime | None = None
    total_tasks_completed: int = 0
    total_tasks_failed: int = 0
    average_task_duration: float = 0.0
    error_count: int = 0
    last_error: str | None = None


@dataclass
class AgentConfiguration:
    """Agent configuration."""

    max_concurrent_tasks: int = 5
    task_timeout: int = 300
    retry_attempts: int = 3
    health_check_interval: int = 60
    capabilities: list[AgentCapability] = field(default_factory=list)


class Agent:
    """
    Core Agent entity representing an autonomous agent in the system.

    Simplified version focusing on essential functionality.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        agent_type: AgentType,
        capabilities: list[AgentCapability] = None,
        configuration: AgentConfiguration | None = None,
    ):
        """Initialize a new Agent."""
        self._id = agent_id
        self._name = name
        self._agent_type = agent_type
        self._status = AgentStatus.INACTIVE
        self._capabilities = capabilities or []
        self._configuration = configuration or AgentConfiguration()
        self._metrics = AgentMetrics()
        self._created_at = datetime.now()
        self._updated_at = datetime.now()
        self._current_tasks: list[str] = []
        self._tags: list[str] = []

        logger.info(f"Agent created: {self._name} ({self._agent_type.value})")

    # Properties
    @property
    def id(self) -> str:
        """Get the agent ID."""
        return self._id

    @property
    def name(self) -> str:
        """Get the agent name."""
        return self._name

    @property
    def agent_type(self) -> AgentType:
        """Get the agent type."""
        return self._agent_type

    @property
    def status(self) -> AgentStatus:
        """Get the current agent status."""
        return self._status

    @property
    def capabilities(self) -> list[AgentCapability]:
        """Get the agent capabilities."""
        return self._capabilities.copy()

    @property
    def configuration(self) -> AgentConfiguration:
        """Get the agent configuration."""
        return self._configuration

    @property
    def metrics(self) -> AgentMetrics:
        """Get the agent metrics."""
        return self._metrics

    @property
    def created_at(self) -> datetime:
        """Get the creation timestamp."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Get the last update timestamp."""
        return self._updated_at

    @property
    def current_tasks(self) -> list[str]:
        """Get the current task IDs."""
        return self._current_tasks.copy()

    @property
    def tags(self) -> list[str]:
        """Get the agent tags."""
        return self._tags.copy()

    # Agent lifecycle methods
    def activate(self) -> bool:
        """Activate the agent."""
        if self._status == AgentStatus.ERROR:
            logger.warning(f"Agent {self._id} cannot be activated from error status")
            return False

        self._status = AgentStatus.ACTIVE
        self._metrics.time_last_active = datetime.now()
        self._updated_at = datetime.now()
        logger.info(f"Agent {self._id} activated")
        return True

    def deactivate(self) -> None:
        """Deactivate the agent."""
        self._status = AgentStatus.INACTIVE
        self._updated_at = datetime.now()
        logger.info(f"Agent {self._id} deactivated")

    def set_busy(self) -> None:
        """Set agent status to busy."""
        if self._status == AgentStatus.ACTIVE:
            self._status = AgentStatus.BUSY
            self._updated_at = datetime.now()
            logger.debug(f"Agent {self._id} set to busy")

    def set_available(self) -> None:
        """Set agent status to available."""
        if self._status == AgentStatus.BUSY:
            self._status = AgentStatus.ACTIVE
            self._metrics.time_last_active = datetime.now()
            self._updated_at = datetime.now()
            logger.debug(f"Agent {self._id} set to available")

    def set_error(self, error_message: str) -> None:
        """Set agent status to error."""
        self._status = AgentStatus.ERROR
        self._metrics.error_count += 1
        self._metrics.last_error = error_message
        self._updated_at = datetime.now()
        logger.error(f"Agent {self._id} error: {error_message}")

    def go_offline(self) -> None:
        """Set agent status to offline."""
        self._status = AgentStatus.OFFLINE
        self._updated_at = datetime.now()
        logger.info(f"Agent {self._id} went offline")

    # Task management methods
    def assign_task(self, task_id: str) -> bool:
        """Assign a task to the agent."""
        if len(self._current_tasks) >= self._configuration.max_concurrent_tasks:
            logger.warning(f"Agent {self._id} at max concurrent tasks")
            return False

        if self._status not in [AgentStatus.ACTIVE, AgentStatus.BUSY]:
            logger.warning(f"Agent {self._id} not available for tasks")
            return False

        self._current_tasks.append(task_id)
        self.set_busy()
        self._updated_at = datetime.now()
        logger.info(f"Task {task_id} assigned to agent {self._id}")
        return True

    def complete_task(self, task_id: str, success: bool = True) -> None:
        """Complete a task."""
        if task_id in self._current_tasks:
            self._current_tasks.remove(task_id)

            if success:
                self._metrics.total_tasks_completed += 1
            else:
                self._metrics.total_tasks_failed += 1

            self._metrics.time_last_active = datetime.now()
            self._updated_at = datetime.now()

            if not self._current_tasks:
                self.set_available()

            logger.info(f"Task {task_id} completed by agent {self._id} (success: {success})")

    def get_task_count(self) -> int:
        """Get the number of current tasks."""
        return len(self._current_tasks)

    def is_available(self) -> bool:
        """Check if the agent is available for new tasks."""
        return (
            self._status == AgentStatus.ACTIVE
            and len(self._current_tasks) < self._configuration.max_concurrent_tasks
        )

    # Capability methods
    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if the agent has a specific capability."""
        return capability in self._capabilities

    def add_capability(self, capability: AgentCapability) -> None:
        """Add a capability to the agent."""
        if capability not in self._capabilities:
            self._capabilities.append(capability)
            self._updated_at = datetime.now()
            logger.debug(f"Capability {capability.value} added to agent {self._id}")

    def remove_capability(self, capability: AgentCapability) -> None:
        """Remove a capability from the agent."""
        if capability in self._capabilities:
            self._capabilities.remove(capability)
            self._updated_at = datetime.now()
            logger.debug(f"Capability {capability.value} removed from agent {self._id}")

    # Utility methods
    def add_tag(self, tag: str) -> None:
        """Add a tag to the agent."""
        if tag not in self._tags:
            self._tags.append(tag)
            self._updated_at = datetime.now()

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the agent."""
        if tag in self._tags:
            self._tags.remove(tag)
            self._updated_at = datetime.now()

    def get_uptime(self) -> timedelta:
        """Get the agent uptime."""
        return datetime.now() - self._created_at

    def get_last_active_time(self) -> datetime | None:
        """Get the last active time."""
        return self._metrics.time_last_active

    def is_healthy(self) -> bool:
        """Check if the agent is healthy."""
        if self._status == AgentStatus.ERROR:
            return False

        if self._metrics.time_last_active:
            time_since_active = datetime.now() - self._metrics.time_last_active
            return time_since_active.total_seconds() < (
                self._configuration.health_check_interval * 2
            )

        return True

    # Serialization methods
    def to_dict(self) -> dict[str, Any]:
        """Convert agent to dictionary representation."""
        return {
            "id": self._id,
            "name": self._name,
            "agent_type": self._agent_type.value,
            "status": self._status.value,
            "capabilities": [cap.value for cap in self._capabilities],
            "configuration": {
                "max_concurrent_tasks": self._configuration.max_concurrent_tasks,
                "task_timeout": self._configuration.task_timeout,
                "retry_attempts": self._configuration.retry_attempts,
                "health_check_interval": self._configuration.health_check_interval,
            },
            "metrics": {
                "time_created": self._metrics.time_created.isoformat(),
                "time_last_active": self._metrics.time_last_active.isoformat()
                if self._metrics.time_last_active
                else None,
                "total_tasks_completed": self._metrics.total_tasks_completed,
                "total_tasks_failed": self._metrics.total_tasks_failed,
                "average_task_duration": self._metrics.average_task_duration,
                "error_count": self._metrics.error_count,
                "last_error": self._metrics.last_error,
            },
            "current_tasks": self._current_tasks,
            "tags": self._tags,
            "created_at": self._created_at.isoformat(),
            "updated_at": self._updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Agent":
        """Create agent from dictionary representation."""
        capabilities = [AgentCapability(cap) for cap in data["capabilities"]]

        config_data = data["configuration"]
        configuration = AgentConfiguration(
            max_concurrent_tasks=config_data["max_concurrent_tasks"],
            task_timeout=config_data["task_timeout"],
            retry_attempts=config_data["retry_attempts"],
            health_check_interval=config_data["health_check_interval"],
            capabilities=capabilities,
        )

        agent = cls(
            agent_id=data["id"],
            name=data["name"],
            agent_type=AgentType(data["agent_type"]),
            capabilities=capabilities,
            configuration=configuration,
        )

        agent._status = AgentStatus(data["status"])
        agent._current_tasks = data["current_tasks"]
        agent._tags = data["tags"]
        agent._created_at = datetime.fromisoformat(data["created_at"])
        agent._updated_at = datetime.fromisoformat(data["updated_at"])

        # Restore metrics
        metrics_data = data["metrics"]
        agent._metrics = AgentMetrics(
            time_created=datetime.fromisoformat(metrics_data["time_created"]),
            time_last_active=datetime.fromisoformat(metrics_data["time_last_active"])
            if metrics_data["time_last_active"]
            else None,
            total_tasks_completed=metrics_data["total_tasks_completed"],
            total_tasks_failed=metrics_data["total_tasks_failed"],
            average_task_duration=metrics_data["average_task_duration"],
            error_count=metrics_data["error_count"],
            last_error=metrics_data["last_error"],
        )

        return agent

    def __str__(self) -> str:
        """String representation of the agent."""
        return f"Agent({self._name}, {self._agent_type.value}, {self._status.value})"

    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        return (
            f"Agent(id='{self._id}', name='{self._name}', "
            f"type={self._agent_type.value}, status={self._status.value})"
        )


class AgentManager:
    """Manager for agent entities."""

    def __init__(self):
        """Initialize agent manager."""
        self._agents: dict[str, Agent] = {}
        self.logger = logging.getLogger(f"{__name__}.AgentManager")

    def register_agent(self, agent: Agent) -> None:
        """Register an agent."""
        self._agents[agent.id] = agent
        self.logger.debug(f"Agent registered: {agent.name}")

    def unregister_agent(self, agent_id: str) -> bool:
        """Unregister an agent."""
        if agent_id in self._agents:
            del self._agents[agent_id]
            self.logger.debug(f"Agent unregistered: {agent_id}")
            return True
        return False

    def get_agent(self, agent_id: str) -> Agent | None:
        """Get an agent by ID."""
        return self._agents.get(agent_id)

    def get_all_agents(self) -> dict[str, Agent]:
        """Get all agents."""
        return self._agents.copy()

    def get_agents_by_type(self, agent_type: AgentType) -> list[Agent]:
        """Get agents by type."""
        return [agent for agent in self._agents.values() if agent.agent_type == agent_type]

    def get_agents_by_capability(self, capability: AgentCapability) -> list[Agent]:
        """Get agents by capability."""
        return [agent for agent in self._agents.values() if agent.has_capability(capability)]

    def get_available_agents(self) -> list[Agent]:
        """Get available agents."""
        return [agent for agent in self._agents.values() if agent.is_available()]

    def cleanup_all(self) -> None:
        """Cleanup all agents."""
        self._agents.clear()
        self.logger.info("All agents cleaned up")

    @property
    def agents(self) -> dict[str, Agent]:
        """Get all agents."""
        return self._agents.copy()


# Global agent manager
agent_manager = AgentManager()
