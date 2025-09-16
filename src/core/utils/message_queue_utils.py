import logging
logger = logging.getLogger(__name__)
#!/usr/bin/env python3
"""
Message Queue Utilities - Agent Cellphone V2
===========================================

Utility functions for message queue system.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import datetime
from datetime import timedelta
import heapq
from typing import List, Dict, Any


class MessageQueueUtils:
    """Utility functions for message queue operations."""

    @staticmethod
    def calculate_priority_score(priority: str, created_at: datetime) -> int:
        """Calculate priority score based on priority and timestamp."""
        base_scores = {"high": 100, "medium": 50, "low": 10}
        return base_scores.get(priority, 0)


def get_example_usage():
    """
    Example usage for MessageQueueUtils.
    
    # Import the core component
    from src.core.utils.message_queue_utils import MessageQueueUtils

# Import the core component
from src.core.utils.message_queue_utils import Message_Queue_Utils

# Initialize with configuration
config = {
    "setting1": "value1",
    "setting2": "value2"
}

component = Message_Queue_Utils(config)

# Execute primary functionality
result = component.process_data(input_data)
logger.info(f"Processing result: {result}")

# Advanced usage with error handling
try:
    advanced_result = component.advanced_operation(data, options={"optimize": True})
    logger.info(f"Advanced operation completed: {advanced_result}")
