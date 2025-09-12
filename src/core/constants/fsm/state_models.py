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

EXAMPLE USAGE:
==============

# Import the core component
from src.core.constants.fsm.state_models import State_Models

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = State_Models(config)

# Execute primary functionality
result = component.process_data(input_data)
print(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    print(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    print(f"Operation failed: {e}")
    # Implement recovery logic

        """Post-initialization validation."""
        if not self.name:
            raise ValueError("State name is required")
        if not self.description:
            raise ValueError("State description is required")

    def is_valid(self) -> bool:
        """Check if state definition is valid."""
        return bool(self.name and self.description)

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
