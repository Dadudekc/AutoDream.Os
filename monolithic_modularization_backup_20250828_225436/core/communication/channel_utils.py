"""Utility helpers for creating channels and their default statistics."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from .channels import Channel, ChannelType


def create_channel(
    channel_id: str,
    name: str,
    channel_type: ChannelType,
    url: str,
    config: Optional[Dict[str, Any]] = None,
) -> Channel:
    """Create a Channel instance with default metadata.

    Args:
        channel_id: Unique identifier for the channel.
        name: Human readable channel name.
        channel_type: Type of the channel (HTTP, WEBSOCKET, etc.).
        url: Endpoint associated with the channel.
        config: Optional configuration dictionary.

    Returns:
        Configured :class:`~src.core.communication.channels.Channel` object.
    """
    now = datetime.now().isoformat()
    return Channel(
        id=channel_id,
        name=name,
        type=channel_type,
        url=url,
        config=config or {},
        status="active",
        created_at=now,
        last_used=now,
        message_count=0,
        error_count=0,
    )


def default_channel_stats() -> Dict[str, Any]:
    """Return a default statistics dictionary for a channel."""
    now = datetime.now().isoformat()
    return {
        "total_messages": 0,
        "successful_messages": 0,
        "failed_messages": 0,
        "last_activity": now,
        "uptime_percentage": 100.0,
        "average_response_time": 0.0,
        "error_rate": 0.0,
    }
