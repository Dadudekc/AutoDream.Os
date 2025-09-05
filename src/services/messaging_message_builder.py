#!/usr/bin/env python3
"""
Messaging Message Builder - V2 Compliance Module
===============================================

Message building and construction system for the messaging service.

V2 Compliance: < 300 lines, single responsibility, message building.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import Any, Dict, Optional
from datetime import datetime
from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType
)


class MessagingMessageBuilder:
    """
    Message building system for creating properly formatted messages.
    
    Provides comprehensive message construction capabilities while maintaining
    all original functionality through efficient design.
    """
    
    def __init__(self):
        """Initialize message builder."""
        self.default_sender = "Captain Agent-4"
        self.default_priority = UnifiedMessagePriority.REGULAR
        self.default_type = UnifiedMessageType.TEXT
    
    def build_message(
        self,
        message: str,
        recipient: str,
        sender: Optional[str] = None,
        message_type: Optional[UnifiedMessageType] = None,
        priority: Optional[UnifiedMessagePriority] = None,
        tags: Optional[list] = None,
        sender_type: Optional[SenderType] = None,
        recipient_type: Optional[RecipientType] = None,
        **kwargs
    ) -> UnifiedMessage:
        """
        Build a unified message with proper defaults and validation.
        
        Args:
            message: Message content
            recipient: Target recipient
            sender: Sender name (defaults to Captain Agent-4)
            message_type: Type of message
            priority: Message priority
            tags: Message tags
            sender_type: Type of sender
            recipient_type: Type of recipient
            **kwargs: Additional message parameters
            
        Returns:
            Properly constructed UnifiedMessage
        """
        # Apply defaults
        sender = sender or self.default_sender
        message_type = message_type or self.default_type
        priority = priority or self.default_priority
        tags = tags or []
        
        # Infer types if not provided
        if not sender_type:
            sender_type = self._infer_sender_type(sender)
        
        if not recipient_type:
            recipient_type = self._infer_recipient_type(recipient)
        
        # Create message
        unified_message = UnifiedMessage(
            content=message,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags,
            sender_type=sender_type,
            recipient_type=recipient_type,
            **kwargs
        )
        
        return unified_message
    
    def build_bulk_message(
        self,
        message: str,
        recipients: list,
        sender: Optional[str] = None,
        message_type: Optional[UnifiedMessageType] = None,
        priority: Optional[UnifiedMessagePriority] = None,
        **kwargs
    ) -> list:
        """
        Build multiple messages for bulk sending.
        
        Args:
            message: Message content
            recipients: List of recipient names
            sender: Sender name
            message_type: Type of message
            priority: Message priority
            **kwargs: Additional message parameters
            
        Returns:
            List of UnifiedMessage objects
        """
        messages = []
        
        for recipient in recipients:
            msg = self.build_message(
                message=message,
                recipient=recipient,
                sender=sender,
                message_type=message_type,
                priority=priority,
                **kwargs
            )
            messages.append(msg)
        
        return messages
    
    def build_onboarding_message(
        self,
        recipient: str,
        style: str = "friendly",
        sender: Optional[str] = None
    ) -> UnifiedMessage:
        """
        Build an onboarding message.
        
        Args:
            recipient: Target recipient
            style: Onboarding style (friendly/professional)
            sender: Sender name
            
        Returns:
            Onboarding UnifiedMessage
        """
        if style == "professional":
            content = self._get_professional_onboarding_content(recipient)
        else:
            content = self._get_friendly_onboarding_content(recipient)
        
        return self.build_message(
            message=content,
            recipient=recipient,
            sender=sender or self.default_sender,
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.REGULAR,
            tags=[UnifiedMessageTag.ONBOARDING]
        )
    
    def build_broadcast_message(
        self,
        message: str,
        sender: Optional[str] = None,
        priority: Optional[UnifiedMessagePriority] = None
    ) -> UnifiedMessage:
        """
        Build a broadcast message for all agents.
        
        Args:
            message: Message content
            sender: Sender name
            priority: Message priority
            
        Returns:
            Broadcast UnifiedMessage
        """
        return self.build_message(
            message=message,
            recipient="All Agents",
            sender=sender or self.default_sender,
            message_type=UnifiedMessageType.BROADCAST,
            priority=priority or self.default_priority,
            tags=[UnifiedMessageTag.CAPTAIN]
        )
    
    def _infer_sender_type(self, sender: str) -> SenderType:
        """Infer sender type from sender name."""
        if sender.startswith("Agent-"):
            return SenderType.AGENT
        elif sender in ["Captain Agent-4", "System"]:
            return SenderType.SYSTEM
        else:
            return SenderType.HUMAN
    
    def _infer_recipient_type(self, recipient: str) -> RecipientType:
        """Infer recipient type from recipient name."""
        if recipient.startswith("Agent-"):
            return RecipientType.AGENT
        elif recipient in ["System", "All Agents"]:
            return RecipientType.SYSTEM
        else:
            return RecipientType.HUMAN
    
    def _get_friendly_onboarding_content(self, recipient: str) -> str:
        """Get friendly onboarding message content."""
        return f"""🚀 Welcome to the Agent Swarm, {recipient}!

I'm Captain Agent-4, your Strategic Oversight & Emergency Intervention Manager. 

Here's what you need to know:
• You are {recipient} - remember your identity!
• Check your inbox regularly: agent_workspaces/{recipient}/inbox/
• Use the messaging system to communicate with other agents
• Follow V2 compliance standards for all code
• Report status updates to me when completing tasks

Ready to get started? Let me know when you're online! 🎯"""
    
    def _get_professional_onboarding_content(self, recipient: str) -> str:
        """Get professional onboarding message content."""
        return f"""AGENT ONBOARDING NOTICE - {recipient}

FROM: Captain Agent-4 (Strategic Oversight & Emergency Intervention Manager)
TO: {recipient}
PRIORITY: STANDARD
TYPE: SYSTEM-TO-AGENT ONBOARDING

MISSION PARAMETERS:
- Agent Identity: {recipient}
- Workspace: agent_workspaces/{recipient}/
- Communication Protocol: Unified Messaging System
- Compliance Standard: V2 Architecture
- Status Reporting: Mandatory

OPERATIONAL REQUIREMENTS:
1. Maintain agent identity awareness
2. Monitor inbox for directives
3. Execute assigned tasks per V2 standards
4. Report completion status
5. Coordinate with other agents as needed

ACKNOWLEDGMENT REQUIRED: Confirm receipt and readiness status."""
