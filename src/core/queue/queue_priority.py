from enum import Enum


class MessagePriority(Enum):
    """Simple priority levels for queued messages."""
    LOW = 1
    NORMAL = 2
    HIGH = 3


def priority_value(priority: MessagePriority) -> int:
    """Return the numeric value for a priority."""
    return priority.value


def is_high_priority(priority: MessagePriority) -> bool:
    """Return True if the priority should be handled urgently."""
    return priority is MessagePriority.HIGH
