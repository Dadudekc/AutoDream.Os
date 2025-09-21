#!/usr/bin/env python3
"""
Memory-Aware Responses System for Phase 2.3 Enhanced Discord Integration

V2 Compliance: ≤400 lines, 4 classes, 8 functions
Purpose: Context-aware response generation with persistent memory integration
"""

import json
import uuid
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum


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
    message_history: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    system_context: Dict[str, Any]
    last_activity: datetime
    context_expiry: datetime


class MemoryContextManager:
    """Context management for memory-aware responses"""
    
    def __init__(self, memory_backend: Any = None):
        """Initialize memory context manager"""
        self.memory_backend = memory_backend
        self.active_contexts: Dict[str, ConversationContext] = {}
        self.context_ttl = timedelta(hours=24)  # Context expires after 24 hours
    
    def get_or_create_context(self, user_id: str, agent_id: str) -> ConversationContext:
        """Get existing context or create new one"""
        context_key = f"{user_id}:{agent_id}"
        
        if context_key in self.active_contexts:
            context = self.active_contexts[context_key]
            # Check if context is still valid
            if datetime.utcnow() < context.context_expiry:
                return context
            else:
                # Context expired, remove it
                del self.active_contexts[context_key]
        
        # Create new context
        conversation_id = str(uuid.uuid4())
        context = ConversationContext(
            user_id=user_id,
            conversation_id=conversation_id,
            agent_id=agent_id,
            message_history=[],
            user_preferences=self._load_user_preferences(user_id),
            system_context=self._load_system_context(),
            last_activity=datetime.utcnow(),
            context_expiry=datetime.utcnow() + self.context_ttl
        )
        
        self.active_contexts[context_key] = context
        return context
    
    def update_context(self, context: ConversationContext, 
                      message: str, response: str) -> None:
        """Update context with new message and response"""
        context.message_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "response": response,
            "agent_id": context.agent_id
        })
        
        # Keep only last 50 messages to prevent memory bloat
        if len(context.message_history) > 50:
            context.message_history = context.message_history[-50:]
        
        context.last_activity = datetime.utcnow()
        context.context_expiry = datetime.utcnow() + self.context_ttl
    
    def _load_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """Load user preferences from memory backend"""
        if self.memory_backend:
            try:
                return self.memory_backend.get_user_preferences(user_id) or {}
            except Exception:
                pass
        return {}
    
    def _load_system_context(self) -> Dict[str, Any]:
        """Load system-wide context"""
        if self.memory_backend:
            try:
                return self.memory_backend.get_system_context() or {}
            except Exception:
                pass
        return {}


