"""
Agent Entity - Core Domain Object
==================================

Represents an agent in the coordination system.
Agents have identity and manage their own state and capabilities.
"""

from dataclasses import dataclass, field
from datetime import datetime

from ..value_objects.ids import AgentId, TaskId


@dataclass
class Agent:
    """
    Agent entity representing an autonomous agent in the system.

    Business Rules:
    - Agents must have unique identifiers
    - Agents have capabilities and roles
    - Agents can be active/inactive
    - Agents track their current task assignments
    """

    id: AgentId
    name: str
    role: str
    capabilities: set[str] = field(default_factory=set)
    max_concurrent_tasks: int = 3
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active_at: datetime | None = None
    current_task_ids: list[TaskId] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.name or not self.name.strip():
            raise ValueError("Agent name cannot be empty")
        if not self.role or not self.role.strip():
            raise ValueError("Agent role cannot be empty")
        if self.max_concurrent_tasks < 1:
            raise ValueError("Agent must be able to handle at least 1 task")

    @property
    def current_task_count(self) -> int:
        """Get the number of currently assigned tasks."""
        return len(self.current_task_ids)

    @property
    def can_accept_more_tasks(self) -> bool:
        """Check if agent can accept more tasks."""
        return self.is_active and self.current_task_count < self.max_concurrent_tasks

    @property
    def workload_percentage(self) -> float:
        """Get current workload as a percentage."""
        if self.max_concurrent_tasks == 0:
            return 100.0
        return (self.current_task_count / self.max_concurrent_tasks) * 100.0

    def has_capability(self, capability: str) -> bool:
        """Check if agent has a specific capability."""
        return capability in self.capabilities

    def add_capability(self, capability: str) -> None:
        """Add a capability to the agent."""
        if not capability or not capability.strip():
            raise ValueError("Capability cannot be empty")
        self.capabilities.add(capability.strip())

    def remove_capability(self, capability: str) -> None:
        """Remove a capability from the agent."""
        self.capabilities.discard(capability)

    def assign_task(self, task_id: TaskId) -> None:
        """
        Assign a task to this agent.

        Business Rules:
        - Agent must be active
        - Agent must not exceed max concurrent tasks
        - Task must not already be assigned
        """
        if not self.is_active:
            raise ValueError("Cannot assign tasks to inactive agent")

        if not self.can_accept_more_tasks:
            raise ValueError("Agent has reached maximum concurrent tasks")

        if task_id in self.current_task_ids:
            return  # Already assigned

        self.current_task_ids.append(task_id)
        self.last_active_at = datetime.utcnow()

    def complete_task(self, task_id: TaskId) -> None:
        """
        Mark a task as completed for this agent.

        Business Rules:
        - Task must be assigned to this agent
        """
        if task_id not in self.current_task_ids:
            raise ValueError("Task is not assigned to this agent")

        self.current_task_ids.remove(task_id)
        self.last_active_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the agent."""
        self.is_active = False

    def reactivate(self) -> None:
        """Reactivate the agent."""
        self.is_active = True
        self.last_active_at = datetime.utcnow()

    def update_activity(self) -> None:
        """Update the last activity timestamp."""
        self.last_active_at = datetime.utcnow()
