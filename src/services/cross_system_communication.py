"""
Cross-System Communication Infrastructure for Agent_Cellphone_V2_Repository
Enables seamless communication between different systems through various protocols.
"""

import asyncio
import json
import logging
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable, Coroutine
from pathlib import Path
import aiohttp
import websockets
from websockets.server import WebSocketServerProtocol
import socket
import ssl
import struct
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CommunicationProtocol(Enum):
    """Supported communication protocols."""
    HTTP = "http"
    HTTPS = "https"
    WEBSOCKET = "websocket"
    TCP = "tcp"
    UDP = "udp"
    GRPC = "grpc"
    MQTT = "mqtt"
    REDIS = "redis"
    RABBITMQ = "rabbitmq"
    KAFKA = "kafka"


class MessageType(Enum):
    """Types of messages that can be sent."""
    REQUEST = "request"
    RESPONSE = "response"
    EVENT = "event"
    COMMAND = "command"
    QUERY = "query"
    NOTIFICATION = "notification"
    HEARTBEAT = "heartbeat"
    ERROR = "error"


class MessagePriority(Enum):
    """Message priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


@dataclass
class SystemEndpoint:
    """Represents a system endpoint for communication."""
    system_id: str
    name: str
    protocol: CommunicationProtocol
    host: str
    port: int
    path: str = ""
    credentials: Optional[Dict[str, str]] = None
    ssl_context: Optional[ssl.SSLContext] = None
    timeout: float = 30.0
    retry_attempts: int = 3
    health_check_interval: float = 60.0
    last_health_check: float = field(default_factory=time.time)
    is_healthy: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CrossSystemMessage:
    """Message structure for cross-system communication."""
    message_id: str
    source_system: str
    target_system: str
    message_type: MessageType
    priority: MessagePriority
    timestamp: float
    payload: Dict[str, Any]
    headers: Dict[str, str] = field(default_factory=dict)
    correlation_id: Optional[str] = None
    reply_to: Optional[str] = None
    ttl: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class CommunicationMetrics:
    """Metrics for cross-system communication."""
    total_messages_sent: int = 0
    total_messages_received: int = 0
    successful_communications: int = 0
    failed_communications: int = 0
    average_response_time: float = 0.0
    total_response_time: float = 0.0
    active_connections: int = 0
    last_activity: float = field(default_factory=time.time)


class BaseCommunicationHandler(ABC):
    """Abstract base class for communication handlers."""
    
    def __init__(self, endpoint: SystemEndpoint):
        self.endpoint = endpoint
        self.is_connected = False
        self.connection_metrics = CommunicationMetrics()
        self.error_callbacks: List[Callable[[str, Exception], None]] = []
        self.message_callbacks: List[Callable[[CrossSystemMessage], None]] = []
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection to the system."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Disconnect from the system."""
        pass
    
    @abstractmethod
    async def send_message(self, message: CrossSystemMessage) -> bool:
        """Send a message to the system."""
        pass
    
    @abstractmethod
    async def receive_message(self) -> Optional[CrossSystemMessage]:
        """Receive a message from the system."""
        pass
    
    def add_error_callback(self, callback: Callable[[str, Exception], None]):
        """Add error callback function."""
        self.error_callbacks.append(callback)
    
    def add_message_callback(self, callback: Callable[[CrossSystemMessage], None]):
        """Add message callback function."""
        self.message_callbacks.append(callback)
    
    def _notify_error(self, error_msg: str, exception: Exception):
        """Notify all error callbacks."""
        for callback in self.error_callbacks:
            try:
                callback(error_msg, exception)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")
    
    def _notify_message(self, message: CrossSystemMessage):
        """Notify all message callbacks."""
        for callback in self.message_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in message callback: {e}")


