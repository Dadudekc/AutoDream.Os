#!/usr/bin/env python3
"""
Messaging Interfaces - V2 Compliant Module
=========================================

Abstract interfaces for messaging system components.
V2 COMPLIANT: Focused interfaces under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from abc import ABC, abstractmethod
from typing import List, Optional

try:
    from ..models.messaging_models import UnifiedMessage, MessageHistory
except ImportError:
    # Fallback for direct execution
    from models.messaging_models import UnifiedMessage, MessageHistory


class MessageDeliveryProvider(ABC):
    """Abstract base class for message delivery providers."""

    @abstractmethod
    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message using this provider."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if this provider is available."""
        pass


class PyAutoGUIDeliveryProvider(MessageDeliveryProvider):
    """PyAutoGUI-based message delivery provider."""

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message via PyAutoGUI automation."""
        # Implementation would go here
        return True

    def is_available(self) -> bool:
        """Check if PyAutoGUI is available."""
        try:
            import pyautogui
            return True
        except ImportError:
            return False


class InboxDeliveryProvider(MessageDeliveryProvider):
    """File-based inbox delivery provider."""

    def send_message(self, message: UnifiedMessage) -> bool:
        """Send message to agent inbox file."""
        # Implementation would go here
        return True

    def is_available(self) -> bool:
        """Check if file system is available."""
        return True


class MessageHistoryProvider(ABC):
    """Abstract base class for message history providers."""

    @abstractmethod
    def get_inbox_messages(self, agent_id: str) -> List[UnifiedMessage]:
        """Get messages from agent's inbox."""
        pass

    @abstractmethod
    def save_message(self, message: UnifiedMessage) -> bool:
        """Save message to history."""
        pass

    @abstractmethod
    def get_message_history(self, agent_id: str, limit: int = 10) -> List[MessageHistory]:
        """Get message history for an agent."""
        pass


class FileBasedMessageHistoryProvider(MessageHistoryProvider):
    """File-based message history provider."""

    def get_inbox_messages(self, agent_id: str) -> List[UnifiedMessage]:
        """Get messages from agent's inbox."""
        # Implementation would go here
        return []

    def save_message(self, message: UnifiedMessage) -> bool:
        """Save message to history."""
        # Implementation would go here
        return True

    def get_message_history(self, agent_id: str, limit: int = 10) -> List[MessageHistory]:
        """Get message history for an agent."""
        # Implementation would go here
        return []