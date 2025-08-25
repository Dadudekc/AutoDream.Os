"""Orchestration layer for message routing.

This module exposes :class:`MessageRouter` which coordinates the underlying
routing components. Detailed implementations live in neighbouring modules:
``routing_core``, ``routing_table``, ``strategy_factory``,
``message_transformer`` and ``message_validator``.
"""

from .shared_enums import MessagePriority, MessageStatus, MessageType
from .routing_models import Message, RoutingRule  # re-export for compatibility
from .routing_core import RoutingCore


class MessageRouter:
    """Thin wrapper delegating routing operations to :class:`RoutingCore`."""

    def __init__(self, messages_dir: str = "messages") -> None:
        self._core = RoutingCore(messages_dir)

    # ------------------------------------------------------------------
    # Delegated public API
    # ------------------------------------------------------------------
    def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: MessageType,
        content,
        priority: MessagePriority = MessagePriority.NORMAL,
        expires_in=None,
    ) -> str:
        return self._core.send_message(
            sender_id, recipient_id, message_type, content, priority, expires_in
        )

    def broadcast_message(
        self,
        sender_id: str,
        message_type: MessageType,
        content,
        priority: MessagePriority = MessagePriority.NORMAL,
        target_agents=None,
    ):
        return self._core.broadcast_message(
            sender_id, message_type, content, priority, target_agents
        )

    def register_delivery_callback(self, message_type: MessageType, callback):
        self._core.register_delivery_callback(message_type, callback)

    def get_message_status(self, message_id: str):
        return self._core.get_message_status(message_id)

    def get_pending_messages(self, recipient_id: str):
        return self._core.get_pending_messages(recipient_id)

    def get_routing_stats(self):
        return self._core.get_routing_stats()

    def run_smoke_test(self) -> bool:
        return self._core.run_smoke_test()

    def shutdown(self) -> None:
        self._core.shutdown()


__all__ = [
    "MessageRouter",
    "Message",
    "RoutingRule",
    "MessagePriority",
    "MessageStatus",
    "MessageType",
]
