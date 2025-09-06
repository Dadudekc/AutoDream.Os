#!/usr/bin/env python3
"""
Messaging Onboarding Module - Agent Cellphone V2
===============================================

Onboarding functionality for the messaging service.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, List, Optional

from ..models.messaging_models import (
    RecipientType,
    SenderType,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)


class MessagingOnboarding:
    """Handles onboarding message generation and delivery."""

    def __init__(self, agents: dict, pyautogui_delivery: PyAutoGUIMessagingDelivery):
        """Initialize onboarding service."""
        self.agents = agents
        self.pyautogui_delivery = pyautogui_delivery
        self.onboarding_service = OnboardingService()

    def generate_onboarding_message(
        self, agent_id: str, style: str = "friendly"
    ) -> str:
        """Generate onboarding message for specific agent using onboarding service."""
        # Get role from agent status.json file for accuracy
        role = self._get_agent_role_from_status(agent_id)
        return self.onboarding_service.generate_onboarding_message(
            agent_id, role, style
        )

    def _get_agent_role_from_status(self, agent_id: str) -> str:
        """Get agent role from their status.json file."""

        status_file = f"agent_workspaces/{agent_id}/status.json"
        if get_unified_utility().path.exists(status_file):
            try:
                with open(status_file, "r") as f:
                    status_data = read_json(f)
                    # Extract role from agent_name field
                    agent_name = status_data.get("agent_name", "")
                    if "Web Development Specialist" in agent_name:
                        return "Web Development Specialist - Comprehensive Testing & Quality Assurance Execution"
                    elif "Business Intelligence" in agent_name:
                        return "Business Intelligence Specialist"
                    # Add more role mappings as needed
            except Exception:
                pass

        # Fallback to agent configuration
        agent_info = self.agents.get(agent_id, {})
        return agent_info.get("description", "Specialist")

    def send_onboarding_message(
        self,
        agent_id: str,
        style: str = "friendly",
        mode: str = "pyautogui",
        new_tab_method: str = "ctrl_t",
    ) -> bool:
        """Send onboarding message to specific agent."""
        message_content = self.generate_onboarding_message(agent_id, style)

        message = UnifiedMessage(
            content=message_content,
            sender="Captain Agent-4",
            recipient=agent_id,
            message_type=UnifiedMessageType.S2A,  # System-to-Agent message
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.CAPTAIN, UnifiedMessageTag.ONBOARDING],
            metadata={"onboarding_style": style, "message_category": "S2A_ONBOARDING"},
            sender_type=SenderType.SYSTEM,
            recipient_type=RecipientType.AGENT,
        )

        get_logger(__name__).info(
            f"✅ ONBOARDING MESSAGE CREATED: Captain Agent-4 → {agent_id}"
        )
        get_logger(__name__).info(f"🎯 Style: {style}")
        get_logger(__name__).info(f"🆔 Message ID: {message.message_id}")

        # Deliver the message
        delivery_success = False
        if mode == "pyautogui":
            delivery_success = self.pyautogui_delivery.send_message_via_pyautogui(
                message, use_paste=True, new_tab_method=new_tab_method
            )
        else:
            # For inbox mode, delivery will be handled by main core
            delivery_success = False  # Placeholder

        if delivery_success:
            get_logger(__name__).info(f"✅ ONBOARDING MESSAGE DELIVERED TO {agent_id}")
        else:
            get_logger(__name__).info(
                f"❌ ONBOARDING MESSAGE DELIVERY FAILED TO {agent_id}"
            )

        get_logger(__name__).info()
        return delivery_success

    def send_bulk_onboarding(
        self,
        style: str = "friendly",
        mode: str = "pyautogui",
        new_tab_method: str = "ctrl_t",
    ) -> List[bool]:
        """Send onboarding messages to all agents."""
        results = []
        get_logger(__name__).info(
            f"🚨 BULK ONBOARDING ACTIVATED - {style.upper()} MODE"
        )
        get_logger(__name__).info(f"📋 CORRECT ORDER: Agent-4 will be onboarded LAST")

        # CORRECT ORDER: Agent-4 LAST
        agent_order = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
            "Agent-4",
        ]

        for agent_id in agent_order:
            success = self.send_onboarding_message(
                agent_id, style, mode, new_tab_method
            )
            results.append(success)

            time.sleep(1)  # Brief pause between agents

        success_count = sum(results)
        total_count = len(results)
        get_logger(__name__).info(
            f"📊 BULK ONBOARDING COMPLETED: {success_count}/{total_count} successful"
        )
        return results
