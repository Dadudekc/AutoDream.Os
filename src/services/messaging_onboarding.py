#!/usr/bin/env python3
"""
Messaging Onboarding Module - Agent Cellphone V2
===============================================

Onboarding functionality for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import List

from .models.messaging_models import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
from .onboarding_service import OnboardingService
from .messaging_pyautogui import PyAutoGUIMessagingDelivery


class MessagingOnboarding:
    """Handles onboarding message generation and delivery."""

    def __init__(self, agents: dict, pyautogui_delivery: PyAutoGUIMessagingDelivery):
        """Initialize onboarding service."""
        self.agents = agents
        self.pyautogui_delivery = pyautogui_delivery
        self.onboarding_service = OnboardingService()

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

        print(f"✅ ONBOARDING MESSAGE CREATED: Captain Agent-4 → {agent_id}")
        print(f"🎯 Style: {style}")
        print(f"🆔 Message ID: {message.message_id}")

        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.pyautogui_delivery.send_message_via_pyautogui(message, use_paste=True, new_tab_method=new_tab_method)
        else:
            # For inbox mode, delivery will be handled by main core
            delivery_success = False  # Placeholder

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
            import time
            time.sleep(1)  # Brief pause between agents

        success_count = sum(results)
        total_count = len(results)
        print(f"📊 BULK ONBOARDING COMPLETED: {success_count}/{total_count} successful")
        return results
