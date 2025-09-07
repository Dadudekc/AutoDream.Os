from typing import Any
import logging

from ...services.messaging.models.v2_message import V2Message
from .channels import Channel, ChannelType
from __future__ import annotations


"""Message routing utilities for the communication system."""



logger = logging.getLogger(__name__)


class MessageRouter:
    """Route messages to the proper protocol adapter."""

    def __init__(self, http_adapter, https_adapter, websocket_adapter) -> None:
        self.http_adapter = http_adapter
        self.https_adapter = https_adapter
        self.websocket_adapter = websocket_adapter

    async def route(self, channel: Channel, message: V2Message) -> bool:
        """Send *message* through *channel* using the correct adapter.

        Returns True if the message was sent successfully.
        """
        try:
            if channel.type == ChannelType.HTTP:
                return await self.http_adapter.send(channel, message)
            if channel.type == ChannelType.HTTPS:
                return await self.https_adapter.send(channel, message)
            if channel.type == ChannelType.WEBSOCKET:
                return await self.websocket_adapter.send(channel.id, message.content)
            logger.warning("Unsupported channel type: %s", channel.type)
            return False
        except Exception as exc:
            logger.error("Routing failure for channel %s: %s", channel.id, exc)
            return False
