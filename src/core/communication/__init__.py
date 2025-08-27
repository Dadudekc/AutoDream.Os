"""Core communication package."""

from .channels import Channel, ChannelType
from .adapters import HTTPAdapter, HTTPSAdapter, WebSocketAdapter
from .router import MessageRouter
from .communication_manager import CommunicationManager

__all__ = [
    "Channel",
    "ChannelType",
    "HTTPAdapter",
    "HTTPSAdapter",
    "WebSocketAdapter",
    "MessageRouter",
    "CommunicationManager",
]
