#!/usr/bin/env python3
"""
Core Messaging Service - Agent Cellphone V2
=========================================

Core messaging functionality for the unified messaging service.
Refactored for V2 compliance (300-line limit).

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List, Dict, Any

from .models.messaging_models import (
    UnifiedMessage,
    UnifiedMessageType,
    UnifiedMessagePriority,
    UnifiedMessageTag,
)
from .messaging_config import MessagingConfiguration
from .messaging_delivery import MessagingDelivery
from .messaging_onboarding import MessagingOnboarding
from .messaging_bulk import MessagingBulk
from .messaging_utils import MessagingUtils
from .messaging_pyautogui import PyAutoGUIMessagingDelivery
from ..utils.logger import get_messaging_logger
from ..core.metrics import MessagingMetrics


class UnifiedMessagingCore:
    """Core unified messaging service functionality."""

    def __init__(self):
        """Initialize the core messaging service."""
        self.messages: List[UnifiedMessage] = []
        self.logger = get_messaging_logger()

        # Initialize modular components
        self.config = MessagingConfiguration()
        self.metrics = MessagingMetrics()
        self.delivery = MessagingDelivery(self.config.inbox_paths, self.metrics)

        # Initialize delivery services
        self.pyautogui_delivery = PyAutoGUIMessagingDelivery(self.config.agents)
        self.onboarding = MessagingOnboarding(self.config.agents, self.pyautogui_delivery)
        self.bulk = MessagingBulk(self.pyautogui_delivery)
        self.utils = MessagingUtils(self.config.agents, self.config.inbox_paths, self.messages)

        self.logger.info("UnifiedMessagingCore initialized successfully")

    def send_message_to_inbox(self, message: UnifiedMessage, max_retries: int = 3) -> bool:
        """Send message to agent's inbox file with retry mechanism."""
        return self.delivery.send_message_to_inbox(message, max_retries)

    def get_metrics(self) -> Dict[str, Any]:
        """Get comprehensive metrics for monitoring and reporting."""
        return {
            "success_rate": self.metrics.get_success_rate(),
            "delivery_stats": self.metrics.get_delivery_stats(),
            "message_counts": self.metrics.get_message_counts(),
            "error_summary": self.metrics.get_error_summary(),
            "total_operations": self.metrics.metrics.total_operations,
            "successful_operations": self.metrics.metrics.successful_operations,
            "failed_operations": self.metrics.metrics.failed_operations,
        }

    def send_message_via_pyautogui(self, message: UnifiedMessage, use_paste: bool = True,
                                  new_tab_method: str = "ctrl_t", use_new_tab: bool = None) -> bool:
        """Send message via PyAutoGUI to agent coordinates."""
        if use_new_tab is None:
            use_new_tab = (message.message_type == UnifiedMessageType.ONBOARDING)
        return self.pyautogui_delivery.send_message_via_pyautogui(message, use_paste, new_tab_method, use_new_tab)

    # Onboarding methods
    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for specific agent."""
        return self.onboarding.generate_onboarding_message(agent_id, style)

    def send_onboarding_message(self, agent_id: str, style: str = "friendly",
                               mode: str = "pyautogui", new_tab_method: str = "ctrl_t") -> bool:
        """Send onboarding message to specific agent."""
        success = self.onboarding.send_onboarding_message(agent_id, style, mode, new_tab_method)
        if success:
            self.messages.append(self._get_last_message())
        return success

    def send_bulk_onboarding(self, style: str = "friendly", mode: str = "pyautogui",
                            new_tab_method: str = "ctrl_t") -> List[bool]:
        """Send onboarding messages to all agents."""
        return self.onboarding.send_bulk_onboarding(style, mode, new_tab_method)

    # Bulk messaging methods
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
        success = self.bulk.send_message(content, sender, recipient, message_type, priority,
                                       tags, metadata, mode, use_paste, new_tab_method, use_new_tab)
        if success:
            self.messages.append(self._get_last_message())
        return success

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
        return self.bulk.send_to_all_agents(content, sender, message_type, priority,
                                          tags, metadata, mode, use_paste, new_tab_method, use_new_tab)

    # Utility methods
    def list_agents(self):
        """List all available agents."""
        self.utils.list_agents()

    def show_coordinates(self):
        """Show agent coordinates."""
        self.utils.show_coordinates()

    def show_message_history(self):
        """Show message history."""
        self.utils.show_message_history()

    def _get_last_message(self) -> UnifiedMessage:
        """Helper to get the most recently created message."""
        # This is a simplified helper - in practice, the message would be tracked
        return self.messages[-1] if self.messages else None
