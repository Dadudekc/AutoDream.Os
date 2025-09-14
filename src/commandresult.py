from dataclasses import dataclass
from typing import Any


@dataclass
class CommandResult:
    """Represents the result of a command execution."""

    success: bool
    message: str
    data: Any | None = None
    execution_time: float | None = None
    agent: str | None = None
