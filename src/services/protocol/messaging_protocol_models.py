"""
Messaging Protocol Models - KISS Simplified
===========================================

Simplified data models for messaging protocol optimization.
KISS PRINCIPLE: Keep It Simple, Stupid - removed overengineering.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-6 - Gaming & Entertainment Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class ProtocolStrategy(Enum):
    """Simple protocol optimization strategies."""

    BATCH = "batch"
    STREAM = "stream"
    ADAPTIVE = "adaptive"


class MessagePriority(Enum):
    """Simple message priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class ProtocolStatus(Enum):
    """Simple protocol status."""

    ACTIVE = "active"
    INACTIVE = "inactive"
    MAINTENANCE = "maintenance"


@dataclass
class ProtocolConfiguration:
    """Simple protocol configuration."""

    config_id: str
    strategy: ProtocolStrategy
    batch_size: int = 100
    timeout: float = 30.0
    retry_attempts: int = 3
    created_at: datetime = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class MessageBatch:
    """Simple message batch model."""

    batch_id: str
    messages: List[Dict[str, Any]]
    priority: MessagePriority
    created_at: datetime = None
    processed_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()

    @property
    def size(self) -> int:
        """Get batch size."""
        return len(self.messages)

    def is_processed(self) -> bool:
        """Check if batch is processed."""
        return self.processed_at is not None


@dataclass
class ProtocolMetrics:
    """Simple protocol metrics."""

    total_messages: int = 0
    processed_messages: int = 0
    failed_messages: int = 0
    average_processing_time: float = 0.0
    last_updated: datetime = None

    def __post_init__(self):
        """Initialize default values."""
        if self.last_updated is None:
            self.last_updated = datetime.now()

    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_messages == 0:
            return 0.0
        return self.processed_messages / self.total_messages


@dataclass
class RoutingRule:
    """Simple routing rule."""

    rule_id: str
    pattern: str
    destination: str
    priority: MessagePriority = MessagePriority.NORMAL
    active: bool = True
    created_at: datetime = None

    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ProtocolStatus:
    """Simple protocol status."""

    protocol_id: str
    status: ProtocolStatus
    last_activity: datetime = None
    message_count: int = 0
    error_count: int = 0

    def __post_init__(self):
        """Initialize default values."""
        if self.last_activity is None:
            self.last_activity = datetime.now()

    @property
    def is_healthy(self) -> bool:
        """Check if protocol is healthy."""
        return self.status == ProtocolStatus.ACTIVE and self.error_count == 0


# Factory functions for backward compatibility
def create_protocol_configuration(
    config_id: str, strategy: ProtocolStrategy = ProtocolStrategy.BATCH
) -> ProtocolConfiguration:
    """Create a protocol configuration."""
    return ProtocolConfiguration(config_id=config_id, strategy=strategy)


def create_message_batch(
    batch_id: str,
    messages: List[Dict[str, Any]],
    priority: MessagePriority = MessagePriority.NORMAL,
) -> MessageBatch:
    """Create a message batch."""
    return MessageBatch(batch_id=batch_id, messages=messages, priority=priority)


def create_protocol_metrics() -> ProtocolMetrics:
    """Create protocol metrics."""
    return ProtocolMetrics()


def create_routing_rule(rule_id: str, pattern: str, destination: str) -> RoutingRule:
    """Create a routing rule."""
    return RoutingRule(rule_id=rule_id, pattern=pattern, destination=destination)


def create_protocol_status(
    protocol_id: str, status: ProtocolStatus = ProtocolStatus.ACTIVE
) -> ProtocolStatus:
    """Create protocol status."""
    return ProtocolStatus(protocol_id=protocol_id, status=status)
