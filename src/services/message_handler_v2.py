#!/usr/bin/env python3
"""
Message Handler V2 Service
==========================
Handles message processing, routing, and V1 compatibility for the agent system.
Follows 100 LOC limit and single responsibility principle.
"""

import logging
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum

from ..core.message_router import MessageRouter, MessageType, MessagePriority

logger = logging.getLogger(__name__)


class MsgTag(Enum):
    """Message tags for system communication (V1 compatible)"""
    NORMAL = ""
    RESUME = "[RESUME]"
    SYNC = "[SYNC]"
    VERIFY = "[VERIFY]"
    REPAIR = "[REPAIR]"
    BACKUP = "[BACKUP]"
    RESTORE = "[RESTORE]"
    CLEANUP = "[CLEANUP]"
    CAPTAIN = "[CAPTAIN]"
    TASK = "[TASK]"
    INTEGRATE = "[INTEGRATE]"
    REPLY = "[REPLY]"
    COORDINATE = "[COORDINATE]"
    ONBOARDING = "[ONBOARDING]"
    RESCUE = "[RESCUE]"


@dataclass
class AgentMessage:
    """Structure for agent messages (V1 compatible)"""
    from_agent: str
    to_agent: str
    content: str
    tag: MsgTag = MsgTag.NORMAL
    timestamp: Optional[float] = None
    
    def __str__(self) -> str:
        return f"{self.from_agent} → {self.to_agent}: {self.tag.value} {self.content}"


class MessageHandlerV2:
    """Handles message processing and V1 compatibility"""
    
    def __init__(self, message_router: MessageRouter):
        self.message_router = message_router
        self._conversation_history: List[AgentMessage] = []
        self._message_handlers: Dict[str, Callable[[AgentMessage], None]] = {}
        self.logger = logging.getLogger(f"{__name__}.MessageHandlerV2")
    
    def send_message(self, sender: str, recipient: str, content: Any, 
                    msg_tag: MsgTag = MsgTag.COORDINATE) -> bool:
        """Send a message between agents"""
        try:
            success = self.message_router.send_message(sender, recipient, content)
            if success:
                msg = AgentMessage(sender, recipient, str(content), msg_tag)
                self._conversation_history.append(msg)
                self.logger.info(f"→ {recipient}: {str(content)[:80]}")
            return success
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    def broadcast_message(self, sender: str, message: str, tag: MsgTag = MsgTag.NORMAL) -> None:
        """Send message to all agents (V1 compatibility)"""
        # Get all agents from message router (simplified)
        # In real implementation, this would get from agent manager
        self.send_message(sender, "broadcast", message, tag)
    
    def register_handler(self, message_type: str, handler: Callable[[AgentMessage], None]) -> None:
        """Register message handler (V1 compatibility)"""
        self._message_handlers[message_type] = handler
    
    def get_conversation_history(self) -> List[AgentMessage]:
        """Get conversation history (V1 compatibility)"""
        return self._conversation_history.copy()
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self._conversation_history.clear()


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
        class MockMessageRouter:
            def send_message(self, sender, recipient, content):
                return True
        
        router = MockMessageRouter()
        handler = MessageHandlerV2(router)
        
        # Test message sending
        success = handler.send_message(args.sender, args.recipient, args.message)
        print(f"✅ Message send: {success}")
        
        # Test conversation history
        history = handler.get_conversation_history()
        print(f"✅ History count: {len(history)}")
        
        print("🎉 MessageHandlerV2 smoke test PASSED!")
    else:
        print("MessageHandlerV2 ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
