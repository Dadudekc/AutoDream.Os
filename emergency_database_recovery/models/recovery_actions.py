#!/usr/bin/env python3
"""
Recovery Actions Data Models.

This module contains data structures for recovery actions and procedures:
- Action definitions and parameters
- Execution order and dependencies
- Status tracking and results
"""

from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class ActionType(Enum):
    """Types of recovery actions."""

    VALIDATION = "VALIDATION"
    REPAIR = "REPAIR"
    RESTORE = "RESTORE"
    VERIFICATION = "VERIFICATION"
    NOTIFICATION = "NOTIFICATION"


class ActionStatus(Enum):
    """Recovery action status."""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class RecoveryAction:
    """Individual recovery action definition."""

    action_id: str
    name: str
    description: str
    action_type: ActionType
    status: ActionStatus
    parameters: Dict[str, Any]
    dependencies: List[str]
    estimated_duration: int  # minutes
    actual_duration: Optional[int] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[str] = None
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @property
    def is_completed(self) -> bool:
        """Check if action is completed."""
        return self.status == ActionStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """Check if action failed."""
        return self.status == ActionStatus.FAILED

    @property
    def can_start(self) -> bool:
        """Check if action can start (dependencies resolved)."""
        return self.status == ActionStatus.PENDING

    def start(self):
        """Start the action execution."""
        if self.can_start:
            self.status = ActionStatus.IN_PROGRESS
            self.started_at = datetime.now().isoformat()
        else:
            raise ValueError("Cannot start action - not in pending status")

    def complete(self, result: str = None):
        """Mark action as completed."""
        if self.status == ActionStatus.IN_PROGRESS:
            self.status = ActionStatus.COMPLETED
            self.completed_at = datetime.now().isoformat()
            if result:
                self.result = result

            # Calculate actual duration
            if self.started_at:
                start_time = datetime.fromisoformat(self.started_at)
                end_time = datetime.now()
                delta = end_time - start_time
                self.actual_duration = int(delta.total_seconds() / 60)
        else:
            raise ValueError("Cannot complete action - not in progress")

    def fail(self, error_message: str):
        """Mark action as failed."""
        if self.status == ActionStatus.IN_PROGRESS:
            self.status = ActionStatus.FAILED
            self.completed_at = datetime.now().isoformat()
            self.error_message = error_message

            # Calculate actual duration
            if self.started_at:
                start_time = datetime.fromisoformat(self.started_at)
                end_time = datetime.now()
                delta = end_time - start_time
                self.actual_duration = int(delta.total_seconds() / 60)
        else:
            raise ValueError("Cannot fail action - not in progress")

    def skip(self, reason: str = None):
        """Skip the action."""
        if self.can_start:
            self.status = ActionStatus.SKIPPED
            if reason:
                self.result = f"SKIPPED: {reason}"
        else:
            raise ValueError("Cannot skip action - not in pending status")


@dataclass
class RecoveryPlan:
    """Complete recovery plan with multiple actions."""

    plan_id: str
    timestamp: str
    strategy: str
    issues_count: int
    actions: List[RecoveryAction]
    estimated_duration_minutes: int
    priority: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @property
    def total_actions(self) -> int:
        """Get total number of actions in plan."""
        return len(self.actions)

    @property
    def completed_actions(self) -> int:
        """Get number of completed actions."""
        return sum(1 for action in self.actions if action.is_completed)

    @property
    def failed_actions(self) -> int:
        """Get number of failed actions."""
        return sum(1 for action in self.actions if action.is_failed)

    @property
    def pending_actions(self) -> int:
        """Get number of pending actions."""
        return sum(1 for action in self.actions if action.status == ActionStatus.PENDING)

    @property
    def progress_percentage(self) -> float:
        """Get completion progress as percentage."""
        if self.total_actions == 0:
            return 0.0
        return (self.completed_actions / self.total_actions) * 100

    @property
    def is_complete(self) -> bool:
        """Check if all actions are completed."""
        return self.completed_actions == self.total_actions

    @property
    def has_failures(self) -> bool:
        """Check if any actions have failed."""
        return self.failed_actions > 0

    def get_action_by_id(self, action_id: str) -> Optional[RecoveryAction]:
        """Get action by its ID."""
        for action in self.actions:
            if action.action_id == action_id:
                return action
        return None

    def add_action(self, action: RecoveryAction):
        """Add a new action to the plan."""
        self.actions.append(action)

    def remove_action(self, action_id: str):
        """Remove an action from the plan."""
        self.actions = [action for action in self.actions if action.action_id != action_id]

    def get_critical_actions(self) -> List[RecoveryAction]:
        """Get actions with critical priority."""
        return [action for action in self.actions if action.priority == "CRITICAL"]

    def get_dependent_actions(self, action_id: str) -> List[RecoveryAction]:
        """Get actions that depend on the specified action."""
        dependent_actions = []
        for action in self.actions:
            if action_id in action.dependencies:
                dependent_actions.append(action)
        return dependent_actions


# Backward compatibility alias
RecoveryActions = RecoveryAction
