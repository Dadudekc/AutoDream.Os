#!/usr/bin/env python3
"""
Soft Onboarding Service
=======================

Service layer for soft onboarding operations.
Delegates to SoftOnboardingHandler for actual execution.

Author: Agent-8 (SSOT & System Integration Specialist)
Created: 2025-10-16 (Quarantine Phase 2 fix)
Mission: Fix missing service - 300 pts
License: MIT
"""

from .handlers.soft_onboarding_handler import SoftOnboardingHandler
from .unified_onboarding_service import UnifiedOnboardingService


class SoftOnboardingService:
    """Soft onboarding service - session cleanup and preparation."""

    def __init__(self):
        """Initialize soft onboarding service."""
        self.handler = SoftOnboardingHandler()
        self.unified = UnifiedOnboardingService()

    def onboard_agent(self, agent_id: str, message: str, **kwargs) -> dict:
        """
        Execute soft onboarding for agent.

        Args:
            agent_id: Agent identifier (e.g., "Agent-7")
            message: Onboarding message
            **kwargs: Additional options

        Returns:
            dict with onboarding result
        """
        return self.handler.handle_soft_onboarding(agent_id, message, **kwargs)

    def prepare_session(self, agent_id: str) -> dict:
        """Prepare agent session for soft onboarding."""
        return self.unified.prepare_soft_onboarding(agent_id)

    def cleanup_previous_session(self, agent_id: str) -> dict:
        """Clean up previous agent session."""
        return self.unified.cleanup_session(agent_id)


__all__ = ["SoftOnboardingService"]

