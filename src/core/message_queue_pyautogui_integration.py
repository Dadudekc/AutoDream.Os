#!/usr/bin/env python3
"""
Message Queue PyAutoGUI Integration - Bridge Between Systems
==========================================================

Integrates the file-based message queue system with PyAutoGUI delivery mechanism.

This module provides:
- PyAutoGUI delivery callbacks for the message queue system
- Unified message format conversion between queue entries and UnifiedMessage
- Error handling and retry logic for PyAutoGUI delivery
- Status tracking integration

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

import logging
from typing import Any, Callable

from .message_queue_interfaces import IQueueEntry
from .messaging_core import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)
from .messaging_pyautogui import (
    PYAUTOGUI_AVAILABLE,
    deliver_message_pyautogui,
    get_agent_coordinates,
)

logger = logging.getLogger(__name__)


class MessageQueuePyAutoGUIIntegration:
    """Integration layer between message queue and PyAutoGUI delivery."""

    def __init__(self):
        self.delivery_attempts = 0
        self.successful_deliveries = 0
        self.failed_deliveries = 0

    def create_pyautogui_delivery_callback(self) -> Callable[[Any], bool]:
        """Create a delivery callback that uses PyAutoGUI for message delivery.

        Returns:
            Callback function that can be used with the message queue system
        """
        def pyautogui_delivery_callback(message_data: Any) -> bool:
            """Deliver message via PyAutoGUI to the target agent."""
            try:
                # Convert queue message data to UnifiedMessage format
                unified_message = self._convert_to_unified_message(message_data)

                if not unified_message:
                    logger.error("Failed to convert message data to UnifiedMessage format")
                    return False

                # Get agent coordinates
                coords = get_agent_coordinates(unified_message.recipient)
                if not coords:
                    logger.error(f"No coordinates available for agent: {unified_message.recipient}")
                    return False

                # Attempt delivery via PyAutoGUI
                success = deliver_message_pyautogui(unified_message, coords)

                # Update statistics
                self.delivery_attempts += 1
                if success:
                    self.successful_deliveries += 1
                    logger.info(f"Successfully delivered message to {unified_message.recipient} via PyAutoGUI")
                else:
                    self.failed_deliveries += 1
                    logger.error(f"Failed to deliver message to {unified_message.recipient} via PyAutoGUI")

                return success

            except Exception as e:
                logger.error(f"Error in PyAutoGUI delivery callback: {e}")
                self.delivery_attempts += 1
                self.failed_deliveries += 1
                return False

        return pyautogui_delivery_callback

    def _convert_to_unified_message(self, message_data: Any) -> UnifiedMessage | None:
        """Convert message queue data to UnifiedMessage format.

        Args:
            message_data: Message data from the queue (can be dict, QueueEntry, or raw data)

        Returns:
            UnifiedMessage instance or None if conversion fails
        """
        try:
            # Handle different input formats
            if hasattr(message_data, 'message'):
                # QueueEntry format
                content = getattr(message_data.message, 'content', str(message_data.message))
                recipient = getattr(message_data.message, 'recipient', getattr(message_data, 'recipient', 'unknown'))
                sender = getattr(message_data.message, 'sender', getattr(message_data, 'sender', 'system'))
                message_type = getattr(message_data.message, 'message_type', 'text')
                priority = getattr(message_data.message, 'priority', 'regular')

            elif isinstance(message_data, dict):
                # Dictionary format
                content = message_data.get('content', message_data.get('message', ''))
                recipient = message_data.get('recipient', message_data.get('agent', 'unknown'))
                sender = message_data.get('sender', 'system')
                message_type = message_data.get('message_type', 'text')
                priority = message_data.get('priority', 'regular')

            else:
                # Raw message format
                content = str(message_data)
                recipient = getattr(message_data, 'recipient', 'unknown')
                sender = getattr(message_data, 'sender', 'system')
                message_type = getattr(message_data, 'message_type', 'text')
                priority = getattr(message_data, 'priority', 'regular')

            # Convert string values to enums
            message_type_enum = self._parse_message_type(message_type)
            priority_enum = self._parse_priority(priority)

            # Create UnifiedMessage
            return UnifiedMessage(
                content=content,
                sender=sender,
                recipient=recipient,
                message_type=message_type_enum,
                priority=priority_enum,
                tags=[],  # Can be extended to parse tags from message_data
                metadata={'source': 'message_queue', 'delivery_method': 'pyautogui'}
            )

        except Exception as e:
            logger.error(f"Failed to convert message data to UnifiedMessage: {e}")
            return None

    def _parse_message_type(self, message_type: str) -> UnifiedMessageType:
        """Parse message type string to UnifiedMessageType enum."""
        type_mapping = {
            'text': UnifiedMessageType.TEXT,
            'broadcast': UnifiedMessageType.BROADCAST,
            'onboarding': UnifiedMessageType.ONBOARDING,
            'agent_to_agent': UnifiedMessageType.AGENT_TO_AGENT,
            'captain_to_agent': UnifiedMessageType.CAPTAIN_TO_AGENT,
            'system_to_agent': UnifiedMessageType.SYSTEM_TO_AGENT,
            'human_to_agent': UnifiedMessageType.HUMAN_TO_AGENT,
        }
        return type_mapping.get(message_type.lower(), UnifiedMessageType.TEXT)

    def _parse_priority(self, priority: str) -> UnifiedMessagePriority:
        """Parse priority string to UnifiedMessagePriority enum."""
        priority_mapping = {
            'regular': UnifiedMessagePriority.REGULAR,
            'urgent': UnifiedMessagePriority.URGENT,
            'high': UnifiedMessagePriority.URGENT,  # Map high to urgent
            'low': UnifiedMessagePriority.REGULAR,  # Map low to regular
        }
        return priority_mapping.get(priority.lower(), UnifiedMessagePriority.REGULAR)

    def get_delivery_statistics(self) -> dict[str, int]:
        """Get delivery statistics for monitoring."""
        return {
            'total_attempts': self.delivery_attempts,
            'successful_deliveries': self.successful_deliveries,
            'failed_deliveries': self.failed_deliveries,
            'success_rate': (self.successful_deliveries / self.delivery_attempts * 100) if self.delivery_attempts > 0 else 0.0
        }

    def reset_statistics(self) -> None:
        """Reset delivery statistics."""
        self.delivery_attempts = 0
        self.successful_deliveries = 0
        self.failed_deliveries = 0


# Global integration instance
_message_queue_integration = None

def get_message_queue_pyautogui_integration() -> MessageQueuePyAutoGUIIntegration:
    """Get global message queue PyAutoGUI integration instance."""
    global _message_queue_integration
    if _message_queue_integration is None:
        _message_queue_integration = MessageQueuePyAutoGUIIntegration()
    return _message_queue_integration

def create_queue_pyautogui_delivery_callback() -> Callable[[Any], bool]:
    """Create a PyAutoGUI delivery callback for the message queue system.

    Returns:
        Delivery callback function that can be passed to the message queue
    """
    integration = get_message_queue_pyautogui_integration()
    return integration.create_pyautogui_delivery_callback()

def get_queue_delivery_statistics() -> dict[str, int]:
    """Get current delivery statistics."""
    integration = get_message_queue_pyautogui_integration()
    return integration.get_delivery_statistics()

def reset_queue_delivery_statistics() -> None:
    """Reset delivery statistics."""
    integration = get_message_queue_pyautogui_integration()
    integration.reset_statistics()


# Convenience functions for direct integration
def enqueue_message_with_pyautogui_delivery(
    queue_system: Any,
    message: Any,
    recipient: str,
    message_type: str = "text",
    priority: str = "regular"
) -> str | None:
    """Enqueue a message with PyAutoGUI delivery.

    Args:
        queue_system: Message queue system instance
        message: Message content
        recipient: Target agent
        message_type: Type of message
        priority: Message priority

    Returns:
        Queue ID if successful, None otherwise
    """
    try:
        # Create delivery callback
        delivery_callback = create_queue_pyautogui_delivery_callback()

        # Format message for queue
        queue_message = {
            'content': str(message),
            'recipient': recipient,
            'sender': 'system',
            'message_type': message_type,
            'priority': priority,
            'timestamp': 'auto'  # Will be set by queue
        }

        # Enqueue with PyAutoGUI delivery
        return queue_system.enqueue(queue_message, delivery_callback)

    except Exception as e:
        logger.error(f"Failed to enqueue message with PyAutoGUI delivery: {e}")
        return None
