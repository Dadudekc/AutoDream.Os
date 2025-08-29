"""Base abstractions for middleware components."""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models import DataPacket, MiddlewareType


class BaseMiddlewareComponent(ABC):
    """Abstract base class for all middleware components."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.name = self.__class__.__name__
        self.middleware_type = self.config.get("type", MiddlewareType.PROCESSING)
        self.enabled = self.config.get("enabled", True)
        self.priority = self.config.get("priority", 0)
        self.conditions = self.config.get("conditions", {})

        # Performance metrics
        self.processed_count = 0
        self.error_count = 0
        self.total_processing_time = 0.0
        self.last_processed: Optional[float] = None

    @abstractmethod
    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        """Process the data packet and return a modified packet.

        Subclasses must implement their core processing logic. Implementations
        may mutate ``data_packet`` in place and should return the packet instance
        that will be passed to subsequent middleware components.
        """

    def should_process(self, data_packet: DataPacket, context: Dict[str, Any]) -> bool:
        """Determine if this middleware should process the given packet."""
        if not self.enabled:
            return False

        # Check conditions
        for key, value in self.conditions.items():
            if key in data_packet.metadata:
                if data_packet.metadata[key] != value:
                    return False
            elif key in data_packet.tags:
                if value not in data_packet.tags:
                    return False
            else:
                return False

        return True

    def update_metrics(self, processing_time: float, success: bool = True) -> None:
        """Update performance metrics."""
        self.processed_count += 1
        if not success:
            self.error_count += 1
        self.total_processing_time += processing_time
        self.last_processed = time.time()

    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        avg_time = (
            self.total_processing_time / self.processed_count
            if self.processed_count > 0
            else 0
        )

        return {
            "name": self.name,
            "type": self.middleware_type.value,
            "enabled": self.enabled,
            "processed_count": self.processed_count,
            "error_count": self.error_count,
            "total_processing_time": self.total_processing_time,
            "average_processing_time": avg_time,
            "last_processed": self.last_processed,
            "success_rate": (
                (self.processed_count - self.error_count) / self.processed_count
                if self.processed_count > 0
                else 0
            ),
        }
