#!/usr/bin/env python3
"""
FSM Task Models V2 - Agent Cellphone V2
=======================================

V2-compliant FSM task data structures.
Max 200 LOC, OOP design, SRP.
"""

import json
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, List, Any, Optional


class TaskState(Enum):
    """Task state enumeration."""

    NEW = "new"
    ONBOARDING = "onboarding"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Task priority enumeration."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FSMTask:
    """FSM task data structure."""

    id: str
    title: str
    description: str
    state: TaskState
    priority: TaskPriority
    assigned_agent: str
    created_at: str
    updated_at: str
    evidence: List[Dict[str, Any]] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []
        if self.metadata is None:
            self.metadata = {}

    def add_evidence(self, agent_id: str, evidence: Dict[str, Any]):
        """Add evidence to the task."""
        self.evidence.append(
            {
                "timestamp": datetime.now().isoformat(),
                "agent_id": agent_id,
                "evidence": evidence,
            }
        )
        self.updated_at = datetime.now().isoformat()

    def update_state(self, new_state: TaskState):
        """Update task state."""
        self.state = new_state
        self.updated_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        task_dict = asdict(self)
        task_dict["state"] = self.state.value
        task_dict["priority"] = self.priority.value
        return task_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FSMTask":
        """Create task from dictionary."""
        data["state"] = TaskState(data["state"])
        data["priority"] = TaskPriority(data["priority"])
        return cls(**data)


@dataclass
class FSMUpdate:
    """FSM update message structure."""

    update_id: str
    task_id: str
    agent_id: str
    state: TaskState
    summary: str
    evidence: Dict[str, Any]
    timestamp: str
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert update to dictionary."""
        update_dict = asdict(self)
        update_dict["state"] = self.state.value
        return update_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FSMUpdate":
        """Create update from dictionary."""
        data["state"] = TaskState(data["state"])
        return cls(**data)


class TaskValidator:
    """Validates FSM tasks and state transitions."""

    VALID_TRANSITIONS = {
        TaskState.NEW: [TaskState.ONBOARDING, TaskState.CANCELLED],
        TaskState.ONBOARDING: [
            TaskState.IN_PROGRESS,
            TaskState.BLOCKED,
            TaskState.CANCELLED,
        ],
        TaskState.IN_PROGRESS: [
            TaskState.COMPLETED,
            TaskState.BLOCKED,
            TaskState.FAILED,
            TaskState.CANCELLED,
        ],
        TaskState.BLOCKED: [TaskState.IN_PROGRESS, TaskState.CANCELLED],
        TaskState.COMPLETED: [],
        TaskState.FAILED: [TaskState.IN_PROGRESS, TaskState.CANCELLED],
        TaskState.CANCELLED: [],
    }

    @classmethod
    def validate_transition(
        cls, current_state: TaskState, new_state: TaskState
    ) -> bool:
        """Validate if state transition is allowed."""
        return new_state in cls.VALID_TRANSITIONS.get(current_state, [])

    @classmethod
    def validate_task(cls, task: FSMTask) -> List[str]:
        """Validate task data."""
        errors = []
        if not task.id:
            errors.append("Task ID is required")
        if not task.title:
            errors.append("Task title is required")
        if not task.assigned_agent:
            errors.append("Assigned agent is required")
        if not task.created_at:
            errors.append("Created timestamp is required")
        return errors


def main():
    """CLI interface for FSM Task testing."""
    import argparse
    import uuid

    parser = argparse.ArgumentParser(description="FSM Task V2 Testing")
    parser.add_argument("--test", action="store_true", help="Run tests")
    args = parser.parse_args()

    print("🤖 FSM Task Models V2 - Agent Cellphone V2")

    if args.test:
        task = FSMTask(
            id=str(uuid.uuid4()),
            title="Test Task",
            description="Test FSM task",
            state=TaskState.NEW,
            priority=TaskPriority.NORMAL,
            assigned_agent="Agent-Test",
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )

        errors = TaskValidator.validate_task(task)
        print(f"Validation: {'✅ Pass' if not errors else '❌ Fail'}")

        valid = TaskValidator.validate_transition(TaskState.NEW, TaskState.ONBOARDING)
        print(f"Transition: {'✅ Valid' if valid else '❌ Invalid'}")

        print("✅ All FSM task V2 tests completed!")


if __name__ == "__main__":
    main()
