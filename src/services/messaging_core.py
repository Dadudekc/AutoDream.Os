#!/usr/bin/env python3
"""
<<<<<<< HEAD
Unified Messaging Core - KISS Simplified
=========================================

Simplified core messaging functionality for the unified messaging service.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined messaging core.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .unified_messaging_imports import (
    logging,
    COORDINATE_CONFIG_FILE,
    get_logger,
    get_unified_utility,
    load_coordinates_from_json,
    json,
)
from ..core.simple_validation_system import get_simple_validator
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
=======
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import os
import time
from typing import List, Dict, Any
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
<<<<<<< HEAD
    UnifiedSenderType,
    UnifiedRecipientType,
)
from .message_identity_clarification import format_message_with_identity_clarification


class UnifiedMessagingCore:
    """Simplified core messaging functionality for the unified messaging service.

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

    def create_message(
        self,
        content: str,
        message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
        priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
        sender_type: UnifiedSenderType = UnifiedSenderType.AGENT,
        recipient_type: UnifiedRecipientType = UnifiedRecipientType.AGENT,
        sender: str = "system",
        recipient: str = "all",
        tags: List[UnifiedMessageTag] = None,
    ) -> UnifiedMessage:
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
                timestamp=datetime.now(),
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

    def send_message(
        self, message: UnifiedMessage, delivery_method: str = "pyautogui"
    ) -> bool:
        """Send message - simplified."""
        try:
            if not self.validate_message(message):
                return False

            # Simplified delivery logic
            self.logger.info(
                f"Sending message via {delivery_method}: {message.message_id}"
            )

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
                "last_updated": datetime.now().isoformat(),
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
            "last_updated": datetime.now().isoformat(),
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


def get_unified_messaging_core(
    config: Optional[Dict[str, Any]] = None,
) -> UnifiedMessagingCore:
    """Returns a global instance of the UnifiedMessagingCore."""
    global _global_messaging_core
    if _global_messaging_core is None:
        _global_messaging_core = UnifiedMessagingCore(config)
    return _global_messaging_core
=======
)
from .onboarding_service import OnboardingService
from .messaging_pyautogui import PyAutoGUIMessagingDelivery
from ..utils.logger import get_messaging_logger


