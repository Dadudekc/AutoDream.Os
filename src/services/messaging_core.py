#!/usr/bin/env python3
"""
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import os
import time
from typing import List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .onboarding_service import OnboardingService
from .messaging_pyautogui import PyAutoGUIMessagingDelivery
from ..utils.logger import get_messaging_logger
from ..core.metrics import MessagingMetrics


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
        self.metrics = MessagingMetrics()

        self.logger.info("UnifiedMessagingCore initialized successfully",
                        extra={"agent_count": len(self.agents), "inbox_paths": len(self.inbox_paths)})

    def _load_configuration(self):
        """Load configuration from centralized SSOT system (V2 compliance requirement).

        This method implements SSOT by using the centralized configuration management.
        """
        try:
            # Import centralized configuration
            from src.utils.config_core import get_config
            
            # Get agent count and captain ID from centralized config
            agent_count = get_config("AGENT_COUNT", 8)
            captain_id = get_config("CAPTAIN_ID", "Agent-4")
            
            # Default configuration using centralized values
            self.agents = {
                "Agent-1": {"description": "Integration & Core Systems Specialist", "coords": (-1269, 481)},
                "Agent-2": {"description": "Architecture & Design Specialist", "coords": (-308, 480)},
                "Agent-3": {"description": "Infrastructure & DevOps Specialist", "coords": (-1269, 1001)},
                "Agent-5": {"description": "Business Intelligence Specialist", "coords": (652, 421)},
                "Agent-6": {"description": "Gaming & Entertainment Specialist", "coords": (1612, 419)},
                "Agent-7": {"description": "Web Development Specialist", "coords": (653, 940)},
                "Agent-8": {"description": "Integration & Performance Specialist", "coords": (1611, 941)},
                "Agent-4": {"description": "Quality Assurance Specialist (CAPTAIN)", "coords": (-308, 1000)},
            }

            # Agent inbox paths using centralized configuration
            self.inbox_paths = {
                "Agent-1": "agent_workspaces/Agent-1/inbox",
                "Agent-2": "agent_workspaces/Agent-2/inbox",
                "Agent-3": "agent_workspaces/Agent-3/inbox",
                "Agent-4": "agent_workspaces/Agent-4/inbox",
                "Agent-5": "agent_workspaces/Agent-5/inbox",
                "Agent-6": "agent_workspaces/Agent-6/inbox",
                "Agent-7": "agent_workspaces/Agent-7/inbox",
                "Agent-8": "agent_workspaces/Agent-8/inbox",
            }

            # Load from config file if it exists
            config_file = "config/messaging_config.json"
            if os.path.exists(config_file):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'agents' in config:
                        self.agents.update(config['agents'])
                    if 'inbox_paths' in config:
                        self.inbox_paths.update(config['inbox_paths'])

                self.logger.info("Configuration loaded from file", extra={"config_file": config_file})
            else:
                self.logger.info("Using default configuration (no config file found)")

        except Exception as e:
            self.logger.error("Failed to load configuration, using defaults", extra={"error": str(e)})
            # Fallback to hardcoded defaults is already set above
    
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

                # Record metrics (V2 compliance)
                self.metrics.record_message_sent(message.message_type.value, recipient, "inbox")

                return True

            except OSError as e:
                self.logger.error(f"Failed to deliver message to inbox (attempt {attempt + 1}/{max_retries})",
                                extra={"recipient": recipient, "message_id": message.message_id, "error": str(e)})

                # Record failure metrics (V2 compliance)
                self.metrics.record_message_failed(message.message_type.value, recipient, "OSError")

                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff
            except Exception as e:
                self.logger.critical(f"Unexpected error delivering message to inbox (attempt {attempt + 1}/{max_retries})",
                                   extra={"recipient": recipient, "message_id": message.message_id, "error": str(e)})

                # Record failure metrics (V2 compliance)
                self.metrics.record_message_failed(message.message_type.value, recipient, "UnexpectedError")

                if attempt < max_retries - 1:
                    time.sleep(1 * (2 ** attempt))  # Exponential backoff

        return False

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for monitoring and reporting (V2 compliance).

        Returns:
            Dictionary containing all messaging metrics
        """
        return {
            "success_rate": self.metrics.get_success_rate(),
            "delivery_stats": self.metrics.get_delivery_stats(),
            "message_counts": self.metrics.get_message_counts(),
            "error_summary": self.metrics.get_error_summary(),
            "total_operations": self.metrics.metrics.total_operations,
            "successful_operations": self.metrics.metrics.successful_operations,
            "failed_operations": self.metrics.metrics.failed_operations,
        }

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
