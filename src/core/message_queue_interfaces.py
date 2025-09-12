"""
Message Queue Interfaces - V2 Compliance Module
==============================================

Abstract interfaces for message queue system following SOLID principles.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class IMessageQueueLogger(Protocol):
    """Interface for message queue logging operations."""

    def info(self, message: str) -> None: ...

    def warning(self, message: str) -> None: ...

    def error(self, message: str) -> None: ...


class IQueueEntry(Protocol):
    """Interface for queue entry objects."""

    @property
    def message(self) -> Any: ...

    @property
    def queue_id(self) -> str: ...

    def to_dict(self) -> dict[str, Any]: ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IQueueEntry": ...


class IMessageQueue(ABC):
    """Abstract interface for message queue operations."""

    @abstractmethod
    def enqueue(self, message: Any) -> str:
        """Add message to queue."""
        pass

    @abstractmethod
    def dequeue(self, batch_size: int | None = None) -> list[IQueueEntry]:
        """Get next messages for processing."""
        pass

    @abstractmethod
    def mark_delivered(self, queue_id: str) -> bool:
        """Mark message as successfully delivered."""
        pass

    @abstractmethod
    def mark_failed(self, queue_id: str, error: str) -> bool:
        """Mark message as failed."""
        pass

    @abstractmethod
    def get_statistics(self) -> dict[str, Any]:
        """Get queue statistics."""
        pass

    @abstractmethod
    def cleanup_expired(self) -> int:
        """Remove expired entries."""
        pass


class IQueuePersistence(ABC):
    """Abstract interface for queue persistence operations."""

    @abstractmethod
    def load_entries(self) -> list[IQueueEntry]:
        """Load queue entries from storage."""
        pass

    @abstractmethod
    def save_entries(self, entries: list[IQueueEntry]) -> None:
        """Save queue entries to storage."""
        pass

    @abstractmethod
    def atomic_operation(self, operation: callable) -> Any:
        """Perform atomic file operation."""
        pass


class IQueueProcessor(ABC):
    """Abstract interface for queue processing operations."""

    @abstractmethod
    async def start_processing(self, interval: float = 5.0) -> None:
        """Start continuous queue processing."""
        pass

    @abstractmethod
    def stop_processing(self) -> None:
        """Stop queue processing."""
        pass

    @abstractmethod
    async def process_batch(self) -> None:
        """Process a batch of messages."""
        pass


class IQueueConfig(Protocol):
    """Interface for queue configuration."""

    @property
    def max_queue_size(self) -> int: ...

    @property
    def processing_batch_size(self) -> int: ...

    @property
    def max_age_days(self) -> int: ...

    @property
    def retry_base_delay(self) -> float: ...

    @property
    def retry_max_delay(self) -> float: ...

    @property
    def cleanup_interval(self) -> int: ...
