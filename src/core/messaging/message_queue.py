"""
Message Queue Implementation - Advanced Messaging System
======================================================

Provides abstract message queue interface and persistent implementation
with priority-based message handling and file-based storage.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from queue import PriorityQueue
from datetime import datetime

from ..v2_comprehensive_messaging_system import V2Message, V2MessagePriority, V2MessageStatus

logger = logging.getLogger(__name__)


class MessageQueue(ABC):
    """
    Abstract base class for message queue implementations.

    Provides a common interface for different queue implementations
    including in-memory, persistent, and distributed queues.
    """

    def __init__(self, name: str, max_size: int = 1000):
        """
        Initialize the message queue.

        Args:
            name: Name of the queue
            max_size: Maximum number of messages in the queue
        """
        self.name = name
        self.max_size = max_size
        self._lock = threading.RLock()
        self._metrics = {
            "enqueue_count": 0,
            "dequeue_count": 0,
            "ack_count": 0,
            "error_count": 0,
            "current_size": 0,
        }

    @abstractmethod
    async def enqueue(self, message: V2Message) -> bool:
        """
        Add a message to the queue.

        Args:
            message: Message to enqueue

        Returns:
            True if message was successfully enqueued, False otherwise
        """
        pass

    @abstractmethod
    async def dequeue(self, agent_id: str) -> Optional[V2Message]:
        """
        Get the next message for an agent.

        Args:
            agent_id: ID of the agent requesting a message

        Returns:
            Next message for the agent, or None if no messages available
        """
        pass

    @abstractmethod
    async def acknowledge(self, message_id: str) -> bool:
        """
        Mark a message as acknowledged.

        Args:
            message_id: ID of the message to acknowledge

        Returns:
            True if message was successfully acknowledged, False otherwise
        """
        pass

    @abstractmethod
    async def get_queue_size(self) -> int:
        """
        Get the current number of messages in the queue.

        Returns:
            Number of messages in the queue
        """
        pass

    @abstractmethod
    async def get_agent_queue_size(self, agent_id: str) -> int:
        """
        Get the number of messages waiting for a specific agent.

        Args:
            agent_id: ID of the agent

        Returns:
            Number of messages waiting for the agent
        """
        pass

    def get_metrics(self) -> Dict[str, Any]:
        """Get queue performance metrics."""
        with self._lock:
            return self._metrics.copy()

    def reset_metrics(self) -> None:
        """Reset queue performance metrics."""
        with self._lock:
            self._metrics = {
                "enqueue_count": 0,
                "dequeue_count": 0,
                "ack_count": 0,
                "error_count": 0,
                "current_size": 0,
            }


class PersistentMessageQueue(MessageQueue):
    """
    Persistent message queue with file-based storage.

    Provides reliable message storage with priority-based ordering,
    automatic cleanup, and recovery capabilities.
    """

    def __init__(
        self,
        name: str,
        storage_dir: Path,
        max_size: int = 1000,
        cleanup_interval: int = 300,  # 5 minutes
        max_age: int = 86400,  # 24 hours
    ):
        """
        Initialize persistent message queue.

        Args:
            name: Queue name
            storage_dir: Directory for message storage
            max_size: Maximum queue size
            cleanup_interval: Cleanup interval in seconds
            max_age: Maximum message age in seconds
        """
        super().__init__(name, max_size)

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        # Queue files
        self.queue_file = self.storage_dir / f"{name}_queue.json"
        self.ack_file = self.storage_dir / f"{name}_acknowledged.json"
        self.failed_file = self.storage_dir / f"{name}_failed.json"

        # Internal queues
        self._pending_queue: PriorityQueue = PriorityQueue(maxsize=max_size)
        self._acknowledged: Set[str] = set()
        self._failed: Set[str] = set()

        # Cleanup settings
        self.cleanup_interval = cleanup_interval
        self.max_age = max_age
        self._last_cleanup = time.time()

        # Load existing messages
        self._load_messages()

        # Start cleanup thread
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_worker, daemon=True
        )
        self._cleanup_thread.start()

    def _load_messages(self) -> None:
        """Load messages from storage files."""
        try:
            # Load pending messages
            if self.queue_file.exists():
                with open(self.queue_file, "r", encoding="utf-8") as f:
                    messages_data = json.load(f)
                    for msg_data in messages_data:
                        try:
                            message = Message.from_dict(msg_data)
                            if not message.is_expired():
                                self._pending_queue.put(
                                    (message.priority.value, message)
                                )
                        except Exception as e:
                            logger.error(f"Failed to load message: {e}")
                            self._metrics["error_count"] += 1

            # Load acknowledged messages
            if self.ack_file.exists():
                with open(self.ack_file, "r", encoding="utf-8") as f:
                    ack_data = json.load(f)
                    self._acknowledged = set(ack_data)

            # Load failed messages
            if self.failed_file.exists():
                with open(self.failed_file, "r", encoding="utf-8") as f:
                    failed_data = json.load(f)
                    self._failed = set(failed_data)

            self._metrics["current_size"] = self._pending_queue.qsize()
            logger.info(
                f"Loaded {self._pending_queue.qsize()} messages for queue {self.name}"
            )

        except Exception as e:
            logger.error(f"Failed to load messages for queue {self.name}: {e}")
            self._metrics["error_count"] += 1

    def _save_messages(self) -> None:
        """Save messages to storage files."""
        try:
            # Save pending messages
            pending_messages = []
            temp_queue = PriorityQueue()

            while not self._pending_queue.empty():
                priority, message = self._pending_queue.get()
                pending_messages.append(message.to_dict())
                temp_queue.put((priority, message))

            # Restore queue
            while not temp_queue.empty():
                self._pending_queue.put(temp_queue.get())

            # Write to file
            with open(self.queue_file, "w", encoding="utf-8") as f:
                json.dump(pending_messages, f, indent=2, default=str)

            # Save acknowledged messages
            with open(self.ack_file, "w", encoding="utf-8") as f:
                json.dump(list(self._acknowledged), f, indent=2)

            # Save failed messages
            with open(self.failed_file, "w", encoding="utf-8") as f:
                json.dump(list(self._failed), f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save messages for queue {self.name}: {e}")
            self._metrics["error_count"] += 1

    async def enqueue(self, message: Message) -> bool:
        """Add a message to the queue."""
        try:
            with self._lock:
                if self._pending_queue.qsize() >= self.max_size:
                    logger.warning(f"Queue {self.name} is full, cannot enqueue message")
                    return False

                # Check if message is expired
                if message.is_expired():
                    logger.warning(
                        f"Message {message.message_id} is expired, not enqueuing"
                    )
                    return False

                # Add to queue with priority ordering
                self._pending_queue.put((message.priority.value, message))
                self._metrics["enqueue_count"] += 1
                self._metrics["current_size"] = self._pending_queue.qsize()

                # Save to storage
                self._save_messages()

                logger.debug(
                    f"Enqueued message {message.message_id} in queue {self.name}"
                )
                return True

        except Exception as e:
            logger.error(f"Failed to enqueue message in queue {self.name}: {e}")
            self._metrics["error_count"] += 1
            return False

    async def dequeue(self, agent_id: str) -> Optional[Message]:
        """Get the next message for an agent."""
        try:
            with self._lock:
                if self._pending_queue.empty():
                    return None

                # Get next message by priority
                priority, message = self._pending_queue.get()

                # Check if message is for this agent or is a broadcast
                if message.to_agent != agent_id and message.to_agent != "broadcast":
                    # Put message back and try to find one for this agent
                    self._pending_queue.put((priority, message))

                    # Look for a message specifically for this agent
                    temp_queue = PriorityQueue()
                    found_message = None

                    while not self._pending_queue.empty():
                        p, msg = self._pending_queue.get()
                        if msg.to_agent == agent_id or msg.to_agent == "broadcast":
                            found_message = msg
                            # Put other messages back
                            while not temp_queue.empty():
                                self._pending_queue.put(temp_queue.get())
                            break
                        else:
                            temp_queue.put((p, msg))

                    # Put all messages back if none found
                    if found_message is None:
                        while not temp_queue.empty():
                            self._pending_queue.put(temp_queue.get())
                        return None

                    message = found_message

                # Update message status
                message.status = MessageStatus.PROCESSING

                # Update metrics
                self._metrics["dequeue_count"] += 1
                self._metrics["current_size"] = self._pending_queue.qsize()

                # Save to storage
                self._save_messages()

                logger.debug(
                    f"Dequeued message {message.message_id} for agent {agent_id}"
                )
                return message

        except Exception as e:
            logger.error(f"Failed to dequeue message from queue {self.name}: {e}")
            self._metrics["error_count"] += 1
            return None

    async def acknowledge(self, message_id: str) -> bool:
        """Mark a message as acknowledged."""
        try:
            with self._lock:
                self._acknowledged.add(message_id)
                self._metrics["ack_count"] += 1

                # Save to storage
                self._save_messages()

                logger.debug(f"Acknowledged message {message_id} in queue {self.name}")
                return True

        except Exception as e:
            logger.error(
                f"Failed to acknowledge message {message_id} in queue {self.name}: {e}"
            )
            self._metrics["error_count"] += 1
            return False

    async def mark_failed(self, message_id: str) -> bool:
        """Mark a message as failed."""
        try:
            with self._lock:
                self._failed.add(message_id)

                # Save to storage
                self._save_messages()

                logger.debug(
                    f"Marked message {message_id} as failed in queue {self.name}"
                )
                return True

        except Exception as e:
            logger.error(
                f"Failed to mark message {message_id} as failed in queue {self.name}: {e}"
            )
            self._metrics["error_count"] += 1
            return False

    async def get_queue_size(self) -> int:
        """Get the current number of messages in the queue."""
        with self._lock:
            return self._pending_queue.qsize()

    async def get_agent_queue_size(self, agent_id: str) -> int:
        """Get the number of messages waiting for a specific agent."""
        with self._lock:
            count = 0
            temp_queue = PriorityQueue()

            while not self._pending_queue.empty():
                priority, message = self._pending_queue.get()
                if message.to_agent == agent_id or message.to_agent == "broadcast":
                    count += 1
                temp_queue.put((priority, message))

            # Restore queue
            while not temp_queue.empty():
                self._pending_queue.put(temp_queue.get())

            return count

    def _cleanup_worker(self) -> None:
        """Background worker for cleaning up old messages."""
        while True:
            try:
                current_time = time.time()

                if current_time - self._last_cleanup >= self.cleanup_interval:
                    self._cleanup_old_messages()
                    self._last_cleanup = current_time

                time.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"Cleanup worker error in queue {self.name}: {e}")
                time.sleep(300)  # Wait 5 minutes on error

    def _cleanup_old_messages(self) -> None:
        """Remove old messages from storage."""
        try:
            with self._lock:
                # Clean up old acknowledged messages
                old_ack = set()
                for msg_id in self._acknowledged:
                    # For now, just remove old acknowledged messages
                    # In a real implementation, you might want to archive them
                    old_ack.add(msg_id)

                for msg_id in old_ack:
                    self._acknowledged.remove(msg_id)

                # Clean up old failed messages
                old_failed = set()
                for msg_id in self._failed:
                    old_failed.add(msg_id)

                for msg_id in old_failed:
                    self._failed.remove(msg_id)

                # Save cleaned up state
                self._save_messages()

                if old_ack or old_failed:
                    logger.info(
                        f"Cleaned up {len(old_ack)} acknowledged and {len(old_failed)} failed messages in queue {self.name}"
                    )

        except Exception as e:
            logger.error(f"Failed to cleanup old messages in queue {self.name}: {e}")

    def get_queue_stats(self) -> Dict[str, Any]:
        """Get detailed queue statistics."""
        with self._lock:
            return {
                "name": self.name,
                "pending_count": self._pending_queue.qsize(),
                "acknowledged_count": len(self._acknowledged),
                "failed_count": len(self._failed),
                "max_size": self.max_size,
                "cleanup_interval": self.cleanup_interval,
                "max_age": self.max_age,
                "metrics": self._metrics.copy(),
            }

    def clear_queue(self) -> None:
        """Clear all messages from the queue."""
        with self._lock:
            while not self._pending_queue.empty():
                self._pending_queue.get()

            self._acknowledged.clear()
            self._failed.clear()

            self._metrics["current_size"] = 0

            # Save empty state
            self._save_messages()

            logger.info(f"Cleared all messages from queue {self.name}")


class InMemoryMessageQueue(MessageQueue):
    """
    Simple in-memory message queue for testing and development.

    Provides fast message handling without persistence.
    """

    def __init__(self, name: str, max_size: int = 1000):
        """Initialize in-memory message queue."""
        super().__init__(name, max_size)
        self._queue: PriorityQueue = PriorityQueue(maxsize=max_size)
        self._acknowledged: Set[str] = set()
        self._failed: Set[str] = set()

    async def enqueue(self, message: Message) -> bool:
        """Add a message to the queue."""
        try:
            with self._lock:
                if self._queue.qsize() >= self.max_size:
                    return False

                self._queue.put((message.priority.value, message))
                self._metrics["enqueue_count"] += 1
                self._metrics["current_size"] = self._queue.qsize()
                return True

        except Exception as e:
            logger.error(f"Failed to enqueue message: {e}")
            self._metrics["error_count"] += 1
            return False

    async def dequeue(self, agent_id: str) -> Optional[Message]:
        """Get the next message for an agent."""
        try:
            with self._lock:
                if self._queue.empty():
                    return None

                # Get next message by priority
                priority, message = self._queue.get()

                # Check if message is for this agent or is a broadcast
                if message.to_agent != agent_id and message.to_agent != "broadcast":
                    # Put message back and try to find one for this agent
                    self._queue.put((priority, message))

                    # Look for a message specifically for this agent
                    temp_queue = PriorityQueue()
                    found_message = None

                    while not self._queue.empty():
                        p, msg = self._queue.get()
                        if msg.to_agent == agent_id or msg.to_agent == "broadcast":
                            found_message = msg
                            # Put other messages back
                            while not temp_queue.empty():
                                self._queue.put(temp_queue.get())
                            break
                        else:
                            temp_queue.put((p, msg))

                    # Put all messages back if none found
                    if found_message is None:
                        while not temp_queue.empty():
                            self._queue.put(temp_queue.get())
                        return None

                    message = found_message

                message.status = MessageStatus.PROCESSING
                self._metrics["dequeue_count"] += 1
                self._metrics["current_size"] = self._queue.qsize()

                return message

        except Exception as e:
            logger.error(f"Failed to dequeue message: {e}")
            self._metrics["error_count"] += 1
            return None

    async def acknowledge(self, message_id: str) -> bool:
        """Mark a message as acknowledged."""
        try:
            with self._lock:
                self._acknowledged.add(message_id)
                self._metrics["ack_count"] += 1
                return True

        except Exception as e:
            logger.error(f"Failed to acknowledge message: {e}")
            self._metrics["error_count"] += 1
            return False

    async def get_queue_size(self) -> int:
        """Get the current number of messages in the queue."""
        with self._lock:
            return self._queue.qsize()

    async def get_agent_queue_size(self, agent_id: str) -> int:
        """Get the number of messages waiting for a specific agent."""
        with self._lock:
            count = 0
            temp_queue = PriorityQueue()

            while not self._queue.empty():
                priority, message = self._queue.get()
                if message.to_agent == agent_id or message.to_agent == "broadcast":
                    count += 1
                temp_queue.put((priority, message))

            # Restore queue
            while not temp_queue.empty():
                self._queue.put(temp_queue.get())

            return count
