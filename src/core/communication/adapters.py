"""Network and protocol adapters for communication channels."""
from typing import Any, Dict, Optional

import json

try:  # optional dependency
    import aiohttp
    from aiohttp import ClientSession
except Exception:  # pragma: no cover - falls back to dummy implementations
    aiohttp = None
    ClientSession = None

import ssl
try:  # optional dependency
    import certifi
except Exception:  # pragma: no cover
    certifi = None

try:  # optional dependency
    import websockets
except Exception:  # pragma: no cover
    websockets = None

from .channels import Channel
from ...services.messaging.models.v2_message import V2Message


class HTTPAdapter:
    """Adapter for sending HTTP messages."""

    def __init__(self) -> None:
        self.session: Optional[ClientSession] = None

    async def send(self, channel: Channel, message: V2Message) -> bool:
        if aiohttp is None:
            return False
        try:
            if self.session is None:
                self.session = aiohttp.ClientSession()
            async with self.session.post(
                f"{channel.url}/message",
                json=message.content,
                headers=message.headers,
                timeout=aiohttp.ClientTimeout(total=message.timeout),
            ) as response:
                return response.status == 200
        except Exception:
            return False

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()


class HTTPSAdapter(HTTPAdapter):
    """Adapter for sending HTTPS messages with SSL."""

    async def send(self, channel: Channel, message: V2Message) -> bool:
        if aiohttp is None:
            return False
        if self.session is None:
            if certifi is not None:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
            else:  # pragma: no cover - fallback without certifi
                ssl_context = ssl.create_default_context()
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            self.session = aiohttp.ClientSession(connector=connector)
        return await super().send(channel, message)


class WebSocketAdapter:
    """Adapter for WebSocket connections."""

    def __init__(self) -> None:
        self.connections: Dict[str, Any] = {}

    async def connect(self, channel: Channel) -> None:
        if websockets is None:
            return
        websocket = await websockets.connect(
            channel.url,
            extra_headers=channel.config.get("headers", {}),
            ping_interval=channel.config.get("ping_interval", 30),
            ping_timeout=channel.config.get("ping_timeout", 10),
        )
        self.connections[channel.id] = websocket

    async def send(self, channel_id: str, data: Any) -> bool:
        websocket = self.connections.get(channel_id)
        if not websocket or websockets is None:
            return False
        try:
            if isinstance(data, (dict, list)):
                data = json.dumps(data)
            await websocket.send(data)
            return True
        except Exception:
            return False

    async def close(self, channel_id: str) -> None:
        websocket = self.connections.pop(channel_id, None)
        if websocket:
            await websocket.close()
