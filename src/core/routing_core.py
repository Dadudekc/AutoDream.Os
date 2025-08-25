"""Core message routing logic separated from orchestration layer."""

import logging
import queue
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

from .shared_enums import MessagePriority, MessageStatus, MessageType
from .routing_models import Message
from .routing_table import RoutingTable
from .strategy_factory import StrategyFactory
from .message_transformer import MessageTransformer
from .message_validator import MessageValidator


class RoutingCore:
    """Implements message queueing and delivery."""

    def __init__(self, messages_dir: str) -> None:
        self.messages_dir = Path(messages_dir)
        self.message_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.delivery_callbacks: Dict[str, Callable[[Message], bool]] = {}
        self.message_history: Dict[str, Message] = {}
        self.logger = logging.getLogger(f"{__name__}.RoutingCore")
        self.routing_table = RoutingTable()
        self.transformer = MessageTransformer()
        self.validator = MessageValidator()
        self.strategy_factory = StrategyFactory(self._default_delivery)
        self.running = False
        self.routing_thread: Optional[threading.Thread] = None
        self._start_routing_thread()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        expires_in: Optional[int] = None,
    ) -> str:
        """Queue a message for delivery."""
        try:
            message_id = f"{sender_id}_{recipient_id}_{int(time.time())}"
            expires_at = None
            if expires_in:
                expires_at = (
                    datetime.now() + timedelta(seconds=expires_in)
                ).isoformat()

            message = Message(
                message_id=message_id,
                sender_id=sender_id,
                recipient_id=recipient_id,
                message_type=message_type,
                priority=priority,
                content=content,
                timestamp=datetime.now().isoformat(),
                expires_at=expires_at,
                status=MessageStatus.PENDING,
            )

            priority_value = self.validator.priority_value(priority)
            # Include timestamp to avoid comparisons between Message objects
            self.message_queue.put((priority_value, time.time(), message))
            self.message_history[message_id] = message
            self.transformer.save(message, self.messages_dir)
            self.logger.info("Message %s queued for delivery", message_id)
            return message_id
        except Exception as e:  # pragma: no cover - unlikely in tests
            self.logger.error("Failed to send message: %s", e)
            return ""

    def broadcast_message(
        self,
        sender_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        target_agents: Optional[List[str]] = None,
    ) -> List[str]:
        """Broadcast a message to multiple agents."""
        message_ids: List[str] = []
        try:
            if target_agents is None:
                target_agents = self._get_all_agent_ids()
            for recipient_id in target_agents:
                if recipient_id != sender_id:
                    mid = self.send_message(
                        sender_id, recipient_id, message_type, content, priority
                    )
                    if mid:
                        message_ids.append(mid)
            self.logger.info("Broadcast message sent to %d agents", len(message_ids))
        except Exception as e:  # pragma: no cover
            self.logger.error("Failed to broadcast message: %s", e)
        return message_ids

    def register_delivery_callback(self, message_type: MessageType, callback: Callable):
        self.delivery_callbacks[message_type.value] = callback

    def get_message_status(self, message_id: str) -> Optional[MessageStatus]:
        if message_id in self.message_history:
            return self.message_history[message_id].status
        return None

    def get_pending_messages(self, recipient_id: str) -> List[Message]:
        pending = [
            m
            for m in self.message_history.values()
            if m.recipient_id == recipient_id
            and m.status == MessageStatus.PENDING
            and not self.validator.is_expired(m)
        ]
        pending.sort(
            key=lambda m: (self.validator.priority_value(m.priority), m.timestamp)
        )
        return pending

    def get_routing_stats(self) -> Dict[str, Any]:
        total = len(self.message_history)
        pending = len(
            [
                m
                for m in self.message_history.values()
                if m.status == MessageStatus.PENDING
            ]
        )
        delivered = len(
            [
                m
                for m in self.message_history.values()
                if m.status == MessageStatus.DELIVERED
            ]
        )
        failed = len(
            [
                m
                for m in self.message_history.values()
                if m.status == MessageStatus.FAILED
            ]
        )
        return {
            "total_messages": total,
            "pending_messages": pending,
            "delivered_messages": delivered,
            "failed_messages": failed,
            "queue_size": self.message_queue.qsize(),
            "delivery_callbacks": len(self.delivery_callbacks),
        }

    def run_smoke_test(self) -> bool:  # pragma: no cover - convenience method
        try:
            mid = self.send_message(
                "Agent-1",
                "Agent-2",
                MessageType.STATUS_UPDATE,
                {"status": "online"},
            )
            if not mid:
                return False
            bids = self.broadcast_message(
                "Agent-1",
                MessageType.COORDINATION,
                {"action": "sync"},
            )
            if not bids:
                return False
            if self.get_message_status(mid) != MessageStatus.PENDING:
                return False
            if not self.get_pending_messages("Agent-2"):
                return False
            if "total_messages" not in self.get_routing_stats():
                return False
            return True
        except Exception:  # pragma: no cover
            return False

    def shutdown(self) -> None:
        self.running = False
        if self.routing_thread:
            self.routing_thread.join(timeout=5)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _start_routing_thread(self) -> None:
        self.running = True
        self.routing_thread = threading.Thread(target=self._routing_loop, daemon=True)
        self.routing_thread.start()

    def _routing_loop(self) -> None:
        while self.running:
            try:
                if not self.message_queue.empty():
                    priority, _, message = self.message_queue.get()
                    if self.validator.is_expired(message):
                        message.status = MessageStatus.EXPIRED
                        self.transformer.save(message, self.messages_dir)
                        continue
                    success = self._attempt_delivery(message)
                    if success:
                        message.status = MessageStatus.DELIVERED
                        self.transformer.save(message, self.messages_dir)
                    else:
                        if message.delivery_attempts < message.max_attempts:
                            message.delivery_attempts += 1
                            self.message_queue.put((priority + 1000, message))
                        else:
                            message.status = MessageStatus.FAILED
                            self.transformer.save(message, self.messages_dir)
                time.sleep(0.1)
            except Exception as e:  # pragma: no cover
                self.logger.error("Routing loop error: %s", e)
                time.sleep(1)

    def _attempt_delivery(self, message: Message) -> bool:
        callback_key = message.message_type.value
        if callback_key in self.delivery_callbacks:
            try:
                return self.delivery_callbacks[callback_key](message)
            except Exception:  # pragma: no cover
                return False
        rule = self.routing_table.get_rule(message.message_type)
        strategy_name = rule.delivery_strategy if rule else "specific"
        strategy = self.strategy_factory.get_strategy(strategy_name)
        return strategy(message)

    def _default_delivery(self, message: Message) -> bool:
        self.logger.info(
            "Message %s delivered to %s", message.message_id, message.recipient_id
        )
        return True

    def _get_all_agent_ids(self) -> List[str]:
        return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
