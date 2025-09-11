#!/usr/bin/env python3
"""
Message Router - Intent-Oriented Subsystem
==========================================

Decomposed from SwarmOrchestrator to handle message routing and delivery logic.
Provides plug-and-play, testable message management with clear separation of concerns.

Author: Swarm Representative (Following Commander Thea directives)
Mission: Orchestration Layer Decomposition - Intent Subsystem Creation
License: MIT
"""

from __future__ import annotations

import logging
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Tuple, Union
from pathlib import Path
import threading
import queue

from ..contracts import OrchestrationContext, OrchestrationResult, Step
from ..registry import StepRegistry


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageType(Enum):
    """Message type enumeration."""
    AGENT_TO_AGENT = "agent_to_agent"
    SYSTEM_TO_AGENT = "system_to_agent"
    HUMAN_TO_AGENT = "human_to_agent"
    CAPTAIN_TO_AGENT = "captain_to_agent"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    COORDINATION = "coordination"
    STATUS = "status"


class DeliveryMethod(Enum):
    """Message delivery method enumeration."""
    PYAUTOGUI = "pyautogui"
    INBOX = "inbox"
    API = "api"
    WEBSOCKET = "websocket"


class MessageStatus(Enum):
    """Message delivery status."""
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    RETRYING = "retrying"
    EXPIRED = "expired"


@dataclass
class MessageTag:
    """Message tag structure."""
    name: str
    value: Any
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MessageAttachment:
    """Message attachment structure."""
    filename: str
    content_type: str
    data: bytes
    size: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Message:
    """Unified message structure."""
    id: str
    sender: str
    recipient: str
    message_type: MessageType
    priority: MessagePriority
    content: str
    tags: List[MessageTag] = field(default_factory=list)
    attachments: List[MessageAttachment] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeliveryResult:
    """Message delivery result."""
    message_id: str
    status: MessageStatus
    method: DeliveryMethod
    attempts: int
    delivered_at: Optional[datetime]
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class MessageHandler(Protocol):
    """Protocol for message handlers."""

    def can_handle(self, message: Message) -> bool: ...

    def handle(self, message: Message) -> DeliveryResult: ...


class RoutingRule(Protocol):
    """Protocol for routing rules."""

    def matches(self, message: Message) -> bool: ...

    def get_delivery_method(self, message: Message) -> DeliveryMethod: ...


class PriorityBasedRoutingRule:
    """Routing rule based on message priority."""

    def __init__(self, priority_threshold: MessagePriority, delivery_method: DeliveryMethod):
        self.priority_threshold = priority_threshold
        self.delivery_method = delivery_method

    def matches(self, message: Message) -> bool:
        """Check if rule matches message."""
        priority_order = {MessagePriority.LOW: 0, MessagePriority.NORMAL: 1,
                         MessagePriority.HIGH: 2, MessagePriority.URGENT: 3}
        return priority_order.get(message.priority, 0) >= priority_order.get(self.priority_threshold, 0)

    def get_delivery_method(self, message: Message) -> DeliveryMethod:
        """Get delivery method for message."""
        return self.delivery_method


class AgentBasedRoutingRule:
    """Routing rule based on agent characteristics."""

    def __init__(self, agent_patterns: List[str], delivery_method: DeliveryMethod):
        self.agent_patterns = agent_patterns
        self.delivery_method = delivery_method

    def matches(self, message: Message) -> bool:
        """Check if rule matches message."""
        return any(pattern in message.recipient for pattern in self.agent_patterns)

    def get_delivery_method(self, message: Message) -> DeliveryMethod:
        """Get delivery method for message."""
        return self.delivery_method


