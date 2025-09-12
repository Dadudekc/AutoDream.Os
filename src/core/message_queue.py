#!/usr/bin/env python3
"""
Message Queue System - Agent Cellphone V2
=========================================

Persistent message queuing system following SOLID principles.

SOLID Principles:
- SRP: Each class has single responsibility
- OCP: Open for extension, closed for modification
- LSP: Proper inheritance hierarchies
- ISP: Small, specific interfaces
- DIP: Dependency injection for abstractions

Architecture:
- Repository Pattern: MessageQueue handles persistent storage
- Service Layer: QueueProcessor orchestrates delivery attempts
- Dependency Injection: Modular components injected via constructor

@maintainer Agent-1 (System Recovery Specialist)
@license MIT
"""

import asyncio
import uuid
from collections.abc import Callable
from datetime import datetime
from pathlib import Path
from typing import Any

from .message_queue_interfaces import (
    IMessageQueue,
    IMessageQueueLogger,
    IQueueEntry,
    IQueuePersistence,
    IQueueProcessor,
)
from .message_queue_persistence import FileQueuePersistence, QueueEntry
from .message_queue_pyautogui_integration import create_queue_pyautogui_delivery_callback
from .message_queue_statistics import QueueHealthMonitor, QueueStatisticsCalculator


class QueueConfig:
    """Configuration for message queue."""

    def __init__(
        self,
        queue_directory: str = "message_queue",
        max_queue_size: int = 1000,
        processing_batch_size: int = 10,
        max_age_days: int = 7,
        retry_base_delay: float = 1.0,
        retry_max_delay: float = 300.0,
        cleanup_interval: int = 3600,
        enable_pyautogui_delivery: bool = True,
        default_delivery_method: str = "pyautogui",
    ):
        """Initialize queue configuration."""
        self.queue_directory = queue_directory
        self.max_queue_size = max_queue_size
        self.processing_batch_size = processing_batch_size
        self.max_age_days = max_age_days
        self.retry_base_delay = retry_base_delay
        self.retry_max_delay = retry_max_delay
        self.cleanup_interval = cleanup_interval
        self.enable_pyautogui_delivery = enable_pyautogui_delivery
        self.default_delivery_method = default_delivery_method


