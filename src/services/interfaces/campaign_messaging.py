"""Campaign messaging interface."""

from abc import ABC, abstractmethod
from typing import Dict


class ICampaignMessaging(ABC):
    """Interface for campaign messaging operations."""

    @abstractmethod
    def send_campaign_message(
        self, message_content: str, campaign_type: str
    ) -> Dict[str, bool]:
        """Send a campaign message to all agents."""
        raise NotImplementedError(
            "send_campaign_message must be implemented by subclasses"
        )
