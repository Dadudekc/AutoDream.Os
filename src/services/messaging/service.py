#!/usr/bin/env python3
"""
Messaging Service - V2 Compliant
===============================

Core messaging service for unified messaging system.
V2 COMPLIANT: Simple service wrapper under 100 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
from .messaging_core import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class MessagingService:
    """Simple wrapper around ConsolidatedMessagingService."""
    
    def __init__(self):
        """Initialize messaging service."""
        self.service = ConsolidatedMessagingService()
    
    def send(self, recipient: str, content: str, sender: str = "System") -> bool:
        """Send message to recipient."""
        try:
            from .models.messaging_models import UnifiedMessage
            from .models.messaging_enums import UnifiedMessageType, UnifiedMessagePriority
            
            # Determine message type based on sender
            if sender.startswith("Agent-"):
                message_type = UnifiedMessageType.AGENT_TO_AGENT
            elif sender == "Captain" or sender.startswith("Captain"):
                message_type = UnifiedMessageType.CAPTAIN_TO_AGENT
            elif sender == "System":
                message_type = UnifiedMessageType.SYSTEM_TO_AGENT
            else:
                message_type = UnifiedMessageType.AGENT_TO_AGENT  # Default to A2A
            
            message = UnifiedMessage(
                content=content,
                recipient=recipient,
                sender=sender,
                message_type=message_type,
                priority=UnifiedMessagePriority.REGULAR
            )
            
            return self.service.send_message_to_agent(
                agent_id=recipient,
                message=content,
                sender=sender,
                priority="NORMAL"
            )
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False
    
    def broadcast(self, content: str, sender: str = "System") -> dict[str, bool]:
        """Broadcast message to all agents."""
        return self.service.broadcast_message(content, sender)
    
    def broadcast_urgent(self, content: str, sender: str = "System") -> dict[str, bool]:
        """Broadcast urgent message to all agents."""
        return self.service.broadcast_message(content, sender, priority="urgent")