#!/usr/bin/env python3
"""
Simple Messaging Utils - KISS Compliant
=======================================

Simple messaging utility functions.
KISS PRINCIPLE: Keep It Simple, Stupid.

Author: Agent-6 - Coordination & Communication Specialist
License: MIT
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from .models.messaging_models import UnifiedMessage
from .utils.messaging_validation_utils import MessagingValidationUtils


class SimpleMessagingUtils:
    """Simple messaging utilities."""

    def __init__(self):
        self.message_log: List[Dict] = []
        self.logger = logging.getLogger(__name__)

    def validate_message(self, message: str) -> bool:
        """Validate a message using shared validation utilities."""
        temp = UnifiedMessage(content=message, sender="system", recipient="temp")
        result = MessagingValidationUtils.validate_message_structure(temp)
        for warning in result.get("warnings", []):
            self.logger.warning(warning)
        for error in result.get("errors", []):
            self.logger.error(error)
        return result.get("valid", False)
    
    def format_message(self, sender: str, recipient: str, content: str) -> str:
        """Format a message."""
        return f"[{sender} -> {recipient}]: {content}"
    
    def log_message(self, sender: str, recipient: str, content: str):
        """Log a message."""
        self.message_log.append({
            "sender": sender,
            "recipient": recipient,
            "content": content,
            "timestamp": datetime.now()
        })
    
    def get_message_history(self, limit: int = 10) -> List[Dict]:
        """Get message history."""
        return self.message_log[-limit:] if limit else self.message_log
    
    def clear_log(self):
        """Clear message log."""
        self.message_log.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get messaging statistics."""
        return {
            "total_messages": len(self.message_log),
            "last_message": self.message_log[-1]["timestamp"] if self.message_log else None
        }
