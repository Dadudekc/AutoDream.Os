#!/usr/bin/env python3
"""
Inbox Types - Agent Cellphone V2
================================

Type definitions for inbox system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageStatus(Enum):
    """Message status states."""
    PENDING = "pending"
    READ = "read"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Message:
    """Message data structure."""
    message_id: str
    sender: str
    recipient: str
    subject: str
    content: str
    priority: MessagePriority
    status: MessageStatus
    created_at: str
    read_at: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class InboxStatus:
    """Inbox status information."""
    agent_id: str
    total_messages: int
    status_counts: Dict[str, int]
    priority_counts: Dict[str, int]
    unread_count: int
    urgent_count: int


@dataclass
class SystemStatus:
    """Overall inbox system status."""
    status: str
    total_messages: int
    pending_messages: int
    urgent_messages: int
    active_agents: int
