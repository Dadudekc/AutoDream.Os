"""
Task Entity - Core Domain Object
=================================

Represents a task in the agent coordination system.
Tasks have identity and encapsulate business rules.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from src.domain.value_objects.ids import TaskId, AgentId


@dataclass
class Task:
    """
    Task entity representing work to be done by agents.

    Business Rules:
    - Tasks must have a unique identifier
    - Tasks can only be assigned to one agent at a time
    - Completed tasks cannot be reassigned
    - Tasks track their lifecycle (created, assigned, completed)
    """

    id: TaskId
    title: str
    description: Optional[str] = None
    assigned_agent_id: Optional[AgentId] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    assigned_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    priority: int = 1  # 1=low, 2=medium, 3=high, 4=critical

    def __post_init__(self) -> None:
        """Validate entity invariants."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")
        if self.priority < 1 or self.priority > 4:
            raise ValueError("Task priority must be between 1 and 4")

    @property
    def is_assigned(self) -> bool:
        """Check if task is assigned to an agent."""
        return self.assigned_agent_id is not None

    @property
    def is_completed(self) -> bool:
        """Check if task is completed."""
        return self.completed_at is not None

    @property
    def is_pending(self) -> bool:
        """Check if task is pending (not assigned and not completed)."""
        return not self.is_assigned and not self.is_completed

    def assign_to(self, agent_id: AgentId) -> None:
        """
        Assign task to an agent.

        Business Rules:
        - Cannot assign completed tasks
        - Cannot assign to the same agent if already assigned
        """
        if self.is_completed:
            raise ValueError("Cannot assign a completed task")

        if self.assigned_agent_id == agent_id:
            return  # Already assigned to this agent

        self.assigned_agent_id = agent_id
        self.assigned_at = datetime.utcnow()

    def unassign(self) -> None:
        """
        Unassign task from current agent.

        Business Rules:
        - Cannot unassign completed tasks
        """
        if self.is_completed:
            raise ValueError("Cannot unassign a completed task")

        self.assigned_agent_id = None
        self.assigned_at = None

    def complete(self) -> None:
        """
        Mark task as completed.

        Business Rules:
        - Can only complete assigned tasks
        - Cannot complete already completed tasks
        """
        if not self.is_assigned:
            raise ValueError("Cannot complete an unassigned task")

        if self.is_completed:
            return  # Already completed

        self.completed_at = datetime.utcnow()

    def can_be_assigned_to(self, agent_id: AgentId) -> bool:
        """Check if task can be assigned to given agent."""
        return not self.is_completed and self.assigned_agent_id != agent_id
