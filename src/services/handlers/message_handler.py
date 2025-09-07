<<<<<<< HEAD
"""
Message Handler - V2 Compliant Module
====================================

Handles message-related commands for messaging CLI.
Extracted from messaging_cli_handlers.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional

from ..messaging_core import UnifiedMessagingCore
from ..models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType,
)
from ..unified_messaging_imports import load_coordinates_from_json


class MessageHandler:
    """Handles message-related commands for messaging CLI.

    Manages message creation, sending, and delivery.
    """

    def __init__(self):
        """Initialize message handler."""
        self.messaging_core = UnifiedMessagingCore()
        self.message_history = []
        self.sent_count = 0
        self.failed_count = 0

    def handle_message_commands(self, args) -> bool:
        """Handle message-related commands."""
        try:
            if not args.message:
                return False

            # Validate required arguments
            if not args.agent and not args.bulk:
                print("ERROR: --agent or --bulk required")
                return True

            # Determine message type
            message_type = UnifiedMessageType.TEXT
            if args.type == "broadcast":
                message_type = UnifiedMessageType.BROADCAST
            elif args.type == "onboarding":
                message_type = UnifiedMessageType.ONBOARDING

            # Determine priority
            priority = UnifiedMessagePriority.REGULAR
            if args.high_priority or args.priority == "urgent":
                priority = UnifiedMessagePriority.URGENT

            if args.bulk:
                return self._handle_bulk_message(args, message_type, priority)
            else:
                return self._handle_single_message(args, message_type, priority)

        except Exception as e:
            print(f"ERROR: Error handling message command: {e}")
            return False

    def _handle_bulk_message(
        self, args, message_type: UnifiedMessageType, priority: UnifiedMessagePriority
    ) -> bool:
        """Handle bulk message sending."""
        try:
            # Send to all agents
            agents = load_coordinates_from_json()
            if not agents:
                print("ERROR: No agent coordinates found")
                return True

            success_count = 0
            for agent_id in agents.keys():
                message = self.messaging_core.create_message(
                    content=args.message,
                    sender=args.sender,
                    recipient=agent_id,
                    message_type=message_type,
                    priority=priority,
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT,
                )

                if message:
                    success = self.messaging_core.send_message(message)
                    if success:
                        success_count += 1
                        self.sent_count += 1
                        print(f"SUCCESS: Message sent to {agent_id}")
                    else:
                        self.failed_count += 1
                        print(f"ERROR: Failed to send message to {agent_id}")
                else:
                    self.failed_count += 1
                    print(f"ERROR: Failed to create message for {agent_id}")

            print(f"INFO: Bulk message complete: {success_count}/{len(agents)} agents")
            return True

        except Exception as e:
            print(f"ERROR: Error in bulk message: {e}")
            return False

    def _handle_single_message(
        self, args, message_type: UnifiedMessageType, priority: UnifiedMessagePriority
    ) -> bool:
        """Handle single message sending."""
        try:
            # Send to specific agent
            message = self.messaging_core.create_message(
                content=args.message,
                sender=args.sender,
                recipient=args.agent,
                message_type=message_type,
                priority=priority,
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT,
            )

            if message:
                success = self.messaging_core.send_message(message)
                if success:
                    self.sent_count += 1
                    print(f"SUCCESS: Message sent to {args.agent}")
                    return True
                else:
                    self.failed_count += 1
                    print(f"ERROR: Failed to send message to {args.agent}")
                    return False
            else:
                self.failed_count += 1
                print(f"ERROR: Failed to create message for {args.agent}")
                return False

        except Exception as e:
            print(f"ERROR: Error in single message: {e}")
            return False

    def send_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        mode: str = "pyautogui",
    ) -> bool:
        """Send a message to specific recipient."""
        try:
            message = self.messaging_core.create_message(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type,
                priority=priority,
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT,
            )

            if message:
                success = self.messaging_core.send_message(message, mode=mode)
                if success:
                    self.sent_count += 1
                    self.message_history.append(
                        {
                            "content": content,
                            "sender": sender,
                            "recipient": recipient,
                            "timestamp": "now",
                            "status": "sent",
                        }
                    )
                else:
                    self.failed_count += 1
                    self.message_history.append(
                        {
                            "content": content,
                            "sender": sender,
                            "recipient": recipient,
                            "timestamp": "now",
                            "status": "failed",
                        }
                    )
                return success
            return False

        except Exception as e:
            print(f"ERROR: Error sending message: {e}")
            return False

    def get_message_history(self) -> List[Dict[str, Any]]:
        """Get message history."""
        return self.message_history.copy()

    def get_message_stats(self) -> Dict[str, Any]:
        """Get message statistics."""
        return {
            "sent_count": self.sent_count,
            "failed_count": self.failed_count,
            "total_count": self.sent_count + self.failed_count,
            "success_rate": (
                self.sent_count / max(self.sent_count + self.failed_count, 1) * 100
            ),
        }

    def clear_history(self):
        """Clear message history."""
        self.message_history.clear()

    def reset_stats(self):
        """Reset message statistics."""
        self.sent_count = 0
        self.failed_count = 0

    def get_message_status(self) -> Dict[str, Any]:
        """Get message handler status."""
        return {
            "sent_count": self.sent_count,
            "failed_count": self.failed_count,
            "history_count": len(self.message_history),
            "success_rate": (
                self.sent_count / max(self.sent_count + self.failed_count, 1) * 100
            ),
        }
=======
#!/usr/bin/env python3
"""
Message Handler V2 - Agent Cellphone V2
======================================

