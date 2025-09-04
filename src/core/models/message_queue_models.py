#!/usr/bin/env python3
"""
Message Queue Models - Agent Cellphone V2
=========================================

Data models and enums for message queue system.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from datetime import datetime
# Removed circular import - using datetime directly



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

    def __lt__(self, other: "QueueEntry") -> bool:
        """Priority comparison for heap operations."""
        if self.priority_score != other.priority_score:
            return (
                self.priority_score > other.priority_score
            )  # Higher score = higher priority
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
                "timestamp": (
                    self.message.timestamp.isoformat()
                    if self.message.timestamp
                    else None
                ),
                "tags": (
                    [tag.value for tag in self.message.tags]
                    if self.message.tags
                    else []
                ),
            },
            "queue_id": self.queue_id,
            "priority_score": self.priority_score,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "delivery_attempts": self.delivery_attempts,
            "max_attempts": self.max_attempts,
            "next_retry_at": (
                self.next_retry_at.isoformat() if self.next_retry_at else None
            ),
            "last_error": self.last_error,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "QueueEntry":
        """Create from dictionary."""
            UnifiedMessage,
            UnifiedMessageTag,
            UnifiedMessageType,
        )

        message_data = data["message"]
        message = UnifiedMessage(
            message_id=message_data["message_id"],
            sender=message_data["sender"],
            recipient=message_data["recipient"],
            content=message_data["content"],
            message_type=UnifiedMessageType(message_data["message_type"]),
            priority=UnifiedMessagePriority(message_data["priority"]),
            timestamp=(
                datetime.fromisoformat(message_data["timestamp"])
                if message_data["timestamp"]
                else None
            ),
            tags=[UnifiedMessageTag(tag) for tag in message_data.get("tags", [])],
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
            next_retry_at=(
                datetime.fromisoformat(data["next_retry_at"])
                if data.get("next_retry_at")
                else None
            ),
            last_error=data.get("last_error"),
            metadata=data.get("metadata", {}),
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
