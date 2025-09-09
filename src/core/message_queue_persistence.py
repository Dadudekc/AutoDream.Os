"""
Message Queue Persistence - V2 Compliance Module
===============================================

Handles queue persistence operations following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable

from .message_queue_interfaces import IQueuePersistence, IQueueEntry


class FileQueuePersistence(IQueuePersistence):
    """Handles file-based queue persistence operations."""

    def __init__(self, queue_file: Path, lock_manager: Optional[Any] = None):
        """Initialize file persistence."""
        self.queue_file = queue_file
        self.lock_manager = lock_manager

    def load_entries(self) -> List[IQueueEntry]:
        """Load queue entries from JSON file."""
        if not self.queue_file.exists():
            return []

        try:
            with open(self.queue_file, encoding="utf-8") as f:
                data = json.load(f)

            return [QueueEntry.from_dict(entry_data) for entry_data in data]
        except (json.JSONDecodeError, KeyError, ValueError, FileNotFoundError) as e:
            # Log error and return empty list
            print(f"Failed to load queue entries: {e}")
            return []

    def save_entries(self, entries: List[IQueueEntry]) -> None:
        """Save queue entries to JSON file."""
        try:
            data = [entry.to_dict() for entry in entries]

            # Direct write for better performance
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(data, f, separators=(',', ':'), ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Failed to save queue entries: {e}")
            raise

    def atomic_operation(self, operation: Callable[[], Any]) -> Any:
        """Perform atomic file operation with locking."""
        if self.lock_manager:
            # Use provided lock manager for atomic operations
            return self.lock_manager.atomic_operation(self.queue_file, operation)
        else:
            # Simple atomic operation without locking
            return operation()


class QueueEntry:
    """Queue entry data structure."""

    def __init__(
        self,
        message: Any,
        queue_id: str,
        priority_score: float,
        status: str,
        created_at: Any,
        updated_at: Any,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize queue entry."""
        self.message = message
        self.queue_id = queue_id
        self.priority_score = priority_score
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'message': self.message,
            'queue_id': self.queue_id,
            'priority_score': self.priority_score,
            'status': self.status,
            'created_at': self.created_at.isoformat() if hasattr(self.created_at, 'isoformat') else str(self.created_at),
            'updated_at': self.updated_at.isoformat() if hasattr(self.updated_at, 'isoformat') else str(self.updated_at),
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueueEntry':
        """Create from dictionary."""
        return cls(
            message=data['message'],
            queue_id=data['queue_id'],
            priority_score=data['priority_score'],
            status=data['status'],
            created_at=data['created_at'],
            updated_at=data['updated_at'],
            metadata=data.get('metadata', {})
        )
