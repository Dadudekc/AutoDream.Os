from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from .shared_enums import MessagePriority, MessageStatus, MessageType


@dataclass
class Message:
    """Data structure representing a routed message."""

    message_id: str
    sender_id: str
    recipient_id: str
    message_type: MessageType
    priority: MessagePriority
    content: Dict[str, Any]
    timestamp: str
    expires_at: Optional[str]
    status: MessageStatus = MessageStatus.PENDING
    delivery_attempts: int = 0
    max_attempts: int = 3


@dataclass
class RoutingRule:
    """Rule describing how a message type should be delivered."""

    message_type: MessageType
    priority: MessagePriority
    target_agents: List[str]
    delivery_strategy: str
    retry_policy: Dict[str, Any]
