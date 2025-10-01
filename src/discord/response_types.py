#!/usr/bin/env python3
"""
Response Types and Data Classes
==============================

Data classes and enums for memory-aware responses.
Extracted to maintain V2 compliance.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class ResponseType(Enum):
    """Types of responses that can be generated"""
    STATUS_UPDATE = "status_update"
    COORDINATION_REQUEST = "coordination_request"
    TASK_COMPLETION = "task_completion"
    SYSTEM_ALERT = "system_alert"
    SWARM_COORDINATION = "swarm_coordination"
    USER_QUERY = "user_query"
    ERROR_RESPONSE = "error_response"


@dataclass
class ConversationContext:
    """Context for conversation tracking"""
    conversation_id: str
    user_id: str
    channel_id: str
    started_at: datetime
    last_interaction: datetime
    message_count: int
    context_summary: str
    active_topics: list[str]


@dataclass
class MemoryContext:
    """Memory context for response generation"""
    recent_interactions: list[dict[str, Any]]
    user_preferences: dict[str, Any]
    conversation_history: list[dict[str, Any]]
    persistent_memory: dict[str, Any]


@dataclass
class ResponseContext:
    """Complete context for response generation"""
    conversation: ConversationContext
    memory: MemoryContext
    system_state: dict[str, Any]
    response_type: ResponseType

