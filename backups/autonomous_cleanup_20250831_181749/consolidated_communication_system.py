"""
Consolidated Communication System
Unified communication infrastructure for the entire project.
V2 Compliance: Under 400 lines, SSOT principles, object-oriented design.
"""

import asyncio
import json
import logging
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from concurrent.futures import ThreadPoolExecutor


class CommunicationType(Enum):
    """Communication protocol types."""
    HTTP = "http"
    WEBSOCKET = "websocket"
    GRPC = "grpc"
    MQTT = "mqtt"
    REDIS = "redis"
    RABBITMQ = "rabbitmq"
    KAFKA = "kafka"
    ZEROMQ = "zeromq"


@dataclass
class Message:
    """Standardized message structure."""
    id: str
    type: str
    payload: Dict[str, Any]
    timestamp: float
    source: str
    destination: str
    priority: int = 0
    metadata: Optional[Dict[str, Any]] = None


class CommunicationInterface(ABC):
    """Abstract base for communication protocols."""
    
    @abstractmethod
    async def connect(self) -> bool:
        """Establish connection."""
        pass
    
    @abstractmethod
    async def disconnect(self) -> bool:
        """Close connection."""
        pass
    
    @abstractmethod
    async def send(self, message: Message) -> bool:
        """Send message."""
        pass
    
    @abstractmethod
    async def receive(self) -> Optional[Message]:
        """Receive message."""
        pass


class HTTPCommunication(CommunicationInterface):
    """HTTP-based communication implementation."""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url
        self.timeout = timeout
        self.session = None
        self._connected = False
    
    async def connect(self) -> bool:
        """Establish HTTP connection."""
        try:
            import aiohttp
            self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=self.timeout))
            self._connected = True
            return True
        except ImportError:
            logging.error("aiohttp not available for HTTP communication")
            return False
    
    async def disconnect(self) -> bool:
        """Close HTTP connection."""
        if self.session:
            await self.session.close()
            self._connected = False
        return True
    
    async def send(self, message: Message) -> bool:
        """Send HTTP message."""
        if not self._connected:
            return False
        try:
            async with self.session.post(
                f"{self.base_url}/message",
                json=message.__dict__
            ) as response:
                return response.status == 200
        except Exception as e:
            logging.error(f"HTTP send error: {e}")
            return False
    
    async def receive(self) -> Optional[Message]:
        """Receive HTTP message."""
        if not self._connected:
            return None
        try:
            async with self.session.get(f"{self.base_url}/message") as response:
                if response.status == 200:
                    data = await response.json()
                    return Message(**data)
        except Exception as e:
            logging.error(f"HTTP receive error: {e}")
        return None


class WebSocketCommunication(CommunicationInterface):
    """WebSocket-based communication implementation."""
    
    def __init__(self, url: str):
        self.url = url
        self.websocket = None
        self._connected = False
    
    async def connect(self) -> bool:
        """Establish WebSocket connection."""
        try:
            import websockets
            self.websocket = await websockets.connect(self.url)
            self._connected = True
            return True
        except ImportError:
            logging.error("websockets not available for WebSocket communication")
            return False
    
    async def disconnect(self) -> bool:
        """Close WebSocket connection."""
        if self.websocket:
            await self.websocket.close()
            self._connected = False
        return True
    
    async def send(self, message: Message) -> bool:
        """Send WebSocket message."""
        if not self._connected:
            return False
        try:
            await self.websocket.send(json.dumps(message.__dict__))
            return True
        except Exception as e:
            logging.error(f"WebSocket send error: {e}")
            return False
    
    async def receive(self) -> Optional[Message]:
        """Receive WebSocket message."""
        if not self._connected:
            return None
        try:
            data = await self.websocket.recv()
            return Message(**json.loads(data))
        except Exception as e:
            logging.error(f"WebSocket receive error: {e}")
        return None


