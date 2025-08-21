"""
Advanced Messaging System - Agent Cellphone V2
==============================================

Enterprise-grade messaging system with advanced features:
- Persistent message queues with priority-based routing
- Message pipeline processing with multi-stage workflows
- Response collection and validation with automated quality checks
- Message history and analytics with persistent storage
- Advanced routing with pattern matching and filtering

This module integrates advanced messaging capabilities from the SWARM system
to provide a unified, scalable messaging infrastructure.
"""

from .message_queue import MessageQueue, PersistentMessageQueue, InMemoryMessageQueue
from .message_types import Message, MessagePriority, MessageType, MessageStatus

__version__ = "2.0.0"
__author__ = "Agent Cellphone V2 Team"

__all__ = [
    "MessageQueue", 
    "PersistentMessageQueue",
    "InMemoryMessageQueue",
    "Message",
    "MessagePriority",
    "MessageType",
    "MessageStatus"
]