class UnifiedMessagingCore:
    """Core unified messaging service functionality."""
    
    def __init__(self):
        """Initialize the core messaging service."""
        self.messages: List[UnifiedMessage] = []
        self.logger = get_messaging_logger()

                # Load configuration from external config files (V2 compliance)
        self._load_configuration()
        # Initialize services
        self.pyautogui_delivery = PyAutoGUIMessagingDelivery(self.agents)
        self.onboarding_service = OnboardingService()

        self.logger.info("UnifiedMessagingCore initialized successfully",
                        extra={"agent_count": len(self.agents), "inbox_paths": len(self.inbox_paths)})
    
    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """Send message to agent's inbox file with retry mechanism.

        Args:
            message: The UnifiedMessage to deliver
            max_retries: Maximum number of retry attempts

        Returns:
            bool: True if delivery successful, False otherwise
        """
        for attempt in range(max_retries):
            try:
                recipient = message.recipient
                if recipient not in self.inbox_paths:
                    print(f"❌ ERROR: Unknown recipient {recipient}")
                    return False

                inbox_path = self.inbox_paths[recipient]
                os.makedirs(inbox_path, exist_ok=True)

                # Create message filename with timestamp
                timestamp = message.timestamp.strftime("%Y%m%d_%H%M%S") if message.timestamp else time.strftime("%Y%m%d_%H%M%S")
                filename = f"CAPTAIN_MESSAGE_{timestamp}_{message.message_id}.md"
                filepath = os.path.join(inbox_path, filename)

                # Write message to file with proper encoding
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# 🚨 CAPTAIN MESSAGE - {message.message_type.value.upper()}\n\n")
                    f.write(f"**From**: {message.sender}\n")
                    f.write(f"**To**: {message.recipient}\n")
                    f.write(f"**Priority**: {message.priority.value}\n")
                    f.write(f"**Message ID**: {message.message_id}\n")
                    f.write(f"**Timestamp**: {message.timestamp.isoformat() if message.timestamp else 'Unknown'}\n\n")
                    f.write("---\n\n")
                    f.write(message.content)
                    f.write("\n\n---\n")
                    f.write(f"*Message delivered via Unified Messaging Service*\n")

                self.logger.info("Message delivered to inbox successfully",
                                extra={"filepath": filepath, "recipient": recipient, "message_id": message.message_id})
                return True

            except OSError as e:
                self.logger.error(f"Failed to deliver message to inbox (attempt {attempt + 1}/{max_retries})",
                                extra={"recipient": recipient, "message_id": message.message_id, "error": str(e)})
                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff
            except Exception as e:
                self.logger.critical(f"Unexpected error delivering message to inbox (attempt {attempt + 1}/{max_retries})",
                                   extra={"recipient": recipient, "message_id": message.message_id, "error": str(e)})
                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff

        return False
    
    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True, new_tab_method: str = "ctrl_t", use_new_tab: bool = None) -> bool:
        """Send message via PyAutoGUI to agent coordinates.

        Args:
            message: The message to send
            use_paste: Whether to use clipboard paste (faster) or typing
            new_tab_method: "ctrl_t" for Ctrl+T or "ctrl_n" for Ctrl+N
            use_new_tab: Whether to create new tab/window. If None, determined by message type.
        """
        # Determine whether to use new tab based on message type if not explicitly set
        if use_new_tab is None:
            # Onboarding messages should use new tab/window
            use_new_tab = (message.message_type == UnifiedMessageType.ONBOARDING)

        return self.pyautogui_delivery.send_message_via_pyautogui(message, use_paste, new_tab_method, use_new_tab)

    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for specific agent using onboarding service."""
        agent_info = self.agents.get(agent_id, {})
        role = agent_info.get("description", "Specialist")
        return self.onboarding_service.generate_onboarding_message(agent_id, role, style)
    
    def send_onboarding_message(self, agent_id: str, style: str = "friendly", mode: str = "pyautogui", new_tab_method: str = "ctrl_t") -> bool:
        """Send onboarding message to specific agent."""
        message_content = self.generate_onboarding_message(agent_id, style)
        
        message = UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            recipient=agent_id,
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": style}
        )
        
        self.messages.append(message)
        print(f"✅ ONBOARDING MESSAGE CREATED: Captain Agent-4 → {agent_id}")
        print(f"🎯 Style: {style}")
        print(f"🆔 Message ID: {message.message_id}")
        
        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.send_message_via_pyautogui(message, use_paste=True, new_tab_method=new_tab_method)
        else:
            delivery_success = self.send_message_to_inbox(message)
        
        if delivery_success:
            print(f"✅ ONBOARDING MESSAGE DELIVERED TO {agent_id}")
        else:
            print(f"❌ ONBOARDING MESSAGE DELIVERY FAILED TO {agent_id}")
        
        print()
        return delivery_success
    
    def send_bulk_onboarding(self, style: str = "friendly", mode: str = "pyautogui", new_tab_method: str = "ctrl_t") -> List[bool]:
        """Send onboarding messages to all agents."""
        results = []
        print(f"🚨 BULK ONBOARDING ACTIVATED - {style.upper()} MODE")
        print(f"📋 CORRECT ORDER: Agent-4 will be onboarded LAST")
        
        # CORRECT ORDER: Agent-4 LAST
        agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
        
        for agent_id in agent_order:
            success = self.send_onboarding_message(agent_id, style, mode, new_tab_method)
            results.append(success)
            time.sleep(1)  # Brief pause between agents
        
        success_count = sum(results)
        total_count = len(results)
        print(f"📊 BULK ONBOARDING COMPLETED: {success_count}/{total_count} successful")
        return results
    
    def send_message(self, content: str, sender: str, recipient: str,
                    message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                    priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
                    tags: List[UnifiedMessageTag] = None,
                    metadata: Dict[str, Any] = None,
                    mode: str = "pyautogui",
                    use_paste: bool = True,
                    new_tab_method: str = "ctrl_t",
                    use_new_tab: bool = None) -> bool:
        """Send a single message to a specific agent."""
        message = UnifiedMessage(
            content=content,
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata or {}
        )
        
        self.messages.append(message)
        print(f"✅ MESSAGE CREATED: {sender} → {recipient}")
        print(f"🎯 Type: {message_type.value}")
        print(f"🆔 Message ID: {message.message_id}")
        
        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.send_message_via_pyautogui(message, use_paste, new_tab_method, use_new_tab)
        else:
            delivery_success = self.send_message_to_inbox(message)
        
        if delivery_success:
            print(f"✅ MESSAGE DELIVERED TO {recipient}")
        else:
            print(f"❌ MESSAGE DELIVERY FAILED TO {recipient}")
        
        print()
        return delivery_success
    
    def send_to_all_agents(self, content: str, sender: str,
                          message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                          priority: UnifiedMessagePriority = UnifiedMessagePriority.NORMAL,
                          tags: List[UnifiedMessageTag] = None,
                          metadata: Dict[str, Any] = None,
                          mode: str = "pyautogui",
                          use_paste: bool = True,
                          new_tab_method: str = "ctrl_t",
                          use_new_tab: bool = None) -> List[bool]:
        """Send message to all agents."""
        results = []
        print(f"🚨 BULK MESSAGE ACTIVATED")
        print(f"📋 SENDING TO ALL AGENTS")
        
        # CORRECT ORDER: Agent-4 LAST
        agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8", "Agent-4"]
        
        for agent_id in agent_order:
            success = self.send_message(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=message_type,
                priority=priority,
                tags=tags or [],
                metadata=metadata or {},
                mode=mode,
                use_paste=use_paste,
                new_tab_method=new_tab_method,
                use_new_tab=use_new_tab
            )
            results.append(success)
            time.sleep(1)  # Brief pause between agents
        
        success_count = sum(results)
        total_count = len(results)
        print(f"📊 BULK MESSAGE COMPLETED: {success_count}/{total_count} successful")
        return results
    
    def list_agents(self):
        """List all available agents."""
        print("📋 AVAILABLE AGENTS:")
        print("=" * 50)
        for agent_id, info in self.agents.items():
            print(f"🤖 {agent_id}: {info['description']}")
            print(f"   📍 Coordinates: {info['coords']}")
            print(f"   📬 Inbox: {self.inbox_paths.get(agent_id, 'N/A')}")
            print()
    
    def show_coordinates(self):
        """Show agent coordinates."""
        print("📍 AGENT COORDINATES:")
        print("=" * 30)
        for agent_id, info in self.agents.items():
            print(f"🤖 {agent_id}: {info['coords']}")
        print()
    
    def show_message_history(self):
        """Show message history."""
        print("📜 MESSAGE HISTORY:")
        print("=" * 30)
        for i, message in enumerate(self.messages, 1):
            print(f"{i}. {message.sender} → {message.recipient}")
            print(f"   Type: {message.message_type.value}")
            print(f"   Priority: {message.priority.value}")
            print(f"   ID: {message.message_id}")
            print()
>>>>>>> origin/cursor/refactor-dashboard-js-to-under-300-lines-dc65
