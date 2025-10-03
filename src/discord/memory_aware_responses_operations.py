#!/usr/bin/env python3
"""
Memory-Aware Responses Operations - Operations Module
=====================================================

Operations and utilities for memory-aware response generation.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: memory_aware_responses.py (488 lines) - Operations module
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.discord.memory_aware_responses_core import (
    ConversationContext,
    MemoryContextManager,
    ResponseGenerator,
    ResponseType,
)


class MemoryBackend:
    """Simple file-based memory backend"""
    
    def __init__(self, data_dir: str = "data/memory"):
        """Initialize memory backend"""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.user_prefs_file = self.data_dir / "user_preferences.json"
        self.conversations_file = self.data_dir / "conversations.json"
    
    def manage_user_preferences(self, user_id: str, preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """Get or save user preferences"""
        if preferences is None:
            # Get preferences
            try:
                if self.user_prefs_file.exists():
                    with open(self.user_prefs_file, 'r') as f:
                        prefs = json.load(f)
                        return prefs.get(user_id, {})
            except Exception:
                pass
            return {}
        else:
            # Save preferences
            try:
                prefs = {}
                if self.user_prefs_file.exists():
                    with open(self.user_prefs_file, 'r') as f:
                        prefs = json.load(f)
                
                prefs[user_id] = preferences
                
                with open(self.user_prefs_file, 'w') as f:
                    json.dump(prefs, f, indent=2)
            except Exception as e:
                print(f"Error saving user preferences: {e}")
    
    def save_conversation(self, context: ConversationContext) -> None:
        """Save conversation context"""
        try:
            conversations = {}
            if self.conversations_file.exists():
                with open(self.conversations_file, 'r') as f:
                    conversations = json.load(f)
            
            conversations[context.conversation_id] = {
                "user_id": context.user_id,
                "agent_id": context.agent_id,
                "message_history": context.message_history,
                "user_preferences": context.user_preferences,
                "system_context": context.system_context,
                "last_activity": context.last_activity.isoformat(),
                "context_expiry": context.context_expiry.isoformat(),
            }
            
            with open(self.conversations_file, 'w') as f:
                json.dump(conversations, f, indent=2)
        except Exception as e:
            print(f"Error saving conversation: {e}")
    
    def load_conversation(self, conversation_id: str) -> Optional[ConversationContext]:
        """Load conversation context"""
        try:
            if self.conversations_file.exists():
                with open(self.conversations_file, 'r') as f:
                    conversations = json.load(f)
                
                if conversation_id in conversations:
                    data = conversations[conversation_id]
                    return ConversationContext(
                        user_id=data["user_id"],
                        conversation_id=conversation_id,
                        agent_id=data["agent_id"],
                        message_history=data["message_history"],
                        user_preferences=data["user_preferences"],
                        system_context=data["system_context"],
                        last_activity=datetime.fromisoformat(data["last_activity"]),
                        context_expiry=datetime.fromisoformat(data["context_expiry"]),
                    )
        except Exception as e:
            print(f"Error loading conversation: {e}")
        return None


class ResponseAnalytics:
    """Analytics for response generation"""
    
    def __init__(self):
        """Initialize analytics"""
        self.response_counts: Dict[str, int] = {}
        self.user_interactions: Dict[str, int] = {}
        self.agent_performance: Dict[str, Dict[str, int]] = {}
    
    def manage_analytics(self, user_id: str = None, agent_id: str = None, response_type: ResponseType = None) -> Dict[str, Any]:
        """Record response or get analytics summary"""
        if user_id and agent_id and response_type:
            # Record response generation
            type_key = response_type.value
            self.response_counts[type_key] = self.response_counts.get(type_key, 0) + 1
            self.user_interactions[user_id] = self.user_interactions.get(user_id, 0) + 1
            
            if agent_id not in self.agent_performance:
                self.agent_performance[agent_id] = {}
            self.agent_performance[agent_id][type_key] = self.agent_performance[agent_id].get(type_key, 0) + 1
        else:
            # Get analytics summary
            return {
                "total_responses": sum(self.response_counts.values()),
                "response_types": self.response_counts,
                "active_users": len(self.user_interactions),
                "user_interactions": self.user_interactions,
                "agent_performance": self.agent_performance,
            }


class MemoryAwareResponseService:
    """Main service for memory-aware responses"""
    
    def __init__(self, memory_backend: Optional[MemoryBackend] = None):
        """Initialize service"""
        self.memory_backend = memory_backend or MemoryBackend()
        self.context_manager = MemoryContextManager(self.memory_backend)
        self.response_generator = ResponseGenerator(self.context_manager)
        self.analytics = ResponseAnalytics()
    
    def process_message(self, user_id: str, agent_id: str, message: str, response_type: ResponseType) -> str:
        """Process message and generate response"""
        # Generate response
        response = self.response_generator.generate_response(user_id, agent_id, message, response_type)
        
        # Record analytics
        self.analytics.manage_analytics(user_id, agent_id, response_type)
        
        # Save context to backend
        context_key = f"{user_id}:{agent_id}"
        if context_key in self.context_manager.active_contexts:
            context = self.context_manager.active_contexts[context_key]
            self.memory_backend.save_conversation(context)
        
        return response
    
    def manage_context(self, user_id: str, agent_id: str, action: str = "get") -> Optional[ConversationContext]:
        """Get, clear, or manage user context"""
        context_key = f"{user_id}:{agent_id}"
        
        if action == "get":
            return self.context_manager.active_contexts.get(context_key)
        elif action == "clear":
            if context_key in self.context_manager.active_contexts:
                del self.context_manager.active_contexts[context_key]
        elif action == "count":
            return len(self.context_manager.active_contexts)
        elif action == "cleanup":
            initial_count = len(self.context_manager.active_contexts)
            self.context_manager._cleanup_old_contexts()
            return initial_count - len(self.context_manager.active_contexts)
        
        return None
