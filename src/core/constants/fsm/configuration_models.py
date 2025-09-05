"""
FSM Configuration Models - V2 Compliance Module
==============================================

FSM configuration-related data models.

V2 Compliance: < 300 lines, single responsibility, configuration models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class FSMConfiguration:
    """FSM configuration with V2 compliance."""
    state_timeout_seconds: Optional[int]
    state_retry_count: int
    state_retry_delay: float
    transition_priority_default: int
    transition_timeout_seconds: Optional[int]
    max_states: int
    max_transitions: int
    validation_enabled: bool
    metadata: Dict[str, Any]

    def __post_init__(self):
        """Post-initialization validation."""
        if self.state_retry_count < 0:
            raise ValueError("State retry count must be non-negative")
        if self.state_retry_delay < 0:
            raise ValueError("State retry delay must be non-negative")
        if self.max_states < 1:
            raise ValueError("Max states must be at least 1")
        if self.max_transitions < 1:
            raise ValueError("Max transitions must be at least 1")
    
    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return (
            self.state_retry_count >= 0 and
            self.state_retry_delay >= 0 and
            self.max_states >= 1 and
            self.max_transitions >= 1
        )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get configuration summary."""
        return {
            "state_timeout_seconds": self.state_timeout_seconds,
            "state_retry_count": self.state_retry_count,
            "state_retry_delay": self.state_retry_delay,
            "transition_priority_default": self.transition_priority_default,
            "transition_timeout_seconds": self.transition_timeout_seconds,
            "max_states": self.max_states,
            "max_transitions": self.max_transitions,
            "validation_enabled": self.validation_enabled
        }
