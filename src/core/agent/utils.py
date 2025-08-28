"""Common utilities shared by agent submodules."""

from datetime import datetime
from typing import Any


def current_time() -> datetime:
    """Return current UTC timestamp."""
    return datetime.utcnow()


def format_message(sender: str, message: str) -> str:
    """Format a simple agent message with sender attribution."""
    return f"[{sender}] {message}"


def ensure_list(value: Any):
    """Ensure a value is a list."""
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
