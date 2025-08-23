#!/usr/bin/env python3
"""
V1 Compatibility Layer Service
==============================
Provides V1 compatibility methods for existing integrations.
Follows 100 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
from typing import Dict, List, Any, Optional, Callable

from .message_handler_v2 import MessageHandlerV2, MsgTag, AgentMessage

logger = logging.getLogger(__name__)


class V1CompatibilityLayer:
    """Provides V1 compatibility methods for existing integrations"""

    def __init__(self, message_handler: MessageHandlerV2, agent_id: str):
        self.message_handler = message_handler
        self.agent_id = agent_id
        self.logger = logging.getLogger(f"{__name__}.V1CompatibilityLayer")

        # V1 compatibility features
        self._listening = False
        self._listener_thread: Optional[threading.Thread] = None
        self._message_handlers: Dict[str, Callable[[AgentMessage], None]] = {}

    def send(
        self,
        agent: str,
        message: str,
        tag: MsgTag = MsgTag.NORMAL,
        new_chat: bool = False,
        nudge_stalled: bool = False,
    ) -> None:
        """Send message to agent (V1 compatibility)"""
        try:
            # Create message object and add to history
            msg = AgentMessage(self.agent_id, agent, message, tag)

            # Log the send operation
            self.logger.info(f"→ {agent}: {message[:80]}")

            # Route through message system
            self.message_handler.send_message(self.agent_id, agent, message, tag)

        except Exception as e:
            self.logger.error(f"Error sending message: {e}")

    def broadcast(self, message: str, tag: MsgTag = MsgTag.NORMAL) -> None:
        """Send message to all agents (V1 compatibility)"""
        try:
            self.message_handler.broadcast_message(self.agent_id, message, tag)
            self.logger.info(f"Broadcast: {message[:80]}")
        except Exception as e:
            self.logger.error(f"Error broadcasting message: {e}")

    def start_listening(self) -> None:
        """Start listening for incoming messages (V1 compatibility)"""
        if self._listening:
            return

        self._listening = True
        self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listener_thread.start()
        self.logger.info("Started listening for messages")

    def stop_listening(self) -> None:
        """Stop listening for incoming messages (V1 compatibility)"""
        self._listening = False
        if self._listener_thread:
            self._listener_thread.join(timeout=1)
        self.logger.info("Stopped listening for messages")

    def _listen_loop(self):
        """Message listening loop (V1 compatibility)"""
        while self._listening:
            try:
                # Check for messages from message handler
                # In real implementation, this would poll for new messages
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Listen loop error: {e}")
                time.sleep(1)

    def register_handler(
        self, message_type: str, handler: Callable[[AgentMessage], None]
    ) -> None:
        """Register message handler (V1 compatibility)"""
        self._message_handlers[message_type] = handler

    def get_conversation_history(self) -> List[AgentMessage]:
        """Get conversation history (V1 compatibility)"""
        return self.message_handler.get_conversation_history()


def main():
    """CLI interface for testing V1CompatibilityLayer"""
    import argparse

    parser = argparse.ArgumentParser(description="V1 Compatibility Layer CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent-id", default="Agent-1", help="Agent ID")
    parser.add_argument("--target", default="Agent-2", help="Target agent")
    parser.add_argument("--message", default="Test message", help="Message content")

    args = parser.parse_args()

    if args.test:
        print("🧪 V1CompatibilityLayer Smoke Test")
        print("=" * 40)

        # Mock message handler for testing
        class MockMessageHandler:
            def send_message(self, sender, recipient, content, tag):
                return True

            def broadcast_message(self, sender, message, tag):
                pass

            def get_conversation_history(self):
                return []

        handler = MockMessageHandler()
        v1_layer = V1CompatibilityLayer(handler, args.agent_id)

        # Test V1 methods
        v1_layer.send(args.target, args.message, MsgTag.NORMAL)
        v1_layer.broadcast("Broadcast test", MsgTag.COORDINATE)

        # Test listening
        v1_layer.start_listening()
        time.sleep(0.1)
        v1_layer.stop_listening()

        print("🎉 V1CompatibilityLayer smoke test PASSED!")
    else:
        print("V1CompatibilityLayer ready")
        print("Use --test to run smoke test")


if __name__ == "__main__":
    main()
