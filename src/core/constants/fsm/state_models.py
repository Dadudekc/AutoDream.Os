"""
FSM State Models - V2 Compliance Module
======================================

FSM state-related data models.

V2 Compliance: < 300 lines, single responsibility, state models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ..fsm_enums import StateStatus


@dataclass
class StateDefinition:
    """FSM state definition with V2 compliance."""

    name: str
    description: str
    entry_actions: List[str]
    exit_actions: List[str]
    timeout_seconds: Optional[int]
    retry_count: int
    retry_delay: float
    required_resources: List[str]
    dependencies: List[str]
    metadata: Dict[str, Any]

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name:
            raise ValueError("State name is required")
        if not self.description:
            raise ValueError("State description is required")

    def is_valid(self) -> bool:
        """Check if state definition is valid."""
        return bool(self.name and self.description)

    def get_summary(self) -> Dict[str, Any]:
        """Get state summary."""
        return {
            "name": self.name,
            "description": self.description,
            "entry_actions_count": len(self.entry_actions),
            "exit_actions_count": len(self.exit_actions),
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "required_resources_count": len(self.required_resources),
            "dependencies_count": len(self.dependencies),
        }