class PyAutoGUIHandler:
    """PyAutoGUI-based message delivery handler."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.available = self._check_availability()

    def _check_availability(self) -> bool:
        """Check if PyAutoGUI is available."""
        try:
            import pyautogui
            import pyperclip
            return True
        except ImportError:
            return False

    def can_handle(self, message: Message) -> bool:
        """Check if this handler can deliver the message."""
        return self.available and message.message_type in [
            MessageType.AGENT_TO_AGENT,
            MessageType.SYSTEM_TO_AGENT,
            MessageType.HUMAN_TO_AGENT,
            MessageType.CAPTAIN_TO_AGENT,
            MessageType.COORDINATION,
            MessageType.STATUS
        ]

    def handle(self, message: Message) -> DeliveryResult:
        """Handle message delivery via PyAutoGUI."""
        if not self.available:
            return DeliveryResult(
                message_id=message.id,
                status=MessageStatus.FAILED,
                method=DeliveryMethod.PYAUTOGUI,
                attempts=1,
                delivered_at=None,
                error_message="PyAutoGUI not available"
            )

        try:
            # Import required modules
            import pyautogui
            from src.core.messaging_pyautogui import deliver_message_pyautogui, get_agent_coordinates

            # Get recipient coordinates
            coords = get_agent_coordinates(message.recipient)
            if not coords:
                return DeliveryResult(
                    message_id=message.id,
                    status=MessageStatus.FAILED,
                    method=DeliveryMethod.PYAUTOGUI,
                    attempts=1,
                    delivered_at=None,
                    error_message=f"No coordinates found for {message.recipient}"
                )

            # Create unified message format
            unified_message = {
                "sender": message.sender,
                "recipient": message.recipient,
                "message_type": message.message_type.value,
                "priority": message.priority.value,
                "tags": [tag.name for tag in message.tags],
                "content": message.content,
                "timestamp": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            }

            # Attempt delivery
            success = deliver_message_pyautogui(unified_message, coords)

            if success:
                return DeliveryResult(
                    message_id=message.id,
                    status=MessageStatus.DELIVERED,
                    method=DeliveryMethod.PYAUTOGUI,
                    attempts=1,
                    delivered_at=datetime.now()
                )
            else:
                return DeliveryResult(
                    message_id=message.id,
                    status=MessageStatus.FAILED,
                    method=DeliveryMethod.PYAUTOGUI,
                    attempts=1,
                    delivered_at=None,
                    error_message="PyAutoGUI delivery failed"
                )

        except Exception as e:
            self.logger.error(f"PyAutoGUI delivery error: {e}")
            return DeliveryResult(
                message_id=message.id,
                status=MessageStatus.FAILED,
                method=DeliveryMethod.PYAUTOGUI,
                attempts=1,
                delivered_at=None,
                error_message=str(e)
            )


class InboxHandler:
    """Inbox-based message delivery handler."""

    def __init__(self, inbox_base_path: str = "agent_workspaces"):
        self.logger = logging.getLogger(__name__)
        self.inbox_base_path = Path(inbox_base_path)
        self.available = True

    def can_handle(self, message: Message) -> bool:
        """Check if this handler can deliver the message."""
        return True  # Inbox is always available as fallback

    def handle(self, message: Message) -> DeliveryResult:
        """Handle message delivery via inbox."""
        try:
            # Create inbox directory
            inbox_dir = self.inbox_base_path / message.recipient / "inbox"
            inbox_dir.mkdir(parents=True, exist_ok=True)

            # Create message filename
            timestamp = message.timestamp.strftime("%Y%m%d_%H%M%S")
            message_filename = f"MESSAGE_{timestamp}_{message.id[:8]}.md"

            # Create enhanced message content
            message_content = self._format_message_content(message)

            # Write message to inbox
            message_file_path = inbox_dir / message_filename
            with open(message_file_path, "w", encoding="utf-8") as f:
                f.write(message_content)

            self.logger.info(f"Message delivered to inbox: {message_filename}")

            return DeliveryResult(
                message_id=message.id,
                status=MessageStatus.DELIVERED,
                method=DeliveryMethod.INBOX,
                attempts=1,
                delivered_at=datetime.now(),
                metadata={"inbox_file": str(message_file_path)}
            )

        except Exception as e:
            self.logger.error(f"Inbox delivery error: {e}")
            return DeliveryResult(
                message_id=message.id,
                status=MessageStatus.FAILED,
                method=DeliveryMethod.INBOX,
                attempts=1,
                delivered_at=None,
                error_message=str(e)
            )

    def _format_message_content(self, message: Message) -> str:
        """Format message content for inbox storage."""
        lines = [
            f"# 📨 MESSAGE - {message.recipient}",
            "",
            f"**From**: {message.sender}",
            f"**To**: {message.recipient}",
            f"**Type**: {message.message_type.value}",
            f"**Priority**: {message.priority.value}",
            f"**Message ID**: {message.id}",
            f"**Timestamp**: {message.timestamp.isoformat()}",
            f"**Delivery Method**: Inbox Fallback (MessageRouter)",
        ]

        if message.correlation_id:
            lines.append(f"**Correlation ID**: {message.correlation_id}")

        if message.tags:
            tag_str = ", ".join(f"{tag.name}: {tag.value}" for tag in message.tags)
            lines.append(f"**Tags**: {tag_str}")

        lines.extend([
            "",
            "---",
            "",
            message.content,
            "",
            "---"
        ])

        # Add attachments info
        if message.attachments:
            lines.extend([
                "",
                "### 📎 ATTACHMENTS",
                ""
            ])
            for attachment in message.attachments:
                lines.extend([
                    f"- **{attachment.filename}** ({attachment.content_type}, {attachment.size} bytes)",
                    f"  Metadata: {attachment.metadata}",
                    ""
                ])

        # Add metadata
        if message.metadata:
            lines.extend([
                "",
                "### 📊 METADATA",
                "",
                f"```json",
                f"{message.metadata}",
                f"```",
                ""
            ])

        return "\n".join(lines)


class MessageRouter:
    """Message Router - Intent-Oriented Subsystem for message routing and delivery."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize handlers
        self.handlers: Dict[DeliveryMethod, MessageHandler] = {
            DeliveryMethod.PYAUTOGUI: PyAutoGUIHandler(),
            DeliveryMethod.INBOX: InboxHandler()
        }

        # Initialize routing rules (priority-based)
        self.routing_rules: List[RoutingRule] = [
            # Urgent messages get PyAutoGUI priority
            PriorityBasedRoutingRule(MessagePriority.URGENT, DeliveryMethod.PYAUTOGUI),
            # High priority messages try PyAutoGUI first
            PriorityBasedRoutingRule(MessagePriority.HIGH, DeliveryMethod.PYAUTOGUI),
            # Agent-1 to Agent-8 get PyAutoGUI preference
            AgentBasedRoutingRule(["Agent-1", "Agent-2", "Agent-3", "Agent-4",
                                 "Agent-5", "Agent-6", "Agent-7", "Agent-8"],
                                DeliveryMethod.PYAUTOGUI)
        ]

        # Message queues
        self.message_queue: queue.Queue = queue.Queue()
        self.delivery_results: Dict[str, DeliveryResult] = {}
        self.retry_counts: Dict[str, int] = {}

        # Start processing thread
        self.processing_thread = threading.Thread(target=self._process_message_queue, daemon=True)
        self.processing_thread.start()

    def route_message(self, message: Message) -> DeliveryMethod:
        """Determine the best delivery method for a message."""
        # Check routing rules in priority order
        for rule in self.routing_rules:
            if rule.matches(message):
                method = rule.get_delivery_method(message)
                if self.handlers[method].can_handle(message):
                    return method

        # Default to inbox as fallback
        return DeliveryMethod.INBOX

    def send_message(self, message: Message) -> str:
        """Send a message through the router."""
        # Add to queue for processing
        self.message_queue.put(message)
        self.logger.info(f"Message queued for delivery: {message.id} to {message.recipient}")
        return message.id

    def send_bulk_messages(self, messages: List[Message]) -> List[str]:
        """Send multiple messages."""
        message_ids = []
        for message in messages:
            message_ids.append(self.send_message(message))
        return message_ids

    def broadcast_message(self, message: Message, recipients: List[str]) -> List[str]:
        """Broadcast message to multiple recipients."""
        message_ids = []
        for recipient in recipients:
            broadcast_msg = Message(
                id=f"{message.id}_broadcast_{recipient}",
                sender=message.sender,
                recipient=recipient,
                message_type=MessageType.BROADCAST,
                priority=message.priority,
                content=message.content,
                tags=message.tags.copy(),
                attachments=message.attachments.copy(),
                timestamp=message.timestamp,
                expires_at=message.expires_at,
                correlation_id=message.correlation_id,
                metadata={**message.metadata, "broadcast_original": message.id}
            )
            message_ids.append(self.send_message(broadcast_msg))

        self.logger.info(f"Broadcast sent to {len(recipients)} recipients")
        return message_ids

    def _process_message_queue(self):
        """Process messages from the queue."""
        while True:
            try:
                message = self.message_queue.get(timeout=1)

                # Check if message has expired
                if message.expires_at and datetime.now() > message.expires_at:
                    self.delivery_results[message.id] = DeliveryResult(
                        message_id=message.id,
                        status=MessageStatus.EXPIRED,
                        method=DeliveryMethod.INBOX,
                        attempts=0,
                        delivered_at=None,
                        error_message="Message expired"
                    )
                    continue

                # Route and deliver
                delivery_method = self.route_message(message)
                handler = self.handlers[delivery_method]

                # Attempt delivery
                result = handler.handle(message)

                # Handle retries if failed
                if result.status == MessageStatus.FAILED:
                    retry_count = self.retry_counts.get(message.id, 0)
                    if retry_count < 3:  # Max 3 retries
                        self.retry_counts[message.id] = retry_count + 1
                        result.status = MessageStatus.RETRYING
                        # Re-queue for retry after delay
                        time.sleep(2 ** retry_count)  # Exponential backoff
                        self.message_queue.put(message)
                    else:
                        result.error_message = f"Failed after {retry_count + 1} attempts"

                # Store result
                self.delivery_results[message.id] = result

                self.logger.info(f"Message {message.id} delivery result: {result.status.value}")

            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Message processing error: {e}")

    def get_delivery_status(self, message_id: str) -> Optional[DeliveryResult]:
        """Get delivery status for a message."""
        return self.delivery_results.get(message_id)

    def get_delivery_stats(self) -> Dict[str, Any]:
        """Get delivery statistics."""
        stats = {
            "total_messages": len(self.delivery_results),
            "delivered": 0,
            "failed": 0,
            "retrying": 0,
            "expired": 0,
            "by_method": {},
            "by_priority": {}
        }

        for result in self.delivery_results.values():
            if result.status == MessageStatus.DELIVERED:
                stats["delivered"] += 1
            elif result.status == MessageStatus.FAILED:
                stats["failed"] += 1
            elif result.status == MessageStatus.RETRYING:
                stats["retrying"] += 1
            elif result.status == MessageStatus.EXPIRED:
                stats["expired"] += 1

            # Count by method
            method = result.method.value
            stats["by_method"][method] = stats["by_method"].get(method, 0) + 1

        return stats

    def create_message(self,
                      sender: str,
                      recipient: str,
                      content: str,
                      message_type: MessageType = MessageType.AGENT_TO_AGENT,
                      priority: MessagePriority = MessagePriority.NORMAL,
                      tags: Optional[List[MessageTag]] = None,
                      attachments: Optional[List[MessageAttachment]] = None,
                      correlation_id: Optional[str] = None,
                      expires_in_hours: Optional[int] = None) -> Message:
        """Create a new message."""
        message_id = str(uuid.uuid4())

        expires_at = None
        if expires_in_hours:
            expires_at = datetime.now() + timedelta(hours=expires_in_hours)

        return Message(
            id=message_id,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            content=content,
            tags=tags or [],
            attachments=attachments or [],
            expires_at=expires_at,
            correlation_id=correlation_id
        )


