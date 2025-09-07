"""
Domain Events - Business Events
===============================

Domain events represent significant business events that occur within the domain.
They enable loose coupling and event-driven architecture.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from src.domain.value_objects.ids import TaskId, AgentId


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events.

    Domain events are immutable and contain all necessary information
    about what happened in the domain.
    """
    event_id: str
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    event_version: int = 1

    @property
    def event_type(self) -> str:
        """Get the event type name."""
        return self.__class__.__name__

    def to_dict(self) -> Dict[str, Any]:
        """Convert event to dictionary representation."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "occurred_at": self.occurred_at.isoformat(),
            "event_version": self.event_version
        }


@dataclass(frozen=True)
class TaskCreated(DomainEvent):
    """Event raised when a new task is created."""
    task_id: TaskId
    title: str
    priority: int

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "task_id": self.task_id,
            "title": self.title,
            "priority": self.priority
        })
        return data


@dataclass(frozen=True)
class TaskAssigned(DomainEvent):
    """Event raised when a task is assigned to an agent."""
    task_id: TaskId
    agent_id: AgentId
    assigned_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "assigned_at": self.assigned_at.isoformat()
        })
        return data


@dataclass(frozen=True)
class TaskCompleted(DomainEvent):
    """Event raised when a task is completed."""
    task_id: TaskId
    agent_id: AgentId
    completed_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "task_id": self.task_id,
            "agent_id": self.agent_id,
            "completed_at": self.completed_at.isoformat()
        })
        return data


@dataclass(frozen=True)
class AgentActivated(DomainEvent):
    """Event raised when an agent becomes active."""
    agent_id: AgentId
    activated_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "agent_id": self.agent_id,
            "activated_at": self.activated_at.isoformat()
        })
        return data


@dataclass(frozen=True)
class AgentDeactivated(DomainEvent):
    """Event raised when an agent becomes inactive."""
    agent_id: AgentId
    deactivated_at: datetime

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data.update({
            "agent_id": self.agent_id,
            "deactivated_at": self.deactivated_at.isoformat()
        })
        return data
