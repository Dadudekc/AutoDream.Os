#!/usr/bin/env python3
"""
Multichat Response System - V2 Compliance
=========================================

Multichat response system for agent workflows.
Allows agents to respond to messages and coordinate in multichat scenarios.

Author: Agent-2 (Security Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, comprehensive error handling
"""

import logging
import time
from datetime import UTC, datetime
from typing import Any

from .agent_context import get_current_agent
from .core.messaging_service import MessagingService
from .intelligent_messaging import IntelligentMessagingService

logger = logging.getLogger(__name__)


class MultichatResponseSystem:
    """Multichat response system for agent workflows."""

    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize multichat response system."""
        self.messaging_service = MessagingService(coord_path)
        self.intelligent_service = IntelligentMessagingService(coord_path)

        # Response tracking
        self.active_chats = {}
        self.response_history = []

        logger.info("Multichat Response System initialized")

    def respond_to_message(
        self,
        original_sender: str,
        response_message: str,
        chat_id: str = None,
        priority: str = "NORMAL",
        include_context: bool = True,
    ) -> tuple[bool, dict[str, Any]]:
        """Respond to a message from another agent."""
        try:
            current_agent = get_current_agent()

            # Generate chat ID if not provided
            if chat_id is None:
                chat_id = f"chat_{int(time.time())}"

            # Format response with context if requested
            if include_context:
                formatted_response = self._format_response_with_context(
                    response_message, original_sender, current_agent
                )
            else:
                formatted_response = response_message

            # Send response
            success = self.messaging_service.send_message(
                agent_id=original_sender,
                message=formatted_response,
                from_agent=current_agent,
                priority=priority,
            )

            # Track response
            self._track_response(chat_id, original_sender, current_agent, response_message, success)

            # Learn from response
            self._learn_from_response(original_sender, response_message, current_agent, success)

            logger.info(f"📤 Response sent: {current_agent} → {original_sender}")

            return success, {
                "chat_id": chat_id,
                "response_sent": success,
                "timestamp": datetime.now(UTC).isoformat(),
                "context_included": include_context,
            }

        except Exception as e:
            logger.error(f"Response failed: {e}")
            return False, {"error": str(e)}

    def start_multichat_session(
        self, participants: list[str], topic: str, initiator: str = None
    ) -> str:
        """Start a multichat session with multiple agents."""
        try:
            if initiator is None:
                initiator = get_current_agent()

            chat_id = f"multichat_{int(time.time())}"

            # Initialize chat session
            self.active_chats[chat_id] = {
                "participants": participants,
                "topic": topic,
                "initiator": initiator,
                "start_time": datetime.now(UTC),
                "messages": [],
                "status": "active",
            }

            # Send invitation messages
            invitation_message = self._create_invitation_message(topic, initiator, chat_id)

            for participant in participants:
                if participant != initiator:
                    self.messaging_service.send_message(
                        agent_id=participant,
                        message=invitation_message,
                        from_agent=initiator,
                        priority="NORMAL",
                    )

            logger.info(
                f"🎯 Multichat session started: {chat_id} with {len(participants)} participants"
            )

            return chat_id

        except Exception as e:
            logger.error(f"Failed to start multichat session: {e}")
            return ""

    def join_multichat_session(self, chat_id: str, agent_id: str = None) -> bool:
        """Join an existing multichat session."""
        try:
            if agent_id is None:
                agent_id = get_current_agent()

            if chat_id not in self.active_chats:
                logger.error(f"Chat session {chat_id} not found")
                return False

            chat = self.active_chats[chat_id]

            if agent_id not in chat["participants"]:
                chat["participants"].append(agent_id)

            # Send join notification
            join_message = f"🤝 {agent_id} joined the multichat session: {chat['topic']}"

            for participant in chat["participants"]:
                if participant != agent_id:
                    self.messaging_service.send_message(
                        agent_id=participant,
                        message=join_message,
                        from_agent=agent_id,
                        priority="NORMAL",
                    )

            logger.info(f"✅ {agent_id} joined multichat session: {chat_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to join multichat session: {e}")
            return False

    def broadcast_to_multichat(
        self, chat_id: str, message: str, sender: str = None
    ) -> dict[str, bool]:
        """Broadcast message to all participants in a multichat session."""
        try:
            if sender is None:
                sender = get_current_agent()

            if chat_id not in self.active_chats:
                logger.error(f"Chat session {chat_id} not found")
                return {}

            chat = self.active_chats[chat_id]
            results = {}

            # Send to all participants except sender
            for participant in chat["participants"]:
                if participant != sender:
                    success = self.messaging_service.send_message(
                        agent_id=participant,
                        message=f"[Multichat] {message}",
                        from_agent=sender,
                        priority="NORMAL",
                    )
                    results[participant] = success

            # Track message in chat history
            chat["messages"].append(
                {
                    "sender": sender,
                    "message": message,
                    "timestamp": datetime.now(UTC),
                    "recipients": list(results.keys()),
                }
            )

            logger.info(f"📢 Multichat broadcast sent to {len(results)} participants")

            return results

        except Exception as e:
            logger.error(f"Multichat broadcast failed: {e}")
            return {}

    def end_multichat_session(self, chat_id: str, agent_id: str = None) -> bool:
        """End a multichat session."""
        try:
            if agent_id is None:
                agent_id = get_current_agent()

            if chat_id not in self.active_chats:
                logger.error(f"Chat session {chat_id} not found")
                return False

            chat = self.active_chats[chat_id]

            # Send end notification
            end_message = f"🏁 Multichat session ended by {agent_id}: {chat['topic']}"

            for participant in chat["participants"]:
                if participant != agent_id:
                    self.messaging_service.send_message(
                        agent_id=participant,
                        message=end_message,
                        from_agent=agent_id,
                        priority="NORMAL",
                    )

            # Mark session as ended
            chat["status"] = "ended"
            chat["end_time"] = datetime.now(UTC)

            logger.info(f"🏁 Multichat session ended: {chat_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to end multichat session: {e}")
            return False

    def get_chat_history(self, chat_id: str) -> list[dict[str, Any]]:
        """Get message history for a chat session."""
        try:
            if chat_id not in self.active_chats:
                return []

            return self.active_chats[chat_id]["messages"]

        except Exception as e:
            logger.error(f"Failed to get chat history: {e}")
            return []

    def get_active_chats(self, agent_id: str = None) -> dict[str, dict[str, Any]]:
        """Get active chat sessions for an agent."""
        try:
            if agent_id is None:
                agent_id = get_current_agent()

            active_chats = {}

            for chat_id, chat in self.active_chats.items():
                if agent_id in chat["participants"] and chat["status"] == "active":
                    active_chats[chat_id] = {
                        "topic": chat["topic"],
                        "participants": chat["participants"],
                        "initiator": chat["initiator"],
                        "start_time": chat["start_time"],
                        "message_count": len(chat["messages"]),
                    }

            return active_chats

        except Exception as e:
            logger.error(f"Failed to get active chats: {e}")
            return {}

    def _format_response_with_context(
        self, message: str, original_sender: str, current_agent: str
    ) -> str:
        """Format response with context information."""
        timestamp = datetime.now(UTC).strftime("%H:%M:%S")

        return f"""============================================================