class MessageQueue(IMessageQueue):
    """SOLID-compliant message queue with dependency injection.

    Provides reliable message queuing with automatic retry and cleanup.
    Follows Single Responsibility Principle with separate persistence layer.
    """

    def __init__(
        self,
        config: QueueConfig | None = None,
        persistence: IQueuePersistence | None = None,
        statistics_calculator: QueueStatisticsCalculator | None = None,
        health_monitor: QueueHealthMonitor | None = None,
        logger: IMessageQueueLogger | None = None,
    ):
        """Initialize message queue with dependency injection."""
        self.config = config or QueueConfig()
        self.persistence = persistence or FileQueuePersistence(
            Path(self.config.queue_directory) / "queue.json"
        )
        self.statistics_calculator = statistics_calculator or QueueStatisticsCalculator()
        self.health_monitor = health_monitor or QueueHealthMonitor(self.statistics_calculator)
        self.logger = logger

        # Initialize PyAutoGUI delivery if enabled
        self.pyautogui_callback = None
        if self.config.enable_pyautogui_delivery:
            try:
                self.pyautogui_callback = create_queue_pyautogui_delivery_callback()
                if self.logger:
                    self.logger.info("PyAutoGUI delivery enabled for message queue")
            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to initialize PyAutoGUI delivery: {e}")

        # Initialize queue file
        queue_file = Path(self.config.queue_directory) / "queue.json"
        queue_file.parent.mkdir(parents=True, exist_ok=True)

    def enqueue(
        self,
        message: Any,
        delivery_callback: Callable[[Any], bool] | None = None,
        use_pyautogui: bool | None = None,
    ) -> str:
        """Add message to queue with priority-based ordering.

        Args:
            message: Message to queue
            delivery_callback: Optional callback for delivery attempts
            use_pyautogui: Whether to use PyAutoGUI delivery (defaults to config setting)

        Returns:
            Queue ID for tracking
        """
        # Determine delivery method
        if use_pyautogui is None:
            use_pyautogui = self.config.enable_pyautogui_delivery

        # Set PyAutoGUI callback if requested and not already set
        if use_pyautogui and delivery_callback is None and self.pyautogui_callback:
            delivery_callback = self.pyautogui_callback

        queue_id = str(uuid.uuid4())
        now = datetime.now()

        # Calculate priority score (simplified for now)
        priority_score = self._calculate_priority_score(message, now)

        # Create queue entry
        entry = QueueEntry(
            message=message,
            queue_id=queue_id,
            priority_score=priority_score,
            status="PENDING",
            created_at=now,
            updated_at=now,
            metadata={
                "delivery_callback": delivery_callback is not None,
                "delivery_method": "pyautogui" if use_pyautogui else "default",
            },
        )

        # Atomic enqueue operation using persistence layer
        def _enqueue_operation():
            entries = self.persistence.load_entries()

            # Check queue size limit
            if len(entries) >= self.config.max_queue_size:
                raise RuntimeError(f"Queue size limit exceeded: {self.config.max_queue_size}")

            entries.append(entry)
            self.persistence.save_entries(entries)

            delivery_info = " with PyAutoGUI delivery" if use_pyautogui else ""
            if self.logger:
                self.logger.info(
                    f"Message queued: {queue_id} (priority: {priority_score}){delivery_info}"
                )
            return queue_id

        return self.persistence.atomic_operation(_enqueue_operation)

    def enqueue_with_pyautogui(
        self, message: Any, recipient: str, message_type: str = "text", priority: str = "regular"
    ) -> str:
        """Convenience method to enqueue message with PyAutoGUI delivery.

        Args:
            message: Message content
            recipient: Target agent
            message_type: Type of message
            priority: Message priority

        Returns:
            Queue ID for tracking
        """
        # Format message for PyAutoGUI delivery
        formatted_message = {
            "content": str(message),
            "recipient": recipient,
            "sender": "system",
            "message_type": message_type,
            "priority": priority,
        }

        return self.enqueue(formatted_message, use_pyautogui=True)

    def enqueue_broadcast_with_pyautogui(self, message: Any, sender: str = "system") -> str:
        """Convenience method to enqueue broadcast message with PyAutoGUI delivery.

        Args:
            message: Message content
            sender: Message sender

        Returns:
            Queue ID for tracking
        """
        # Format broadcast message
        formatted_message = {
            "content": str(message),
            "recipient": "broadcast",
            "sender": sender,
            "message_type": "broadcast",
            "priority": "urgent",
        }

        return self.enqueue(formatted_message, use_pyautogui=True)

    def _calculate_priority_score(self, message: Any, now: datetime) -> float:
        """Calculate priority score for message."""
        # Simplified priority calculation
        if hasattr(message, "priority"):
            if hasattr(message.priority, "value"):
                return float(message.priority.value)
            elif isinstance(message.priority, (int, float)):
                return float(message.priority)

        # Default priority
        return 0.5

    def dequeue(self, batch_size: int | None = None) -> list[IQueueEntry]:
        """Get next messages for processing based on priority.

        Args:
            batch_size: Number of messages to retrieve (defaults to config)

        Returns:
            List of queue entries ready for processing
        """
        batch_size = batch_size or self.config.processing_batch_size

        def _dequeue_operation():
            entries = self.persistence.load_entries()

            # More efficient priority queue using heap
            import heapq

            # Create max-heap by negating priority scores
            pending_entries = [
                (-getattr(e, "priority_score", 0), i, e)
                for i, e in enumerate(entries)
                if getattr(e, "status", "") == "PENDING"
            ]

            if not pending_entries:
                return []

            # Get top priority entries
            heapq.heapify(pending_entries)
            entries_to_process = []

            for _ in range(min(batch_size, len(pending_entries))):
                neg_priority, original_index, entry = heapq.heappop(pending_entries)
                entry.status = "PROCESSING"
                entry.updated_at = datetime.now()
                entries_to_process.append(entry)

            # Save updated entries
            self.persistence.save_entries(entries)

            if self.logger:
                self.logger.info(f"Dequeued {len(entries_to_process)} messages for processing")
            return entries_to_process

        return self.persistence.atomic_operation(_dequeue_operation)

    def mark_delivered(self, queue_id: str) -> bool:
        """Mark message as successfully delivered."""

        def _mark_delivered_operation():
            entries = self.persistence.load_entries()

            for entry in entries:
                if getattr(entry, "queue_id", "") == queue_id:
                    entry.status = "DELIVERED"
                    entry.updated_at = datetime.now()
                    self.persistence.save_entries(entries)
                    if self.logger:
                        self.logger.info(f"Message marked as delivered: {queue_id}")
                    return True

            if self.logger:
                self.logger.warning(f"Queue entry not found: {queue_id}")
            return False

        return self.persistence.atomic_operation(_mark_delivered_operation)

    def mark_failed(self, queue_id: str, error: str) -> bool:
        """Mark message as failed and schedule retry."""

        def _mark_failed_operation():
            entries = self.persistence.load_entries()

            for entry in entries:
                if getattr(entry, "queue_id", "") == queue_id:
                    entry.status = "FAILED"
                    entry.updated_at = datetime.now()

                    # Update delivery attempts
                    if not hasattr(entry, "delivery_attempts"):
                        entry.delivery_attempts = 0
                    entry.delivery_attempts += 1

                    # Add error to metadata
                    if not hasattr(entry, "metadata"):
                        entry.metadata = {}
                    entry.metadata["last_error"] = error

                    self.persistence.save_entries(entries)
                    if self.logger:
                        self.logger.warning(f"Message marked as failed: {queue_id} - {error}")
                    return True

            if self.logger:
                self.logger.warning(f"Queue entry not found: {queue_id}")
            return False

        return self.persistence.atomic_operation(_mark_failed_operation)

    def get_statistics(self) -> dict[str, Any]:
        """Get comprehensive queue statistics."""

        def _get_statistics_operation():
            entries = self.persistence.load_entries()
            return self.statistics_calculator.calculate_statistics(entries)

        return self.persistence.atomic_operation(_get_statistics_operation)

    def cleanup_expired(self) -> int:
        """Remove expired entries from queue."""

        def _cleanup_operation():
            entries = self.persistence.load_entries()
            original_count = len(entries)

            # Filter out expired entries
            max_age_seconds = self.config.max_age_days * 24 * 60 * 60
            now = datetime.now()

            active_entries = []
            for entry in entries:
                if hasattr(entry, "created_at"):
                    age = (now - entry.created_at).total_seconds()
                    if age <= max_age_seconds:
                        active_entries.append(entry)
                else:
                    active_entries.append(entry)  # Keep entries without timestamp

            expired_count = original_count - len(active_entries)
            self.persistence.save_entries(active_entries)

            if expired_count > 0 and self.logger:
                self.logger.info(f"Cleaned up {expired_count} expired entries")

            return expired_count

        return self.persistence.atomic_operation(_cleanup_operation)

    def get_health_status(self) -> dict[str, Any]:
        """Get comprehensive queue health status."""

        def _get_health_operation():
            entries = self.persistence.load_entries()
            return self.health_monitor.assess_health(entries)

        return self.persistence.atomic_operation(_get_health_operation)

    def get_pyautogui_delivery_stats(self) -> dict[str, Any]:
        """Get PyAutoGUI delivery statistics if available."""
        try:
            from .message_queue_pyautogui_integration import get_queue_delivery_statistics

            return get_queue_delivery_statistics()
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Could not get PyAutoGUI delivery stats: {e}")
            return {
                "total_attempts": 0,
                "successful_deliveries": 0,
                "failed_deliveries": 0,
                "success_rate": 0.0,
            }


