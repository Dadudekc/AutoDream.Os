"""
Engine State Management - V2 Compliance Module
=============================================

Manages engine state transitions following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from enum import Enum
from typing import Any


class EngineState(Enum):
    """Engine lifecycle states."""

    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    READY = "ready"
    ACTIVE = "active"
    DEGRADED = "degraded"
    ERROR = "error"
    CLEANING_UP = "cleaning_up"
    TERMINATED = "terminated"


class EngineStateManager:
    """Manages engine state transitions and validation."""

    # Valid state transitions
    VALID_TRANSITIONS = {
        EngineState.UNINITIALIZED: [EngineState.INITIALIZING],
        EngineState.INITIALIZING: [EngineState.READY, EngineState.ERROR],
        EngineState.READY: [EngineState.ACTIVE, EngineState.ERROR, EngineState.TERMINATED],
        EngineState.ACTIVE: [EngineState.DEGRADED, EngineState.ERROR, EngineState.CLEANING_UP],
        EngineState.DEGRADED: [EngineState.ACTIVE, EngineState.ERROR, EngineState.CLEANING_UP],
        EngineState.ERROR: [EngineState.INITIALIZING, EngineState.CLEANING_UP],
        EngineState.CLEANING_UP: [EngineState.TERMINATED],
        EngineState.TERMINATED: []
    }

    def __init__(self, engine_id: str, initial_state: EngineState = EngineState.UNINITIALIZED):
        """Initialize state manager."""
        self.engine_id = engine_id
        self.current_state = initial_state
        self.state_history: list[dict[str, Any]] = []
        self.error_count = 0
        self.last_error: str | None = None

        # Record initial state
        self._record_state_change(initial_state, "initialization")

    def transition_to(self, new_state: EngineState, reason: str = "state_change") -> bool:
        """Transition to a new state if valid."""
        if new_state in self.VALID_TRANSITIONS.get(self.current_state, []):
            old_state = self.current_state
            self.current_state = new_state
            self._record_state_change(new_state, reason)

            # Handle error state
            if new_state == EngineState.ERROR:
                self.error_count += 1

            return True
        return False

    def can_transition_to(self, target_state: EngineState) -> bool:
        """Check if transition to target state is valid."""
        return target_state in self.VALID_TRANSITIONS.get(self.current_state, [])

    def get_valid_transitions(self) -> list[EngineState]:
        """Get list of valid transitions from current state."""
        return self.VALID_TRANSITIONS.get(self.current_state, [])

    def is_stable_state(self) -> bool:
        """Check if current state is stable (not transitioning)."""
        stable_states = [EngineState.READY, EngineState.ACTIVE, EngineState.DEGRADED, EngineState.TERMINATED]
        return self.current_state in stable_states

    def is_error_state(self) -> bool:
        """Check if engine is in error state."""
        return self.current_state == EngineState.ERROR

    def record_error(self, error_message: str):
        """Record an error and potentially transition to error state."""
        self.last_error = error_message
        self.error_count += 1

        # Auto-transition to error state if not already there
        if self.current_state != EngineState.ERROR:
            self.transition_to(EngineState.ERROR, f"error: {error_message}")

    def reset_error_state(self):
        """Reset error state and attempt to recover."""
        if self.current_state == EngineState.ERROR:
            self.transition_to(EngineState.INITIALIZING, "error_recovery")
            self.last_error = None

    def _record_state_change(self, new_state: EngineState, reason: str):
        """Record a state change in history."""
        from datetime import datetime

        self.state_history.append({
            "timestamp": datetime.now().isoformat(),
            "from_state": self.current_state.value if hasattr(self.current_state, 'value') else str(self.current_state),
            "to_state": new_state.value if hasattr(new_state, 'value') else str(new_state),
            "reason": reason
        })

    def get_state_summary(self) -> dict[str, Any]:
        """Get comprehensive state summary."""
        return {
            "engine_id": self.engine_id,
            "current_state": self.current_state.value if hasattr(self.current_state, 'value') else str(self.current_state),
            "error_count": self.error_count,
            "last_error": self.last_error,
            "is_stable": self.is_stable_state(),
            "is_error": self.is_error_state(),
            "valid_transitions": [s.value if hasattr(s, 'value') else str(s) for s in self.get_valid_transitions()],
            "state_history_count": len(self.state_history)
        }
