@dataclass
class CommandResult:
    """Represents the result of a command execution."""

    success: bool
    message: str
    data: Optional[Any] = None
    execution_time: Optional[float] = None
    agent: Optional[str] = None
