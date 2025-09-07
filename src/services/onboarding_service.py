#!/usr/bin/env python3
"""
Onboarding Service - Agent Cellphone V2
======================================

Dedicated service for agent onboarding functionality.
Extracted from messaging_core.py to maintain LOC compliance.

Author: V2 SWARM CAPTAIN
License: MIT
"""
from src.services.models.messaging_models import (
    RecipientType,
    SenderType,
    UnifiedMessage,
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
)


class OnboardingService:
    """Dedicated service for agent onboarding operations."""

    def __init__(self):
        """Initialize onboarding service with template."""
        self.onboarding_template = self._load_onboarding_template()

    def _load_onboarding_template(self) -> str:
        """Load onboarding template content from SSOT; provide fallback if missing."""
        template_path = "prompts/agents/onboarding.md"
        try:
            if get_unified_utility().path.exists(template_path):
                with open(template_path, "r", encoding="utf-8") as f:
                    return f.read()
        except Exception as e:
            get_logger(__name__).warning(f"Error loading onboarding template: {e}")
            pass

        # Fallback minimal template to ensure continuity if SSOT missing
        return (
            "🎯 **ONBOARDING - FRIENDLY MODE** 🎯\n\n"
            "**Agent**: {agent_id}\n"
            "**Role**: {role}\n"
            "**Captain**: Agent-4 - Strategic Oversight & Emergency Intervention Manager\n\n"
            "**WELCOME TO THE SWARM!** 🚀\n\n"
            "Use --get-next-task to claim your first contract.\n\n"
            "**WE. ARE. SWARM.** ⚡️🔥"
        )

    def generate_onboarding_message(
        self, agent_id: str, role: str, style: str = "friendly"
    ) -> str:
        """Generate onboarding message for specific agent from SSOT template."""

        class _SafeDict(dict):
            def __missing__(self, key):  # type: ignore[override]
                return ""

        values: Dict[str, Any] = {
            "agent_id": agent_id,
            "role": role,
            "description": role,  # backward compat key if used in templates
            "contract_info": "Use --get-next-task to claim your first contract",
            "custom_message": "",
            "style": style,
        }

        try:
            return self.onboarding_template.format_map(_SafeDict(values))
        except Exception:
            # As an ultimate fallback, return a simple constructed message
            return (
                f"🎯 **ONBOARDING - {style.upper()} MODE** 🎯\n\n"
                f"**Agent**: {agent_id}\n"
                f"**Role**: {role}\n\n"
                "Use --get-next-task to claim your first contract.\n\n"
                "**WE. ARE. SWARM.** ⚡️🔥"
            )

    def create_onboarding_message(
        self, agent_id: str, role: str, style: str = "friendly"
    ) -> UnifiedMessage:
        """Create UnifiedMessage for onboarding."""
        message_content = self.generate_onboarding_message(agent_id, role, style)

        return UnifiedMessage(
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
