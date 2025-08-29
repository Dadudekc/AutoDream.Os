from __future__ import annotations

"""Centralized error handling for middleware execution."""

import logging

from .models import DataPacket

logger = logging.getLogger(__name__)


def handle_middleware_error(
    packet: DataPacket,
    middleware_name: str,
    exc: Exception,
) -> None:
    """Handle errors raised by individual middleware components."""
    logger.exception("Error in middleware %s", middleware_name)
    packet.metadata["error"] = f"Error in {middleware_name}: {type(exc).__name__}"
    packet.metadata["failed_middleware"] = middleware_name


def handle_packet_error(packet: DataPacket, exc: Exception) -> DataPacket:
    """Handle errors during overall packet processing."""
    logger.error("Error processing data packet %s: %s", packet.id, exc)
    packet.metadata["error"] = str(exc)
    packet.metadata["processing_failed"] = True
    return packet
