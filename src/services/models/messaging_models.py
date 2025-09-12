"""Messaging models for the unified messaging system."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any
from uuid import uuid4


class MessageType(Enum):

EXAMPLE USAGE:
==============

# Import the service
from src.services.models.messaging_models import Messaging_ModelsService

# Initialize service
service = Messaging_ModelsService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Messaging_ModelsService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

    """Types of messages in the system."""

    CHAT = "chat"
    ONBOARDING = "onboarding"
    COORDINATION = "coordination"
    NOTIFICATION = "notification"
    COMMAND = "command"
    RESPONSE = "response"
    STATUS_UPDATE = "status_update"
    DEBATE_CONTRIBUTION = "debate_contribution"


class MessagePriority(Enum):
    """Message priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    CRITICAL = "critical"


class MessageStatus(Enum):
    """Message delivery status."""

    PENDING = "pending"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"
    EXPIRED = "expired"


@dataclass
class Message:
    """Core message model."""

    id: str
    sender: str
    recipient: str
    content: str
    message_type: MessageType
    priority: MessagePriority
    status: MessageStatus
    created_at: datetime
    sent_at: datetime | None = None
    delivered_at: datetime | None = None
    read_at: datetime | None = None
    metadata: dict[str, Any] | None = None
    reply_to: str | None = None
    thread_id: str | None = None

    @classmethod
    def create(
        cls,
        sender: str,
        recipient: str,
        content: str,
        message_type: MessageType = MessageType.CHAT,
        priority: MessagePriority = MessagePriority.NORMAL,
        metadata: dict[str, Any] | None = None,
        reply_to: str | None = None,
        thread_id: str | None = None,
    ) -> Message:
        """Create a new message."""
        return cls(
            id=str(uuid4()),
            sender=sender,
            recipient=recipient,
            content=content,
            message_type=message_type,
            priority=priority,
            status=MessageStatus.PENDING,
            created_at=datetime.now(),
            metadata=metadata or {},
            reply_to=reply_to,
            thread_id=thread_id,
        )


@dataclass
class AgentMessage:
    """Message specifically for agent communication."""

    message: Message
    agent_id: str
    coordinates: tuple[int, int] | None = None
    delivery_method: str = "pyautogui"
    retry_count: int = 0
    max_retries: int = 3

    def should_retry(self) -> bool:
        """Check if message should be retried."""
        return self.retry_count < self.max_retries and self.message.status == MessageStatus.FAILED


@dataclass
class MessageThread:
    """Message thread for conversation tracking."""

    id: str
    participants: list[str]
    created_at: datetime
    last_activity: datetime
    messages: list[Message]
    metadata: dict[str, Any] | None = None

    @classmethod
    def create(
        cls, participants: list[str], metadata: dict[str, Any] | None = None
    ) -> MessageThread:
        """Create a new message thread."""
        thread_id = str(uuid4())
        now = datetime.now()
        return cls(
            id=thread_id,
            participants=participants,
            created_at=now,
            last_activity=now,
            messages=[],
            metadata=metadata or {},
        )


@dataclass
class InboxMessage:
    """Message in agent inbox."""

    message: Message
    agent_id: str
    received_at: datetime
    is_read: bool = False
    is_archived: bool = False
    tags: list[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []


@dataclass
class MessageDeliveryResult:
    """Result of message delivery attempt."""

    message_id: str
    success: bool
    delivery_method: str
    delivered_at: datetime | None = None
    error_message: str | None = None
    retry_required: bool = False
    coordinates_used: tuple[int, int] | None = None


@dataclass
class AgentStatus:
    """Agent status information."""

    agent_id: str
    is_online: bool
    last_seen: datetime
    current_task: str | None = None
    coordinates: tuple[int, int] | None = None
    capabilities: list[str] = None
    status_message: str | None = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []


@dataclass
class MessageQueue:
    """Message queue for processing."""

    agent_id: str
    messages: list[Message]
    max_size: int = 100
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()

    def add_message(self, message: Message) -> bool:
        """Add message to queue."""
        if len(self.messages) >= self.max_size:
            return False
        self.messages.append(message)
        return True

    def get_next_message(self) -> Message | None:
        """Get next message from queue."""
        if not self.messages:
            return None
        return self.messages.pop(0)

    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self.messages) == 0

    def size(self) -> int:
        """Get queue size."""
        return len(self.messages)