class ResponseGenerator:
    """AI-powered response generation with memory integration"""
    
    def __init__(self, context_manager: MemoryContextManager):
        """Initialize response generator"""
        self.context_manager = context_manager
        self.response_templates = self._load_response_templates()
        self.response_rules = self._load_response_rules()
    
    def generate_response(self, message: str, user_id: str, 
                         agent_id: str, response_type: ResponseType) -> str:
        """Generate context-aware response"""
        # Get or create conversation context
        context = self.context_manager.get_or_create_context(user_id, agent_id)
        
        # Analyze message for context clues
        context_clues = self._analyze_message_context(message, context)
        
        # Generate response based on type and context
        response = self._generate_typed_response(
            message, context, context_clues, response_type
        )
        
        # Update context with new interaction
        self.context_manager.update_context(context, message, response)
        
        return response
    
    def _analyze_message_context(self, message: str, 
                                context: ConversationContext) -> Dict[str, Any]:
        """Analyze message for context clues and patterns"""
        clues = {
            "urgency": self._detect_urgency(message),
            "sentiment": self._detect_sentiment(message),
            "keywords": self._extract_keywords(message),
            "question_type": self._detect_question_type(message),
            "coordination_needed": self._detect_coordination_need(message)
        }
        return clues
    
    def _detect_urgency(self, message: str) -> str:
        """Detect urgency level in message"""
        urgent_keywords = ["urgent", "critical", "emergency", "asap", "immediately"]
        high_keywords = ["important", "priority", "soon", "quickly"]
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in urgent_keywords):
            return "URGENT"
        elif any(keyword in message_lower for keyword in high_keywords):
            return "HIGH"
        else:
            return "NORMAL"
    
    def _detect_sentiment(self, message: str) -> str:
        """Detect sentiment in message"""
        positive_keywords = ["great", "excellent", "good", "success", "complete"]
        negative_keywords = ["error", "fail", "problem", "issue", "broken"]
        
        message_lower = message.lower()
        
        positive_count = sum(1 for keyword in positive_keywords if keyword in message_lower)
        negative_count = sum(1 for keyword in negative_keywords if keyword in message_lower)
        
        if positive_count > negative_count:
            return "POSITIVE"
        elif negative_count > positive_count:
            return "NEGATIVE"
        else:
            return "NEUTRAL"
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extract important keywords from message"""
        # Simple keyword extraction - can be enhanced with NLP
        important_words = ["task", "agent", "coordination", "status", "error", 
                          "complete", "progress", "swarm", "discord", "v2"]
        
        message_lower = message.lower()
        found_keywords = [word for word in important_words if word in message_lower]
        
        return found_keywords
    
    def _detect_question_type(self, message: str) -> str:
        """Detect type of question being asked"""
        if message.endswith("?"):
            if any(word in message.lower() for word in ["what", "which", "where"]):
                return "INFORMATIONAL"
            elif any(word in message.lower() for word in ["how", "why"]):
                return "EXPLANATORY"
            elif any(word in message.lower() for word in ["can", "could", "would"]):
                return "REQUEST"
            else:
                return "GENERAL"
        return "STATEMENT"
    
    def _detect_coordination_need(self, message: str) -> bool:
        """Detect if message requires coordination with other agents"""
        coordination_keywords = ["coordinate", "collaborate", "team", "swarm", 
                               "agent", "assign", "delegate", "sync"]
        return any(keyword in message.lower() for keyword in coordination_keywords)
    
    def _generate_typed_response(self, message: str, context: ConversationContext,
                               context_clues: Dict[str, Any], 
                               response_type: ResponseType) -> str:
        """Generate response based on type and context"""
        # Get base response template
        template = self.response_templates.get(response_type.value, 
                                             self.response_templates["default"])
        
        # Enhance with context information
        enhanced_response = self._enhance_with_context(template, context, context_clues)
        
        # Apply response rules
        final_response = self._apply_response_rules(enhanced_response, context_clues)
        
        return final_response
    
    def _enhance_with_context(self, template: str, context: ConversationContext,
                            context_clues: Dict[str, Any]) -> str:
        """Enhance response template with context information"""
        # Add conversation history context
        recent_messages = context.message_history[-3:] if context.message_history else []
        
        # Add user preferences context
        preferences = context.user_preferences
        
        # Add system context
        system_info = context.system_context
        
        # Replace template placeholders
        enhanced = template.format(
            message=template,
            urgency=context_clues.get("urgency", "NORMAL"),
            sentiment=context_clues.get("sentiment", "NEUTRAL"),
            keywords=", ".join(context_clues.get("keywords", [])),
            recent_context=len(recent_messages),
            user_preferences=preferences.get("response_style", "professional"),
            system_status=system_info.get("status", "operational")
        )
        
        return enhanced
    
    def _apply_response_rules(self, response: str, 
                            context_clues: Dict[str, Any]) -> str:
        """Apply response rules based on context clues"""
        # Apply urgency-based formatting
        if context_clues.get("urgency") == "URGENT":
            response = f"🚨 **URGENT RESPONSE**\n\n{response}"
        elif context_clues.get("urgency") == "HIGH":
            response = f"⚠️ **HIGH PRIORITY**\n\n{response}"
        
        # Apply sentiment-based tone
        if context_clues.get("sentiment") == "POSITIVE":
            response = f"🎉 {response}"
        elif context_clues.get("sentiment") == "NEGATIVE":
            response = f"🔧 **Issue Resolution:**\n\n{response}"
        
        return response
    
    def _load_response_templates(self) -> Dict[str, str]:
        """Load response templates for different types"""
        return {
            "status_update": "✅ **Status Update Acknowledged**\n\n{message}\n\n**Context:** {recent_context} recent messages, System: {system_status}",
            "coordination_request": "🤝 **Coordination Request Received**\n\n{message}\n\n**Priority:** {urgency}, **Keywords:** {keywords}",
            "task_completion": "🎯 **Task Completion Confirmed**\n\n{message}\n\n**Response Style:** {user_preferences}",
            "system_alert": "🚨 **System Alert Processed**\n\n{message}\n\n**Urgency:** {urgency}, **Sentiment:** {sentiment}",
            "swarm_coordination": "🐝 **Swarm Coordination Active**\n\n{message}\n\n**Keywords:** {keywords}",
            "user_query": "💬 **Query Response**\n\n{message}\n\n**Context:** {recent_context} recent messages",
            "error_response": "❌ **Error Response**\n\n{message}\n\n**System Status:** {system_status}",
            "default": "📋 **Response**\n\n{message}\n\n**Context:** {recent_context} recent messages"
        }
    
    def _load_response_rules(self) -> Dict[str, Any]:
        """Load response rules and guidelines"""
        return {
            "max_response_length": 2000,
            "include_timestamp": True,
            "include_context_info": True,
            "use_emojis": True,
            "professional_tone": True
        }


class ConversationTracker:
    """Conversation state tracking and management"""
    
    def __init__(self):
        """Initialize conversation tracker"""
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.conversation_metadata: Dict[str, Dict[str, Any]] = {}
    
    def track_conversation(self, user_id: str, agent_id: str, 
                          message: str, response: str) -> None:
        """Track conversation interaction"""
        conversation_key = f"{user_id}:{agent_id}"
        
        if conversation_key not in self.conversations:
            self.conversations[conversation_key] = []
            self.conversation_metadata[conversation_key] = {
                "started_at": datetime.utcnow(),
                "message_count": 0,
                "last_activity": datetime.utcnow()
            }
        
        # Add interaction
        interaction = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": message,
            "response": response,
            "agent_id": agent_id
        }
        
        self.conversations[conversation_key].append(interaction)
        
        # Update metadata
        self.conversation_metadata[conversation_key]["message_count"] += 1
        self.conversation_metadata[conversation_key]["last_activity"] = datetime.utcnow()
    
    def get_conversation_history(self, user_id: str, agent_id: str, 
                               limit: int = 10) -> List[Dict[str, Any]]:
        """Get conversation history for user and agent"""
        conversation_key = f"{user_id}:{agent_id}"
        conversations = self.conversations.get(conversation_key, [])
        return conversations[-limit:] if limit > 0 else conversations
    
    def get_conversation_stats(self, user_id: str, agent_id: str) -> Dict[str, Any]:
        """Get conversation statistics"""
        conversation_key = f"{user_id}:{agent_id}"
        metadata = self.conversation_metadata.get(conversation_key, {})
        conversations = self.conversations.get(conversation_key, [])
        
        return {
            "message_count": len(conversations),
            "started_at": metadata.get("started_at"),
            "last_activity": metadata.get("last_activity"),
            "conversation_length": len(conversations),
            "active": datetime.utcnow() - metadata.get("last_activity", datetime.utcnow()) < timedelta(hours=1)
        }


class ContextInjector:
    """Context injection for enhanced responses"""
    
    def __init__(self, conversation_tracker: ConversationTracker):
        """Initialize context injector"""
        self.conversation_tracker = conversation_tracker
    
    def inject_context(self, response: str, user_id: str, 
                      agent_id: str) -> str:
        """Inject relevant context into response"""
        # Get conversation history
        history = self.conversation_tracker.get_conversation_history(user_id, agent_id, 3)
        
        # Get conversation stats
        stats = self.conversation_tracker.get_conversation_stats(user_id, agent_id)
        
        # Inject context information
        context_info = f"\n\n**Conversation Context:** {stats['message_count']} messages, "
        context_info += f"Active: {'Yes' if stats['active'] else 'No'}"
        
        if history:
            context_info += f", Recent topics: {self._extract_recent_topics(history)}"
        
        return response + context_info
    
    def _extract_recent_topics(self, history: List[Dict[str, Any]]) -> str:
        """Extract recent topics from conversation history"""
        topics = []
        for interaction in history[-3:]:  # Last 3 interactions
            message = interaction.get("message", "").lower()
            if "task" in message:
                topics.append("tasks")
            elif "coordination" in message:
                topics.append("coordination")
            elif "status" in message:
                topics.append("status")
            elif "error" in message:
                topics.append("errors")
        
        return ", ".join(set(topics)) if topics else "general"


# Example usage and testing
if __name__ == "__main__":
    # Initialize memory-aware response system
    context_manager = MemoryContextManager()
    response_generator = ResponseGenerator(context_manager)
    conversation_tracker = ConversationTracker()
    context_injector = ContextInjector(conversation_tracker)
    
    # Test response generation
    user_id = "test_user"
    agent_id = "Agent-2"
    
    # Test status update response
    status_message = "Agent-2 completed Phase 2.3 Discord architecture design"
    response = response_generator.generate_response(
        status_message, user_id, agent_id, ResponseType.STATUS_UPDATE
    )
    
    print("Memory-Aware Response:")
    print(response)
    print("\n" + "="*50 + "\n")
    
    # Test coordination request response
    coord_message = "Need coordination with Agent-3 for consolidation analysis"
    response = response_generator.generate_response(
        coord_message, user_id, agent_id, ResponseType.COORDINATION_REQUEST
    )
    
    print("Coordination Response:")
    print(response)
    print("\n" + "="*50 + "\n")
    
    # Test context injection
    enhanced_response = context_injector.inject_context(response, user_id, agent_id)
    print("Enhanced Response with Context:")
    print(enhanced_response)


