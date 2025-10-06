#!/usr/bin/env python3
"""
Enhanced Messaging Service
==========================

Integrated messaging service with validation, queuing, and UI Ops facade.
Provides robust agent-to-agent messaging with coordinate validation,
clipboard validation, and conflict prevention.

Author: Agent-4 (Captain)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import logging
import time
from typing import Dict, Tuple

from .enhanced_message_queue import (
    EnhancedMessageCoordinator,
    MessagePriority,
    get_message_coordinator,
    initialize_message_coordinator
)
from .enhanced_message_sender import get_enhanced_sender

logger = logging.getLogger(__name__)


class EnhancedMessagingService:
    """Enhanced messaging service with full validation and queuing."""
    
    def __init__(self):
        """Initialize enhanced messaging service."""
        self.sender = get_enhanced_sender()
        self.coordinator = get_message_coordinator()
        self.coordinator.initialize(self.sender)
        self._message_formatter = self._create_message_formatter()
        
        logger.info("Enhanced messaging service initialized with validation and queuing")
    
    def _create_message_formatter(self):
        """Create message formatter for A2A messages."""
        class MessageFormatter:
            @staticmethod
            def format_a2a_message(from_agent: str, to_agent: str, message: str, priority: str = "NORMAL") -> str:
                """Format agent-to-agent message."""
                timestamp = time.strftime("%H:%M:%S")
                priority_emoji = {
                    "LOW": "🟢",
                    "NORMAL": "🔵", 
                    "HIGH": "🟡",
                    "CRITICAL": "🔴"
                }.get(priority.upper(), "🔵")
                
                formatted = f"""[A2A] MESSAGE
{priority_emoji} PRIORITY: {priority}
📤 FROM: {from_agent}
📥 TO: {to_agent}
⏰ TIME: {timestamp}
📝 CONTENT: {message}
=========================================="""
                
                return formatted
        
        return MessageFormatter()
    
    def send_message(
        self,
        agent_id: str,
        message: str,
        from_agent: str = "Agent-4",
        priority: str = "NORMAL",
        coordinates: Tuple[int, int] = None,
        compact: bool = False,
        minimal: bool = False
    ) -> Tuple[bool, str]:
        """
        Send message to agent with full validation and queuing.
        
        Args:
            agent_id: Target agent ID
            message: Message content
            from_agent: Sender agent ID
            priority: Message priority (LOW, NORMAL, HIGH, CRITICAL)
            coordinates: Agent coordinates (if None, will be looked up)
            compact: Use compact template format (default: False)
            minimal: Use minimal template format (default: False)
            
        Returns:
            Tuple of (success: bool, message_id: str)
        """
        try:
            # Step 1: Validate inputs
            if not agent_id or not message:
                logger.error("❌ Invalid agent_id or message")
                return False, "Invalid agent_id or message"
            
            # Step 2: Get coordinates if not provided
            if coordinates is None:
                coordinates = self._get_agent_coordinates(agent_id)
                if not coordinates:
                    logger.error(f"❌ Could not get coordinates for {agent_id}")
                    return False, f"Could not get coordinates for {agent_id}"
            
            # Step 3: Format message
            formatted_message = self._message_formatter.format_a2a_message(
                from_agent, agent_id, message, priority, compact, minimal
            )
            
            # Step 4: Convert priority string to enum
            priority_enum = MessagePriority(priority.upper()) if priority.upper() in ["LOW", "NORMAL", "HIGH", "CRITICAL"] else MessagePriority.NORMAL
            
            # Step 5: Queue message
            message_id = self.coordinator.send_message(
                agent_id=agent_id,
                message=formatted_message,
                from_agent=from_agent,
                coordinates=coordinates,
                priority=priority_enum
            )
            
            logger.info(f"✅ Message queued: {message_id} from {from_agent} to {agent_id}")
            return True, message_id
            
        except Exception as e:
            logger.error(f"❌ Failed to send message: {e}")
            return False, str(e)
    
    def _get_agent_coordinates(self, agent_id: str) -> Tuple[int, int]:
        """Get coordinates for agent (simplified implementation)."""
        # This would normally load from coordinates.json
        # For now, return mock coordinates
        coordinate_map = {
            "Agent-1": (100, 100),
            "Agent-2": (200, 200),
            "Agent-3": (300, 300),
            "Agent-4": (400, 400),
            "Agent-5": (500, 500),
            "Agent-6": (600, 600),
            "Agent-7": (700, 700),
            "Agent-8": (800, 800)
        }
        
        return coordinate_map.get(agent_id)
    
    def get_service_status(self) -> Dict:
        """Get comprehensive service status."""
        try:
            coordinator_stats = self.coordinator.get_stats()
            sender_clipboard_status = self.sender.get_clipboard_status()
            
            return {
                "service": "EnhancedMessagingService",
                "status": "active",
                "coordinator_stats": coordinator_stats,
                "clipboard_status": sender_clipboard_status,
                "sender_available": True,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
        except Exception as e:
            logger.error(f"Error getting service status: {e}")
            return {
                "service": "EnhancedMessagingService",
                "status": "error",
                "error": str(e),
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def validate_coordinates(self, coordinates: Tuple[int, int]) -> Dict:
        """Validate coordinates using enhanced sender."""
        return self.sender.get_coordinate_status(coordinates)
    
    def get_clipboard_status(self) -> Dict:
        """Get clipboard status using enhanced sender."""
        return self.sender.get_clipboard_status()
    
    def shutdown(self):
        """Shutdown enhanced messaging service."""
        try:
            self.coordinator.shutdown()
            logger.info("Enhanced messaging service shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# Global enhanced service instance
_global_enhanced_service = None


def get_enhanced_messaging_service() -> EnhancedMessagingService:
    """Get global enhanced messaging service instance."""
    global _global_enhanced_service
    if _global_enhanced_service is None:
        _global_enhanced_service = EnhancedMessagingService()
    return _global_enhanced_service


def shutdown_enhanced_messaging_service():
    """Shutdown global enhanced messaging service."""
    global _global_enhanced_service
    if _global_enhanced_service:
        _global_enhanced_service.shutdown()
        _global_enhanced_service = None

