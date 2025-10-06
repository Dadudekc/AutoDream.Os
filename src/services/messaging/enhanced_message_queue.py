#!/usr/bin/env python3
"""
Enhanced Message Queue System
=============================

Provides thread-safe message queuing and coordination to prevent
multiple agents from interfering with each other during messaging.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import asyncio
import logging
import queue
import threading
import time
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class QueuedMessage:
    """Represents a message in the queue."""
    message_id: str
    agent_id: str
    message: str
    from_agent: str
    priority: MessagePriority
    coordinates: tuple[int, int]
    timestamp: float
    retry_count: int = 0
    max_retries: int = 3
    
    def __lt__(self, other):
        """Enable comparison for priority queue."""
        if not isinstance(other, QueuedMessage):
            return NotImplemented
        return self.timestamp < other.timestamp


class MessageQueue:
    """Thread-safe message queue with priority handling."""
    
    def __init__(self, max_size: int = 100):
        """Initialize message queue."""
        self.max_size = max_size
        self._queue: queue.PriorityQueue = queue.PriorityQueue(maxsize=max_size)
        self._lock = threading.Lock()
        self._processing = False
        self._stats = {
            "total_queued": 0,
            "total_processed": 0,
            "total_failed": 0,
            "current_queue_size": 0
        }
        
    def _get_priority_value(self, priority: MessagePriority) -> int:
        """Get numeric priority value (lower = higher priority)."""
        priority_map = {
            MessagePriority.CRITICAL: 0,
            MessagePriority.HIGH: 1,
            MessagePriority.NORMAL: 2,
            MessagePriority.LOW: 3
        }
        return priority_map.get(priority, 2)
    
    def enqueue(self, message: QueuedMessage) -> bool:
        """Add message to queue."""
        try:
            with self._lock:
                if self._queue.qsize() >= self.max_size:
                    logger.warning(f"Message queue full, dropping message from {message.from_agent}")
                    return False
                
                # Create priority item (priority, timestamp, message)
                priority_item = (
                    self._get_priority_value(message.priority),
                    message.timestamp,
                    message
                )
                
                self._queue.put(priority_item, block=False)
                self._stats["total_queued"] += 1
                self._stats["current_queue_size"] = self._queue.qsize()
                
                logger.info(f"Message queued: {message.message_id} from {message.from_agent} to {message.agent_id}")
                return True
                
        except queue.Full:
            logger.error(f"Failed to queue message: queue full")
            return False
        except Exception as e:
            logger.error(f"Failed to queue message: {e}")
            return False
    
    def dequeue(self, timeout: float = 1.0) -> Optional[QueuedMessage]:
        """Get next message from queue."""
        try:
            priority_item = self._queue.get(timeout=timeout)
            message = priority_item[2]  # Extract message from (priority, timestamp, message)
            
            with self._lock:
                self._stats["current_queue_size"] = self._queue.qsize()
            
            return message
            
        except queue.Empty:
            return None
        except Exception as e:
            logger.error(f"Failed to dequeue message: {e}")
            return None
    
    def requeue(self, message: QueuedMessage) -> bool:
        """Requeue a failed message for retry."""
        if message.retry_count >= message.max_retries:
            logger.warning(f"Message {message.message_id} exceeded max retries, dropping")
            with self._lock:
                self._stats["total_failed"] += 1
            return False
        
        message.retry_count += 1
        message.timestamp = time.time()  # Update timestamp for priority
        
        logger.info(f"Requeuing message {message.message_id} (retry {message.retry_count}/{message.max_retries})")
        return self.enqueue(message)
    
    def get_stats(self) -> Dict:
        """Get queue statistics."""
        with self._lock:
            return self._stats.copy()
    
    def clear(self):
        """Clear all messages from queue."""
        with self._lock:
            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    break
            self._stats["current_queue_size"] = 0


class MessageQueueProcessor:
    """Processes messages from the queue."""
    
    def __init__(self, queue: MessageQueue, message_sender):
        """Initialize message processor."""
        self.queue = queue
        self.message_sender = message_sender
        self._running = False
        self._thread: Optional[threading.Thread] = None
        
    def start(self):
        """Start message processing thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._process_loop, daemon=True)
        self._thread.start()
        logger.info("Message queue processor started")
    
    def stop(self):
        """Stop message processing thread."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        logger.info("Message queue processor stopped")
    
    def _process_loop(self):
        """Main processing loop."""
        while self._running:
            try:
                message = self.queue.dequeue(timeout=1.0)
                if message is None:
                    continue
                
                # Process the message
                success = self._send_message(message)
                
                if success:
                    with self.queue._lock:
                        self.queue._stats["total_processed"] += 1
                    logger.info(f"Message processed successfully: {message.message_id}")
                else:
                    # Requeue for retry
                    self.queue.requeue(message)
                
            except Exception as e:
                logger.error(f"Error in message processing loop: {e}")
                time.sleep(1.0)
    
    def _send_message(self, message: QueuedMessage) -> bool:
        """Send a single message."""
        try:
            # Validate coordinates
            if not self._validate_coordinates(message.coordinates):
                logger.error(f"Invalid coordinates for {message.agent_id}: {message.coordinates}")
                return False
            
            # Send message using the message sender
            return self.message_sender.send_to_coordinates(
                message.coordinates, 
                message.message
            )
            
        except Exception as e:
            logger.error(f"Failed to send message {message.message_id}: {e}")
            return False
    
    def _validate_coordinates(self, coords: tuple[int, int]) -> bool:
        """Validate coordinates are within reasonable bounds."""
        if not coords or len(coords) != 2:
            return False
        
        x, y = coords
        # Basic screen bounds validation (adjust for your setup)
        return 0 <= x <= 4000 and 0 <= y <= 4000


class EnhancedMessageCoordinator:
    """Coordinates message sending across all agents."""
    
    def __init__(self):
        """Initialize message coordinator."""
        self.queue = MessageQueue()
        self.processor: Optional[MessageQueueProcessor] = None
        self._message_counter = 0
        
    def initialize(self, message_sender):
        """Initialize with message sender."""
        self.processor = MessageQueueProcessor(self.queue, message_sender)
        self.processor.start()
        logger.info("Enhanced message coordinator initialized")
    
    def shutdown(self):
        """Shutdown coordinator."""
        if self.processor:
            self.processor.stop()
        self.queue.clear()
        logger.info("Enhanced message coordinator shutdown")
    
    def send_message(
        self,
        agent_id: str,
        message: str,
        from_agent: str,
        coordinates: tuple[int, int],
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> str:
        """Queue a message for sending."""
        self._message_counter += 1
        message_id = f"{from_agent}_{agent_id}_{self._message_counter}_{int(time.time())}"
        
        queued_message = QueuedMessage(
            message_id=message_id,
            agent_id=agent_id,
            message=message,
            from_agent=from_agent,
            priority=priority,
            coordinates=coordinates,
            timestamp=time.time()
        )
        
        if self.queue.enqueue(queued_message):
            return message_id
        else:
            raise RuntimeError(f"Failed to queue message to {agent_id}")
    
    def get_stats(self) -> Dict:
        """Get coordinator statistics."""
        return self.queue.get_stats()


# Global coordinator instance
_global_coordinator: Optional[EnhancedMessageCoordinator] = None


def get_message_coordinator() -> EnhancedMessageCoordinator:
    """Get global message coordinator instance."""
    global _global_coordinator
    if _global_coordinator is None:
        _global_coordinator = EnhancedMessageCoordinator()
    return _global_coordinator


def initialize_message_coordinator(message_sender):
    """Initialize global message coordinator."""
    coordinator = get_message_coordinator()
    coordinator.initialize(message_sender)
    return coordinator


def shutdown_message_coordinator():
    """Shutdown global message coordinator."""
    global _global_coordinator
    if _global_coordinator:
        _global_coordinator.shutdown()
        _global_coordinator = None
