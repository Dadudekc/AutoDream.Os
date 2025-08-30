#!/usr/bin/env python3
"""
Recovery Actions Data Models

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
    """Types of recovery actions"""

    VALIDATION = "VALIDATION"
    REPAIR = "REPAIR"
    RESTORE = "RESTORE"
    VERIFICATION = "VERIFICATION"
    NOTIFICATION = "NOTIFICATION"


class ActionStatus(Enum):
    """Recovery action status"""

    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


@dataclass
class RecoveryActions:
    """Individual recovery action definition"""

    action_id: str
    name: str
    description: str
    action_type: ActionType
    status: ActionStatus
    parameters: Dict[str, Any]
    dependencies: List[str]
    estimated_duration: int  # minutes
    actual_duration: Optional[int]
    started_at: Optional[str]
    completed_at: Optional[str]
    result: Optional[str]
    error_message: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return asdict(self)

    @property
    def is_completed(self) -> bool:
        """Check if action is completed"""
        return self.status == ActionStatus.COMPLETED

    @property
    def is_failed(self) -> bool:
        """Check if action failed"""
        return self.status == ActionStatus.FAILED

    @property
    def can_start(self) -> bool:
        """Check if action can start (dependencies resolved)"""
        return self.status == ActionStatus.PENDING

    def start(self):
        """Start the action execution"""
        if self.can_start:
            self.status = ActionStatus.IN_PROGRESS
            self.started_at = datetime.now().isoformat()
        else:
            raise ValueError("Cannot start action - not in pending status")

    def complete(self, result: str = None):
        """Mark action as completed"""
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
        """Mark action as failed"""
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
        """Skip the action"""
        if self.can_start:
            self.status = ActionStatus.SKIPPED
            if reason:
                self.result = f"SKIPPED: {reason}"
        else:
            raise ValueError("Cannot skip action - not in pending status")
