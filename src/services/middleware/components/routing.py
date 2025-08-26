"""Data routing middleware components."""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

from ..base import BaseMiddlewareComponent
from ..models import DataPacket, MiddlewareType


class RoutingMiddleware(BaseMiddlewareComponent):
    """Middleware for intelligent data routing."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config)
        self.middleware_type = MiddlewareType.ROUTING
        self.routing_rules = self.config.get("routing_rules", {})
        self.default_route = self.config.get("default_route", "default")

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        start_time = time.time()
        success = True

        try:
            route = self._determine_route(data_packet)
            data_packet.metadata["route"] = route
            data_packet.metadata["routed"] = True
            data_packet.tags.add(f"route:{route}")
            if not data_packet.destination:
                data_packet.destination = route
            data_packet.processing_history.append(f"{self.name}:{route}")
        except Exception as exc:  # noqa: BLE001
            success = False
            logger.exception("Error in %s for packet %s", self.name, data_packet.id)
            data_packet.metadata["error"] = f"{type(exc).__name__} in {self.name}"

        processing_time = time.time() - start_time
        self.update_metrics(processing_time, success)
        return data_packet

    def _determine_route(self, data_packet: DataPacket) -> str:
        """Determine the appropriate route for the data packet."""
        for pattern, route in self.routing_rules.items():
            if self._matches_pattern(data_packet, pattern):
                return route
        return self.default_route

    def _matches_pattern(self, data_packet: DataPacket, pattern: str) -> bool:
        """Check if packet matches routing pattern."""
        if pattern.startswith("tag:"):
            tag = pattern[4:]
            return tag in data_packet.tags
        if pattern.startswith("metadata:"):
            key_value = pattern[9:].split("=", 1)
            if len(key_value) == 2:
                key, value = key_value
                return data_packet.metadata.get(key) == value
        if pattern.startswith("source:"):
            source = pattern[7:]
            return data_packet.source == source
        return False