except ProcessingError as e:
    logger.info(f"Operation failed: {e}")
    # Implement recovery logic

        """Calculate priority score for queue entry."""
        base_scores = {"urgent": 1000, "normal": 500, "low": 100}

        base_score = base_scores.get(priority, 500)

        # Age penalty: older messages get lower priority
        age_hours = (datetime.now() - created_at).total_seconds() / 3600
        age_penalty = int(age_hours * 10)  # 10 points per hour

        return max(0, base_score - age_penalty)

    @staticmethod
    def calculate_retry_delay(attempt: int, base_delay: float, max_delay: float) -> float:
        """Calculate exponential backoff delay for retries."""
        delay = base_delay * (2**attempt)
        return min(delay, max_delay)

    @staticmethod
    def is_entry_ready_for_retry(entry: QueueEntry) -> bool:
        """Check if queue entry is ready for retry."""
        if entry.status != QueueStatus.FAILED:
            return False

        if entry.delivery_attempts >= entry.max_attempts:
            return False

        if entry.next_retry_at is None:
            return True

        return datetime.now() >= entry.next_retry_at

    @staticmethod
    def is_entry_expired(entry: QueueEntry, max_age_days: int) -> bool:
        """Check if queue entry has expired."""
        max_age = timedelta(days=max_age_days)
        return datetime.now() - entry.created_at > max_age

    @staticmethod
    def build_priority_heap(entries: List[QueueEntry]) -> List[QueueEntry]:
        """Build priority heap from queue entries."""
        heap = []
        for entry in entries:
            if entry.status == QueueStatus.PENDING:
                heapq.heappush(heap, entry)
        return heap

    @staticmethod
    def get_next_entries_for_processing(
        heap: List[QueueEntry], batch_size: int, max_age_days: int
    ) -> List[QueueEntry]:
        """Get next entries for processing from priority heap."""
        entries_to_process = []

        while heap and len(entries_to_process) < batch_size:
            entry = heapq.heappop(heap)

            # Skip expired entries
            if MessageQueueUtils.is_entry_expired(entry, max_age_days):
                entry.status = QueueStatus.EXPIRED
                continue

            # Skip entries not ready for retry
            if (
                entry.status == QueueStatus.FAILED
                and not MessageQueueUtils.is_entry_ready_for_retry(entry)
            ):
                heapq.heappush(heap, entry)  # Put back in heap
                continue

            entries_to_process.append(entry)

        return entries_to_process

    @staticmethod
    def update_entry_for_retry(entry: QueueEntry, base_delay: float, max_delay: float) -> None:
        """Update queue entry for retry with exponential backoff."""
        entry.delivery_attempts += 1
        entry.status = QueueStatus.FAILED

        if entry.delivery_attempts < entry.max_attempts:
            retry_delay = MessageQueueUtils.calculate_retry_delay(
                entry.delivery_attempts, base_delay, max_delay
            )
            entry.next_retry_at = datetime.now() + timedelta(seconds=retry_delay)
        else:
            entry.next_retry_at = None

        entry.updated_at = datetime.now()

    @staticmethod
    def mark_entry_delivered(entry: QueueEntry) -> None:
        """Mark queue entry as delivered."""
        entry.status = QueueStatus.DELIVERED
        entry.updated_at = datetime.now()
        entry.last_error = None

    @staticmethod
    def mark_entry_failed(entry: QueueEntry, error: str) -> None:
        """Mark queue entry as failed with error message."""
        entry.status = QueueStatus.FAILED
        entry.updated_at = datetime.now()
        entry.last_error = error

    @staticmethod
    def mark_entry_processing(entry: QueueEntry) -> None:
        """Mark queue entry as processing."""
        entry.status = QueueStatus.PROCESSING
        entry.updated_at = datetime.now()

    @staticmethod
    def calculate_queue_statistics(entries: List[QueueEntry]) -> Dict[str, Any]:
        """Calculate queue statistics from entries."""
        total_entries = len(entries)

        status_counts = {}
        for status in QueueStatus:
            status_counts[status.value] = sum(1 for entry in entries if entry.status == status)

        # Calculate age statistics
        now = datetime.now()
        ages = [(now - entry.created_at).total_seconds() / 3600 for entry in entries]

        age_stats = {
            "avg_age_hours": sum(ages) / len(ages) if ages else 0,
            "max_age_hours": max(ages) if ages else 0,
            "min_age_hours": min(ages) if ages else 0,
        }

        # Calculate retry statistics
        retry_attempts = [
            entry.delivery_attempts for entry in entries if entry.delivery_attempts > 0
        ]
        retry_stats = {
            "avg_retry_attempts": (
                sum(retry_attempts) / len(retry_attempts) if retry_attempts else 0
            ),
            "max_retry_attempts": max(retry_attempts) if retry_attempts else 0,
            "total_retry_attempts": sum(retry_attempts),
        }

        return {
            "total_entries": total_entries,
            "status_counts": status_counts,
            "age_statistics": age_stats,
            "retry_statistics": retry_stats,
            "queue_health": {
                "pending_ratio": (
                    status_counts.get("pending", 0) / total_entries if total_entries > 0 else 0
                ),
                "failed_ratio": (
                    status_counts.get("failed", 0) / total_entries if total_entries > 0 else 0
                ),
                "delivered_ratio": (
                    status_counts.get("delivered", 0) / total_entries if total_entries > 0 else 0
                ),
            },
        }

    @staticmethod
    def cleanup_expired_entries(entries: List[QueueEntry], max_age_days: int) -> List[QueueEntry]:
        """Remove expired entries from the list."""
        active_entries = []
        expired_count = 0

        for entry in entries:
            if MessageQueueUtils.is_entry_expired(entry, max_age_days):
                entry.status = QueueStatus.EXPIRED
                expired_count += 1
            else:
                active_entries.append(entry)

        return active_entries

    @staticmethod
    def validate_queue_config(config: QueueConfig) -> List[str]:
        """Validate queue configuration and return any issues."""
        issues = []

        if config.max_queue_size <= 0:
            issues.append("max_queue_size must be positive")

        if config.max_age_days <= 0:
            issues.append("max_age_days must be positive")

        if config.retry_base_delay <= 0:
            issues.append("retry_base_delay must be positive")

        if config.retry_max_delay <= config.retry_base_delay:
            issues.append("retry_max_delay must be greater than retry_base_delay")

        if config.processing_batch_size <= 0:
            issues.append("processing_batch_size must be positive")

        if config.cleanup_interval <= 0:
            issues.append("cleanup_interval must be positive")

        return issues
