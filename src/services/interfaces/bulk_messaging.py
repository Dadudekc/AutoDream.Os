"""Bulk messaging interface."""

from abc import ABC, abstractmethod
from typing import Dict


class IBulkMessaging(ABC):
    """Interface for bulk messaging operations."""

    @abstractmethod
    def send_bulk_messages(
        self, messages: Dict[str, str], mode: str
    ) -> Dict[str, bool]:
        """Send messages to multiple agents."""
        raise NotImplementedError(
            "send_bulk_messages must be implemented by subclasses"
        )
