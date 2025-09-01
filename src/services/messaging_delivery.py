#!/usr/bin/env python3
"""
Messaging Delivery Module - Agent Cellphone V2
=============================================

Inbox delivery functionality for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import os
import time
from typing import Dict, Any, Optional

from .models.messaging_models import UnifiedMessage
from ..utils.logger import get_messaging_logger
from ..core.metrics import MessagingMetrics
from ..core.file_lock import FileLockManager, LockConfig
from ..core.message_queue import MessageQueue, QueueConfig, QueueProcessor


class MessagingDelivery:
    """Handles message delivery to agent inboxes."""

    def __init__(self, inbox_paths: Dict[str, str], metrics: MessagingMetrics,
                 lock_config: Optional[LockConfig] = None,
                 queue_config: Optional[QueueConfig] = None):
        """Initialize delivery service."""
        self.inbox_paths = inbox_paths
        self.metrics = metrics
        self.logger = get_messaging_logger()
        self.lock_manager = FileLockManager(lock_config)

        # Initialize message queue
        self.queue = MessageQueue(queue_config, lock_config)
        self.queue_processor = QueueProcessor(self.queue, self._deliver_message_immediate)

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3,
                             use_queue: bool = True) -> bool:
        """Send message to agent's inbox file with queuing support.

        Args:
            message: The UnifiedMessage to deliver
            max_retries: Maximum number of retry attempts
            use_queue: Whether to queue message if immediate delivery fails

        Returns:
            bool: True if delivery successful or queued, False only on critical errors
        """
        try:
            # First attempt immediate delivery
            success = self._deliver_message_immediate(message)

            if success:
                self.logger.info(f"Message delivered immediately: {message.message_id}")
                return True

            # If immediate delivery failed and queuing is enabled
            if use_queue:
                queue_id = self.queue.enqueue(message)
                self.logger.info(f"Message queued for later delivery: {message.message_id} (queue_id: {queue_id})")

                # Record queue metrics (V2 compliance)
                self.metrics.record_message_queued(message.message_type.value, message.recipient)

                return True  # Message successfully queued

            return False

        except Exception as e:
            self.logger.error(f"Critical error in message delivery: {e}")
            return False

    def _deliver_message_immediate(self, message: UnifiedMessage) -> bool:
        """Attempt immediate delivery of message to inbox.

        Args:
            message: The UnifiedMessage to deliver

        Returns:
            bool: True if delivery successful, False otherwise
        """
        try:
            recipient = message.recipient
            if recipient not in self.inbox_paths:
                self.logger.error(f"Unknown recipient: {recipient}")
                return False

            inbox_path = self.inbox_paths[recipient]
            os.makedirs(inbox_path, exist_ok=True)

            # Create message filename with timestamp
            timestamp = message.timestamp.strftime("%Y%m%d_%H%M%S") if message.timestamp else time.strftime("%Y%m%d_%H%M%S")
            filename = f"CAPTAIN_MESSAGE_{timestamp}_{message.message_id}.md"
            filepath = os.path.join(inbox_path, filename)

            # Prepare message content
            message_content = (
                f"# 🚨 CAPTAIN MESSAGE - {message.message_type.value.upper()}\n\n"
                f"**From**: {message.sender}\n"
                f"**To**: {message.recipient}\n"
                f"**Priority**: {message.priority.value}\n"
                f"**Message ID**: {message.message_id}\n"
                f"**Timestamp**: {message.timestamp.isoformat() if message.timestamp else 'Unknown'}\n\n"
                "---\n\n"
                f"{message.content}\n\n"
                "---\n"
                f"*Message delivered via Unified Messaging Service*\n"
            )

            # Write message to file atomically with locking
            success = self.lock_manager.atomic_write(
                filepath=filepath,
                content=message_content,
                operation="inbox_delivery",
                metadata={
                    "recipient": recipient,
                    "message_id": message.message_id,
                    "sender": message.sender,
                    "priority": message.priority.value
                }
            )

            if not success:
                return False

            self.logger.info("Message delivered to inbox successfully",
                            extra={"filepath": filepath, "recipient": recipient, "message_id": message.message_id})

            # Record metrics (V2 compliance)
            self.metrics.record_message_sent(message.message_type.value, recipient, "inbox")

            return True

        except Exception as e:
            self.logger.error(f"Failed to deliver message to inbox: {e}",
                            extra={"recipient": message.recipient, "message_id": message.message_id})
            return False

    def start_queue_processor(self) -> None:
        """Start the queue processor in a background thread."""
        import threading
        processor_thread = threading.Thread(target=self.queue_processor.start_processing, daemon=True)
        processor_thread.start()
        self.logger.info("Message queue processor started in background")

    def stop_queue_processor(self) -> None:
        """Stop the queue processor."""
        self.queue_processor.stop_processing()
        self.logger.info("Message queue processor stopped")

    def process_queue_batch(self) -> int:
        """Process one batch of queued messages.

        Returns:
            int: Number of messages processed
        """
        return self.queue_processor.process_batch()

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get queue statistics.

        Returns:
            Dict[str, Any]: Queue statistics
        """
        return self.queue.get_queue_stats()