class MessageRouterOrchestrationStep(Step):
    """Orchestration step for message routing operations."""

    def __init__(self, message_router: MessageRouter, operation: str, **params):
        self.message_router = message_router
        self.operation = operation
        self.params = params

    def name(self) -> str:
        return f"message_router_{self.operation}"

    def run(self, ctx: OrchestrationContext, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute message routing operation."""
        try:
            if self.operation == "send":
                message = self.params.get("message")
                if message:
                    message_id = self.message_router.send_message(message)
                    payload["message_id"] = message_id

            elif self.operation == "broadcast":
                message = self.params.get("message")
                recipients = self.params.get("recipients", [])
                if message and recipients:
                    message_ids = self.message_router.broadcast_message(message, recipients)
                    payload["broadcast_message_ids"] = message_ids

            elif self.operation == "status":
                message_id = payload.get("message_id")
                if message_id:
                    status = self.message_router.get_delivery_status(message_id)
                    payload["message_status"] = status

            elif self.operation == "stats":
                stats = self.message_router.get_delivery_stats()
                payload["message_stats"] = stats

            ctx.logger(f"Message router operation completed: {self.operation}")
            return payload

        except Exception as e:
            ctx.logger(f"Message router operation failed: {e}")
            payload["message_router_error"] = str(e)
            return payload


# Factory function for creating MessageRouter instances
def create_message_router() -> MessageRouter:
    """Factory function for MessageRouter creation."""
    return MessageRouter()


__all__ = [
    "MessageRouter",
    "Message",
    "MessagePriority",
    "MessageType",
    "DeliveryMethod",
    "MessageStatus",
    "MessageTag",
    "MessageAttachment",
    "DeliveryResult",
    "MessageHandler",
    "RoutingRule",
    "PriorityBasedRoutingRule",
    "AgentBasedRoutingRule",
    "PyAutoGUIHandler",
    "InboxHandler",
    "MessageRouterOrchestrationStep",
    "create_message_router"
]
