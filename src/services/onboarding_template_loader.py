#!/usr/bin/env python3
"""
Onboarding Template Loader
===========================

Loads the full onboarding template from prompts/agents/onboarding.md
and merges it with custom mission details.

This ensures agents receive:
- Operating cycle duties
- Expected workflow loop
- Actionable results requirements
- Critical communication protocols
- All standard onboarding procedures

V2 Compliance: <300 lines
Author: Captain Agent-4 - Fixing Onboarding Template System
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class OnboardingTemplateLoader:
    """Loads and merges onboarding templates."""

    def __init__(self):
        """Initialize template loader."""
        self.project_root = Path(__file__).resolve().parents[2]
        self.template_path = self.project_root / "prompts" / "agents" / "onboarding.md"

    def load_full_template(self) -> str:
        """Load the full onboarding template with operating cycle duties."""
        try:
            if not self.template_path.exists():
                logger.warning(f"Template not found: {self.template_path}")
                return ""

            with open(self.template_path, encoding="utf-8") as f:
                template = f.read()

            logger.info(f"✅ Loaded full onboarding template ({len(template)} chars)")
            return template

        except Exception as e:
            logger.error(f"Error loading template: {e}")
            return ""

    def create_onboarding_message(
        self, agent_id: str, role: str, custom_message: str = "", contract_info: str = ""
    ) -> str:
        """
        Create complete onboarding message by merging template + custom content.

        Args:
            agent_id: Agent ID (e.g., "Agent-1")
            role: Agent role (e.g., "Integration & Core Systems Specialist")
            custom_message: Custom mission/instructions
            contract_info: Optional contract details

        Returns:
            Complete onboarding message with template + custom content
        """
        # Load full template
        template = self.load_full_template()

        if not template:
            # Fallback to custom message only if template missing
            logger.warning("Using custom message only (template missing)")
            return self._format_custom_message(agent_id, role, custom_message)

        # Replace placeholders in template
        message = template.replace("{agent_id}", agent_id)
        message = message.replace("{role}", role)
        message = message.replace(
            "{contract_info}", contract_info or "See custom instructions below"
        )
        message = message.replace(
            "{custom_message}", custom_message or "No additional instructions"
        )

        logger.info(f"✅ Created full onboarding message for {agent_id} ({len(message)} chars)")
        return message

    def _format_custom_message(self, agent_id: str, role: str, custom_message: str) -> str:
        """Fallback: Format custom message if template missing."""
        return f"""🚨 AGENT IDENTITY CONFIRMATION: You are {agent_id} - {role} 🚨

🎯 YOUR MISSION:
{custom_message}

📋 IMPORTANT: Full onboarding template not loaded. 
Please reference docs/ONBOARDING_GUIDE.md for complete procedures.

🐝 WE. ARE. SWARM. ⚡
"""


def load_onboarding_template(
    agent_id: str, role: str, custom_message: str = "", contract_info: str = ""
) -> str:
    """
    Convenience function to load complete onboarding message.

    Usage:
        message = load_onboarding_template(
            agent_id="Agent-1",
            role="Integration & Core Systems Specialist",
            custom_message="Your specific mission details here"
        )
    """
    loader = OnboardingTemplateLoader()
    return loader.create_onboarding_message(agent_id, role, custom_message, contract_info)


if __name__ == "__main__":
    # Test template loading
    loader = OnboardingTemplateLoader()
    template = loader.load_full_template()
    print(f"Template loaded: {len(template)} characters")
    print(f"Template path: {loader.template_path}")

    # Test message creation
    message = load_onboarding_template(
        agent_id="Agent-1",
        role="Integration & Core Systems Specialist",
        custom_message="Execute Vector Integration Consolidation",
    )
    print(f"\nFull message: {len(message)} characters")
    print(f"Includes cycle duties: {'AGENT CYCLE SYSTEM' in message}")
    print(f"Includes workflow loop: {'EXPECTED AGENT WORKFLOW' in message}")