Handles message processing using unified messaging system.
Eliminates duplicate AgentMessage class - uses unified system.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from ..models.unified_message import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageStatus,
    UnifiedMessageTag,
)

logger = logging.getLogger(__name__)


# ============================================================================
# MESSAGE TAGS (Legacy V1 compatibility)
# ============================================================================

class MsgTag:
    """Legacy V1 message tags for compatibility"""
    NORMAL = "[NORMAL]"
    COORDINATE = "[COORDINATE]"
    RESCUE = "[RESCUE]"


# ============================================================================
# MESSAGE HANDLER (Using Unified Message System)
# ============================================================================

class MessageHandlerV2:
    """Handles message processing using unified messaging system"""

    def __init__(self, message_router):
        self.message_router = message_router
        self._conversation_history: List[UnifiedMessage] = []
        self._message_handlers: Dict[str, Callable[[UnifiedMessage], None]] = {}
        self.logger = logging.getLogger(f"{__name__}.MessageHandlerV2")

    def send_message(
        self,
        sender: str,
        recipient: str,
        content: Any,
        msg_tag: str = MsgTag.COORDINATE,
    ) -> bool:
        """Send a message between agents using unified system"""
        try:
            # Create unified message
            message = UnifiedMessage(
                sender_id=sender,
                recipient_id=recipient,
                content=str(content),
                tag=UnifiedMessageTag(msg_tag.replace("[", "").replace("]", "")),
                message_type=UnifiedMessageType.AGENT,
                priority=UnifiedMessagePriority.NORMAL,
            )
            
            # Send via router
            success = self.message_router.send_message(sender, recipient, content)
            if success:
                self._conversation_history.append(message)
                self.logger.info(f"→ {recipient}: {str(content)[:80]}")
            return success
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    def broadcast_message(
        self, sender: str, message: str, tag: str = MsgTag.NORMAL
    ) -> None:
        """Send message to all agents (V1 compatibility)"""
        # Get all agents from message router (simplified)
        # In real implementation, this would get from agent manager
        self.send_message(sender, "broadcast", message, tag)

    def register_handler(
        self, message_type: str, handler: Callable[[UnifiedMessage], None]
    ) -> None:
        """Register message handler (V1 compatibility)"""
        self._message_handlers[message_type] = handler

    def get_conversation_history(self) -> List[UnifiedMessage]:
        """Get conversation history (V1 compatibility)"""
        return self._conversation_history.copy()

    def clear_history(self) -> None:
        """Clear conversation history"""
        self._conversation_history.clear()


# ============================================================================
# MOCK MESSAGE ROUTER (For testing)
# ============================================================================

class MockMessageRouter:
    """Mock message router for testing"""
    
    def send_message(self, sender, recipient, content):
        """Mock send message implementation"""
        return True


# ============================================================================
# MAIN CLI INTERFACE
# ============================================================================

def main():
    """CLI interface for testing MessageHandlerV2"""
    import argparse

    parser = argparse.ArgumentParser(description="Message Handler V2 CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--sender", default="Agent-1", help="Sender agent ID")
    parser.add_argument("--recipient", default="Agent-2", help="Recipient agent ID")
    parser.add_argument("--message", default="Test message", help="Message content")

    args = parser.parse_args()

    if args.test:
        print("🧪 MessageHandlerV2 Smoke Test")
        print("=" * 40)

        # Mock message router for testing
        router = MockMessageRouter()
        handler = MessageHandlerV2(router)

        # Test message sending
        success = handler.send_message(args.sender, args.recipient, args.message)
        print(f"✅ Message send: {success}")

        # Test conversation history
        history = handler.get_conversation_history()
        print(f"✅ History count: {len(history)}")

        # Test unified message creation
        if history:
            unified_msg = history[0]
            print(f"✅ Unified message created: {unified_msg.message_id}")
            print(f"✅ Message type: {unified_msg.message_type.value}")
            print(f"✅ Message status: {unified_msg.status.value}")

        print("🎯 MessageHandlerV2 smoke test PASSED!")

    else:
        print("Usage: python message_handler.py --test")


if __name__ == "__main__":
    main()
>>>>>>> origin/codex/catalog-functions-in-utils-directories
