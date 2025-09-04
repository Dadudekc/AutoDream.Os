#!/usr/bin/env python3
"""
Message Identity Clarification System - Agent Cellphone V2
=========================================================

Enhanced message formatting system that provides clear sender/recipient identification
and message type clarification for improved swarm coordination.

V2 Compliance: < 300 lines, single responsibility, message identity clarification.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Dict, Any, Optional
from datetime import datetime
from ..services.models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    SenderType,
    RecipientType
)


class MessageIdentityClarification:
    """
    Enhanced message identity clarification system.
    
    Provides clear sender/recipient identification and message type clarification
    for improved swarm coordination and communication clarity.
    """
    
    def __init__(self):
        """Initialize the message identity clarification system."""
        self.identity_templates = self._initialize_identity_templates()
        self.message_type_templates = self._initialize_message_type_templates()
    
    def _initialize_identity_templates(self) -> Dict[str, str]:
        """Initialize identity clarification templates."""
        return {
            "agent_reminder": "🚨 **ATTENTION {recipient}** - YOU ARE {recipient} 🚨\n\n",
            "sender_identification": "📤 **FROM:** {sender} ({sender_type})\n",
            "recipient_identification": "📥 **TO:** {recipient} ({recipient_type})\n",
            "message_type_header": "📡 **{message_type} MESSAGE**\n",
            "timestamp_header": "🕐 **TIMESTAMP:** {timestamp}\n",
            "priority_header": "⚡ **PRIORITY:** {priority}\n",
            "message_id_header": "🆔 **MESSAGE ID:** {message_id}\n"
        }
    
    def _initialize_message_type_templates(self) -> Dict[UnifiedMessageType, str]:
        """Initialize message type clarification templates."""
        return {
            UnifiedMessageType.A2A: "A2A (Agent-to-Agent)",
            UnifiedMessageType.S2A: "S2A (System-to-Agent)",
            UnifiedMessageType.H2A: "H2A (Human-to-Agent)",
            UnifiedMessageType.C2A: "C2A (Captain-to-Agent)",
            UnifiedMessageType.ONBOARDING: "ONBOARDING (System-to-Agent)",
            UnifiedMessageType.BROADCAST: "BROADCAST (Swarm-wide)",
            UnifiedMessageType.TEXT: "TEXT (Standard Message)"
        }
    
    def format_message_with_identity_clarification(
        self, 
        message: UnifiedMessage, 
        recipient: str
    ) -> str:
        """
        Format message with enhanced identity clarification.
        
        Args:
            message: The unified message to format
            recipient: The target recipient
            
        Returns:
            Formatted message with clear identity clarification
        """
        # Base agent identity reminder
        agent_reminder = self.identity_templates["agent_reminder"].format(
            recipient=recipient
        )
        
        # Message type header
        message_type_text = self.message_type_templates.get(
            message.message_type, 
            "UNKNOWN"
        )
        message_type_header = self.identity_templates["message_type_header"].format(
            message_type=message_type_text
        )
        
        # Sender identification
        sender_type = self._get_sender_type_display(message.sender, message.sender_type)
        sender_identification = self.identity_templates["sender_identification"].format(
            sender=message.sender,
            sender_type=sender_type
        )
        
        # Recipient identification
        recipient_type = self._get_recipient_type_display(recipient, message.recipient_type)
        recipient_identification = self.identity_templates["recipient_identification"].format(
            recipient=recipient,
            recipient_type=recipient_type
        )
        
        # Additional metadata headers
        metadata_headers = self._format_metadata_headers(message)
        
        # Combine all headers
        headers = (
            agent_reminder +
            message_type_header +
            sender_identification +
            recipient_identification +
            metadata_headers
        )
        
        # Format the complete message
        formatted_message = headers + message.content
        
        return formatted_message
    
    def _get_sender_type_display(self, sender: str, sender_type: Optional[SenderType]) -> str:
        """Get display text for sender type."""
        if sender_type:
            return sender_type.value.upper()
        
        # Infer from sender name
        if sender.startswith("Agent-"):
            return "AGENT"
        elif sender in ["Captain Agent-4", "System"]:
            return "SYSTEM"
        elif sender == "Captain Agent-4":
            return "CAPTAIN"
        else:
            return "UNKNOWN"
    
    def _get_recipient_type_display(self, recipient: str, recipient_type: Optional[RecipientType]) -> str:
        """Get display text for recipient type."""
        if recipient_type:
            return recipient_type.value.upper()
        
        # Infer from recipient name
        if recipient.startswith("Agent-"):
            return "AGENT"
        elif recipient in ["System", "All Agents"]:
            return "SYSTEM"
        else:
            return "UNKNOWN"
    
    def _format_metadata_headers(self, message: UnifiedMessage) -> str:
        """Format additional metadata headers."""
        headers = ""
        
        # Timestamp
        if message.timestamp:
            timestamp_str = message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            headers += self.identity_templates["timestamp_header"].format(
                timestamp=timestamp_str
            )
        
        # Priority
        if message.priority:
            headers += self.identity_templates["priority_header"].format(
                priority=message.priority.value.upper()
            )
        
        # Message ID
        if message.message_id:
            headers += self.identity_templates["message_id_header"].format(
                message_id=message.message_id
            )
        
        # Add spacing if headers exist
        if headers:
            headers += "\n"
        
        return headers
    
    def create_identity_clarified_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        sender_type: Optional[SenderType] = None,
        recipient_type: Optional[RecipientType] = None,
        **kwargs
    ) -> str:
        """
        Create a message with enhanced identity clarification.
        
        Args:
            content: Message content
            sender: Sender identification
            recipient: Recipient identification
            message_type: Type of message
            sender_type: Type of sender
            recipient_type: Type of recipient
            **kwargs: Additional message parameters
            
        Returns:
            Formatted message with identity clarification
        """
        # Create a temporary message object for formatting
        temp_message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            sender_type=sender_type,
            recipient_type=recipient_type,
            **kwargs
        )
        
        return self.format_message_with_identity_clarification(temp_message, recipient)
    
    def enhance_existing_message(self, message: UnifiedMessage) -> str:
        """
        Enhance an existing message with identity clarification.
        
        Args:
            message: The message to enhance
            
        Returns:
            Enhanced message with identity clarification
        """
        return self.format_message_with_identity_clarification(message, message.recipient)


# Global instance for easy access
message_identity_clarification = MessageIdentityClarification()
