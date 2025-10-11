"""
Manager State - Base Manager State Management
==============================================
Extracted from base_manager.py for V2 compliance.
Handles manager state tracking, enums, and lifecycle states.

Author: Agent-5 (refactored from Agent-2's base_manager.py)
License: MIT
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any


class ManagerType(Enum):
    """Manager type enumeration for specialization."""

    CONFIGURATION = "configuration"
    EXECUTION = "execution"
    MONITORING = "monitoring"
    ONBOARDING = "onboarding"
    RECOVERY = "recovery"
    RESOURCE = "resource"
    RESULTS = "results"
    SERVICE = "service"
    COORDINATION = "coordination"
    PERFORMANCE = "performance"
    SECURITY = "security"


class ManagerState(Enum):
    """Manager lifecycle states."""

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ERROR = "error"
    CLEANING_UP = "cleaning_up"
    TERMINATED = "terminated"


class ManagerStateTracker:
    """Tracks manager state and identity."""

    def __init__(self, manager_type: ManagerType, manager_name: str | None = None):
        """Initialize state tracker."""
        # Core identity
        self.manager_type = manager_type
        self.manager_name = manager_name or f"{manager_type.value}_manager"
        self.manager_id = f"{self.manager_name}_{id(self)}"

        # Lifecycle state
        self.state = ManagerState.UNINITIALIZED
        self.initialized_at: datetime | None = None
        self.last_operation_at: datetime | None = None

        # Error tracking
        self.last_error: str | None = None

        # Context and configuration
        self.context: Any = None  # ManagerContext
        self.config: dict[str, Any] = {}

    def set_state(self, new_state: ManagerState) -> None:
        """Update manager state."""
        self.state = new_state

    def mark_initialized(self) -> None:
        """Mark manager as initialized."""
        self.state = ManagerState.READY
        self.initialized_at = datetime.now()

    def mark_operation(self) -> None:
        """Mark that an operation occurred."""
        self.last_operation_at = datetime.now()
        self.state = ManagerState.ACTIVE

    def mark_ready(self) -> None:
        """Mark manager as ready."""
        self.state = ManagerState.READY

    def mark_error(self, error: str) -> None:
        """Mark manager in error state."""
        self.state = ManagerState.ERROR
        self.last_error = error

    def get_status_dict(self) -> dict[str, Any]:
        """Get state as dictionary."""
        return {
            "manager_id": self.manager_id,
            "manager_name": self.manager_name,
            "manager_type": self.manager_type.value,
            "state": self.state.value,
            "initialized_at": self.initialized_at.isoformat() if self.initialized_at else None,
            "last_operation_at": (
                self.last_operation_at.isoformat() if self.last_operation_at else None
            ),
            "last_error": self.last_error,
            "config_keys": list(self.config.keys()),
        }

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ManagerStateTracker(id={self.manager_id}, "
            f"type={self.manager_type.value}, state={self.state.value})"
        )
