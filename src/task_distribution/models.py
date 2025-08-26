from dataclasses import dataclass

@dataclass
class TaskContract:
    """Representation of a single task contract."""
    agent: str
    task_id: str
    content: str
