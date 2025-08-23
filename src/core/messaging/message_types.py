"""
Message Types and Enums - Advanced Messaging System
==================================================

Defines the core message structures and enums used throughout the
advanced messaging system for type safety and consistency.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional, Generic, TypeVar

# Import V2 comprehensive messaging system
from ..v2_comprehensive_messaging_system import (
    V2MessagePriority, V2MessageType, V2MessageStatus
)

T = TypeVar("T")


@dataclass
class Message(Generic[T]):
    """
    Core message structure for the advanced messaging system.

    Attributes:
        message_id: Unique identifier for the message
        type: Type of message (coordination, task, response, etc.)
        content: The actual message content (generic type)
        from_agent: ID of the sending agent
        to_agent: ID of the receiving agent (or 'broadcast' for all)
        priority: Priority level for routing and processing
        timestamp: When the message was created
        status: Current status of the message
        metadata: Additional message metadata
        sequence_number: Message sequence for ordering
        ttl: Time-to-live in seconds (None for no expiration)
        retry_count: Number of delivery attempts
        max_retries: Maximum retry attempts
        dependencies: List of message IDs this message depends on
        tags: List of tags for categorization and filtering
    """

    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: V2MessageType = V2MessageType.COORDINATION
    content: T = None
    from_agent: str = ""
    to_agent: str = ""
    priority: V2MessagePriority = V2MessagePriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    status: V2MessageStatus = V2MessageStatus.PENDING
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)
    sequence_number: Optional[int] = None
    ttl: Optional[int] = None  # Time-to-live in seconds
    retry_count: int = 0
    max_retries: int = 3
    dependencies: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Post-initialization validation and setup."""
        if not self.message_id:
            self.message_id = str(uuid.uuid4())

        if not self.timestamp:
            self.timestamp = datetime.now()

        # Ensure metadata is always a dict
        if self.metadata is None:
            self.metadata = {}

    def is_expired(self) -> bool:
        """Check if the message has expired based on TTL."""
        if self.ttl is None:
            return False

        age = (datetime.now() - self.timestamp).total_seconds()
        return age > self.ttl

    def can_retry(self) -> bool:
        """Check if the message can be retried."""
        return self.retry_count < self.max_retries and not self.is_expired()

    def increment_retry(self) -> bool:
        """Increment retry count and return if retry is still possible."""
        self.retry_count += 1
        return self.can_retry()

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["type"] = self.type.value
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Message[T]":
        """Create message from dictionary."""
        # Convert enum values back to enum objects
        if "type" in data:
            data["type"] = MessageType(data["type"])
        if "priority" in data:
            data["priority"] = MessagePriority(data["priority"])
        if "status" in data:
            data["status"] = MessageStatus(data["status"])

        # Parse timestamp
        if "timestamp" in data and isinstance(data["timestamp"], str):
            data["timestamp"] = datetime.fromisoformat(data["timestamp"])

        return cls(**data)

    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> "Message[T]":
        """Create message from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def add_tag(self, tag: str) -> None:
        """Add a tag to the message."""
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag from the message."""
        if tag in self.tags:
            self.tags.remove(tag)

    def has_tag(self, tag: str) -> bool:
        """Check if message has a specific tag."""
        return tag in self.tags

    def add_dependency(self, message_id: str) -> None:
        """Add a message dependency."""
        if message_id not in self.dependencies:
            self.dependencies.append(message_id)

    def remove_dependency(self, message_id: str) -> None:
        """Remove a message dependency."""
        if message_id in self.dependencies:
            self.dependencies.remove(message_id)

    def is_ready(self, completed_messages: set[str]) -> bool:
        """Check if all dependencies are satisfied."""
        return all(dep in completed_messages for dep in self.dependencies)

    def __str__(self) -> str:
        """String representation of the message."""
        return f"Message[{self.type.value}]({self.message_id[:8]}): {self.from_agent} -> {self.to_agent}"

    def __repr__(self) -> str:
        """Detailed representation of the message."""
        return (
            f"Message(message_id='{self.message_id}', type={self.type.value}, "
            f"from_agent='{self.from_agent}', to_agent='{self.to_agent}', "
            f"priority={self.priority.value}, status={self.status.value})"
        )


@dataclass
class MessageBatch:
    """Batch of messages for bulk operations."""

    messages: list[Message] = field(default_factory=list)
    batch_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def add_message(self, message: Message) -> None:
        """Add a message to the batch."""
        self.messages.append(message)

    def remove_message(self, message_id: str) -> bool:
        """Remove a message from the batch by ID."""
        for i, msg in enumerate(self.messages):
            if msg.message_id == message_id:
                del self.messages[i]
                return True
        return False

    def get_messages_by_type(self, message_type: MessageType) -> list[Message]:
        """Get all messages of a specific type."""
        return [msg for msg in self.messages if msg.type == message_type]

    def get_messages_by_priority(self, priority: MessagePriority) -> list[Message]:
        """Get all messages of a specific priority."""
        return [msg for msg in self.messages if msg.priority == priority]

    def get_messages_by_agent(self, agent_id: str) -> list[Message]:
        """Get all messages to or from a specific agent."""
        return [
            msg
            for msg in self.messages
            if msg.from_agent == agent_id or msg.to_agent == agent_id
        ]

    def size(self) -> int:
        """Get the number of messages in the batch."""
        return len(self.messages)

    def is_empty(self) -> bool:
        """Check if the batch is empty."""
        return len(self.messages) == 0

    def clear(self) -> None:
        """Clear all messages from the batch."""
        self.messages.clear()

    def to_dict(self) -> Dict[str, Any]:
        """Convert batch to dictionary."""
        return {
            "batch_id": self.batch_id,
            "created_at": self.created_at.isoformat(),
            "message_count": len(self.messages),
            "messages": [msg.to_dict() for msg in self.messages],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MessageBatch":
        """Create batch from dictionary."""
        batch = cls(
            batch_id=data.get("batch_id", str(uuid.uuid4())),
            created_at=datetime.fromisoformat(data["created_at"])
            if "created_at" in data
            else datetime.now(),
            metadata=data.get("metadata", {}),
        )

        # Reconstruct messages
        for msg_data in data.get("messages", []):
            message = Message.from_dict(msg_data)
            batch.add_message(message)

        return batch
