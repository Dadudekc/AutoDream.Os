"""
Onboarding Message Generator - V2 Compliance Module
==================================================

Generates customized onboarding messages following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from .architectural_models import ArchitecturalPrinciple, ArchitecturalGuidance


class OnboardingMessageGenerator:
    """Generates customized onboarding messages for agents."""

    def __init__(self, principle_definitions: dict[ArchitecturalPrinciple, ArchitecturalGuidance]):
        """Initialize message generator."""
        self.principle_definitions = principle_definitions

    def create_onboarding_message(self, agent_id: str, principle: ArchitecturalPrinciple) -> str:
        """Create a customized onboarding message for an agent."""
        if not principle:
            return f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM."

        guidance = self.principle_definitions.get(principle)
        if not guidance:
            return f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM."

        message = f"""
🎯 **ARCHITECTURAL ONBOARDING - {guidance.display_name}**

Welcome to the team, {agent_id}! You are now part of the V2 SWARM.

**Your Architectural Responsibility:**
{guidance.description}

**Key Responsibilities:**
{chr(10).join(f"• {resp}" for resp in guidance.responsibilities[:3])}

**Validation Rules:**
{chr(10).join(f"• {rule}" for rule in guidance.validation_rules[:3])}

**Remember:** Your work will be validated against these architectural principles.
Every commit will be reviewed for compliance with {principle.value} standards.

Welcome aboard! Let's build something architecturally sound! 🚀
        """.strip()

        return message

    def create_welcome_message(self, agent_id: str) -> str:
        """Create a basic welcome message for agents without specific assignments."""
        return f"Welcome to the team, {agent_id}! You are now part of the V2 SWARM."

    def create_principle_summary_message(self, principle: ArchitecturalPrinciple) -> str:
        """Create a summary message for a specific principle."""
        guidance = self.principle_definitions.get(principle)
        if not guidance:
            return f"Principle: {principle.value}"

        return f"""
📋 **{guidance.display_name}**

{guidance.description}

**Quick Guidelines:**
{chr(10).join(f"• {guideline}" for guideline in guidance.guidelines[:3])}
        """.strip()
