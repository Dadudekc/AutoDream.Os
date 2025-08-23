#!/usr/bin/env python3
"""
Message Router - V2 Core Message Routing System

This module manages inter-agent message routing, queuing, and delivery.
Follows Single Responsibility Principle - only message routing.
Architecture: Single Responsibility Principle - message routing only
LOC: Target 200 lines (under 200 limit)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import queue
from collections import defaultdict

logger = logging.getLogger(__name__)


from .v2_comprehensive_messaging_system import (
    V2MessagePriority,
    V2MessageStatus,
    V2MessageType,
)
from .shared_enums import MessagePriority, MessageStatus, MessageType


@dataclass
class Message:
    """Message structure for inter-agent communication"""

    message_id: str
    sender_id: str
    recipient_id: str
    message_type: V2MessageType
    priority: V2MessagePriority
    content: Dict[str, Any]
    timestamp: str
    expires_at: Optional[str]
    status: V2MessageStatus = V2MessageStatus.PENDING
    delivery_attempts: int = 0
    max_attempts: int = 3


@dataclass
class RoutingRule:
    """Routing rule for message delivery"""

    message_type: V2MessageType
    priority: V2MessagePriority
    target_agents: List[str]
    delivery_strategy: str  # "broadcast", "round_robin", "specific"
    retry_policy: Dict[str, Any]


class MessageRouter:
    """
    Manages inter-agent message routing, queuing, and delivery

    Responsibilities:
    - Message queuing and prioritization
    - Intelligent routing based on message type
    - Delivery confirmation and retry logic
    - Message expiration and cleanup
    """

    def __init__(self, messages_dir: str = "messages"):
        self.messages_dir = Path(messages_dir)
        self.message_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.routing_rules: Dict[V2MessageType, RoutingRule] = {}
        self.delivery_callbacks: Dict[str, Callable] = {}
        self.message_history: Dict[str, Message] = {}
        self.logger = logging.getLogger(f"{__name__}.MessageRouter")
        self.routing_thread = None
        self.running = False

        # Ensure messages directory exists
        self.messages_dir.mkdir(exist_ok=True)

        # Initialize default routing rules
        self._initialize_default_routing_rules()

        # Start routing thread
        self._start_routing_thread()

    def _initialize_default_routing_rules(self):
        """Initialize default routing rules for different message types"""
        self.routing_rules = {
            V2MessageType.CONTRACT_ASSIGNMENT: RoutingRule(
                message_type=V2MessageType.CONTRACT_ASSIGNMENT,
                priority=V2MessagePriority.HIGH,
                target_agents=[],
                delivery_strategy="specific",
                retry_policy={"max_attempts": 3, "retry_delay": 5},
            ),
            V2MessageType.STATUS_UPDATE: RoutingRule(
                message_type=V2MessageType.STATUS_UPDATE,
                priority=V2MessagePriority.NORMAL,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 1, "retry_delay": 0},
            ),
            V2MessageType.COORDINATION: RoutingRule(
                message_type=V2MessageType.COORDINATION,
                priority=V2MessagePriority.NORMAL,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 2, "retry_delay": 10},
            ),
            V2MessageType.EMERGENCY: RoutingRule(
                message_type=V2MessageType.EMERGENCY,
                priority=V2MessagePriority.URGENT,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 5, "retry_delay": 1},
            ),
            V2MessageType.HEARTBEAT: RoutingRule(
                message_type=V2MessageType.HEARTBEAT,
                priority=V2MessagePriority.LOW,
                target_agents=[],
                delivery_strategy="broadcast",
                retry_policy={"max_attempts": 1, "retry_delay": 0},
            ),
            MessageType.SYSTEM_COMMAND: RoutingRule(
                message_type=MessageType.SYSTEM_COMMAND,
                priority=MessagePriority.HIGH,
                target_agents=[],
                delivery_strategy="specific",
                retry_policy={"max_attempts": 3, "retry_delay": 5},
            ),
        }

    def send_message(
        self,
        sender_id: str,
        recipient_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        expires_in: Optional[int] = None,
    ) -> str:
        """Send a message to a recipient"""
        try:
            # Generate unique message ID
            message_id = f"{sender_id}_{recipient_id}_{int(time.time())}"

            # Calculate expiration time
            expires_at = None
            if expires_in:
                expires_at = (
                    datetime.now() + timedelta(seconds=expires_in)
                ).isoformat()

            # Create message
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

            # Add to queue with priority
            priority_value = self._get_priority_value(priority)
            self.message_queue.put((priority_value, message))

            # Store in history
            self.message_history[message_id] = message

            # Save message to file
            self._save_message(message)

            self.logger.info(f"Message {message_id} queued for delivery")
            return message_id

        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return ""

    def broadcast_message(
        self,
        sender_id: str,
        message_type: MessageType,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        target_agents: Optional[List[str]] = None,
    ) -> List[str]:
        """Broadcast a message to multiple agents"""
        try:
            message_ids = []

            # Use provided target agents or get all available
            if target_agents is None:
                target_agents = self._get_all_agent_ids()

            # Send message to each target
            for recipient_id in target_agents:
                if recipient_id != sender_id:  # Don't send to self
                    message_id = self.send_message(
                        sender_id, recipient_id, message_type, content, priority
                    )
                    if message_id:
                        message_ids.append(message_id)

            self.logger.info(f"Broadcast message sent to {len(message_ids)} agents")
            return message_ids

        except Exception as e:
            self.logger.error(f"Failed to broadcast message: {e}")
            return []

    def register_delivery_callback(self, message_type: MessageType, callback: Callable):
        """Register a callback for message delivery"""
        self.delivery_callbacks[message_type.value] = callback
        self.logger.info(f"Registered delivery callback for {message_type.value}")

    def get_message_status(self, message_id: str) -> Optional[MessageStatus]:
        """Get the delivery status of a message"""
        if message_id in self.message_history:
            return self.message_history[message_id].status
        return None

    def get_pending_messages(self, recipient_id: str) -> List[Message]:
        """Get all pending messages for a recipient"""
        pending_messages = []
        for message in self.message_history.values():
            if (
                message.recipient_id == recipient_id
                and message.status == MessageStatus.PENDING
                and not self._is_message_expired(message)
            ):
                pending_messages.append(message)

        # Sort by priority and timestamp
        pending_messages.sort(
            key=lambda m: (self._get_priority_value(m.priority), m.timestamp)
        )
        return pending_messages

    def _start_routing_thread(self):
        """Start the message routing thread"""
        self.running = True
        self.routing_thread = threading.Thread(target=self._routing_loop, daemon=True)
        self.routing_thread.start()

    def _routing_loop(self):
        """Main routing loop for processing messages"""
        while self.running:
            try:
                if not self.message_queue.empty():
                    priority, message = self.message_queue.get()

                    # Check if message is expired
                    if self._is_message_expired(message):
                        message.status = MessageStatus.EXPIRED
                        self._update_message_status(message)
                        continue

                    # Attempt delivery
                    success = self._attempt_delivery(message)

                    if success:
                        message.status = MessageStatus.DELIVERED
                        self._update_message_status(message)
                    else:
                        # Handle retry logic
                        if message.delivery_attempts < message.max_attempts:
                            message.delivery_attempts += 1
                            # Re-queue with lower priority for retry
                            retry_priority = (
                                priority + 1000
                            )  # Lower priority for retries
                            self.message_queue.put((retry_priority, message))
                            self.logger.warning(
                                f"Message {message.message_id} queued for retry"
                            )
                        else:
                            message.status = MessageStatus.FAILED
                            self._update_message_status(message)
                            self.logger.error(
                                f"Message {message.message_id} delivery failed after {message.max_attempts} attempts"
                            )

                time.sleep(0.1)  # Small delay to prevent busy waiting

            except Exception as e:
                self.logger.error(f"Routing loop error: {e}")
                time.sleep(1)

    def _attempt_delivery(self, message: Message) -> bool:
        """Attempt to deliver a message"""
        try:
            # Check if we have a callback for this message type
            callback_key = message.message_type.value
            if callback_key in self.delivery_callbacks:
                callback = self.delivery_callbacks[callback_key]
                return callback(message)

            # Default delivery logic
            return self._default_delivery(message)

        except Exception as e:
            self.logger.error(
                f"Delivery attempt failed for message {message.message_id}: {e}"
            )
            return False

    def _default_delivery(self, message: Message) -> bool:
        """Default message delivery logic"""
        try:
            # For now, just mark as delivered
            # In a real system, this would involve actual agent communication
            self.logger.info(
                f"Message {message.message_id} delivered to {message.recipient_id}"
            )
            return True

        except Exception as e:
            self.logger.error(f"Default delivery failed: {e}")
            return False

    def _is_message_expired(self, message: Message) -> bool:
        """Check if a message has expired"""
        if message.expires_at is None:
            return False

        try:
            expires_time = datetime.fromisoformat(message.expires_at)
            return datetime.now() > expires_time
        except Exception:
            return False

    def _get_priority_value(self, priority: MessagePriority) -> int:
        """Get numeric priority value for queue ordering"""
        priority_map = {
            MessagePriority.LOW: 1000,
            MessagePriority.NORMAL: 500,
            MessagePriority.HIGH: 100,
            MessagePriority.URGENT: 0,
        }
        return priority_map.get(priority, 500)

    def _get_all_agent_ids(self) -> List[str]:
        """Get all available agent IDs"""
        # This would typically query the agent manager
        # For now, return a default list
        return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]

    def _save_message(self, message: Message):
        """Save message to file"""
        try:
            message_file = self.messages_dir / f"{message.message_id}.json"
            message_data = asdict(message)
            message_data["message_type"] = message.message_type.value
            message_data["priority"] = message.priority.value
            message_data["status"] = message.status.value

            with open(message_file, "w") as f:
                json.dump(message_data, f, indent=2, default=str)

        except Exception as e:
            self.logger.error(f"Failed to save message {message.message_id}: {e}")

    def _update_message_status(self, message: Message):
        """Update message status in file"""
        self._save_message(message)

    def get_routing_stats(self) -> Dict[str, Any]:
        """Get routing statistics"""
        try:
            total_messages = len(self.message_history)
            pending_messages = len(
                [
                    m
                    for m in self.message_history.values()
                    if m.status == MessageStatus.PENDING
                ]
            )
            delivered_messages = len(
                [
                    m
                    for m in self.message_history.values()
                    if m.status == MessageStatus.DELIVERED
                ]
            )
            failed_messages = len(
                [
                    m
                    for m in self.message_history.values()
                    if m.status == MessageStatus.FAILED
                ]
            )

            return {
                "total_messages": total_messages,
                "pending_messages": pending_messages,
                "delivered_messages": delivered_messages,
                "failed_messages": failed_messages,
                "queue_size": self.message_queue.qsize(),
                "delivery_callbacks": len(self.delivery_callbacks),
            }
        except Exception as e:
            self.logger.error(f"Failed to get routing stats: {e}")
            return {"error": str(e)}

    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test message sending
            message_id = self.send_message(
                "Agent-1",
                "Agent-2",
                MessageType.STATUS_UPDATE,
                {"status": "online"},
                MessagePriority.NORMAL,
            )
            if not message_id:
                return False

            # Test broadcast
            broadcast_ids = self.broadcast_message(
                "Agent-1",
                MessageType.COORDINATION,
                {"action": "sync"},
                MessagePriority.NORMAL,
            )
            if len(broadcast_ids) == 0:
                return False

            # Test message status
            status = self.get_message_status(message_id)
            if status != MessageStatus.PENDING:
                return False

            # Test pending messages
            pending = self.get_pending_messages("Agent-2")
            if len(pending) == 0:
                return False

            # Test routing stats
            stats = self.get_routing_stats()
            if "total_messages" not in stats:
                return False

            return True

        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False

    def shutdown(self):
        """Shutdown the message router"""
        self.running = False
        if self.routing_thread:
            self.routing_thread.join(timeout=5)


def run_smoke_test():
    """Run basic functionality test for MessageRouter"""
    print("🧪 Running MessageRouter Smoke Test...")

    try:
        import tempfile

        with tempfile.TemporaryDirectory() as temp_dir:
            router = MessageRouter(temp_dir)

            # Test message sending
            message_id = router.send_message(
                "Agent-1",
                "Agent-2",
                MessageType.STATUS_UPDATE,
                {"status": "online"},
                MessagePriority.NORMAL,
            )
            assert message_id

            # Test broadcast
            broadcast_ids = router.broadcast_message(
                "Agent-1",
                MessageType.COORDINATION,
                {"action": "sync"},
                MessagePriority.NORMAL,
            )
            assert len(broadcast_ids) > 0

            # Test message status
            status = router.get_message_status(message_id)
            assert status == MessageStatus.PENDING

            # Test pending messages
            pending = router.get_pending_messages("Agent-2")
            assert len(pending) > 0

            # Test routing stats
            stats = router.get_routing_stats()
            assert "total_messages" in stats

            router.shutdown()

        print("✅ MessageRouter Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ MessageRouter Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for MessageRouter testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Message Router CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--send",
        nargs=4,
        metavar=("SENDER", "RECIPIENT", "TYPE", "CONTENT"),
        help="Send message",
    )
    parser.add_argument(
        "--broadcast",
        nargs=3,
        metavar=("SENDER", "TYPE", "CONTENT"),
        help="Broadcast message",
    )
    parser.add_argument("--status", help="Get message status by ID")
    parser.add_argument("--pending", help="Get pending messages for agent")
    parser.add_argument("--stats", action="store_true", help="Show routing statistics")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    router = MessageRouter()

    if args.send:
        sender, recipient, msg_type, content = args.send
        try:
            message_type = MessageType(msg_type)
            message_id = router.send_message(
                sender, recipient, message_type, {"data": content}
            )
            print(f"Message sent: {'✅ Success' if message_id else '❌ Failed'}")
            if message_id:
                print(f"Message ID: {message_id}")
        except ValueError:
            print(f"❌ Invalid message type: {msg_type}")
            print(f"Valid types: {[t.value for t in MessageType]}")
    elif args.broadcast:
        sender, msg_type, content = args.broadcast
        try:
            message_type = MessageType(msg_type)
            message_ids = router.broadcast_message(
                sender, message_type, {"data": content}
            )
            print(f"Broadcast sent: {'✅ Success' if message_ids else '❌ Failed'}")
            print(f"Messages sent: {len(message_ids)}")
        except ValueError:
            print(f"❌ Invalid message type: {msg_type}")
            print(f"Valid types: {[t.value for t in MessageType]}")
    elif args.status:
        status = router.get_message_status(args.status)
        if status:
            print(f"Message status: {status.value}")
        else:
            print(f"Message '{args.status}' not found")
    elif args.pending:
        pending = router.get_pending_messages(args.pending)
        print(f"Pending messages for {args.pending}:")
        for msg in pending:
            print(f"  {msg.message_id}: {msg.message_type.value} from {msg.sender_id}")
    elif args.stats:
        stats = router.get_routing_stats()
        print("Routing Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    else:
        parser.print_help()

    router.shutdown()


if __name__ == "__main__":
    main()
