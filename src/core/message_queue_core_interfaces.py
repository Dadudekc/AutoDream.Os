"""
Message Queue Core Interfaces - V2 Compliance Module
====================================================

Core abstract interfaces for message queue system following SOLID principles.

Refactored for V2 compliance: ≤5 classes, ≤10 functions per class.
Analytics interfaces moved to message_queue_analytics_interfaces.py

Author: Agent-5 (Business Intelligence & Team Beta Leader) - V2 Refactoring
Original: Agent-1 (System Recovery Specialist)
License: MIT
"""

from abc import ABC, abstractmethod
from typing import Any, Protocol


class IQueueEntry(Protocol):
    """Interface for queue entry objects."""

    @property
    def message(self) -> Any:
        """Get the message content."""
        ...

    @property
    def queue_id(self) -> str:
        """Get the unique queue identifier."""
        ...

    def to_dict(self) -> dict[str, Any]:
        """Convert entry to dictionary format."""
        ...

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "IQueueEntry":
        """Create entry from dictionary data."""
        ...


class IMessageQueue(ABC):
    """Abstract interface for message queue operations."""

    @abstractmethod
    def enqueue(self, message: Any) -> str:
        """Add message to queue.

        Args:
            message: Message content to enqueue

        Returns:
            Queue ID of the enqueued message
        """
        pass

    @abstractmethod
    def dequeue(self, batch_size: int | None = None) -> list[IQueueEntry]:
        """Get next messages for processing.

        Args:
            batch_size: Optional number of messages to dequeue

        Returns:
            List of queue entries ready for processing
        """
        pass

    @abstractmethod
    def mark_delivered(self, queue_id: str) -> bool:
        """Mark message as successfully delivered.

        Args:
            queue_id: Queue identifier of delivered message

        Returns:
            True if marked successfully, False otherwise
        """
        pass

    @abstractmethod
    def mark_failed(self, queue_id: str, error: str) -> bool:
        """Mark message as failed.

        Args:
            queue_id: Queue identifier of failed message
            error: Error description

        Returns:
            True if marked successfully, False otherwise
        """
        pass

    @abstractmethod
    def get_statistics(self) -> dict[str, Any]:
        """Get queue statistics.

        Returns:
            Dictionary containing queue metrics and statistics
        """
        pass

    @abstractmethod
    def cleanup_expired(self) -> int:
        """Remove expired entries.

        Returns:
            Number of entries removed
        """
        pass


class IQueuePersistence(ABC):
    """Abstract interface for queue persistence operations."""

    @abstractmethod
    def load_entries(self) -> list[IQueueEntry]:
        """Load queue entries from storage.

        Returns:
            List of queue entries loaded from persistent storage
        """
        pass

    @abstractmethod
    def save_entries(self, entries: list[IQueueEntry]) -> None:
        """Save queue entries to storage.

        Args:
            entries: List of queue entries to persist
        """
        pass

    @abstractmethod
    def atomic_operation(self, operation: callable) -> Any:
        """Perform atomic file operation.

        Args:
            operation: Callable to execute atomically

        Returns:
            Result of the atomic operation
        """
        pass


class IQueueProcessor(ABC):
    """Abstract interface for queue processing operations."""

    @abstractmethod
    async def start_processing(self, interval: float = 5.0) -> None:
        """Start continuous queue processing.

        Args:
            interval: Processing interval in seconds
        """
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
    def max_queue_size(self) -> int:
        """Maximum number of messages in queue."""
        ...

    @property
    def processing_batch_size(self) -> int:
        """Number of messages to process per batch."""
        ...

    @property
    def max_age_days(self) -> int:
        """Maximum age of messages in days before expiration."""
        ...

    @property
    def retry_base_delay(self) -> float:
        """Base delay in seconds for retry operations."""
        ...

    @property
    def retry_max_delay(self) -> float:
        """Maximum delay in seconds for retry operations."""
        ...

    @property
    def cleanup_interval(self) -> int:
        """Interval in seconds between cleanup operations."""
        ...
