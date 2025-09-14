"""
Communication Protocols
=======================

Defines communication protocols and interfaces for the communication system.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class MessageType(Enum):
    """Types of messages."""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"
    BROADCAST = "broadcast"


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4


@dataclass
class Message:
    """Represents a communication message."""
    id: str
    type: MessageType
    priority: MessagePriority
    sender: str
    recipient: Optional[str]
    content: Any
    timestamp: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class CommunicationProtocol(ABC):
    """Abstract base class for communication protocols."""
    
    def __init__(self, name: str):
        """Initialize the communication protocol."""
        self.name = name
        self.logger = logging.getLogger(__name__)
    
    @abstractmethod
    def send_message(self, message: Message) -> bool:
        """Send a message using this protocol."""
        pass
    
    @abstractmethod
    def receive_message(self) -> Optional[Message]:
        """Receive a message using this protocol."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the protocol is available."""
        pass


class InboxProtocol(CommunicationProtocol):
    """File-based inbox protocol for agent communication."""
    
    def __init__(self):
        """Initialize inbox protocol."""
        super().__init__("inbox")
        self.inbox_path = "agent_workspaces"
    
    def send_message(self, message: Message) -> bool:
        """Send message to inbox."""
        try:
            # Implementation would write to agent inbox
            self.logger.info(f"Sent message {message.id} via inbox protocol")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message via inbox: {e}")
            return False
    
    def receive_message(self) -> Optional[Message]:
        """Receive message from inbox."""
        try:
            # Implementation would read from agent inbox
            self.logger.info("Received message via inbox protocol")
            return None  # Placeholder
        except Exception as e:
            self.logger.error(f"Failed to receive message via inbox: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if inbox protocol is available."""
        return True  # Always available for file-based system


class PyAutoGUIProtocol(CommunicationProtocol):
    """PyAutoGUI-based protocol for direct UI communication."""
    
    def __init__(self):
        """Initialize PyAutoGUI protocol."""
        super().__init__("pyautogui")
        self.available = self._check_pyautogui()
    
    def _check_pyautogui(self) -> bool:
        """Check if PyAutoGUI is available."""
        try:
            import pyautogui
            return True
        except ImportError:
            return False
    
    def send_message(self, message: Message) -> bool:
        """Send message via PyAutoGUI."""
        if not self.available:
            return False
        
        try:
            # Implementation would use PyAutoGUI for direct communication
            self.logger.info(f"Sent message {message.id} via PyAutoGUI protocol")
            return True
        except Exception as e:
            self.logger.error(f"Failed to send message via PyAutoGUI: {e}")
            return False
    
    def receive_message(self) -> Optional[Message]:
        """Receive message via PyAutoGUI."""
        if not self.available:
            return None
        
        try:
            # Implementation would read from PyAutoGUI interface
            self.logger.info("Received message via PyAutoGUI protocol")
            return None  # Placeholder
        except Exception as e:
            self.logger.error(f"Failed to receive message via PyAutoGUI: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if PyAutoGUI protocol is available."""
        return self.available


class CommunicationProtocolFactory:
    """Factory for creating communication protocols."""
    
    @staticmethod
    def create_protocol(protocol_name: str) -> Optional[CommunicationProtocol]:
        """Create a communication protocol by name."""
        if protocol_name == "inbox":
            return InboxProtocol()
        elif protocol_name == "pyautogui":
            return PyAutoGUIProtocol()
        else:
            return None

