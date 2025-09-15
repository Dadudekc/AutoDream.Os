#!/usr/bin/env python3
"""
FSM State Models - V2 Compliance Module
======================================

FSM state-related data models.

V2 Compliance: < 300 lines, single responsibility, state models.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Any

@dataclass
class StateDefinition:
    """FSM state definition with V2 compliance."""

    name: str
    description: str
    entry_actions: list[str]
    exit_actions: list[str]
    timeout_seconds: int | None
    retry_count: int
    retry_delay: float
    required_resources: list[str]
    dependencies: list[str]
    metadata: dict[str, Any]

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.name:
            raise ValueError("State name is required")
        if not self.description:
            raise ValueError("State description is required")

    def is_valid(self) -> bool:
        """Check if state definition is valid."""
        try:
            self.__post_init__()
            return True
        except ValueError:
            return False

    def get_summary(self) -> dict[str, Any]:
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