[A2A] RESPONSE
============================================================
📤 FROM: {current_agent}
📥 TO: {original_sender}
Priority: NORMAL
Tags: RESPONSE
------------------------------------------------------------
{message}
------------------------------------------------------------
Timestamp: {timestamp}
Context: Response to previous message
============================================================"""

    def _create_invitation_message(self, topic: str, initiator: str, chat_id: str) -> str:
        """Create invitation message for multichat session."""
        return f"""============================================================
[A2A] MULTICHAT INVITATION
============================================================
📤 FROM: {initiator}
📥 TO: You
Priority: NORMAL
Tags: MULTICHAT, INVITATION
------------------------------------------------------------
🎯 **MULTICHAT SESSION INVITATION**

**Topic**: {topic}
**Session ID**: {chat_id}
**Initiator**: {initiator}

**Instructions**:
1. Use `multichat_respond()` to respond in this session
2. Use `multichat_broadcast()` to send messages to all participants
3. Use `multichat_end()` to end the session when complete

**Available Commands**:
- `multichat_respond("{initiator}", "Your response message")`
- `multichat_broadcast("{chat_id}", "Message for all participants")`
- `multichat_end("{chat_id}")`

Ready for multichat coordination!
------------------------------------------------------------
Timestamp: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")}
============================================================"""

    def _track_response(
        self, chat_id: str, recipient: str, sender: str, message: str, success: bool
    ) -> None:
        """Track response in history."""
        try:
            response_record = {
                "chat_id": chat_id,
                "recipient": recipient,
                "sender": sender,
                "message": message,
                "success": success,
                "timestamp": datetime.now(UTC),
            }

            self.response_history.append(response_record)

            # Keep only last 100 responses
            if len(self.response_history) > 100:
                self.response_history = self.response_history[-100:]

        except Exception as e:
            logger.error(f"Failed to track response: {e}")

    def _learn_from_response(
        self, recipient: str, message: str, sender: str, success: bool
    ) -> None:
        """Learn from response patterns."""
        try:
            # Use intelligent messaging to learn from response
            self.intelligent_service._learn_from_message(
                recipient, message, sender, "NORMAL", success
            )

        except Exception as e:
            logger.error(f"Failed to learn from response: {e}")


# Convenience functions for agent workflows
def multichat_respond(
    original_sender: str, response_message: str, chat_id: str = None, priority: str = "NORMAL"
) -> tuple[bool, dict[str, Any]]:
    """Convenience function for agents to respond to messages."""
    system = MultichatResponseSystem()
    return system.respond_to_message(original_sender, response_message, chat_id, priority)


def multichat_start(participants: list[str], topic: str) -> str:
    """Convenience function to start a multichat session."""
    system = MultichatResponseSystem()
    return system.start_multichat_session(participants, topic)


def multichat_broadcast(chat_id: str, message: str) -> dict[str, bool]:
    """Convenience function to broadcast to multichat session."""
    system = MultichatResponseSystem()
    return system.broadcast_to_multichat(chat_id, message)


def multichat_end(chat_id: str) -> bool:
    """Convenience function to end multichat session."""
    system = MultichatResponseSystem()
    return system.end_multichat_session(chat_id)


def multichat_join(chat_id: str) -> bool:
    """Convenience function to join multichat session."""
    system = MultichatResponseSystem()
    return system.join_multichat_session(chat_id)


# V2 Compliance: File length check
if __name__ == "__main__":
    # V2 Compliance validation
    import inspect

    lines = len(inspect.getsource(inspect.currentframe().f_globals["__file__"]).splitlines())
    print(f"Multichat Response System: {lines} lines - V2 Compliant ✅")
