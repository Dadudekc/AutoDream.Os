"""Task data structures and mock enums for development tasks."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional


class DevelopmentTask:
    """Simple task model used by the executor."""

    def __init__(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.status = MockTaskStatus.AVAILABLE
        self.claimed_by: Optional[str] = None
        self.completed_at: Optional[str] = None
        self.started_at: Optional[str] = None
        self.metadata: Dict[str, Any] = {}

    def is_available(self) -> bool:
        return self.status == MockTaskStatus.AVAILABLE

    def is_completed(self) -> bool:
        return self.status == MockTaskStatus.COMPLETED

    def claim(self, agent_id: str) -> bool:
        if self.is_available():
            self.claimed_by = agent_id
            self.status = MockTaskStatus.CLAIMED
            return True
        return False

    def start_work(self) -> bool:
        if self.status == MockTaskStatus.CLAIMED:
            self.status = MockTaskStatus.IN_PROGRESS
            self.started_at = datetime.now().isoformat()
            return True
        return False

    def complete(self) -> bool:
        if self.status in [MockTaskStatus.IN_PROGRESS, MockTaskStatus.CLAIMED]:
            self.status = MockTaskStatus.COMPLETED
            self.completed_at = datetime.now().isoformat()
            return True
        return False

    def block(self, reason: str) -> bool:
        if self.status != MockTaskStatus.COMPLETED:
            self.status = MockTaskStatus.BLOCKED
            self.metadata.setdefault("block_reason", reason)
            return True
        return False

    def unblock(self) -> bool:
        if self.status == MockTaskStatus.BLOCKED:
            self.status = MockTaskStatus.CLAIMED
            return True
        return False

    def cancel(self) -> bool:
        if self.status != MockTaskStatus.COMPLETED:
            self.status = MockTaskStatus.CANCELLED
            return True
        return False

    def update_progress(self, percentage: float) -> bool:
        if hasattr(self, "progress"):
            self.progress = max(0, min(100, percentage))
            return True
        return False

    def get_elapsed_time(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            return (end - start).total_seconds() / 3600
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items()}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DevelopmentTask":
        return cls(**data)


class MockTaskStatus:
    AVAILABLE = "available"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


class MockTaskPriorityMeta(type):
    def __getitem__(cls, key: str):
        mapping = {
            "MINIMAL": cls.MINIMAL,
            "LOW": cls.LOW,
            "MEDIUM": cls.MEDIUM,
            "HIGH": cls.HIGH,
            "CRITICAL": cls.CRITICAL,
        }
        if key not in mapping:
            raise KeyError(f"'{key}' is not a valid MockTaskPriority key")
        return mapping[key]

    def __iter__(cls):
        return iter([cls.MINIMAL, cls.LOW, cls.MEDIUM, cls.HIGH, cls.CRITICAL])


class MockTaskPriority(metaclass=MockTaskPriorityMeta):
    MINIMAL = type("MockPriority", (), {"value": 1})()
    LOW = type("MockPriority", (), {"value": 2})()
    MEDIUM = type("MockPriority", (), {"value": 3})()
    HIGH = type("MockPriority", (), {"value": 4})()
    CRITICAL = type("MockPriority", (), {"value": 5})()

    def __new__(cls, value: int):
        mapping = {
            1: cls.MINIMAL,
            2: cls.LOW,
            3: cls.MEDIUM,
            4: cls.HIGH,
            5: cls.CRITICAL,
        }
        if value not in mapping:
            raise ValueError(f"'{value}' is not a valid MockTaskPriority")
        return mapping[value]


class MockTaskComplexity:
    LOW = type("MockComplexity", (), {"value": "low"})()
    MEDIUM = type("MockComplexity", (), {"value": "medium"})()
    HIGH = type("MockComplexity", (), {"value": "high"})()

    def __new__(cls, value: str):
        mapping = {
            "low": cls.LOW,
            "medium": cls.MEDIUM,
            "high": cls.HIGH,
        }
        if value not in mapping:
            raise ValueError(f"'{value}' is not a valid MockTaskComplexity")
        return mapping[value]

    @classmethod
    def __iter__(cls):
        return iter([cls.LOW, cls.MEDIUM, cls.HIGH])


__all__ = [
    "DevelopmentTask",
    "MockTaskStatus",
    "MockTaskPriority",
    "MockTaskComplexity",
]
