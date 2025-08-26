"""
TDD Refactored Message Queue System - Agent Cellphone V2
=======================================================

PHASE 3: TDD Architecture Restructuring - Clean Interface Design
Following test-driven architecture principles for maintainable, testable code

Original Component: src/core/messaging/message_queue.py (587 lines)
TDD Refactor: Modular, testable, clean architecture (≤200 LOC per module)
Architecture: Repository Pattern + Dependency Injection + Abstract Interfaces
"""

from __future__ import annotations

import json
import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional, Protocol, Any
from queue import PriorityQueue
from datetime import datetime
from dataclasses import dataclass

from ..models.unified_message import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
)

logger = logging.getLogger(__name__)


# TDD ARCHITECTURE: Abstract Interfaces (Test-Driven Design)
class MessageQueueInterface(Protocol):
    """
    TDD Interface: Message Queue Contract
    
    Defines the exact contract that TDD tests expect.
    All implementations must satisfy these test contracts.
    """
    
    def enqueue(self, message: UnifiedMessage) -> bool:
        """Enqueue message. Return True if successful."""
        ...
    
    def dequeue(self) -> Optional[UnifiedMessage]:
        """Dequeue highest priority message. Return None if empty."""
        ...
    
    def ack_message(self, message_id: str) -> bool:
        """Acknowledge message processing. Return True if successful."""
        ...
    
    def size(self) -> int:
        """Return current queue size."""
        ...
    
    def is_empty(self) -> bool:
        """Return True if queue is empty."""
        ...
    
    def is_full(self) -> bool:
        """Return True if queue is at max capacity."""
        ...
    
    def get_metrics(self) -> Dict[str, Any]:
        """Return comprehensive metrics dictionary."""
        ...


class MessageStorageInterface(Protocol):
    """
    TDD Interface: Message Persistence Contract
    
    Defines storage operations that TDD tests verify.
    """
    
    def save_message(self, message: UnifiedMessage) -> bool:
        """Persist message to storage."""
        ...
    
    def load_messages(self) -> List[UnifiedMessage]:
        """Load all messages from storage."""
        ...
    
    def remove_message(self, message_id: str) -> bool:
        """Remove message from storage."""
        ...
    
    def clear_storage(self) -> bool:
        """Clear all stored messages."""
        ...


