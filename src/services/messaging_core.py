#!/usr/bin/env python3
"""
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import os
import time
from typing import List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    SenderType,
    RecipientType,
)
from .onboarding_service import OnboardingService
from .messaging_pyautogui import PyAutoGUIMessagingDelivery
import logging

def get_messaging_logger():
    return logging.getLogger(__name__)


# DIP: Abstract interfaces for delivery and onboarding
from abc import ABC, abstractmethod
from typing import Protocol

class IMessageDelivery(Protocol):
    """Interface for message delivery mechanisms."""
    def send_message(self, message: UnifiedMessage) -> bool:
        """Send a message."""
        ...

class IOnboardingService(Protocol):
    """Interface for onboarding operations."""
    def generate_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate onboarding message."""
        ...

class UnifiedMessagingCore:
    """Core unified messaging service functionality - SOLID Compliant."""

    def __init__(self, delivery_service: IMessageDelivery = None, onboarding_service: IOnboardingService = None):
        """Initialize the core messaging service with dependency injection."""
        self.messages: List[UnifiedMessage] = []
        self.logger = get_messaging_logger()

        # DIP: Depend on abstractions, not concretions
        self.delivery_service = delivery_service or PyAutoGUIMessagingDelivery({})
        self.onboarding_service = onboarding_service or OnboardingService()

        # Load configuration from external config files (V2 compliance)
        self._load_configuration()

        self.logger.info("UnifiedMessagingCore initialized successfully")

    def _load_configuration(self):
        """Load configuration from external config files (V2 compliance)."""
        try:
            # Load agent registry
            from agent_registry import COORDINATES

            # Set up agents configuration
            self.agents = COORDINATES.copy()

            # Set up inbox paths for all agents
            self.inbox_paths = {}
            for agent_id in self.agents.keys():
                inbox_path = os.path.join("agent_workspaces", agent_id, "inbox")
                self.inbox_paths[agent_id] = inbox_path

            self.logger.info(f"Configuration loaded successfully: {len(self.agents)} agents, {len(self.inbox_paths)} inbox paths")

        except ImportError as e:
            self.logger.warning(f"Could not load agent registry: {e}")
            # Fallback to empty configuration
            self.agents = {}
            self.inbox_paths = {}
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            # Fallback to empty configuration
            self.agents = {}
            self.inbox_paths = {}

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """Send message to agent's inbox file with retry mechanism."""
        for attempt in range(max_retries):
            try:
                recipient = message.recipient
                if recipient not in self.inbox_paths:
                    print(f"❌ ERROR: Unknown recipient {recipient}")
                    return False

                inbox_path = self.inbox_paths[recipient]
                os.makedirs(inbox_path, exist_ok=True)

                # Create message filename with timestamp
                if message.timestamp and isinstance(message.timestamp, str):
                    # Convert string timestamp to filename format
                    timestamp = message.timestamp.replace(" ", "_").replace("-", "").replace(":", "")
                elif message.timestamp:
                    # Handle datetime object
                    timestamp = message.timestamp.strftime("%Y%m%d_%H%M%S")
                else:
                    # Fallback to current time
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"CAPTAIN_MESSAGE_{timestamp}_{message.message_id}.md"
                filepath = os.path.join(inbox_path, filename)

                # Write message to file with proper encoding
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(f"# 🚨 CAPTAIN MESSAGE - {message.message_type.value.upper()}\n\n")
                    f.write(f"**From**: {message.sender}\n")
                    f.write(f"**To**: {message.recipient}\n")
                    f.write(f"**Priority**: {message.priority.value}\n")
                    f.write(f"**Message ID**: {message.message_id}\n")
                    f.write(f"**Timestamp**: {message.timestamp if message.timestamp else 'Unknown'}\n\n")
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

    def send_message_via_delivery_service(self, message: UnifiedMessage, **kwargs) -> bool:
        """Send message via the configured delivery service."""
        # OCP: Extension point for different delivery mechanisms
        return self.delivery_service.send_message(message)

    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for specific agent using onboarding service."""
        # ISP: Focused interface usage
        return self.onboarding_service.generate_onboarding_message(agent_id, style)

    def send_onboarding_message(self, agent_id: str, style: str = "friendly", mode: str = "pyautogui", new_tab_method: str = "ctrl_t") -> bool:
        """Send onboarding message to specific agent."""
        message_content = self.generate_onboarding_message(agent_id, style)

        message = UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            sender_type=SenderType.AGENT,
            recipient=agent_id,
            recipient_type=RecipientType.AGENT,
            message_type=UnifiedMessageType.ONBOARDING,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": style}
        )

        self.messages.append(message)
        print(f"✅ ONBOARDING MESSAGE CREATED: Captain Agent-4 → {agent_id}")
        print(f"🎯 Style: {style}")
        print(f"🆔 Message ID: {message.message_id}")

        # SRP: Use abstracted delivery service
        delivery_success = self.send_message_via_delivery_service(message)

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
                    priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
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
            sender_type=SenderType.AGENT,
            recipient=recipient,
            recipient_type=RecipientType.AGENT,
            message_type=message_type,
            priority=priority,
            tags=tags or [],
            metadata=metadata or {}
        )

        self.messages.append(message)
        print(f"✅ MESSAGE CREATED: {sender} → {recipient}")
        print(f"🎯 Type: {message_type.value}")
        print(f"🆔 Message ID: {message.message_id}")

        # SRP: Use abstracted delivery service
        delivery_success = self.send_message_via_delivery_service(message)

        if delivery_success:
            print(f"✅ MESSAGE DELIVERED TO {recipient}")
        else:
            print(f"❌ MESSAGE DELIVERY FAILED TO {recipient}")

        print()
        return delivery_success

    def send_to_all_agents(self, content: str, sender: str,
                          message_type: UnifiedMessageType = UnifiedMessageType.TEXT,
                          priority: UnifiedMessagePriority = UnifiedMessagePriority.REGULAR,
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
                metadata=metadata or {}
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