class AsyncQueueProcessor(IQueueProcessor):
    """SOLID-compliant asynchronous queue processor.

    Processes queued messages with retry logic and error handling.
    Follows Single Responsibility Principle with focused processing logic.
    """

    def __init__(
        self,
        queue: IMessageQueue,
        delivery_callback: Callable[[Any], bool] | None = None,
        logger: IMessageQueueLogger | None = None,
    ):
        """Initialize queue processor with dependency injection."""
        self.queue = queue
        self.delivery_callback = delivery_callback
        self.logger = logger
        self.running = False
        self.last_cleanup = 0.0

        # Use PyAutoGUI callback if available and none provided
        if (
            self.delivery_callback is None
            and hasattr(queue, "pyautogui_callback")
            and queue.pyautogui_callback
        ):
            self.delivery_callback = queue.pyautogui_callback
            if self.logger:
                self.logger.info("Using PyAutoGUI delivery callback for queue processor")

    async def start_processing(self, interval: float = 5.0) -> None:
        """Start continuous queue processing."""
        self.running = True
        if self.logger:
            self.logger.info("Queue processor started")

        while self.running:
            try:
                await self.process_batch()
                await self._cleanup_if_needed(interval)
                await asyncio.sleep(interval)
            except Exception as e:
                if self.logger:
                    self.logger.error(f"Queue processing error: {e}")
                await asyncio.sleep(interval)

    def stop_processing(self) -> None:
        """Stop queue processing."""
        self.running = False
        if self.logger:
            self.logger.info("Queue processor stopped")

    async def process_batch(self) -> None:
        """Process a batch of queued messages."""
        entries = self.queue.dequeue()

        for entry in entries:
            try:
                message = getattr(entry, "message", None)
                queue_id = getattr(entry, "queue_id", "")

                if message is None:
                    if self.logger:
                        self.logger.warning(f"Entry missing message: {queue_id}")
                    continue

                success = self.delivery_callback(message)

                if success:
                    self.queue.mark_delivered(queue_id)
                else:
                    self.queue.mark_failed(queue_id, "Delivery callback returned False")

            except Exception as e:
                queue_id = getattr(entry, "queue_id", "unknown")
                self.queue.mark_failed(queue_id, str(e))

    async def _cleanup_if_needed(self, interval: float) -> None:
        """Perform cleanup if interval has passed."""
        import time

        now = time.time()
        cleanup_interval = getattr(self.queue.config, "cleanup_interval", 3600)

        if now - self.last_cleanup >= cleanup_interval:
            expired_count = self.queue.cleanup_expired()
            if expired_count > 0 and self.logger:
                self.logger.info(f"Cleanup completed: {expired_count} expired entries removed")
            self.last_cleanup = now


# Backward compatibility alias
QueueProcessor = AsyncQueueProcessor
