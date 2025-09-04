#!/usr/bin/env python3
"""
Messaging Message Builder Module - V2 Compliant
==============================================

Message construction and validation for the messaging system.
Builds UnifiedMessage objects with proper validation and metadata.

Author: Agent-5 - Business Intelligence Specialist
License: MIT
"""

from .unified_messaging_imports import logging
from typing import Optional, List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    SenderType,
    RecipientType,
)


class MessagingMessageBuilder:
    """
    Message builder for creating and validating UnifiedMessage objects.
    
    Provides methods for building messages with proper validation,
    metadata handling, and type safety.
    """

    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the message builder.
        
        Args:
            logger: Optional logger instance
        """
        self.logger = logger or logging.getLogger(__name__)

    def build_message(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: Optional[List[UnifiedMessageTag]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        sender_type: SenderType = SenderType.SYSTEM,
        recipient_type: RecipientType = RecipientType.AGENT,
    ) -> UnifiedMessage:
        """
        Build a UnifiedMessage with validation.
        
        Args:
            content: Message content
            sender: Message sender
            recipient: Message recipient
            message_type: Type of message
            priority: Message priority
            tags: Message tags
            metadata: Additional metadata
            sender_type: Type of sender
            recipient_type: Type of recipient
            
        Returns:
            Built UnifiedMessage object
            
        Raises:
            ValueError: If message validation fails
        """
        try:
            # Validate required fields
            if not content or not content.strip():
                get_unified_validator().raise_validation_error("Message content cannot be empty")
            
            if not sender or not sender.strip():
                get_unified_validator().raise_validation_error("Message sender cannot be empty")
                
            if not recipient or not recipient.strip():
                get_unified_validator().raise_validation_error("Message recipient cannot be empty")

            # Build metadata with defaults
            message_metadata = {
                'builder_version': 'v2.0',
                **(metadata or {})
            }

            # Create message
            message = UnifiedMessage(
                content=content.strip(),
                sender=sender.strip(),
                recipient=recipient.strip(),
                message_type=message_type,
                priority=priority,
                tags=tags or [],
                metadata=message_metadata,
                sender_type=sender_type,
                recipient_type=recipient_type,
            )

            # Validate the built message
            if not self.validate_message(message):
                get_unified_validator().raise_validation_error("Built message failed validation")

            self.get_logger(__name__).debug(f"✅ Built message: {sender} → {recipient} ({message_type.value})")
            return message

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error building message: {e}")
            raise

    def create_broadcast_message(
        self,
        content: str,
        sender: str,
        recipients: List[str],
        message_type: UnifiedMessageType = UnifiedMessageType.BROADCAST,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        tags: Optional[List[UnifiedMessageTag]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> List[UnifiedMessage]:
        """
        Create broadcast messages for multiple recipients.
        
        Args:
            content: Message content
            sender: Message sender
            recipients: List of recipients
            message_type: Type of message
            priority: Message priority
            tags: Message tags
            metadata: Additional metadata
            
        Returns:
            List of UnifiedMessage objects for each recipient
        """
        try:
            if not get_unified_validator().validate_required(recipients):
                get_unified_validator().raise_validation_error("Recipients list cannot be empty")

            messages = []
            broadcast_metadata = {
                'broadcast_id': f"broadcast_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                'total_recipients': len(recipients),
                **(metadata or {})
            }

            for recipient in recipients:
                message = self.build_message(
                    content=content,
                    sender=sender,
                    recipient=recipient,
                    message_type=message_type,
                    priority=priority,
                    tags=tags,
                    metadata=broadcast_metadata,
                    sender_type=SenderType.SYSTEM,
                    recipient_type=RecipientType.AGENT,
                )
                messages.append(message)

            self.get_logger(__name__).info(f"📢 Created broadcast for {len(recipients)} recipients")
            return messages

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error creating broadcast messages: {e}")
            raise

    def validate_message(self, message: UnifiedMessage) -> bool:
        """
        Validate a UnifiedMessage object using shared validation utilities.
        
        Args:
            message: Message to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            
            # Use shared validation logic
            validation_result = MessagingValidationUtils.validate_message_structure(message)
            
            # Log validation results
            if not validation_result["valid"]:
                for error in validation_result["errors"]:
                    self.get_logger(__name__).warning(f"❌ {error}")
                return False
                
            for warning in validation_result["warnings"]:
                self.get_logger(__name__).warning(f"⚠️ {warning}")
                
            return True

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error validating message: {e}")
            return False

    def create_onboarding_message(
        self,
        agent_id: str,
        agent_role: str,
        style: str = "friendly"
    ) -> UnifiedMessage:
        """
        Create a personalized onboarding message.
        
        Args:
            agent_id: Target agent ID
            agent_role: Agent role/name
            style: Message style (friendly/professional)
            
        Returns:
            Onboarding UnifiedMessage
        """
        try:
            if style == "friendly":
                content = f"""🚨 **ATTENTION {agent_id}** - YOU ARE {agent_id} 🚨

📡 **S2A MESSAGE (System-to-Agent)**
📤 **FROM:** Captain Agent-4 (System)
📥 **TO:** {agent_id} (Agent)

🔍 **SENDER TYPE:** system
🔍 **RECIPIENT TYPE:** agent

🎯 **ONBOARDING - FRIENDLY MODE** 🎯

**Agent**: {agent_id}
**Role**: {agent_role}

Use --get-next-task to claim your first contract.

**WE. ARE. SWARM.** ⚡️🔥"""
            else:
                content = f"""SYSTEM MESSAGE - AGENT ONBOARDING
================================

Agent: {agent_id}
Role: {agent_role}
Status: ACTIVE_AGENT_MODE
Phase: TASK_EXECUTION

Instructions:
1. Use --get-next-task to claim your first contract
2. Maintain V2 compliance standards
3. Provide progress reports via inbox
4. Coordinate with other agents as needed

Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"""

            return self.build_message(
                content=content,
                sender="Captain Agent-4",
                recipient=agent_id,
                message_type=UnifiedMessageType.ONBOARDING,
                priority=UnifiedMessagePriority.HIGH,
                tags=[UnifiedMessageTag.ONBOARDING],
                metadata={
                    'onboarding_style': style,
                    'agent_role': agent_role,
                    'onboarding_timestamp': datetime.now().isoformat()
                },
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error creating onboarding message: {e}")
            raise

    def create_wrapup_message(
        self,
        agent_id: str,
        achievements: Optional[List[str]] = None
    ) -> UnifiedMessage:
        """
        Create a wrapup message for an agent.
        
        Args:
            agent_id: Target agent ID
            achievements: List of achievements to include
            
        Returns:
            Wrapup UnifiedMessage
        """
        try:
            achievements_text = ""
            if achievements:
                achievements_text = "\n\n🏆 **ACHIEVEMENTS:**\n" + "\n".join(f"- {achievement}" for achievement in achievements)

            content = f"""🎯 **WRAPUP MESSAGE** 🎯

**Agent**: {agent_id}
**Status**: Mission Complete
**Timestamp**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Excellent work! Mission objectives completed successfully.{achievements_text}

**WE. ARE. SWARM.** ⚡️🔥"""

            return self.build_message(
                content=content,
                sender="Captain Agent-4",
                recipient=agent_id,
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR,
                tags=[UnifiedMessageTag.WRAPUP],
                metadata={
                    'wrapup_timestamp': datetime.now().isoformat(),
                    'achievements': achievements or []
                },
                sender_type=SenderType.SYSTEM,
                recipient_type=RecipientType.AGENT,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error creating wrapup message: {e}")
            raise
