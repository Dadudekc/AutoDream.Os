"""
Unified Messaging Service - Wrapper for Messaging Service
==========================================================

Provides unified interface to messaging system.
Wraps ConsolidatedMessagingService for backward compatibility.

V2 Compliance: Wrapper pattern, <400 lines
"""

import logging
from .messaging_service import ConsolidatedMessagingService

logger = logging.getLogger(__name__)


class UnifiedMessagingService:
    """Unified messaging service wrapper."""
    
    def __init__(self):
        """Initialize unified messaging service."""
        self.messaging = ConsolidatedMessagingService()
        logger.info("UnifiedMessagingService initialized")
    
    def send_message(
        self, agent: str, message: str, priority: str = "regular", use_pyautogui: bool = True
    ) -> bool:
        """
        Send message to agent.
        
        Args:
            agent: Target agent ID
            message: Message content
            priority: Message priority (regular/urgent)
            use_pyautogui: Use PyAutoGUI delivery
            
        Returns:
            True if successful
        """
        return self.messaging.send_message(agent, message, priority, use_pyautogui)
    
    def broadcast_message(self, message: str, priority: str = "regular") -> dict:
        """
        Broadcast message to all agents.
        
        Args:
            message: Message content
            priority: Message priority
            
        Returns:
            Dictionary of results {agent_id: success}
        """
        return self.messaging.broadcast_message(message, priority)


# Alias for backward compatibility
MessagingService = UnifiedMessagingService