class HTTPCommunicationHandler(BaseCommunicationHandler):
    """HTTP/HTTPS communication handler."""
    
    def __init__(self, endpoint: SystemEndpoint):
        super().__init__(endpoint)
        self.session: Optional[aiohttp.ClientSession] = None
        self._setup_ssl_context()
    
    def _setup_ssl_context(self):
        """Setup SSL context for HTTPS connections."""
        if self.endpoint.protocol == CommunicationProtocol.HTTPS:
            if self.endpoint.ssl_context:
                self.ssl_context = self.endpoint.ssl_context
            else:
                self.ssl_context = ssl.create_default_context()
    
    async def connect(self) -> bool:
        """Establish HTTP connection."""
        try:
            connector = aiohttp.TCPConnector(ssl=self.ssl_context if self.endpoint.protocol == CommunicationProtocol.HTTPS else False)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=aiohttp.ClientTimeout(total=self.endpoint.timeout)
            )
            self.is_connected = True
            self.connection_metrics.active_connections += 1
            logger.info(f"Connected to HTTP endpoint: {self.endpoint.host}:{self.endpoint.port}")
            return True
        except Exception as e:
            self._notify_error(f"Failed to connect to HTTP endpoint: {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect HTTP connection."""
        try:
            if self.session:
                await self.session.close()
                self.session = None
            self.is_connected = False
            self.connection_metrics.active_connections = max(0, self.connection_metrics.active_connections - 1)
            logger.info(f"Disconnected from HTTP endpoint: {self.endpoint.host}:{self.endpoint.port}")
            return True
        except Exception as e:
            self._notify_error(f"Error disconnecting from HTTP endpoint: {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def send_message(self, message: CrossSystemMessage) -> bool:
        """Send HTTP message."""
        if not self.is_connected or not self.session:
            return False
        
        start_time = time.time()
        try:
            url = f"{self.endpoint.protocol.value}://{self.endpoint.host}:{self.endpoint.port}{self.endpoint.path}"
            
            # Prepare headers
            headers = {
                "Content-Type": "application/json",
                "X-Message-ID": message.message_id,
                "X-Source-System": message.source_system,
                "X-Message-Type": message.message_type.value,
                "X-Priority": str(message.priority.value),
                "X-Correlation-ID": message.correlation_id or "",
                **message.headers
            }
            
            # Send request based on message type
            if message.message_type == MessageType.REQUEST:
                async with self.session.post(url, json=message.payload, headers=headers) as response:
                    response_data = await response.json()
                    self._handle_response(message, response_data, response.status)
            elif message.message_type == MessageType.COMMAND:
                async with self.session.put(url, json=message.payload, headers=headers) as response:
                    response_data = await response.json()
                    self._handle_response(message, response_data, response.status)
            elif message.message_type == MessageType.QUERY:
                async with self.session.get(url, params=message.payload, headers=headers) as response:
                    response_data = await response.json()
                    self._handle_response(message, response_data, response.status)
            else:
                # For other message types, use POST
                async with self.session.post(url, json=message.payload, headers=headers) as response:
                    response_data = await response.json()
                    self._handle_response(message, response_data, response.status)
            
            # Update metrics
            response_time = time.time() - start_time
            self.connection_metrics.total_messages_sent += 1
            self.connection_metrics.successful_communications += 1
            self.connection_metrics.total_response_time += response_time
            self.connection_metrics.average_response_time = (
                self.connection_metrics.total_response_time / self.connection_metrics.successful_communications
            )
            
            return True
            
        except Exception as e:
            self.connection_metrics.failed_communications += 1
            self._notify_error(f"Failed to send HTTP message to {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    def _handle_response(self, original_message: CrossSystemMessage, response_data: Dict[str, Any], status_code: int):
        """Handle HTTP response."""
        if status_code >= 400:
            # Create error message
            error_message = CrossSystemMessage(
                message_id=f"error_{original_message.message_id}",
                source_system=self.endpoint.system_id,
                target_system=original_message.source_system,
                message_type=MessageType.ERROR,
                priority=MessagePriority.HIGH,
                timestamp=time.time(),
                payload={
                    "error": "HTTP Error",
                    "status_code": status_code,
                    "original_message_id": original_message.message_id,
                    "response_data": response_data
                },
                correlation_id=original_message.correlation_id
            )
            self._notify_message(error_message)
        else:
            # Create response message
            response_message = CrossSystemMessage(
                message_id=f"response_{original_message.message_id}",
                source_system=self.endpoint.system_id,
                target_system=original_message.source_system,
                message_type=MessageType.RESPONSE,
                priority=MessagePriority.NORMAL,
                timestamp=time.time(),
                payload=response_data,
                correlation_id=original_message.correlation_id
            )
            self._notify_message(response_message)
    
    async def receive_message(self) -> Optional[CrossSystemMessage]:
        """HTTP is request-response, so this method is not applicable."""
        return None


class WebSocketCommunicationHandler(BaseCommunicationHandler):
    """WebSocket communication handler."""
    
    def __init__(self, endpoint: SystemEndpoint):
        super().__init__(endpoint)
        self.websocket: Optional[WebSocketServerProtocol] = None
        self._receive_task: Optional[asyncio.Task] = None
    
    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            protocol = "wss" if self.endpoint.protocol == CommunicationProtocol.HTTPS else "ws"
            url = f"{protocol}://{self.endpoint.host}:{self.endpoint.port}{self.endpoint.path}"
            
            self.websocket = await websockets.connect(
                url,
                ssl=self.endpoint.ssl_context if self.endpoint.protocol == CommunicationProtocol.HTTPS else None
            )
            
            self.is_connected = True
            self.connection_metrics.active_connections += 1
            
            # Start receive task
            self._receive_task = asyncio.create_task(self._receive_loop())
            
            logger.info(f"Connected to WebSocket endpoint: {self.endpoint.host}:{self.endpoint.port}")
            return True
            
        except Exception as e:
            self._notify_error(f"Failed to connect to WebSocket endpoint: {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect WebSocket connection."""
        try:
            if self._receive_task:
                self._receive_task.cancel()
                try:
                    await self._receive_task
                except asyncio.CancelledError:
                    pass
            
            if self.websocket:
                await self.websocket.close()
                self.websocket = None
            
            self.is_connected = False
            self.connection_metrics.active_connections = max(0, self.connection_metrics.active_connections - 1)
            logger.info(f"Disconnected from WebSocket endpoint: {self.endpoint.host}:{self.endpoint.port}")
            return True
            
        except Exception as e:
            self._notify_error(f"Error disconnecting from WebSocket endpoint: {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def send_message(self, message: CrossSystemMessage) -> bool:
        """Send WebSocket message."""
        if not self.is_connected or not self.websocket:
            return False
        
        try:
            message_data = {
                "message_id": message.message_id,
                "source_system": message.source_system,
                "target_system": message.target_system,
                "message_type": message.message_type.value,
                "priority": message.priority.value,
                "timestamp": message.timestamp,
                "payload": message.payload,
                "headers": message.headers,
                "correlation_id": message.correlation_id,
                "reply_to": message.reply_to
            }
            
            await self.websocket.send(json.dumps(message_data))
            self.connection_metrics.total_messages_sent += 1
            return True
            
        except Exception as e:
            self.connection_metrics.failed_communications += 1
            self._notify_error(f"Failed to send WebSocket message to {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def receive_message(self) -> Optional[CrossSystemMessage]:
        """Receive WebSocket message."""
        if not self.is_connected or not self.websocket:
            return None
        
        try:
            message_data = await self.websocket.recv()
            message_dict = json.loads(message_data)
            
            message = CrossSystemMessage(
                message_id=message_dict["message_id"],
                source_system=message_dict["source_system"],
                target_system=message_dict["target_system"],
                message_type=MessageType(message_dict["message_type"]),
                priority=MessagePriority(message_dict["priority"]),
                timestamp=message_dict["timestamp"],
                payload=message_dict["payload"],
                headers=message_dict.get("headers", {}),
                correlation_id=message_dict.get("correlation_id"),
                reply_to=message_dict.get("reply_to")
            )
            
            self.connection_metrics.total_messages_received += 1
            return message
            
        except Exception as e:
            self._notify_error(f"Failed to receive WebSocket message from {self.endpoint.host}:{self.endpoint.port}", e)
            return None
    
    async def _receive_loop(self):
        """Background task for receiving messages."""
        while self.is_connected and self.websocket:
            try:
                message = await self.receive_message()
                if message:
                    self._notify_message(message)
            except websockets.exceptions.ConnectionClosed:
                logger.warning(f"WebSocket connection closed for {self.endpoint.host}:{self.endpoint.port}")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket receive loop: {e}")
                break
        
        self.is_connected = False


class TCPCommunicationHandler(BaseCommunicationHandler):
    """TCP communication handler."""
    
    def __init__(self, endpoint: SystemEndpoint):
        super().__init__(endpoint)
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self._receive_task: Optional[asyncio.Task] = None
    
    async def connect(self) -> bool:
        """Establish TCP connection."""
        try:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(
                    self.endpoint.host,
                    self.endpoint.port,
                    ssl=self.endpoint.ssl_context if self.endpoint.protocol == CommunicationProtocol.HTTPS else None
                ),
                timeout=self.endpoint.timeout
            )
            
            self.is_connected = True
            self.connection_metrics.active_connections += 1
            
            # Start receive task
            self._receive_task = asyncio.create_task(self._receive_loop())
            
            logger.info(f"Connected to TCP endpoint: {self.endpoint.host}:{self.endpoint.port}")
            return True
            
        except Exception as e:
            self._notify_error(f"Failed to connect to TCP endpoint: {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def disconnect(self) -> bool:
        """Disconnect TCP connection."""
        try:
            if self._receive_task:
                self._receive_task.cancel()
                try:
                    await self._receive_task
                except asyncio.CancelledError:
                    pass
            
            if self.writer:
                self.writer.close()
                await self.writer.wait_closed()
                self.writer = None
            
            self.reader = None
            self.is_connected = False
            self.connection_metrics.active_connections = max(0, self.connection_metrics.active_connections - 1)
            logger.info(f"Disconnected from TCP endpoint: {self.endpoint.host}:{self.endpoint.port}")
            return True
            
        except Exception as e:
            self._notify_error(f"Error disconnecting from TCP endpoint: {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def send_message(self, message: CrossSystemMessage) -> bool:
        """Send TCP message."""
        if not self.is_connected or not self.writer:
            return False
        
        try:
            message_data = {
                "message_id": message.message_id,
                "source_system": message.source_system,
                "target_system": message.target_system,
                "message_type": message.message_type.value,
                "priority": message.priority.value,
                "timestamp": message.timestamp,
                "payload": message.payload,
                "headers": message.headers,
                "correlation_id": message.correlation_id,
                "reply_to": message.reply_to
            }
            
            # Send message length first, then message data
            message_bytes = json.dumps(message_data).encode('utf-8')
            length_bytes = struct.pack('!I', len(message_bytes))
            
            self.writer.write(length_bytes + message_bytes)
            await self.writer.drain()
            
            self.connection_metrics.total_messages_sent += 1
            return True
            
        except Exception as e:
            self.connection_metrics.failed_communications += 1
            self._notify_error(f"Failed to send TCP message to {self.endpoint.host}:{self.endpoint.port}", e)
            return False
    
    async def receive_message(self) -> Optional[CrossSystemMessage]:
        """Receive TCP message."""
        if not self.is_connected or not self.reader:
            return None
        
        try:
            # Read message length first
            length_bytes = await self.reader.readexactly(4)
            message_length = struct.unpack('!I', length_bytes)[0]
            
            # Read message data
            message_bytes = await self.reader.readexactly(message_length)
            message_data = json.loads(message_bytes.decode('utf-8'))
            
            message = CrossSystemMessage(
                message_id=message_data["message_id"],
                source_system=message_data["source_system"],
                target_system=message_data["target_system"],
                message_type=MessageType(message_data["message_type"]),
                priority=MessagePriority(message_data["priority"]),
                timestamp=message_data["timestamp"],
                payload=message_data["payload"],
                headers=message_data.get("headers", {}),
                correlation_id=message_data.get("correlation_id"),
                reply_to=message_data.get("reply_to")
            )
            
            self.connection_metrics.total_messages_received += 1
            return message
            
        except Exception as e:
            self._notify_error(f"Failed to receive TCP message from {self.endpoint.host}:{self.endpoint.port}", e)
            return None
    
    async def _receive_loop(self):
        """Background task for receiving messages."""
        while self.is_connected and self.reader:
            try:
                message = await self.receive_message()
                if message:
                    self._notify_message(message)
            except asyncio.IncompleteReadError:
                logger.warning(f"TCP connection closed for {self.endpoint.host}:{self.endpoint.port}")
                break
            except Exception as e:
                logger.error(f"Error in TCP receive loop: {e}")
                break
        
        self.is_connected = False


class CrossSystemCommunicationManager:
    """Manages cross-system communication across all protocols."""
    
    def __init__(self):
        self.endpoints: Dict[str, SystemEndpoint] = {}
        self.handlers: Dict[str, BaseCommunicationHandler] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.running = False
        self.metrics = CommunicationMetrics()
        
        # Event callbacks
        self.connection_callbacks: List[Callable[[str, bool], None]] = []
        self.message_callbacks: List[Callable[[CrossSystemMessage], None]] = []
        self.error_callbacks: List[Callable[[str, Exception], None]] = []
        
        # Background tasks
        self._message_processor_task: Optional[asyncio.Task] = None
        self._health_check_task: Optional[asyncio.Task] = None
    
    def add_endpoint(self, endpoint: SystemEndpoint) -> bool:
        """Add a new system endpoint."""
        try:
            self.endpoints[endpoint.system_id] = endpoint
            logger.info(f"Added endpoint: {endpoint.system_id} ({endpoint.protocol.value}://{endpoint.host}:{endpoint.port})")
            return True
        except Exception as e:
            logger.error(f"Failed to add endpoint {endpoint.system_id}: {e}")
            return False
    
    def remove_endpoint(self, system_id: str) -> bool:
        """Remove a system endpoint."""
        try:
            if system_id in self.handlers:
                asyncio.create_task(self.disconnect_system(system_id))
            
            if system_id in self.endpoints:
                del self.endpoints[system_id]
                logger.info(f"Removed endpoint: {system_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to remove endpoint {system_id}: {e}")
            return False
    
    async def connect_system(self, system_id: str) -> bool:
        """Connect to a specific system."""
        if system_id not in self.endpoints:
            logger.error(f"Endpoint not found: {system_id}")
            return False
        
        endpoint = self.endpoints[system_id]
        
        # Create appropriate handler based on protocol
        if endpoint.protocol in [CommunicationProtocol.HTTP, CommunicationProtocol.HTTPS]:
            handler = HTTPCommunicationHandler(endpoint)
        elif endpoint.protocol == CommunicationProtocol.WEBSOCKET:
            handler = WebSocketCommunicationHandler(endpoint)
        elif endpoint.protocol == CommunicationProtocol.TCP:
            handler = TCPCommunicationHandler(endpoint)
        else:
            logger.error(f"Unsupported protocol: {endpoint.protocol}")
            return False
        
        # Setup callbacks
        handler.add_error_callback(self._handle_handler_error)
        handler.add_message_callback(self._handle_handler_message)
        
        # Connect
        if await handler.connect():
            self.handlers[system_id] = handler
            self._notify_connection_change(system_id, True)
            logger.info(f"Connected to system: {system_id}")
            return True
        else:
            logger.error(f"Failed to connect to system: {system_id}")
            return False
    
    async def disconnect_system(self, system_id: str) -> bool:
        """Disconnect from a specific system."""
        if system_id not in self.handlers:
            return True
        
        handler = self.handlers[system_id]
        if await handler.disconnect():
            del self.handlers[system_id]
            self._notify_connection_change(system_id, False)
            logger.info(f"Disconnected from system: {system_id}")
            return True
        return False
    
    async def send_message(self, message: CrossSystemMessage) -> bool:
        """Send a message to a target system."""
        if message.target_system not in self.handlers:
            logger.error(f"Target system not connected: {message.target_system}")
            return False
        
        handler = self.handlers[message.target_system]
        return await handler.send_message(message)
    
    async def broadcast_message(self, message: CrossSystemMessage, exclude_systems: Optional[List[str]] = None) -> Dict[str, bool]:
        """Broadcast a message to all connected systems."""
        exclude_systems = exclude_systems or []
        results = {}
        
        for system_id, handler in self.handlers.items():
            if system_id not in exclude_systems:
                results[system_id] = await handler.send_message(message)
        
        return results
    
    def add_connection_callback(self, callback: Callable[[str, bool], None]):
        """Add connection change callback."""
        self.connection_callbacks.append(callback)
    
    def add_message_callback(self, callback: Callable[[CrossSystemMessage], None]):
        """Add message callback."""
        self.message_callbacks.append(callback)
    
    def add_error_callback(self, callback: Callable[[str, Exception], None]):
        """Add error callback."""
        self.error_callbacks.append(callback)
    
    def _notify_connection_change(self, system_id: str, connected: bool):
        """Notify connection change callbacks."""
        for callback in self.connection_callbacks:
            try:
                callback(system_id, connected)
            except Exception as e:
                logger.error(f"Error in connection callback: {e}")
    
    def _handle_handler_message(self, message: CrossSystemMessage):
        """Handle messages from handlers."""
        self._notify_message(message)
        asyncio.create_task(self.message_queue.put(message))
    
    def _handle_handler_error(self, error_msg: str, exception: Exception):
        """Handle errors from handlers."""
        for callback in self.error_callbacks:
            try:
                callback(error_msg, exception)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")
    
    def _notify_message(self, message: CrossSystemMessage):
        """Notify message callbacks."""
        for callback in self.message_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in message callback: {e}")
    
    async def start(self):
        """Start the communication manager."""
        if self.running:
            return
        
        self.running = True
        
        # Start background tasks
        self._message_processor_task = asyncio.create_task(self._message_processor_loop())
        self._health_check_task = asyncio.create_task(self._health_check_loop())
        
        logger.info("Cross-system communication manager started")
    
    async def stop(self):
        """Stop the communication manager."""
        if not self.running:
            return
        
        self.running = False
        
        # Cancel background tasks
        if self._message_processor_task:
            self._message_processor_task.cancel()
            try:
                await self._message_processor_task
            except asyncio.CancelledError:
                pass
        
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
        
        # Disconnect all systems
        for system_id in list(self.handlers.keys()):
            await self.disconnect_system(system_id)
        
        logger.info("Cross-system communication manager stopped")
    
    async def _message_processor_loop(self):
        """Background task for processing messages from the queue."""
        while self.running:
            try:
                message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
                # Process message here if needed
                self.message_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error in message processor loop: {e}")
    
    async def _health_check_loop(self):
        """Background task for health checking all endpoints."""
        while self.running:
            try:
                for endpoint in self.endpoints.values():
                    if time.time() - endpoint.last_health_check >= endpoint.health_check_interval:
                        await self._perform_health_check(endpoint)
                        endpoint.last_health_check = time.time()
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in health check loop: {e}")
                await asyncio.sleep(10)
    
    async def _perform_health_check(self, endpoint: SystemEndpoint):
        """Perform health check for a specific endpoint."""
        try:
            if endpoint.protocol in [CommunicationProtocol.HTTP, CommunicationProtocol.HTTPS]:
                # Simple HTTP health check
                url = f"{endpoint.protocol.value}://{endpoint.host}:{endpoint.port}/health"
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, timeout=5.0) as response:
                        endpoint.is_healthy = response.status == 200
            else:
                # For other protocols, check if handler is connected
                if endpoint.system_id in self.handlers:
                    endpoint.is_healthy = self.handlers[endpoint.system_id].is_connected
                else:
                    endpoint.is_healthy = False
            
            if not endpoint.is_healthy:
                logger.warning(f"Health check failed for endpoint: {endpoint.system_id}")
                
        except Exception as e:
            endpoint.is_healthy = False
            logger.error(f"Health check error for endpoint {endpoint.system_id}: {e}")
    
    def get_system_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all systems."""
        status = {}
        for system_id, endpoint in self.endpoints.items():
            handler = self.handlers.get(system_id)
            status[system_id] = {
                "name": endpoint.name,
                "protocol": endpoint.protocol.value,
                "host": endpoint.host,
                "port": endpoint.port,
                "connected": handler.is_connected if handler else False,
                "healthy": endpoint.is_healthy,
                "last_health_check": endpoint.last_health_check,
                "metrics": handler.connection_metrics if handler else None
            }
        return status
    
    def get_metrics(self) -> CommunicationMetrics:
        """Get overall communication metrics."""
        # Aggregate metrics from all handlers
        total_sent = sum(h.connection_metrics.total_messages_sent for h in self.handlers.values())
        total_received = sum(h.connection_metrics.total_messages_received for h in self.handlers.values())
        total_successful = sum(h.connection_metrics.successful_communications for h in self.handlers.values())
        total_failed = sum(h.connection_metrics.failed_communications for h in self.handlers.values())
        total_response_time = sum(h.connection_metrics.total_response_time for h in self.handlers.values())
        active_connections = sum(h.connection_metrics.active_connections for h in self.handlers.values())
        
        self.metrics.total_messages_sent = total_sent
        self.metrics.total_messages_received = total_received
        self.metrics.successful_communications = total_successful
        self.metrics.failed_communications = total_failed
        self.metrics.active_connections = active_connections
        
        if total_successful > 0:
            self.metrics.average_response_time = total_response_time / total_successful
            self.metrics.total_response_time = total_response_time
        
        return self.metrics
