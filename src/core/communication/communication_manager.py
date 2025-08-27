"""Streamlined communication manager coordinating channels and routing."""
from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, Optional

from ...services.messaging.models.v2_message import V2Message
from ...services.messaging.types.v2_message_enums import (
    V2MessageStatus,
    V2MessageType,
)

from .channels import Channel, ChannelType
from .adapters import HTTPAdapter, HTTPSAdapter, WebSocketAdapter

logger = logging.getLogger(__name__)


class CommunicationManager:
    """Coordinate channels and route messages using adapters."""

    def __init__(self) -> None:
        self.channels: Dict[str, Channel] = {}
        self.http_adapter = HTTPAdapter()
        self.https_adapter = HTTPSAdapter()
        self.websocket_adapter = WebSocketAdapter()

    async def create_channel(
        self,
        name: str,
        channel_type: ChannelType,
        url: str,
        config: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Register a new channel and initialise protocol adapters as needed."""
        channel_id = f"{channel_type.value}_{len(self.channels)}"
        channel = Channel(
            id=channel_id,
            name=name,
            type=channel_type,
            url=url,
            config=config or {},
            status="active",
            created_at=datetime.now().isoformat(),
            last_used=datetime.now().isoformat(),
            message_count=0,
            error_count=0,
        )
        self.channels[channel_id] = channel

        if channel.type == ChannelType.WEBSOCKET:
            await self.websocket_adapter.connect(channel)

        logger.info("Created channel %s (%s)", channel_id, channel.type.value)
        return channel_id

    async def send_message(
        self,
        channel_id: str,
        content: Any,
        message_type: V2MessageType = V2MessageType.TASK,
        recipient: str = "all",
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> str:
        """Send message through a channel using the appropriate adapter."""
        channel = self.channels.get(channel_id)
        if not channel:
            logger.warning("Channel not found: %s", channel_id)
            return ""

        message_id = f"outgoing_{channel_id}_{int(datetime.now().timestamp())}"
        message = V2Message(
            message_id=message_id,
            message_type=message_type,
            sender_id="system",
            recipient_id=recipient,
            content=content,
            payload={},
            timestamp=datetime.now(),
            status=V2MessageStatus.PENDING,
            retry_count=0,
            max_retries=channel.config.get("retry_count", 3),
            headers=headers or {},
            timeout=timeout or 30.0,
        )

        success = False
        if channel.type == ChannelType.HTTP:
            success = await self.http_adapter.send(channel, message)
        elif channel.type == ChannelType.HTTPS:
            success = await self.https_adapter.send(channel, message)
        elif channel.type == ChannelType.WEBSOCKET:
            success = await self.websocket_adapter.send(channel_id, message.content)
        else:
            logger.warning("Unsupported channel type: %s", channel.type)

        if success:
            message.status = V2MessageStatus.SENT
            channel.message_count += 1
        else:
            message.status = V2MessageStatus.FAILED
            channel.error_count += 1

        channel.last_used = datetime.now().isoformat()
        return message_id

    async def close(self) -> None:
        """Close any open network resources."""
        await self.http_adapter.close()
        await self.https_adapter.close()
        for cid in list(self.websocket_adapter.connections.keys()):
            await self.websocket_adapter.close(cid)
