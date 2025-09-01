#!/usr/bin/env python3
"""
Message Queue System - Agent Cellphone V2
=========================================

Persistent message queuing system for reliable message delivery.
Stores messages when immediate delivery fails and processes them asynchronously.

Features:
- Persistent queue storage with atomic operations
- Priority-based message processing
- Automatic retry with exponential backoff
- Queue statistics and monitoring
- Integration with file locking system

Architecture:
- Repository Pattern: MessageQueue handles persistent storage
- Service Layer: QueueProcessor orchestrates delivery attempts
- Dependency Injection: Modular components injected via constructor

@maintainer Agent-1 (Integration & Core Systems Specialist)
@license MIT
"""

import os
import json
import time
import uuid
import heapq
from typing import List, Dict, Any, Optional, Callable
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum

from .file_lock import FileLockManager, LockConfig, atomic_file_operation
from ..utils.logger import get_messaging_logger
from ..services.models.messaging_models import UnifiedMessage, UnifiedMessagePriority


class QueueStatus(Enum):
    """Queue entry status values."""
    PENDING = "pending"
    PROCESSING = "processing"
    DELIVERED = "delivered"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class QueueEntry:
    """Message queue entry with metadata."""
    message: UnifiedMessage
    queue_id: str
    priority_score: int
    status: QueueStatus
    created_at: datetime
    updated_at: datetime
    delivery_attempts: int = 0
    max_attempts: int = 5
    next_retry_at: Optional[datetime] = None
    last_error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __lt__(self, other: 'QueueEntry') -> bool:
        """Priority comparison for heap operations."""
        if self.priority_score != other.priority_score:
            return self.priority_score > other.priority_score  # Higher score = higher priority
        return self.created_at < other.created_at  # FIFO within same priority

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "message": {
                "message_id": self.message.message_id,
                "sender": self.message.sender,
                "recipient": self.message.recipient,
                "content": self.message.content,
                "message_type": self.message.message_type.value,
                "priority": self.message.priority.value,
                "timestamp": self.message.timestamp.isoformat() if self.message.timestamp else None,
                "tags": [tag.value for tag in self.message.tags] if self.message.tags else []
            },
            "queue_id": self.queue_id,
            "priority_score": self.priority_score,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "delivery_attempts": self.delivery_attempts,
            "max_attempts": self.max_attempts,
            "next_retry_at": self.next_retry_at.isoformat() if self.next_retry_at else None,
            "last_error": self.last_error,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QueueEntry':
        """Create from dictionary."""
        from ..services.models.messaging_models import UnifiedMessage, UnifiedMessageType, UnifiedMessageTag

        message_data = data["message"]
        message = UnifiedMessage(
            message_id=message_data["message_id"],
            sender=message_data["sender"],
            recipient=message_data["recipient"],
            content=message_data["content"],
            message_type=UnifiedMessageType(message_data["message_type"]),
            priority=UnifiedMessagePriority(message_data["priority"]),
            timestamp=datetime.fromisoformat(message_data["timestamp"]) if message_data["timestamp"] else None,
            tags=[UnifiedMessageTag(tag) for tag in message_data.get("tags", [])]
        )

        return cls(
            message=message,
            queue_id=data["queue_id"],
            priority_score=data["priority_score"],
            status=QueueStatus(data["status"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            delivery_attempts=data["delivery_attempts"],
            max_attempts=data["max_attempts"],
            next_retry_at=datetime.fromisoformat(data["next_retry_at"]) if data.get("next_retry_at") else None,
            last_error=data.get("last_error"),
            metadata=data.get("metadata", {})
        )


@dataclass
class QueueConfig:
    """Configuration for message queue operations."""
    queue_directory: str = "message_queue"
    max_queue_size: int = 10000
    max_age_days: int = 7
    retry_base_delay: float = 1.0
    retry_max_delay: float = 300.0
    processing_batch_size: int = 10
    cleanup_interval: float = 3600.0  # 1 hour


class MessageQueue:
    """
    Persistent message queue with atomic operations and priority processing.

    Provides reliable message queuing with automatic retry and cleanup.
    Integrates with file locking system for thread-safe operations.
    """

    def __init__(self, config: Optional[QueueConfig] = None,
                 lock_config: Optional[LockConfig] = None):
        """Initialize message queue.

        Args:
            config: Queue configuration
            lock_config: File locking configuration
        """
        self.config = config or QueueConfig()
        self.lock_config = lock_config or LockConfig()
        self.lock_manager = FileLockManager(self.lock_config)
        self.logger = get_messaging_logger()

        # Ensure queue directory exists
        self.queue_dir = Path(self.config.queue_directory)
        self.queue_dir.mkdir(parents=True, exist_ok=True)

        # Queue files
        self.pending_file = self.queue_dir / "pending.json"
        self.processing_file = self.queue_dir / "processing.json"
        self.failed_file = self.queue_dir / "failed.json"
        self.delivered_file = self.queue_dir / "delivered.json"

        self.logger.info(f"MessageQueue initialized in {self.queue_dir}")

    def enqueue(self, message: UnifiedMessage, priority: Optional[int] = None) -> str:
        """Add message to queue.

        Args:
            message: Message to queue
            priority: Optional priority score (higher = more urgent)

        Returns:
            str: Queue ID for tracking
        """
        queue_id = str(uuid.uuid4())
        priority_score = priority or self._calculate_priority_score(message)

        entry = QueueEntry(
            message=message,
            queue_id=queue_id,
            priority_score=priority_score,
            status=QueueStatus.PENDING,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        # Atomically add to pending queue
        success = self._add_to_queue_file(self.pending_file, entry)
        if success:
            self.logger.info(f"Message enqueued: {queue_id} ({message.recipient})")
        else:
            self.logger.error(f"Failed to enqueue message: {queue_id}")

        return queue_id

    def dequeue(self) -> Optional[QueueEntry]:
        """Get next message from queue for processing.

        Returns:
            Optional[QueueEntry]: Next message to process, or None if queue empty
        """
        entries = self._load_pending_entries()
        if not entries:
            return None

        # Get highest priority entry
        entry = heapq.heappop(entries)

        # Mark as processing
        entry.status = QueueStatus.PROCESSING
        entry.updated_at = datetime.now()

        # Move to processing file
        self._save_processing_entry(entry)
        self._save_pending_entries(entries)

        self.logger.debug(f"Message dequeued for processing: {entry.queue_id}")
        return entry

    def mark_delivered(self, queue_id: str) -> bool:
        """Mark message as successfully delivered.

        Args:
            queue_id: Queue ID to mark as delivered

        Returns:
            bool: True if marked successfully
        """
        return self._move_entry(queue_id, self.processing_file, self.delivered_file, QueueStatus.DELIVERED)

    def mark_failed(self, queue_id: str, error: str, retry: bool = True) -> bool:
        """Mark message as failed.

        Args:
            queue_id: Queue ID to mark as failed
            error: Error message
            retry: Whether to schedule retry

        Returns:
            bool: True if marked successfully
        """
        entry = self._get_processing_entry(queue_id)
        if not entry:
            return False

        entry.status = QueueStatus.FAILED
        entry.last_error = error
        entry.delivery_attempts += 1
        entry.updated_at = datetime.now()

        if retry and entry.delivery_attempts < entry.max_attempts:
            # Schedule retry with exponential backoff
            delay = min(
                self.config.retry_base_delay * (2 ** (entry.delivery_attempts - 1)),
                self.config.retry_max_delay
            )
            entry.next_retry_at = datetime.now() + timedelta(seconds=delay)
            entry.status = QueueStatus.PENDING

            # Move back to pending
            self._move_to_pending(entry)
        else:
            # Move to failed
            self._move_to_failed(entry)

        return True

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get comprehensive queue statistics.

        Returns:
            Dict[str, Any]: Queue statistics
        """
        stats = {
            "pending_count": 0,
            "processing_count": 0,
            "delivered_count": 0,
            "failed_count": 0,
            "total_count": 0,
            "oldest_pending": None,
            "newest_pending": None
        }

        # Count entries in each file
        stats["pending_count"] = len(self._load_pending_entries())
        stats["processing_count"] = len(self._load_processing_entries())
        stats["delivered_count"] = len(self._load_delivered_entries())
        stats["failed_count"] = len(self._load_failed_entries())
        stats["total_count"] = (stats["pending_count"] + stats["processing_count"] +
                               stats["delivered_count"] + stats["failed_count"])

        # Get age stats for pending entries
        pending_entries = self._load_pending_entries()
        if pending_entries:
            oldest = min(entry.created_at for entry in pending_entries)
            newest = max(entry.created_at for entry in pending_entries)
            stats["oldest_pending"] = oldest.isoformat()
            stats["newest_pending"] = newest.isoformat()

        return stats

    def cleanup_expired_entries(self) -> int:
        """Clean up expired entries from all queues.

        Returns:
            int: Number of entries cleaned up
        """
        cleaned = 0
        cutoff_date = datetime.now() - timedelta(days=self.config.max_age_days)

        # Clean pending entries
        pending_entries = self._load_pending_entries()
        active_pending = [e for e in pending_entries if e.created_at > cutoff_date]
        expired_count = len(pending_entries) - len(active_pending)
        if expired_count > 0:
            self._save_pending_entries(active_pending)
            cleaned += expired_count

        # Clean failed entries
        failed_entries = self._load_failed_entries()
        active_failed = [e for e in failed_entries if e.created_at > cutoff_date]
        expired_count = len(failed_entries) - len(active_failed)
        if expired_count > 0:
            self._save_failed_entries(active_failed)
            cleaned += expired_count

        if cleaned > 0:
            self.logger.info(f"Cleaned up {cleaned} expired queue entries")

        return cleaned

    def retry_failed_messages(self) -> int:
        """Retry messages that are scheduled for retry.

        Returns:
            int: Number of messages moved to pending for retry
        """
        processing_entries = self._load_processing_entries()
        pending_entries = self._load_pending_entries()

        retry_count = 0
        now = datetime.now()

        # Find entries ready for retry
        for entry in processing_entries:
            if (entry.status == QueueStatus.FAILED and
                entry.next_retry_at and
                entry.next_retry_at <= now and
                entry.delivery_attempts < entry.max_attempts):

                entry.status = QueueStatus.PENDING
                entry.updated_at = now
                pending_entries.append(entry)
                retry_count += 1

        if retry_count > 0:
            heapq.heapify(pending_entries)  # Restore heap property
            self._save_pending_entries(pending_entries)
            self.logger.info(f"Moved {retry_count} messages to pending for retry")

        return retry_count

    def _calculate_priority_score(self, message: UnifiedMessage) -> int:
        """Calculate priority score for message.

        Args:
            message: Message to score

        Returns:
            int: Priority score (higher = more urgent)
        """
        score = 0

        # Priority-based scoring
        if message.priority == UnifiedMessagePriority.URGENT:
            score += 100
        else:
            score += 10

        # Message type scoring
        from ..services.models.messaging_models import UnifiedMessageType
        if message.message_type == UnifiedMessageType.BROADCAST:
            score += 50
        elif message.message_type == UnifiedMessageType.ONBOARDING:
            score += 75

        # Age-based scoring (newer messages get slight boost)
        if message.timestamp:
            age_hours = (datetime.now() - message.timestamp).total_seconds() / 3600
            score += max(0, 10 - int(age_hours))  # Boost for newer messages

        return score

    def _add_to_queue_file(self, queue_file: Path, entry: QueueEntry) -> bool:
        """Add entry to queue file atomically."""
        def update_func(current: str) -> str:
            entries = []
            if current.strip():
                try:
                    entries_data = json.loads(current)
                    entries = [QueueEntry.from_dict(e) for e in entries_data]
                except json.JSONDecodeError:
                    entries = []

            entries.append(entry)

            # For pending queue, maintain heap property
            if "pending" in str(queue_file):
                heapq.heapify(entries)

            return json.dumps([e.to_dict() for e in entries], indent=2)

        return self.lock_manager.atomic_update(
            str(queue_file),
            update_func,
            operation="queue_add",
            metadata={"queue_id": entry.queue_id}
        )

    def _load_pending_entries(self) -> List[QueueEntry]:
        """Load pending entries from file."""
        return self._load_entries_from_file(self.pending_file)

    def _load_processing_entries(self) -> List[QueueEntry]:
        """Load processing entries from file."""
        return self._load_entries_from_file(self.processing_file)

    def _load_delivered_entries(self) -> List[QueueEntry]:
        """Load delivered entries from file."""
        return self._load_entries_from_file(self.delivered_file)

    def _load_failed_entries(self) -> List[QueueEntry]:
        """Load failed entries from file."""
        return self._load_entries_from_file(self.failed_file)

    def _load_entries_from_file(self, queue_file: Path) -> List[QueueEntry]:
        """Load entries from queue file."""
        content = self.lock_manager.atomic_read(str(queue_file), operation="queue_load")
        if not content:
            return []

        try:
            entries_data = json.loads(content)
            return [QueueEntry.from_dict(e) for e in entries_data]
        except json.JSONDecodeError:
            self.logger.error(f"Corrupted queue file: {queue_file}")
            return []

    def _save_pending_entries(self, entries: List[QueueEntry]) -> bool:
        """Save pending entries to file."""
        return self._save_entries_to_file(self.pending_file, entries)

    def _save_processing_entry(self, entry: QueueEntry) -> bool:
        """Save processing entry to file."""
        return self._add_to_queue_file(self.processing_file, entry)

    def _save_delivered_entries(self, entries: List[QueueEntry]) -> bool:
        """Save delivered entries to file."""
        return self._save_entries_to_file(self.delivered_file, entries)

    def _save_failed_entries(self, entries: List[QueueEntry]) -> bool:
        """Save failed entries to file."""
        return self._save_entries_to_file(self.failed_file, entries)

    def _save_entries_to_file(self, queue_file: Path, entries: List[QueueEntry]) -> bool:
        """Save entries to queue file atomically."""
        entries_data = [e.to_dict() for e in entries]
        return self.lock_manager.atomic_write(
            str(queue_file),
            json.dumps(entries_data, indent=2),
            operation="queue_save",
            metadata={"entry_count": len(entries)}
        )

    def _get_processing_entry(self, queue_id: str) -> Optional[QueueEntry]:
        """Get entry from processing queue."""
        entries = self._load_processing_entries()
        for entry in entries:
            if entry.queue_id == queue_id:
                return entry
        return None

    def _move_entry(self, queue_id: str, from_file: Path, to_file: Path, new_status: QueueStatus) -> bool:
        """Move entry between queue files."""
        # Load source entries
        source_entries = self._load_entries_from_file(from_file)

        # Find and remove entry
        entry = None
        remaining_entries = []
        for e in source_entries:
            if e.queue_id == queue_id:
                entry = e
            else:
                remaining_entries.append(e)

        if not entry:
            return False

        # Update entry status
        entry.status = new_status
        entry.updated_at = datetime.now()

        # Save updated source
        self._save_entries_to_file(from_file, remaining_entries)

        # Add to destination
        return self._add_to_queue_file(to_file, entry)

    def _move_to_pending(self, entry: QueueEntry) -> bool:
        """Move entry back to pending queue."""
        entry.status = QueueStatus.PENDING
        pending_entries = self._load_pending_entries()
        pending_entries.append(entry)
        heapq.heapify(pending_entries)
        return self._save_pending_entries(pending_entries)

    def _move_to_failed(self, entry: QueueEntry) -> bool:
        """Move entry to failed queue."""
        failed_entries = self._load_failed_entries()
        failed_entries.append(entry)
        return self._save_failed_entries(failed_entries)


class QueueProcessor:
    """
    Message queue processor with automatic retry and monitoring.

    Processes queued messages asynchronously with configurable batch sizes
    and retry policies.
    """

    def __init__(self, queue: MessageQueue, delivery_func: Callable[[UnifiedMessage], bool],
                 config: Optional[QueueConfig] = None):
        """Initialize queue processor.

        Args:
            queue: Message queue to process
            delivery_func: Function to attempt message delivery
            config: Queue processor configuration
        """
        self.queue = queue
        self.delivery_func = delivery_func
        self.config = config or QueueConfig()
        self.logger = get_messaging_logger()
        self.processing = False

    def start_processing(self) -> None:
        """Start queue processing loop."""
        if self.processing:
            self.logger.warning("Queue processor already running")
            return

        self.processing = True
        self.logger.info("Queue processor started")

        try:
            while self.processing:
                self._process_batch()
                time.sleep(1)  # Brief pause between batches
        except Exception as e:
            self.logger.error(f"Queue processor error: {e}")
        finally:
            self.processing = False
            self.logger.info("Queue processor stopped")

    def stop_processing(self) -> None:
        """Stop queue processing."""
        self.processing = False
        self.logger.info("Queue processor stop requested")

    def process_batch(self) -> int:
        """Process one batch of messages.

        Returns:
            int: Number of messages processed
        """
        return self._process_batch()

    def _process_batch(self) -> int:
        """Process a batch of messages from the queue."""
        processed = 0

        for _ in range(self.config.processing_batch_size):
            entry = self.queue.dequeue()
            if not entry:
                break

            try:
                # Attempt delivery
                success = self.delivery_func(entry.message)

                if success:
                    self.queue.mark_delivered(entry.queue_id)
                    self.logger.info(f"Message delivered: {entry.queue_id}")
                else:
                    self.queue.mark_failed(entry.queue_id, "Delivery failed")
                    self.logger.warning(f"Message delivery failed: {entry.queue_id}")

            except Exception as e:
                error_msg = f"Delivery exception: {str(e)}"
                self.queue.mark_failed(entry.queue_id, error_msg)
                self.logger.error(f"Message processing error: {entry.queue_id} - {error_msg}")

            processed += 1

        # Clean up and retry operations
        if processed > 0:
            self.queue.cleanup_expired_entries()
            self.queue.retry_failed_messages()

        return processed
