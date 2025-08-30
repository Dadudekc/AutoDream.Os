"""Onboarding messaging interface."""

from abc import ABC, abstractmethod

from .enums import MessageType


class IOnboardingMessaging(ABC):
    """Interface for agent onboarding messaging."""

    @abstractmethod
    def send_onboarding_message(
        self, agent_id: str, onboarding_type: MessageType, content: str
    ) -> bool:
        """Send an onboarding message to a new agent."""
        raise NotImplementedError(
            "send_onboarding_message must be implemented by subclasses"
        )
