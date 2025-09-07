#!/usr/bin/env python3
"""
Base Message Model - common message fields and serialization logic.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar, Dict, List, Optional, Type


@dataclass
class BaseMessage:
    """Base message structure with common fields."""

    message_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    message_type: Enum | None = None
    priority: Enum | None = None
    status: Enum | None = None
    sender_id: str = ""
    recipient_id: str = ""
    subject: str = ""
    content: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    delivered_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    read_at: Optional[datetime] = None
    retry_count: int = 0
    max_retries: int = 3
    ttl: Optional[int] = None
    sequence_number: Optional[int] = None
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    requires_acknowledgment: bool = False
    is_onboarding_message: bool = False
    phase_number: Optional[int] = None
    workflow_id: Optional[str] = None
    task_id: Optional[str] = None

    _enum_fields: ClassVar[Dict[str, Type[Enum]]] = {}

    def __post_init__(self) -> None:
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.now()
        if not self.created_at:
            self.created_at = self.timestamp
        if self.payload is None:
            self.payload = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for serialization."""
        data = {
            "message_id": self.message_id,
            "message_type": self.message_type.value if isinstance(self.message_type, Enum) else self.message_type,
            "priority": self.priority.value if isinstance(self.priority, Enum) else self.priority,
            "status": self.status.value if isinstance(self.status, Enum) else self.status,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "subject": self.subject,
            "content": self.content,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "created_at": self.created_at.isoformat(),
            "delivered_at": self.delivered_at.isoformat() if self.delivered_at else None,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "ttl": self.ttl,
            "sequence_number": self.sequence_number,
            "dependencies": self.dependencies,
            "tags": self.tags,
            "requires_acknowledgment": self.requires_acknowledgment,
            "is_onboarding_message": self.is_onboarding_message,
            "phase_number": self.phase_number,
            "workflow_id": self.workflow_id,
            "task_id": self.task_id,
        }
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BaseMessage:
        """Create message from dictionary."""
        timestamp_fields = [
            "timestamp",
            "created_at",
            "delivered_at",
            "acknowledged_at",
            "read_at",
        ]
        for field_name in timestamp_fields:
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = datetime.fromisoformat(data[field_name])
        for field_name, enum_cls in cls._enum_fields.items():
            if field_name in data and isinstance(data[field_name], str):
                data[field_name] = enum_cls(data[field_name])
        return cls(**data)


__all__ = ["BaseMessage"]
