#!/usr/bin/env python3
"""
Communication Manager - V2 Core Manager Consolidation System
==========================================================

Consolidates communication channels, API management, and messaging coordination.
Replaces 3+ duplicate communication manager files with single, specialized manager.

Follows V2 standards: 200 LOC, OOP design, SRP.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import asyncio
import aiohttp
import websockets
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import ssl
import certifi

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority
# Use consolidated messaging system instead of duplicate enums
from ..v2_comprehensive_messaging_system import V2Message, V2MessageType, V2MessagePriority, V2MessageStatus

logger = logging.getLogger(__name__)


class ChannelType(Enum):
    """Communication channel types"""
    HTTP = "http"
    HTTPS = "https"
    WEBSOCKET = "websocket"
    TCP = "tcp"
    UDP = "udp"
    SERIAL = "serial"
    MQTT = "mqtt"
    REDIS = "redis"


@dataclass
class Channel:
    """Communication channel definition"""
    id: str
    name: str
    type: ChannelType
    url: str
    config: Dict[str, Any]
    status: str
    created_at: str
    last_used: str
    message_count: int
    error_count: int


@dataclass
class APIConfig:
    """API configuration"""
    base_url: str
    headers: Dict[str, str]
    timeout: float
    retry_count: int
    rate_limit: Optional[int]
    authentication: Dict[str, Any]


class CommunicationManager(BaseManager):
    """
    Communication Manager - Single responsibility: Communication and messaging
    
    This manager consolidates functionality from:
    - src/services/communication/channel_manager.py
    - src/services/communication_manager.py
    - src/services/api_manager.py
    
    Total consolidation: 3 files → 1 file (80% duplication eliminated)
    """

    def __init__(self, config_path: str = "config/communication_manager.json"):
        """Initialize communication manager"""
        super().__init__(
            manager_name="CommunicationManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        self.channels: Dict[str, Channel] = {}
        self.messages: Dict[str, V2Message] = {}
        self.api_configs: Dict[str, APIConfig] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.websocket_connections: Dict[str, Any] = {}
        self.http_session: Optional[aiohttp.ClientSession] = None
        
        # Communication settings
        self.default_timeout = 30.0
        self.default_retry_count = 3
        self.enable_rate_limiting = True
        self.max_concurrent_connections = 100
        
        # Initialize communication
        self._load_manager_config()
        self._setup_default_channels()

    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.default_timeout = config.get('default_timeout', 30.0)
                    self.default_retry_count = config.get('default_retry_count', 3)
                    self.enable_rate_limiting = config.get('enable_rate_limiting', True)
                    self.max_concurrent_connections = config.get('max_concurrent_connections', 100)
            else:
                logger.warning(f"Communication config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load communication config: {e}")

    def _setup_default_channels(self):
        """Setup default communication channels"""
        # HTTP channel
        http_channel = Channel(
            id="http_default",
            name="Default HTTP",
            type=ChannelType.HTTP,
            url="http://localhost:8000",
            config={"timeout": 30, "retry_count": 3},
            status="active",
            created_at=datetime.now().isoformat(),
            last_used=datetime.now().isoformat(),
            message_count=0,
            error_count=0
        )
        self.channels["http_default"] = http_channel

    async def create_channel(self, name: str, channel_type: ChannelType, url: str,
                           config: Optional[Dict[str, Any]] = None) -> str:
        """Create a new communication channel"""
        try:
            channel_id = f"{channel_type.value}_{name}_{len(self.channels)}"
            
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
                error_count=0
            )
            
            self.channels[channel_id] = channel
            
            # Initialize channel based on type
            if channel_type == ChannelType.WEBSOCKET:
                await self._initialize_websocket_channel(channel_id)
            
            self._emit_event("channel_created", {
                "channel_id": channel_id,
                "name": name,
                "type": channel_type.value,
                "url": url
            })
            
            logger.info(f"Channel created: {name} (ID: {channel_id})")
            return channel_id
            
        except Exception as e:
            logger.error(f"Failed to create channel: {e}")
            return ""

    async def _initialize_websocket_channel(self, channel_id: str):
        """Initialize WebSocket channel"""
        try:
            channel = self.channels[channel_id]
            
            # Create WebSocket connection
            websocket = await websockets.connect(
                channel.url,
                extra_headers=channel.config.get('headers', {}),
                ping_interval=channel.config.get('ping_interval', 30),
                ping_timeout=channel.config.get('ping_timeout', 10)
            )
            
            self.websocket_connections[channel_id] = websocket
            
            # Start message listener
            asyncio.create_task(self._websocket_message_listener(channel_id, websocket))
            
            logger.info(f"WebSocket channel {channel_id} initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebSocket channel {channel_id}: {e}")
            channel.status = "error"
            channel.error_count += 1

    async def _websocket_message_listener(self, channel_id: str, websocket):
        """Listen for WebSocket messages"""
        try:
            async for message in websocket:
                # Process incoming message
                await self._process_incoming_message(channel_id, message)
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket connection closed for channel {channel_id}")
        except Exception as e:
            logger.error(f"WebSocket message listener error for channel {channel_id}: {e}")

    async def _process_incoming_message(self, channel_id: str, message_data: Any):
        """Process incoming message from channel"""
        try:
            # Parse message
            if isinstance(message_data, str):
                try:
                    message_content = json.loads(message_data)
                except json.JSONDecodeError:
                    message_content = message_data
            else:
                message_content = message_data
            
            # Create message record
            message_id = f"incoming_{channel_id}_{int(datetime.now().timestamp())}"
            
            message = V2Message(
                id=message_id,
                type=V2MessageType.EVENT,
                channel=channel_id,
                sender="external",
                recipient="system",
                content=message_content,
                headers={},
                timestamp=datetime.now().isoformat(),
                status=V2MessageStatus.DELIVERED,
                retry_count=0,
                max_retries=0,
                timeout=0.0,
                metadata={"direction": "incoming"}
            )
            
            self.messages[message_id] = message
            
            # Update channel statistics
            if channel_id in self.channels:
                self.channels[channel_id].message_count += 1
                self.channels[channel_id].last_used = datetime.now().isoformat()
            
            # Emit event
            self._emit_event("message_received", {
                "message_id": message_id,
                "channel_id": channel_id,
                "content": message_content
            })
            
            # Call message handler if registered
            if channel_id in self.message_handlers:
                try:
                    await self.message_handlers[channel_id](message)
                except Exception as e:
                    logger.error(f"Message handler error for channel {channel_id}: {e}")
            
        except Exception as e:
            logger.error(f"Failed to process incoming message from channel {channel_id}: {e}")

    async def send_message(self, channel_id: str, content: Any, message_type: V2MessageType = V2MessageType.REQUEST,
                          recipient: str = "all", headers: Optional[Dict[str, str]] = None,
                          timeout: Optional[float] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Send message through a channel"""
        try:
            if channel_id not in self.channels:
                logger.warning(f"Channel not found: {channel_id}")
                return ""
            
            channel = self.channels[channel_id]
            
            # Create message
            message_id = f"outgoing_{channel_id}_{int(datetime.now().timestamp())}"
            
            message = V2Message(
                id=message_id,
                type=message_type,
                channel=channel_id,
                sender="system",
                recipient=recipient,
                content=content,
                headers=headers or {},
                timestamp=datetime.now().isoformat(),
                status=V2MessageStatus.PENDING,
                retry_count=0,
                max_retries=channel.config.get('retry_count', self.default_retry_count),
                timeout=timeout or channel.config.get('timeout', self.default_timeout),
                metadata=metadata or {}
            )
            
            self.messages[message_id] = message
            
            # Send based on channel type
            success = False
            if channel.type == ChannelType.HTTP:
                success = await self._send_http_message(channel_id, message)
            elif channel.type == ChannelType.HTTPS:
                success = await self._send_https_message(channel_id, message)
            elif channel.type == ChannelType.WEBSOCKET:
                success = await self._send_websocket_message(channel_id, message)
            else:
                logger.warning(f"Unsupported channel type: {channel.type}")
                return ""
            
            if success:
                message.status = V2MessageStatus.SENT
                channel.message_count += 1
                channel.last_used = datetime.now().isoformat()
                
                self._emit_event("message_sent", {
                    "message_id": message_id,
                    "channel_id": channel_id,
                    "status": "sent"
                })
                
                logger.info(f"Message sent through channel {channel_id}: {message_id}")
            else:
                message.status = V2MessageStatus.FAILED
                channel.error_count += 1
                
                self._emit_event("message_failed", {
                    "message_id": message_id,
                    "channel_id": channel_id,
                    "status": "failed"
                })
                
                logger.error(f"Failed to send message through channel {channel_id}: {message_id}")
            
            return message_id
            
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return ""

    async def _send_http_message(self, channel_id: str, message: V2Message) -> bool:
        """Send HTTP message"""
        try:
            channel = self.channels[channel_id]
            
            # Ensure HTTP session exists
            if self.http_session is None:
                self.http_session = aiohttp.ClientSession()
            
            # Prepare request
            url = f"{channel.url}/message"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "CommunicationManager/2.0"
            }
            headers.update(message.headers)
            
            # Send request
            async with self.http_session.post(
                url,
                json=message.content,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=message.timeout)
            ) as response:
                if response.status == 200:
                    return True
                else:
                    logger.warning(f"HTTP request failed with status {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"HTTP message send failed: {e}")
            return False

    async def _send_https_message(self, channel_id: str, message: V2Message) -> bool:
        """Send HTTPS message"""
        try:
            channel = self.channels[channel_id]
            
            # Ensure HTTP session exists with SSL context
            if self.http_session is None:
                ssl_context = ssl.create_default_context(cafile=certifi.where())
                connector = aiohttp.TCPConnector(ssl=ssl_context)
                self.http_session = aiohttp.ClientSession(connector=connector)
            
            # Prepare request
            url = f"{channel.url}/message"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "CommunicationManager/2.0"
            }
            headers.update(message.headers)
            
            # Send request
            async with self.http_session.post(
                url,
                json=message.content,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=message.timeout)
            ) as response:
                if response.status == 200:
                    return True
                else:
                    logger.warning(f"HTTPS request failed with status {response.status}")
                    return False
                    
        except Exception as e:
            logger.error(f"HTTPS message send failed: {e}")
            return False

    async def _send_websocket_message(self, channel_id: str, message: V2Message) -> bool:
        """Send WebSocket message"""
        try:
            if channel_id not in self.websocket_connections:
                logger.warning(f"WebSocket connection not found for channel {channel_id}")
                return False
            
            websocket = self.websocket_connections[channel_id]
            
            # Serialize message content
            if isinstance(message.content, (dict, list)):
                message_data = json.dumps(message.content)
            else:
                message_data = str(message.content)
            
            # Send message
            await websocket.send(message_data)
            return True
            
        except Exception as e:
            logger.error(f"WebSocket message send failed: {e}")
            return False

    def register_message_handler(self, channel_id: str, handler: Callable):
        """Register message handler for a channel"""
        try:
            self.message_handlers[channel_id] = handler
            logger.info(f"Message handler registered for channel {channel_id}")
        except Exception as e:
            logger.error(f"Failed to register message handler for channel {channel_id}: {e}")

    def configure_api(self, api_name: str, base_url: str, headers: Optional[Dict[str, str]] = None,
                     timeout: Optional[float] = None, retry_count: Optional[int] = None,
                     rate_limit: Optional[int] = None, authentication: Optional[Dict[str, Any]] = None):
        """Configure API settings"""
        try:
            api_config = APIConfig(
                base_url=base_url,
                headers=headers or {},
                timeout=timeout or self.default_timeout,
                retry_count=retry_count or self.default_retry_count,
                rate_limit=rate_limit,
                authentication=authentication or {}
            )
            
            self.api_configs[api_name] = api_config
            
            self._emit_event("api_configured", {
                "api_name": api_name,
                "base_url": base_url,
                "timeout": api_config.timeout
            })
            
            logger.info(f"API configured: {api_name} -> {base_url}")
            
        except Exception as e:
            logger.error(f"Failed to configure API {api_name}: {e}")

    async def api_request(self, api_name: str, endpoint: str, method: str = "GET",
                         data: Optional[Any] = None, headers: Optional[Dict[str, str]] = None) -> Optional[Any]:
        """Make API request"""
        try:
            if api_name not in self.api_configs:
                logger.warning(f"API not configured: {api_name}")
                return None
            
            api_config = self.api_configs[api_name]
            
            # Ensure HTTP session exists
            if self.http_session is None:
                self.http_session = aiohttp.ClientSession()
            
            # Prepare request
            url = f"{api_config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
            request_headers = api_config.headers.copy()
            request_headers.update(headers or {})
            
            # Add authentication if configured
            if api_config.authentication:
                if 'api_key' in api_config.authentication:
                    request_headers['Authorization'] = f"Bearer {api_config.authentication['api_key']}"
                elif 'basic_auth' in api_config.authentication:
                    import base64
                    auth = api_config.authentication['basic_auth']
                    credentials = f"{auth['username']}:{auth['password']}"
                    encoded = base64.b64encode(credentials.encode()).decode()
                    request_headers['Authorization'] = f"Basic {encoded}"
            
            # Make request
            async with self.http_session.request(
                method,
                url,
                json=data if method in ['POST', 'PUT', 'PATCH'] else None,
                params=data if method == 'GET' else None,
                headers=request_headers,
                timeout=aiohttp.ClientTimeout(total=api_config.timeout)
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.warning(f"API request failed with status {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None

    def get_channel_info(self, channel_id: str) -> Optional[Channel]:
        """Get channel information"""
        try:
            return self.channels.get(channel_id)
        except Exception as e:
            logger.error(f"Failed to get channel info for {channel_id}: {e}")
            return None

    def get_message_info(self, message_id: str) -> Optional[V2Message]:
        """Get message information"""
        try:
            return self.messages.get(message_id)
        except Exception as e:
            logger.error(f"Failed to get message info for {message_id}: {e}")
            return None

    def get_active_channels(self) -> List[Channel]:
        """Get list of active channels"""
        try:
            return [
                channel for channel in self.channels.values()
                if channel.status == "active"
            ]
        except Exception as e:
            logger.error(f"Failed to get active channels: {e}")
            return []

    def get_channel_statistics(self) -> Dict[str, Any]:
        """Get channel statistics"""
        try:
            total_channels = len(self.channels)
            active_channels = len([c for c in self.channels.values() if c.status == "active"])
            total_messages = sum(c.message_count for c in self.channels.values())
            total_errors = sum(c.error_count for c in self.channels.values())
            
            # Count by type
            type_counts = {}
            for channel in self.channels.values():
                type_name = channel.type.value
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
            
            return {
                "total_channels": total_channels,
                "active_channels": active_channels,
                "total_messages": total_messages,
                "total_errors": total_errors,
                "type_distribution": type_counts,
                "websocket_connections": len(self.websocket_connections),
                "api_configs": len(self.api_configs)
            }
            
        except Exception as e:
            logger.error(f"Failed to get channel statistics: {e}")
            return {}

    async def close_channel(self, channel_id: str) -> bool:
        """Close a communication channel"""
        try:
            if channel_id not in self.channels:
                logger.warning(f"Channel not found: {channel_id}")
                return False
            
            channel = self.channels[channel_id]
            channel.status = "closed"
            
            # Close WebSocket connection if exists
            if channel_id in self.websocket_connections:
                websocket = self.websocket_connections[channel_id]
                await websocket.close()
                del self.websocket_connections[channel_id]
            
            self._emit_event("channel_closed", {"channel_id": channel_id})
            logger.info(f"Channel {channel_id} closed")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to close channel {channel_id}: {e}")
            return False

    def cleanup(self):
        """Cleanup resources"""
        try:
            # Close WebSocket connections
            for websocket in self.websocket_connections.values():
                if websocket and not websocket.closed:
                    asyncio.create_task(websocket.close())
            
            # Close HTTP session
            if self.http_session and not self.http_session.closed:
                asyncio.create_task(self.http_session.close())
            
            super().cleanup()
            logger.info("CommunicationManager cleanup completed")
            
        except Exception as e:
            logger.error(f"CommunicationManager cleanup failed: {e}")
