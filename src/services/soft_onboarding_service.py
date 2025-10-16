"""
Soft Onboarding Service - Wrapper for Unified Onboarding
=========================================================

Provides backward compatibility and simplified interface.
Delegates to handlers and unified onboarding service.

V2 Compliance: Wrapper pattern, <400 lines
"""

import logging

logger = logging.getLogger(__name__)


class SoftOnboardingService:
    """Soft onboarding service - delegates to handler."""

    def __init__(self):
        """Initialize soft onboarding service."""
        from .handlers.soft_onboarding_handler import SoftOnboardingHandler

        self.handler = SoftOnboardingHandler()
        logger.info("SoftOnboardingService initialized")

    def onboard_agent(self, agent_id: str, message: str, **kwargs) -> bool:
        """
        Execute soft onboarding for an agent.

        Args:
            agent_id: Target agent ID
            message: Onboarding message
            **kwargs: Additional options

        Returns:
            True if successful
        """
        try:
            # Delegate to handler
            class Args:
                def __init__(self, agent_id, message, **kwargs):
                    self.agent = agent_id
                    self.message = message
                    self.__dict__.update(kwargs)

            args = Args(agent_id, message, **kwargs)
            return self.handler.handle(args)
        except Exception as e:
            logger.error(f"Soft onboarding failed: {e}")
            return False


def soft_onboard_agent(agent_id: str, message: str, **kwargs) -> bool:
    """
    Convenience function for soft onboarding.

    Args:
        agent_id: Target agent ID
        message: Onboarding message
        **kwargs: Additional options

    Returns:
        True if successful
    """
    service = SoftOnboardingService()
    return service.onboard_agent(agent_id, message, **kwargs)
