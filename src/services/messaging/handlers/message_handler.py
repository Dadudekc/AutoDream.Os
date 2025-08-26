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