# TDD ARCHITECTURE: Clean Implementation Classes
@dataclass
class QueueMetrics:
    """
    TDD Data Class: Queue Metrics
    
    Encapsulates all queue metrics in a clean, testable structure.
    """
    enqueue_count: int = 0
    dequeue_count: int = 0
    ack_count: int = 0
    error_count: int = 0
    current_size: int = 0
    queue_name: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for TDD test verification."""
        return {
            'enqueue_count': self.enqueue_count,
            'dequeue_count': self.dequeue_count,
            'ack_count': self.ack_count,
            'error_count': self.error_count,
            'current_size': self.current_size,
            'queue_name': self.queue_name
        }
    
    def increment_enqueue(self):
        """Thread-safe enqueue counter increment."""
        self.enqueue_count += 1
        self.current_size += 1
    
    def increment_dequeue(self):
        """Thread-safe dequeue counter increment."""
        self.dequeue_count += 1
        self.current_size -= 1
    
    def increment_ack(self):
        """Thread-safe acknowledgment counter increment."""
        self.ack_count += 1
    
    def increment_error(self):
        """Thread-safe error counter increment."""
        self.error_count += 1


class FileMessageStorage:
    """
    TDD Storage Implementation: File-based Message Persistence
    
    Clean, testable storage implementation that satisfies TDD contracts.
    Single Responsibility: Handle file-based message persistence only.
    """
    
    def __init__(self, storage_dir: Path):
        """Initialize file storage with directory."""
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._lock = threading.RLock()
    
    def save_message(self, message: Message) -> bool:
        """Save message to file storage."""
        try:
            with self._lock:
                file_path = self.storage_dir / f"{message.message_id}.json"
                message_data = {
                    'id': message.message_id,
                    'content': message.content,
                    'priority': message.priority.value,
                    'sender': message.sender,
                    'recipient': message.recipient,
                    'status': message.status.value,
                    'timestamp': message.timestamp.isoformat(),
                    'metadata': message.metadata
                }
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(message_data, f, indent=2)
                
                return True
        except Exception as e:
            logger.error(f"Failed to save message {message.message_id}: {e}")
            return False
    
    def load_messages(self) -> List[Message]:
        """Load all messages from file storage."""
        messages = []
        try:
            with self._lock:
                for file_path in self.storage_dir.glob("*.json"):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            message = UnifiedMessage(
                                message_id=data['id'],
                                content=data['content'],
                                priority=UnifiedMessagePriority(data['priority']),
                                sender_id=data['sender'],
                                recipient_id=data['recipient'],
                                status=UnifiedMessageStatus(data['status']),
                                timestamp=datetime.fromisoformat(data['timestamp']),
                                payload=data.get('metadata', {})
                            )
                            messages.append(message)
                    except Exception as e:
                        logger.error(f"Failed to load message from {file_path}: {e}")
        except Exception as e:
            logger.error(f"Failed to load messages: {e}")
        
        return messages
    
    def remove_message(self, message_id: str) -> bool:
        """Remove message file from storage."""
        try:
            with self._lock:
                file_path = self.storage_dir / f"{message_id}.json"
                if file_path.exists():
                    file_path.unlink()
                    return True
                return False
        except Exception as e:
            logger.error(f"Failed to remove message {message_id}: {e}")
            return False
    
    def clear_storage(self) -> bool:
        """Clear all message files from storage."""
        try:
            with self._lock:
                for file_path in self.storage_dir.glob("*.json"):
                    file_path.unlink()
                return True
        except Exception as e:
            logger.error(f"Failed to clear storage: {e}")
            return False


class TDDMessageQueue:
    """
    TDD Refactored Message Queue: Clean Architecture Implementation
    
    Architecture Principles:
    - Single Responsibility: Queue operations only
    - Dependency Injection: Storage injected, not created
    - Interface Segregation: Clean contracts
    - Test-Driven: Built to satisfy TDD test contracts
    - Thread-Safe: All operations protected
    - Observable: Comprehensive metrics
    
    LOC: Under 200 lines (V2 compliance)
    """
    
    def __init__(self, 
                 name: str, 
                 max_size: int = 1000,
                 storage: Optional[MessageStorageInterface] = None):
        """
        Initialize TDD message queue with clean architecture.
        
        Args:
            name: Queue name for identification
            max_size: Maximum queue capacity
            storage: Optional storage interface (dependency injection)
        """
        self.name = name
        self.max_size = max_size
        self._storage = storage
        self._queue: PriorityQueue = PriorityQueue()
        self._messages: Dict[str, UnifiedMessage] = {}
        self._metrics = QueueMetrics(queue_name=name)
        self._lock = threading.RLock()
        
        # Load persisted messages if storage available
        if self._storage:
            self._load_persisted_messages()
    
    def enqueue(self, message: UnifiedMessage) -> bool:
        """
        TDD Contract: Enqueue message with priority ordering.
        
        Returns:
            True if successful, False if queue full or error
        """
        try:
            with self._lock:
                if self.is_full():
                    self._metrics.increment_error()
                    return False
                
                # Priority queue ordering (lower number = higher priority)
                priority_value = self._get_priority_value(message.priority)
                self._queue.put((priority_value, time.time(), message))
                self._messages[message.message_id] = message
                self._metrics.increment_enqueue()
                
                # Persist if storage available
                if self._storage:
                    self._storage.save_message(message)
                
                return True
                
        except Exception as e:
            logger.error(f"Failed to enqueue message {message.message_id}: {e}")
            self._metrics.increment_error()
            return False
    
    def dequeue(self) -> Optional[UnifiedMessage]:
        """
        TDD Contract: Dequeue highest priority message.
        
        Returns:
            Message if available, None if queue empty
        """
        try:
            with self._lock:
                if self.is_empty():
                    return None
                
                priority_value, timestamp, message = self._queue.get()
                message.status = UnifiedMessageStatus.DELIVERED
                self._metrics.increment_dequeue()
                
                return message
                
        except Exception as e:
            logger.error(f"Failed to dequeue message: {e}")
            self._metrics.increment_error()
            return None
    
    def ack_message(self, message_id: str) -> bool:
        """
        TDD Contract: Acknowledge message processing completion.
        
        Returns:
            True if acknowledgment successful
        """
        try:
            with self._lock:
                if message_id in self._messages:
                    message = self._messages[message_id]
                    message.status = UnifiedMessageStatus.PROCESSED
                    self._metrics.increment_ack()
                    
                    # Remove from storage if available
                    if self._storage:
                        self._storage.remove_message(message_id)
                    
                    # Remove from memory
                    del self._messages[message_id]
                    
                    return True
                return False
                
        except Exception as e:
            logger.error(f"Failed to ack message {message_id}: {e}")
            self._metrics.increment_error()
            return False
    
    def size(self) -> int:
        """TDD Contract: Return current queue size."""
        return self._metrics.current_size
    
    def is_empty(self) -> bool:
        """TDD Contract: Check if queue is empty."""
        return self.size() == 0
    
    def is_full(self) -> bool:
        """TDD Contract: Check if queue is at maximum capacity."""
        return self.size() >= self.max_size
    
    def get_metrics(self) -> Dict[str, Any]:
        """TDD Contract: Return comprehensive metrics."""
        return self._metrics.to_dict()
    
    def get_message_by_id(self, message_id: str) -> Optional[UnifiedMessage]:
        """TDD Contract: Retrieve message by ID."""
        return self._messages.get(message_id)
    
    # Private helper methods
    def _get_priority_value(self, priority: UnifiedMessagePriority) -> int:
        """Convert priority enum to queue ordering value."""
        priority_map = {
            UnifiedMessagePriority.CRITICAL: 1,
            UnifiedMessagePriority.URGENT: 2,
            UnifiedMessagePriority.HIGH: 3,
            UnifiedMessagePriority.MEDIUM: 4,
            UnifiedMessagePriority.NORMAL: 5,
            UnifiedMessagePriority.LOW: 6,
        }
        return priority_map.get(priority, 7)
    
    def _load_persisted_messages(self) -> None:
        """Load messages from storage on initialization."""
        try:
            if not self._storage:
                return
                
            messages = self._storage.load_messages()
            for message in messages:
                if message.status != UnifiedMessageStatus.PROCESSED:
                    priority_value = self._get_priority_value(message.priority)
                    self._queue.put((priority_value, time.time(), message))
                    self._messages[message.message_id] = message
                    self._metrics.current_size += 1
                    
        except Exception as e:
            logger.error(f"Failed to load persisted messages: {e}")


# TDD Factory: Clean Object Creation
class TDDMessageQueueFactory:
    """
    TDD Factory: Clean message queue creation with dependency injection.
    
    Enables easy testing with mock dependencies.
    """
    
    @staticmethod
    def create_persistent_queue(name: str, 
                               storage_dir: Path, 
                               max_size: int = 1000) -> TDDMessageQueue:
        """Create queue with file-based persistence."""
        storage = FileMessageStorage(storage_dir)
        return TDDMessageQueue(name, max_size, storage)
    
    @staticmethod
    def create_memory_queue(name: str, max_size: int = 1000) -> TDDMessageQueue:
        """Create in-memory queue (for testing)."""
        return TDDMessageQueue(name, max_size, None)


# TDD Alias: Backward Compatibility
PersistentMessageQueue = TDDMessageQueue