#!/usr/bin/env python3
"""
Message Identity Clarification - Agent Cellphone V2
==================================================

Provides message formatting with agent identity clarification to prevent confusion.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .models.messaging_models import UnifiedMessage


class MessageIdentityClarification:
    """Handles message formatting with agent identity clarification."""

    def __init__(self):

EXAMPLE USAGE:
==============

# Import the service
from src.services.message_identity_clarification import Message_Identity_ClarificationService

# Initialize service
service = Message_Identity_ClarificationService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Message_Identity_ClarificationService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Initialize the message identity clarification system."""
        pass

    def format_message_with_identity_clarification(
        self, message: UnifiedMessage, recipient: str
    ) -> str:
        """Format message with agent identity clarification.

        Args:
            message: The message to format
            recipient: The recipient agent

        Returns:
            Formatted message with identity clarification
        """
        # Base agent identity reminder
        agent_reminder = f"🚨 **ATTENTION {recipient}** - YOU ARE {recipient} 🚨\n\n"

        # Add message type-specific header
        message_type_header = ""
        if message.message_type.value == "agent_to_agent":
            message_type_header = "📡 **A2A MESSAGE (Agent-to-Agent)**\n"
            message_type_header += f"📤 **FROM:** {message.sender} (Agent)\n"
            message_type_header += f"📥 **TO:** {recipient} (Agent)\n\n"
        elif message.message_type.value == "system_to_agent":
            message_type_header = "📡 **S2A MESSAGE (System-to-Agent)**\n"
            message_type_header += f"📤 **FROM:** {message.sender} (System)\n"
            message_type_header += f"📥 **TO:** {recipient} (Agent)\n\n"
        elif message.message_type.value == "human_to_agent":
            message_type_header = "📡 **H2A MESSAGE (Human-to-Agent)**\n"
            message_type_header += f"📤 **FROM:** {message.sender} (Human)\n"
            message_type_header += f"📥 **TO:** {recipient} (Agent)\n\n"
        elif message.message_type.value == "onboarding":
            message_type_header = "📡 **S2A ONBOARDING MESSAGE (System-to-Agent)**\n"
            message_type_header += f"📤 **FROM:** {message.sender} (System)\n"
            message_type_header += f"📥 **TO:** {recipient} (Agent)\n\n"
        elif message.message_type.value == "captain_to_agent":
            message_type_header = "📡 **C2A MESSAGE (Captain-to-Agent)**\n"
            message_type_header += f"📤 **FROM:** {message.sender} (Captain)\n"
            message_type_header += f"📥 **TO:** {recipient} (Agent)\n\n"
        elif message.message_type.value == "broadcast":
            message_type_header = "📡 **BROADCAST MESSAGE**\n"
            message_type_header += f"📤 **FROM:** {message.sender}\n"
            message_type_header += "📥 **TO:** All Agents\n\n"

        # Add priority information
        priority_info = ""
        if message.priority.value == "urgent":
            priority_info = "🚨 **PRIORITY: URGENT** 🚨\n\n"

        # Combine all formatting
        formatted_message = agent_reminder + message_type_header + priority_info + message.content

        return formatted_message


# Global instance for easy access
_message_identity_clarification = MessageIdentityClarification()


def format_message_with_identity_clarification(message: UnifiedMessage, recipient: str) -> str:
    """Format message with agent identity clarification."""
    return _message_identity_clarification.format_message_with_identity_clarification(
        message, recipient
    )
