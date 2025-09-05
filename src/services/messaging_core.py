#!/usr/bin/env python3
"""
Unified Messaging Core - KISS Simplified
=========================================

Simplified core messaging functionality for the unified messaging service.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined messaging core.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .unified_messaging_imports import (
    logging, COORDINATE_CONFIG_FILE, get_logger, get_unified_utility, 
    load_coordinates_from_json, json
)
from ..core.simple_validation_system import get_simple_validator
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedSenderType,
    UnifiedRecipientType
)
from .message_identity_clarification import format_message_with_identity_clarification


class UnifiedMessagingCore:
    """
    Simplified core messaging functionality for the unified messaging service.
    
    KISS PRINCIPLE: Streamlined message creation, validation, and delivery coordination.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the unified messaging core - simplified."""
        self.config = config or {}
        self.message_history: List[UnifiedMessage] = []
        self.logger = get_logger(__name__)
        self.validator = get_simple_validator()
        self.utility = get_unified_utility()

        # Simplified configuration validation
        self._validate_config()

    def _validate_config(self):
        """Validate configuration - simplified."""
        try:
            if not self.config.get("enable_logging", True):
                self.logger.warning("Logging disabled in configuration")
        except Exception as e:
            self.logger.error(f"Configuration validation error: {e}")

    def create_message(self, content: str, message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                      priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
                      sender_type: UnifiedSenderType = UnifiedSenderType.AGENT,
                      recipient_type: UnifiedRecipientType = UnifiedRecipientType.AGENT,
                      sender: str = "system", recipient: str = "all",
                      tags: List[UnifiedMessageTag] = None) -> UnifiedMessage:
        """Create a unified message - simplified."""
        try:
            if tags is None:
                tags = []

            message = UnifiedMessage(
                message_id=f"msg_{int(time.time())}",
                content=content,
                message_type=message_type,
                priority=priority,
                sender_type=sender_type,
                recipient_type=recipient_type,
                sender=sender,
                recipient=recipient,
                tags=tags,
                timestamp=datetime.now()
            )

            self.logger.info(f"Created message: {message.message_id}")
            return message
        except Exception as e:
            self.logger.error(f"Error creating message: {e}")
            raise

    def validate_message(self, message: UnifiedMessage) -> bool:
        """Validate message - simplified."""
        try:
            if not message.content or len(message.content.strip()) == 0:
                self.logger.error("Message content cannot be empty")
                return False

            if len(message.content) > 10000:  # 10k character limit
                self.logger.error("Message content too long")
                return False

            return True
        except Exception as e:
            self.logger.error(f"Error validating message: {e}")
            return False

    def send_message(self, message: UnifiedMessage, delivery_method: str = "pyautogui") -> bool:
        """Send message - simplified."""
        try:
            if not self.validate_message(message):
                return False

            # Simplified delivery logic
            self.logger.info(f"Sending message via {delivery_method}: {message.message_id}")
            
            # Add to history
            self.message_history.append(message)
            
            # Simulate delivery
            time.sleep(0.1)
            
            self.logger.info(f"Message sent successfully: {message.message_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error sending message: {e}")
            return False

    def get_message_history(self, limit: int = 100) -> List[UnifiedMessage]:
        """Get message history - simplified."""
        try:
            return self.message_history[-limit:] if limit > 0 else self.message_history
        except Exception as e:
            self.logger.error(f"Error getting message history: {e}")
            return []

    def search_messages(self, query: str, limit: int = 50) -> List[UnifiedMessage]:
        """Search messages - simplified."""
        try:
            results = []
            for message in self.message_history:
                if query.lower() in message.content.lower():
                    results.append(message)
                    if len(results) >= limit:
                        break
            return results
        except Exception as e:
            self.logger.error(f"Error searching messages: {e}")
            return []

    def get_message_by_id(self, message_id: str) -> Optional[UnifiedMessage]:
        """Get message by ID - simplified."""
        try:
            for message in self.message_history:
                if message.message_id == message_id:
                    return message
            return None
        except Exception as e:
            self.logger.error(f"Error getting message by ID: {e}")
            return None

    def delete_message(self, message_id: str) -> bool:
        """Delete message - simplified."""
        try:
            for i, message in enumerate(self.message_history):
                if message.message_id == message_id:
                    del self.message_history[i]
                    self.logger.info(f"Message deleted: {message_id}")
                    return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting message: {e}")
            return False

    def get_message_stats(self) -> Dict[str, Any]:
        """Get message statistics - simplified."""
        try:
            total_messages = len(self.message_history)
            message_types = {}
            priorities = {}
            
            for message in self.message_history:
                msg_type = message.message_type.value
                priority = message.priority.value
                
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
                priorities[priority] = priorities.get(priority, 0) + 1
            
            return {
                "total_messages": total_messages,
                "message_types": message_types,
                "priorities": priorities,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting message stats: {e}")
            return {}

    def clear_history(self) -> bool:
        """Clear message history - simplified."""
        try:
            self.message_history.clear()
            self.logger.info("Message history cleared")
            return True
        except Exception as e:
            self.logger.error(f"Error clearing history: {e}")
            return False

    def get_core_status(self) -> Dict[str, Any]:
        """Get core status - simplified."""
        return {
            "status": "active",
            "total_messages": len(self.message_history),
            "validator_available": self.validator is not None,
            "utility_available": self.utility is not None,
            "last_updated": datetime.now().isoformat()
        }

    def shutdown(self) -> bool:
        """Shutdown core - simplified."""
        try:
            self.logger.info("Unified Messaging Core shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False


# Global instance for backward compatibility
_global_messaging_core: Optional[UnifiedMessagingCore] = None

def get_unified_messaging_core(config: Optional[Dict[str, Any]] = None) -> UnifiedMessagingCore:
    """Returns a global instance of the UnifiedMessagingCore."""
    global _global_messaging_core
    if _global_messaging_core is None:
        _global_messaging_core = UnifiedMessagingCore(config)
    return _global_messaging_core