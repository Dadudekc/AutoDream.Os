"""Cross-system messaging interface."""

from abc import ABC, abstractmethod


class ICrossSystemMessaging(ABC):
    """Interface for cross-system communication."""

    @abstractmethod
    async def send_cross_system_message(
        self, target_system: str, message_content: str, protocol: str
    ) -> bool:
        """Send a message using cross-system communication protocols."""
        raise NotImplementedError(
            "send_cross_system_message must be implemented by subclasses"
        )
