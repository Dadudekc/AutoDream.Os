"""
FSM Transition Models - V2 Compliance Module
===========================================

FSM transition-related data models.

V2 Compliance: < 300 lines, single responsibility, transition models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..fsm_enums import TransitionType, TransitionStatus


@dataclass
class TransitionDefinition:
    """FSM transition definition with V2 compliance."""

    from_state: str
    to_state: str
    transition_type: TransitionType
    condition: Optional[str]
    priority: int
    timeout_seconds: Optional[int]
    actions: List[str]
    metadata: Dict[str, Any]

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.from_state:
            raise ValueError("From state is required")
        if not self.to_state:
            raise ValueError("To state is required")
        if self.from_state == self.to_state:
            raise ValueError("From state and to state cannot be the same")

    def is_valid(self) -> bool:
        """Check if transition definition is valid."""
        return bool(
            self.from_state and self.to_state and self.from_state != self.to_state
        )

    def get_summary(self) -> Dict[str, Any]:
        """Get transition summary."""
        return {
            "from_state": self.from_state,
            "to_state": self.to_state,
            "transition_type": self.transition_type.value,
            "priority": self.priority,
            "timeout_seconds": self.timeout_seconds,
            "actions_count": len(self.actions),
            "has_condition": bool(self.condition),
        }
