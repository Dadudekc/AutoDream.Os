#!/usr/bin/env python3
"""
Communication Interfaces - Communication Protocol Definitions
==========================================================

Communication interface definitions for system components.
Part of the modularization of unified_core_interfaces.py for V2 compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol


class IMessageHandler(Protocol):
    """Interface for message handling components."""

    def handle_message(self, message: Any) -> bool:
        """Handle a message."""
        ...

    def can_handle(self, message_type: str) -> bool:
        """Check if handler can handle message type."""
        ...

    def get_supported_types(self) -> List[str]:
        """Get list of supported message types."""
        ...


class ICommunicationChannel(ABC):
    """Abstract base class for communication channels."""

    @abstractmethod
    def send(self, message: Any) -> bool:
        """Send a message through the channel."""
        pass

    @abstractmethod
    def receive(self) -> Optional[Any]:
        """Receive a message from the channel."""
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if channel is connected."""
        pass

    @abstractmethod
    def connect(self) -> bool:
        """Connect the channel."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect the channel."""
        pass


class ICommunicationSystem(Protocol):
    """Interface for communication systems."""

    def register_channel(self, channel_id: str, channel: ICommunicationChannel) -> bool:
        """Register a communication channel."""
        ...

    def unregister_channel(self, channel_id: str) -> bool:
        """Unregister a communication channel."""
        ...

    def send_message(self, channel_id: str, message: Any) -> bool:
        """Send message through specific channel."""
        ...

    def broadcast_message(self, message: Any) -> bool:
        """Broadcast message to all channels."""
        ...

    def get_available_channels(self) -> List[str]:
        """Get list of available channels."""
        ...





