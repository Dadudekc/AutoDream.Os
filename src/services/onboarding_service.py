#!/usr/bin/env python3
"""
Onboarding Service Implementation - V2 Compliant Module
=======================================================

Concrete implementation of IOnboardingService protocol.
V2 Compliance: < 200 lines, single responsibility.

Author: V2 Implementation Team
License: MIT
"""

from typing import Dict, Any
import logging

from .onboarding_handler import OnboardingHandler

logger = logging.getLogger(__name__)


class OnboardingService:
    """Concrete implementation of IOnboardingService protocol."""

    def __init__(self):
        """Initialize onboarding service."""
        self.logger = logger
        self.onboarding_handler = OnboardingHandler()
        self.logger.info("OnboardingService initialized")

    def generate_onboarding_message(self, agent_id: str, style: str = "friendly") -> str:
        """Generate onboarding message for an agent.

        Args:
            agent_id: Agent ID to generate message for
            style: Message style (friendly, professional, technical)

        Returns:
            Generated onboarding message content
        """
        try:
            self.logger.info(f"Generating onboarding message for {agent_id} with style: {style}")

            # Get agent status from onboarding handler
            agent_status = self.onboarding_handler.get_onboarding_status(agent_id)

            if agent_status:
                # Agent is already onboarded, generate welcome back message
                return self._generate_welcome_back_message(agent_id, agent_status, style)
            else:
                # Agent is new, generate initial onboarding message
                return self._generate_initial_onboarding_message(agent_id, style)

        except Exception as e:
            self.logger.error(f"Error generating onboarding message for {agent_id}: {e}")
            return f"Hello {agent_id}! Welcome to the V2 Swarm System. There was an error during onboarding setup."

    def _generate_initial_onboarding_message(self, agent_id: str, style: str) -> str:
        """Generate initial onboarding message for new agent."""
        base_message = f"Hello {agent_id}! Welcome to the V2 Swarm System."

        style_templates = {
            "friendly": {
                "greeting": "Hey there!",
                "body": f"{base_message} We're excited to have you join our collaborative team. You'll be working with cutting-edge AI technologies and contributing to innovative projects.",
                "closing": "Let's make some amazing things together! 🚀"
            },
            "professional": {
                "greeting": "Dear Colleague,",
                "body": f"{base_message} As part of our professional development team, you will be responsible for delivering high-quality solutions and maintaining system excellence.",
                "closing": "We look forward to your valuable contributions to our mission."
            },
            "technical": {
                "greeting": "Greetings,",
                "body": f"{base_message} You will be integrated into our distributed processing network. Your primary responsibilities include system optimization, debugging, and maintaining code quality standards.",
                "closing": "System integration complete. Awaiting your first task assignment."
            }
        }

        template = style_templates.get(style, style_templates["friendly"])

        return f"""
{template['greeting']}

{template['body']}

Key responsibilities:
- Execute assigned tasks efficiently
- Maintain communication with the swarm
- Contribute to system improvements
- Follow V2 compliance standards

{template['closing']}

Best regards,
V2 Swarm Captain
"""

    def _generate_welcome_back_message(self, agent_id: str, agent_status: Dict[str, Any], style: str) -> str:
        """Generate welcome back message for existing agent."""
        role = agent_status.get("role", "Specialist")
        onboarded_at = agent_status.get("onboarded_at", "recently")

        style_templates = {
            "friendly": {
                "greeting": f"Welcome back, {agent_id}!",
                "body": f"Great to see you again! As a {role} in our V2 Swarm System, you're already making valuable contributions. Ready to tackle some new challenges?",
                "closing": "Let's continue building amazing things together! 🚀"
            },
            "professional": {
                "greeting": f"Welcome back, {agent_id}.",
                "body": f"As a {role} in our professional development team since {onboarded_at}, you continue to demonstrate excellent performance and dedication to our mission.",
                "closing": "We look forward to your continued contributions."
            },
            "technical": {
                "greeting": f"Agent {agent_id} reconnected.",
                "body": f"System recognizes {role} agent onboarded {onboarded_at}. Agent status: ACTIVE. Ready for task assignment and system integration.",
                "closing": "Awaiting task assignment. System ready."
            }
        }

        template = style_templates.get(style, style_templates["friendly"])

        return f"""
{template['greeting']}

{template['body']}

Current status:
- Role: {role}
- Onboarded: {onboarded_at}
- System Status: ACTIVE

{template['closing']}

Best regards,
V2 Swarm Captain
"""

    def get_service_status(self) -> Dict[str, Any]:
        """Get onboarding service status."""
        try:
            onboarded_agents = self.onboarding_handler.list_onboarded_agents()
            return {
                "service": "onboarding",
                "status": "active",
                "onboarded_agents_count": len(onboarded_agents),
                "onboarded_agents": onboarded_agents
            }
        except Exception as e:
            self.logger.error(f"Error getting service status: {e}")
            return {
                "service": "onboarding",
                "status": "error",
                "error": str(e)
            }


__all__ = ["OnboardingService"]