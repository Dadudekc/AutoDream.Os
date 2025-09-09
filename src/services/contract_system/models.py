#!/usr/bin/env python3
"""
Contract Models - Agent Cellphone V2
===================================

Data models for the contract system.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from datetime import datetime
from enum import Enum
from typing import Any


class ContractStatus(Enum):
    """Contract status enumeration."""

    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ContractPriority(Enum):
    """Contract priority enumeration."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(Enum):
    """Task status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Task:
    """Task data model."""

    def __init__(self, **kwargs):
        """Initialize task with provided data."""
        self.task_id = kwargs.get("task_id", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.status = kwargs.get("status", TaskStatus.PENDING.value)
        self.priority = kwargs.get("priority", ContractPriority.MEDIUM.value)
        self.assigned_to = kwargs.get("assigned_to", "")
        self.created_at = kwargs.get("created_at", datetime.now().isoformat())
        self.due_date = kwargs.get("due_date", "")
        self.completed_at = kwargs.get("completed_at", "")
        self.last_updated = kwargs.get("last_updated", datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "due_date": self.due_date,
            "completed_at": self.completed_at,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Create task from dictionary."""
        return cls(**data)

    def update_status(self, status: str) -> None:
        """Update task status."""
        self.status = status
        self.last_updated = datetime.now().isoformat()

        if status == TaskStatus.COMPLETED.value:
            self.completed_at = datetime.now().isoformat()

    def assign_to(self, agent_id: str) -> None:
        """Assign task to agent."""
        self.assigned_to = agent_id
        self.status = TaskStatus.IN_PROGRESS.value
        self.last_updated = datetime.now().isoformat()


class Contract:
    """Contract data model."""

    def __init__(self, **kwargs):
        """Initialize contract with provided data."""
        self.contract_id = kwargs.get("contract_id", "")
        self.title = kwargs.get("title", "")
        self.description = kwargs.get("description", "")
        self.status = kwargs.get("status", ContractStatus.PENDING.value)
        self.priority = kwargs.get("priority", ContractPriority.MEDIUM.value)
        self.assigned_to = kwargs.get("assigned_to", "")
        self.created_at = kwargs.get("created_at", datetime.now().isoformat())
        self.assigned_at = kwargs.get("assigned_at", "")
        self.completed_at = kwargs.get("completed_at", "")
        self.tasks = kwargs.get("tasks", [])
        self.last_updated = kwargs.get("last_updated", datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        """Convert contract to dictionary."""
        return {
            "contract_id": self.contract_id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "assigned_to": self.assigned_to,
            "created_at": self.created_at,
            "assigned_at": self.assigned_at,
            "completed_at": self.completed_at,
            "tasks": self.tasks,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Contract":
        """Create contract from dictionary."""
        return cls(**data)

    def update_status(self, status: str) -> None:
        """Update contract status."""
        self.status = status
        self.last_updated = datetime.now().isoformat()

        if status == ContractStatus.COMPLETED.value:
            self.completed_at = datetime.now().isoformat()

    def assign_to(self, agent_id: str) -> None:
        """Assign contract to agent."""
        self.assigned_to = agent_id
        self.status = ContractStatus.ACTIVE.value
        self.assigned_at = datetime.now().isoformat()
        self.last_updated = datetime.now().isoformat()

    def add_task(self, task: dict[str, Any]) -> None:
        """Add task to contract."""
        if not self.tasks:
            self.tasks = []
        self.tasks.append(task)
        self.last_updated = datetime.now().isoformat()
