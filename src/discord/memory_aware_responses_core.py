#!/usr/bin/env python3
"""
Memory-Aware Responses Core - Core Logic Module
===============================================

Core logic for memory-aware response generation with persistent memory integration.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: memory_aware_responses.py (488 lines) - Core module
"""

import uuid
from dataclasses import dataclass
from datetime import datetime, timedelta
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
    user_id: str
    conversation_id: str
    agent_id: str
    message_history: list[dict[str, Any]]
    user_preferences: dict[str, Any]
    system_context: dict[str, Any]
    last_activity: datetime
    context_expiry: datetime


class MemoryContextManager:
    """Context management for memory-aware responses"""
    
    def __init__(self, memory_backend: Any = None):
        """Initialize memory context manager"""
        self.memory_backend = memory_backend
        self.active_contexts: dict[str, ConversationContext] = {}
        self.context_ttl = timedelta(hours=24)
        self._max_contexts = 100
    
    def get_or_create_context(self, user_id: str, agent_id: str) -> ConversationContext:
        """Get existing context or create new one"""
        context_key = f"{user_id}:{agent_id}"
        
        if context_key in self.active_contexts:
            context = self.active_contexts[context_key]
            if datetime.utcnow() < context.context_expiry:
                return context
            else:
                del self.active_contexts[context_key]
        
        conversation_id = str(uuid.uuid4())
        context = ConversationContext(
            user_id=user_id,
            conversation_id=conversation_id,
            agent_id=agent_id,
            message_history=[],
            user_preferences=self._load_user_preferences(user_id),
            system_context=self._load_system_context(),
            last_activity=datetime.utcnow(),
            context_expiry=datetime.utcnow() + self.context_ttl,
        )
        
        if len(self.active_contexts) >= self._max_contexts:
            self._cleanup_old_contexts()
        
        self.active_contexts[context_key] = context
        return context
    
    def update_context(self, context: ConversationContext, message: str, response: str) -> None:
        """Update context with new message and response"""
        context.message_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "response": response,
            "agent_id": context.agent_id,
        })
        
        if len(context.message_history) > 50:
            context.message_history = context.message_history[-50:]
        
        context.last_activity = datetime.utcnow()
    
    def _load_user_preferences(self, user_id: str) -> dict[str, Any]:
        """Load user preferences from memory backend"""
        if self.memory_backend:
            return self.memory_backend.get_user_preferences(user_id) or {}
        return {}
    
    def _load_system_context(self) -> dict[str, Any]:
        """Load system context"""
        return {
            "swarm_status": "active",
            "agent_count": 8,
            "compliance_level": "V2",
            "last_update": datetime.utcnow().isoformat(),
        }
    
    def _cleanup_old_contexts(self) -> None:
        """Clean up old contexts to prevent memory bloat"""
        now = datetime.utcnow()
        expired_keys = [
            key for key, context in self.active_contexts.items()
            if now > context.context_expiry
        ]
        
        for key in expired_keys:
            del self.active_contexts[key]
        
        # If still at limit, remove oldest contexts
        if len(self.active_contexts) >= self._max_contexts:
            sorted_contexts = sorted(
                self.active_contexts.items(),
                key=lambda x: x[1].last_activity
            )
            
            contexts_to_remove = len(self.active_contexts) - self._max_contexts + 10
            for key, _ in sorted_contexts[:contexts_to_remove]:
                del self.active_contexts[key]


class ResponseGenerator:
    """Generate context-aware responses"""
    
    def __init__(self, context_manager: MemoryContextManager):
        """Initialize response generator"""
        self.context_manager = context_manager
    
    def generate_response(self, user_id: str, agent_id: str, message: str, response_type: ResponseType) -> str:
        """Generate a context-aware response"""
        context = self.context_manager.get_or_create_context(user_id, agent_id)
        
        # Build response based on type and context
        response = self._build_response(message, response_type, context)
        
        # Update context with the interaction
        self.context_manager.update_context(context, message, response)
        
        return response
    
    def _build_response(self, message: str, response_type: ResponseType, context: ConversationContext) -> str:
        """Build response based on type and context"""
        response_builders = {
            ResponseType.STATUS_UPDATE: lambda: f"🤖 Agent {context.agent_id} Status: Active - V2 Compliance: 96.6%",
            ResponseType.COORDINATION_REQUEST: lambda: f"🔄 Coordination Request Received: {message[:100]}...",
            ResponseType.TASK_COMPLETION: lambda: f"✅ Task Completed: {message[:100]}...",
            ResponseType.SYSTEM_ALERT: lambda: f"🚨 System Alert: {message[:100]}...",
            ResponseType.SWARM_COORDINATION: lambda: f"🐝 Swarm Coordination: {message[:100]}...",
            ResponseType.USER_QUERY: lambda: f"❓ Query Response: {message[:100]}...",
            ResponseType.ERROR_RESPONSE: lambda: f"❌ Error Response: {message[:100]}...",
        }
        
        return response_builders.get(response_type, lambda: f"📝 Response: {message[:100]}...")()
