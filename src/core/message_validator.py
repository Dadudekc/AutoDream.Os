"""Validation helpers for routed messages."""

from datetime import datetime

from .routing_models import Message
from .shared_enums import MessagePriority


class MessageValidator:
    """Validate message metadata and priorities."""

    def is_expired(self, message: Message) -> bool:
        if message.expires_at is None:
            return False
        try:
            return datetime.now() > datetime.fromisoformat(message.expires_at)
        except Exception:
            return False

    def priority_value(self, priority: MessagePriority) -> int:
        priority_map = {
            MessagePriority.LOW: 1000,
            MessagePriority.NORMAL: 500,
            MessagePriority.HIGH: 100,
            MessagePriority.URGENT: 0,
        }
        return priority_map.get(priority, 500)