class MessageQueue(CommunicationInterface):
    """Message queue communication implementation."""
    
    def __init__(self, queue_name: str, broker_url: str):
        self.queue_name = queue_name
        self.broker_url = broker_url
        self.connection = None
        self.channel = None
        self._connected = False
    
    async def connect(self) -> bool:
        """Establish queue connection."""
        try:
            import pika
            self.connection = pika.BlockingConnection(pika.URLParameters(self.broker_url))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            self._connected = True
            return True
        except ImportError:
            logging.error("pika not available for message queue communication")
            return False
    
    async def disconnect(self) -> bool:
        """Close queue connection."""
        if self.connection:
            self.connection.close()
            self._connected = False
        return True
    
    async def send(self, message: Message) -> bool:
        """Send queue message."""
        if not self._connected:
            return False
        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message.__dict__)
            )
            return True
        except Exception as e:
            logging.error(f"Queue send error: {e}")
            return False
    
    async def receive(self) -> Optional[Message]:
        """Receive queue message."""
        if not self._connected:
            return None
        try:
            method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
            if method_frame:
                self.channel.basic_ack(method_frame.delivery_tag)
                return Message(**json.loads(body))
        except Exception as e:
            logging.error(f"Queue receive error: {e}")
        return None


class CommunicationManager:
    """Centralized communication management system."""
    
    def __init__(self):
        self.protocols: Dict[CommunicationType, CommunicationInterface] = {}
        self.message_handlers: Dict[str, callable] = {}
        self.running = False
        self._lock = threading.Lock()
    
    def register_protocol(self, comm_type: CommunicationType, protocol: CommunicationInterface):
        """Register communication protocol."""
        with self._lock:
            self.protocols[comm_type] = protocol
    
    def register_handler(self, message_type: str, handler: callable):
        """Register message handler."""
        self.message_handlers[message_type] = handler
    
    async def start(self):
        """Start communication manager."""
        self.running = True
        for protocol in self.protocols.values():
            await protocol.connect()
    
    async def stop(self):
        """Stop communication manager."""
        self.running = False
        for protocol in self.protocols.values():
            await protocol.disconnect()
    
    async def broadcast(self, message: Message):
        """Broadcast message across all protocols."""
        for protocol in self.protocols.values():
            await protocol.send(message)
    
    async def route_message(self, message: Message):
        """Route message to appropriate handler."""
        if message.type in self.message_handlers:
            handler = self.message_handlers[message.type]
            await handler(message)


class ConsolidatedCommunicationSystem:
    """Main consolidated communication system."""
    
    def __init__(self):
        self.manager = CommunicationManager()
        self.http_comm = None
        self.websocket_comm = None
        self.queue_comm = None
        self._initialized = False
    
    def initialize(self, config: Dict[str, Any]):
        """Initialize communication system with configuration."""
        if self._initialized:
            return
        
        # Initialize HTTP communication
        if 'http' in config:
            self.http_comm = HTTPCommunication(
                config['http']['base_url'],
                config['http'].get('timeout', 30)
            )
            self.manager.register_protocol(CommunicationType.HTTP, self.http_comm)
        
        # Initialize WebSocket communication
        if 'websocket' in config:
            self.websocket_comm = WebSocketCommunication(config['websocket']['url'])
            self.manager.register_protocol(CommunicationType.WEBSOCKET, self.websocket_comm)
        
        # Initialize message queue communication
        if 'queue' in config:
            self.queue_comm = MessageQueue(
                config['queue']['name'],
                config['queue']['broker_url']
            )
            self.manager.register_protocol(CommunicationType.RABBITMQ, self.queue_comm)
        
        self._initialized = True
    
    async def start_system(self):
        """Start the communication system."""
        if not self._initialized:
            raise RuntimeError("Communication system not initialized")
        await self.manager.start()
    
    async def stop_system(self):
        """Stop the communication system."""
        await self.manager.stop()
    
    async def send_message(self, message: Message, protocol: CommunicationType = None):
        """Send message using specified or default protocol."""
        if protocol and protocol in self.manager.protocols:
            await self.manager.protocols[protocol].send(message)
        else:
            await self.manager.broadcast(message)
    
    def register_message_handler(self, message_type: str, handler: callable):
        """Register message handler."""
        self.manager.register_handler(message_type, handler)
    
    async def process_messages(self):
        """Process incoming messages."""
        while self.manager.running:
            for protocol in self.manager.protocols.values():
                message = await protocol.receive()
                if message:
                    await self.manager.route_message(message)
            await asyncio.sleep(0.1)


# Global communication system instance
communication_system = ConsolidatedCommunicationSystem()
