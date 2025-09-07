"""YOLO activation messaging interface."""

from abc import ABC, abstractmethod
from typing import Dict


class IYOLOMessaging(ABC):
    """Interface for YOLO automatic activation messaging."""

    @abstractmethod
    def activate_yolo_mode(self, message_content: str) -> Dict[str, bool]:
        """Activate YOLO mode with automatic agent activation."""
        raise NotImplementedError(
            "activate_yolo_mode must be implemented by subclasses"
        )
