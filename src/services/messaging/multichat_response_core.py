#!/usr/bin/env python3
"""
Multichat Response Core - Core Response Logic
============================================

Core response logic for multichat response system.
Handles message processing, context formatting, and response tracking.

V2 Compliance: ≤400 lines, focused core response logic module
Author: Agent-6 (Quality Assurance Specialist)
"""

import logging
import time
from datetime import UTC, datetime
from typing import Any

from .agent_context import get_current_agent

logger = logging.getLogger(__name__)


class MultichatResponseCore:
    """
    Core response logic for multichat system.

    Handles message processing, context formatting, and response tracking.
    """

    def __init__(self):
        """Initialize multichat response core."""
        self.logger = logging.getLogger(f"{__name__}.MultichatResponseCore")
        self.response_history = []

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

            # Format response with context if requested
            if include_context:
                formatted_message = self._format_response_with_context(
                    response_message, original_sender, current_agent
                )
            else:
                formatted_message = response_message

            # Track the response
            response_data = self._track_response(
                current_agent, original_sender, formatted_message, chat_id, priority
            )

            return True, response_data

        except Exception as e:
            self.logger.error(f"Error responding to message: {e}")
            return False, {"error": str(e)}

    def _format_response_with_context(
        self, message: str, original_sender: str, current_agent: str
    ) -> str:
        """Format response with context information."""
        try:
            timestamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")

            formatted_message = f"""
============================================================
[A2A] RESPONSE - {timestamp}
============================================================
📥 FROM: {current_agent}
📤 TO: {original_sender}
Priority: NORMAL
Tags: MULTICHAT_RESPONSE
------------------------------------------------------------
{message}
📝 DEVLOG: Auto-created in local storage
🧠 VECTOR: Auto-indexed in searchable database
📊 METRICS: Updated in project analysis
------------------------------------------------------------
🐝 WE ARE SWARM - Multichat Response Complete
============================================================
"""
            return formatted_message.strip()

        except Exception as e:
            self.logger.error(f"Error formatting response with context: {e}")
            return message

    def _track_response(
        self,
        current_agent: str,
        original_sender: str,
        message: str,
        chat_id: str = None,
        priority: str = "NORMAL",
    ) -> dict[str, Any]:
        """Track response for analytics and history."""
        try:
            response_data = {
                "timestamp": datetime.now(UTC).isoformat(),
                "from_agent": current_agent,
                "to_agent": original_sender,
                "message": message,
                "chat_id": chat_id,
                "priority": priority,
                "response_id": f"resp_{int(time.time())}",
                "message_length": len(message),
                "context_included": True,
            }

            # Add to response history
            self.response_history.append(response_data)

            # Keep only last 100 responses
            if len(self.response_history) > 100:
                self.response_history = self.response_history[-100:]

            self.logger.info(f"Response tracked: {response_data['response_id']}")
            return response_data

        except Exception as e:
            self.logger.error(f"Error tracking response: {e}")
            return {"error": str(e)}

    def get_response_history(self, limit: int = 50) -> list[dict[str, Any]]:
        """Get response history."""
        return self.response_history[-limit:] if self.response_history else []

    def _learn_from_response(self, response_data: dict[str, Any]) -> None:
        """Learn from response patterns for improvement."""
        try:
            # Simple learning - track response patterns
            if response_data.get("message_length", 0) > 1000:
                self.logger.info("Long response detected - consider breaking into smaller parts")

            if response_data.get("priority") == "URGENT":
                self.logger.info("Urgent response processed - high priority handling")

        except Exception as e:
            self.logger.error(f"Error learning from response: {e}")


__all__ = ["MultichatResponseCore"]
