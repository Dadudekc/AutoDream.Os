"""
Value Objects - Immutable Domain Objects
========================================

Value objects represent concepts in the domain that don't have identity.
They are immutable and compared by value, not reference.
"""

from dataclasses import dataclass
from typing import NewType

# Type aliases for better type safety and documentation
TaskId = NewType("TaskId", str)
AgentId = NewType("AgentId", str)
MessageId = NewType("MessageId", str)
FSMStateId = NewType("FSMStateId", str)


@dataclass(frozen=True, slots=True)
class TaskIdentifier:
    """Value object for task identification."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Task ID cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class AgentIdentifier:
    """Value object for agent identification."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Agent ID cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class MessageIdentifier:
    """Value object for message identification."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("Message ID cannot be empty")

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True, slots=True)
class FSMStateIdentifier:
    """Value object for FSM state identification."""

    value: str

    def __post_init__(self) -> None:
        if not self.value or not self.value.strip():
            raise ValueError("FSM State ID cannot be empty")

    def __str__(self) -> str:
        return self.value
