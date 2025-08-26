"""Example implementation of BaseMiddlewareComponent."""

from typing import Any, Dict

from src.services.middleware_orchestrator import BaseMiddlewareComponent, DataPacket


class ExampleMiddleware(BaseMiddlewareComponent):
    """Middleware that echoes the data packet without modification."""

    async def process(
        self, data_packet: DataPacket, context: Dict[str, Any]
    ) -> DataPacket:
        return data_packet
