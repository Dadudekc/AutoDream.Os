#!/usr/bin/env python3
"""
Cross-Agent Communication Protocol
Agent_Cellphone_V2_Repository - Multi-Agent Web Integration

This module implements the standardized communication protocol for all agents
to interact via web APIs, WebSockets, and message queues.
"""

import json
import logging
import asyncio
import time
import uuid

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable, Union
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import hashlib
import hmac
import base64

from flask import Flask, request, jsonify, current_app
from flask_socketio import SocketIO, emit, join_room, leave_room
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import pika

# Protocol Constants
PROTOCOL_VERSION = "1.0.0"
MESSAGE_TYPES = {
    "COMMAND": "command",
    "RESPONSE": "response",
    "EVENT": "event",
    "STATUS": "status",
    "ERROR": "error",
    "HEARTBEAT": "heartbeat",
}

COMMAND_CATEGORIES = {
    "SYSTEM": "system",
    "WEB": "web",
    "AUTOMATION": "automation",
    "DATA": "data",
    "COORDINATION": "coordination",
}


class MessagePriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


class AgentStatus(Enum):
    OFFLINE = "offline"
    ONLINE = "online"
    BUSY = "busy"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class AgentMessage:
    """Standardized message format for cross-agent communication"""

    message_id: str
    timestamp: str
    sender_id: str
    recipient_id: Optional[str] = None
    message_type: str = MESSAGE_TYPES["COMMAND"]
    category: str = COMMAND_CATEGORIES["SYSTEM"]
    priority: MessagePriority = MessagePriority.NORMAL
    payload: Dict[str, Any] = None
    correlation_id: Optional[str] = None
    requires_response: bool = False
    ttl: Optional[int] = None  # Time to live in seconds

    def __post_init__(self):
        if self.payload is None:
            self.payload = {}
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class AgentResponse:
    """Standardized response format for cross-agent communication"""

    response_id: str
    original_message_id: str
    timestamp: str
    sender_id: str
    recipient_id: str
    success: bool
    payload: Dict[str, Any] = None
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = None

    def __post_init__(self):
        if self.payload is None:
            self.payload = {}
        if not self.response_id:
            self.response_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class AgentStatus:
    """Agent status information for monitoring and coordination"""

    agent_id: str
    status: AgentStatus
    timestamp: str
    capabilities: List[str] = None
    current_task: Optional[str] = None
    load_percentage: float = 0.0
    memory_usage: float = 0.0
    cpu_usage: float = 0.0
    last_heartbeat: str = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []
        if self.metadata is None:
            self.metadata = {}
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


class MessageValidator:
    """Validates incoming messages according to protocol rules"""

    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """Validate message structure and required fields"""
        required_fields = ["message_id", "timestamp", "sender_id", "message_type"]

        for field in required_fields:
            if field not in message:
                return False

        # Validate message type
        if message["message_type"] not in MESSAGE_TYPES.values():
            return False

        # Validate timestamp format
        try:
            datetime.fromisoformat(message["timestamp"])
        except ValueError:
            return False

        return True

    @staticmethod
    def validate_response(response: Dict[str, Any]) -> bool:
        """Validate response structure and required fields"""
        required_fields = [
            "response_id",
            "original_message_id",
            "timestamp",
            "sender_id",
            "recipient_id",
            "success",
        ]

        for field in required_fields:
            if field not in response:
                return False

        return True


class AuthenticationManager:
    """Manages authentication and authorization for cross-agent communication"""

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or "default-secret-key-change-in-production"
        self.agent_tokens = {}
        self.token_expiry = {}

    def generate_agent_token(self, agent_id: str, expires_in: int = 3600) -> str:
        """Generate authentication token for an agent"""
        payload = {
            "agent_id": agent_id,
            "exp": int(time.time()) + expires_in,
            "iat": int(time.time()),
        }

        # Create JWT-like token (simplified)
        header = base64.b64encode(
            json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
        ).decode()
        payload_b64 = base64.b64encode(json.dumps(payload).encode()).decode()

        # Create signature
        message = f"{header}.{payload_b64}"
        signature = hmac.new(
            self.secret_key.encode(), message.encode(), hashlib.sha256
        ).hexdigest()

        token = f"{header}.{payload_b64}.{signature}"

        # Store token
        self.agent_tokens[agent_id] = token
        self.token_expiry[agent_id] = payload["exp"]

        return token

    def validate_agent_token(self, token: str) -> Optional[str]:
        """Validate authentication token and return agent_id if valid"""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_b64, payload_b64, signature = parts

            # Verify signature
            message = f"{header_b64}.{payload_b64}"
            expected_signature = hmac.new(
                self.secret_key.encode(), message.encode(), hashlib.sha256
            ).hexdigest()

            if signature != expected_signature:
                return None

            # Decode payload
            payload = json.loads(base64.b64decode(payload_b64).decode())

            # Check expiration
            if payload["exp"] < int(time.time()):
                return None

            return payload["agent_id"]

        except Exception:
            return None

    def revoke_agent_token(self, agent_id: str) -> bool:
        """Revoke authentication token for an agent"""
        if agent_id in self.agent_tokens:
            del self.agent_tokens[agent_id]
            if agent_id in self.token_expiry:
                del self.token_expiry[agent_id]
            return True
        return False


class CrossAgentCommunicator:
    """Main class for cross-agent communication"""

    def __init__(self, agent_id: str, config: Dict[str, Any] = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = self._setup_logging()
        self.auth_manager = AuthenticationManager(
            self.config.get("secret_key", "default-secret-key")
        )
        self.message_handlers = {}
        self.status_callbacks = []
        self.connected_agents = set()
        self.message_queue = []
        self.response_waiters = {}

        # Initialize communication backends
        self.redis_client = None
        self.rabbitmq_connection = None
        self._setup_backends()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the communicator"""
        logger = logging.getLogger(f"CrossAgentCommunicator.{self.agent_id}")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _setup_backends(self):
        """Setup Redis and RabbitMQ backends for communication"""
        try:
            # Redis setup
            redis_config = self.config.get("redis", {})
            if redis_config.get("enabled", True):
                self.redis_client = redis.Redis(
                    host=redis_config.get("host", "localhost"),
                    port=redis_config.get("port", 6379),
                    db=redis_config.get("db", 0),
                    decode_responses=True,
                )
                self.logger.info("Redis backend initialized")
        except Exception as e:
            self.logger.warning(f"Redis backend not available: {e}")

        try:
            # RabbitMQ setup
            rabbitmq_config = self.config.get("rabbitmq", {})
            if rabbitmq_config.get("enabled", True):
                credentials = pika.PlainCredentials(
                    rabbitmq_config.get("username", "guest"),
                    rabbitmq_config.get("password", "guest"),
                )
                parameters = pika.ConnectionParameters(
                    host=rabbitmq_config.get("host", "localhost"),
                    port=rabbitmq_config.get("port", 5672),
                    virtual_host=rabbitmq_config.get("vhost", "/"),
                    credentials=credentials,
                )
                self.rabbitmq_connection = pika.BlockingConnection(parameters)
                self.logger.info("RabbitMQ backend initialized")
        except Exception as e:
            self.logger.warning(f"RabbitMQ backend not available: {e}")

    def register_message_handler(self, message_type: str, handler: Callable):
        """Register a handler for specific message types"""
        self.message_handlers[message_type] = handler
        self.logger.info(f"Registered handler for message type: {message_type}")

    def register_status_callback(self, callback: Callable):
        """Register a callback for status updates"""
        self.status_callbacks.append(callback)

    def send_message(
        self,
        recipient_id: str,
        message_type: str,
        payload: Dict[str, Any] = None,
        category: str = COMMAND_CATEGORIES["SYSTEM"],
        priority: MessagePriority = MessagePriority.NORMAL,
        requires_response: bool = False,
        correlation_id: str = None,
    ) -> str:
        """Send a message to another agent"""

        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            category=category,
            priority=priority,
            payload=payload or {},
            correlation_id=correlation_id,
            requires_response=requires_response,
        )

        message_dict = asdict(message)
        message_dict["priority"] = message.priority.value

        # Store message if response is required
        if requires_response:
            self.response_waiters[message.message_id] = {
                "timestamp": time.time(),
                "correlation_id": correlation_id,
            }

        # Send via available backends
        self._send_via_redis(message_dict)
        self._send_via_rabbitmq(message_dict)

        self.logger.info(f"Sent message {message.message_id} to {recipient_id}")
        return message.message_id

    def broadcast_message(
        self,
        message_type: str,
        payload: Dict[str, Any] = None,
        category: str = COMMAND_CATEGORIES["SYSTEM"],
        priority: MessagePriority = MessagePriority.NORMAL,
    ) -> str:
        """Broadcast a message to all connected agents"""

        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            sender_id=self.agent_id,
            message_type=message_type,
            category=category,
            priority=priority,
            payload=payload or {},
        )

        message_dict = asdict(message)
        message_dict["priority"] = message.priority.value

        # Broadcast via available backends
        self._broadcast_via_redis(message_dict)
        self._broadcast_via_rabbitmq(message_dict)

        self.logger.info(f"Broadcasted message {message.message_id} to all agents")
        return message.message_id

    def send_response(
        self,
        original_message: AgentMessage,
        success: bool,
        payload: Dict[str, Any] = None,
        error_code: str = None,
        error_message: str = None,
        execution_time: float = None,
    ) -> str:
        """Send a response to a received message"""

        response = AgentResponse(
            response_id=str(uuid.uuid4()),
            original_message_id=original_message.message_id,
            timestamp=datetime.utcnow().isoformat(),
            sender_id=self.agent_id,
            recipient_id=original_message.sender_id,
            success=success,
            payload=payload or {},
            error_code=error_code,
            error_message=error_message,
            execution_time=execution_time,
        )

        response_dict = asdict(response)

        # Send response via available backends
        self._send_via_redis(response_dict, f"response:{original_message.sender_id}")
        self._send_via_rabbitmq(response_dict, f"response.{original_message.sender_id}")

        self.logger.info(
            f"Sent response {response.response_id} to {original_message.sender_id}"
        )
        return response.response_id

    def update_status(
        self,
        status: AgentStatus,
        current_task: str = None,
        load_percentage: float = 0.0,
        memory_usage: float = 0.0,
        cpu_usage: float = 0.0,
        metadata: Dict[str, Any] = None,
    ):
        """Update agent status and notify other agents"""

        agent_status = AgentStatus(
            agent_id=self.agent_id,
            status=status,
            timestamp=datetime.utcnow().isoformat(),
            current_task=current_task,
            load_percentage=load_percentage,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            metadata=metadata or {},
        )

        status_dict = asdict(agent_status)
        status_dict["status"] = agent_status.status.value

        # Broadcast status update
        self._broadcast_via_redis(status_dict, "status")
        self._broadcast_via_rabbitmq(status_dict, "status")

        # Notify local callbacks
        for callback in self.status_callbacks:
            try:
                callback(agent_status)
            except Exception as e:
                self.logger.error(f"Error in status callback: {e}")

        self.logger.info(f"Updated status to {status.value}")

    def _send_via_redis(self, message: Dict[str, Any], channel: str = None):
        """Send message via Redis pub/sub"""
        if self.redis_client:
            try:
                channel = channel or f"agent:{message.get('recipient_id', 'broadcast')}"
                self.redis_client.publish(channel, json.dumps(message))
            except Exception as e:
                self.logger.error(f"Error sending via Redis: {e}")

    def _send_via_rabbitmq(self, message: Dict[str, Any], routing_key: str = None):
        """Send message via RabbitMQ"""
        if self.rabbitmq_connection:
            try:
                channel = self.rabbitmq_connection.channel()
                exchange = "agent_communication"
                routing_key = (
                    routing_key or f"agent.{message.get('recipient_id', 'broadcast')}"
                )

                channel.exchange_declare(
                    exchange=exchange, exchange_type="topic", durable=True
                )
                channel.basic_publish(
                    exchange=exchange, routing_key=routing_key, body=json.dumps(message)
                )
            except Exception as e:
                self.logger.error(f"Error sending via RabbitMQ: {e}")

    def _broadcast_via_redis(self, message: Dict[str, Any], channel: str = "broadcast"):
        """Broadcast message via Redis"""
        if self.redis_client:
            try:
                self.redis_client.publish(channel, json.dumps(message))
            except Exception as e:
                self.logger.error(f"Error broadcasting via Redis: {e}")

    def _broadcast_via_rabbitmq(
        self, message: Dict[str, Any], routing_key: str = "broadcast"
    ):
        """Broadcast message via RabbitMQ"""
        if self.rabbitmq_connection:
            try:
                channel = self.rabbitmq_connection.channel()
                exchange = "agent_communication"

                channel.exchange_declare(
                    exchange=exchange, exchange_type="topic", durable=True
                )
                channel.basic_publish(
                    exchange=exchange, routing_key=routing_key, body=json.dumps(message)
                )
            except Exception as e:
                self.logger.error(f"Error broadcasting via RabbitMQ: {e}")

    def start_listening(self):
        """Start listening for incoming messages"""
        self.logger.info(f"Starting message listener for {self.agent_id}")

        # Start Redis listener
        if self.redis_client:
            self._start_redis_listener()

        # Start RabbitMQ listener
        if self.rabbitmq_connection:
            self._start_rabbitmq_listener()

    def _start_redis_listener(self):
        """Start Redis pub/sub listener"""
        try:
            pubsub = self.redis_client.pubsub()
            pubsub.subscribe(f"agent:{self.agent_id}", "broadcast", "status")

            # Start listening in a separate thread
            import threading

            def listen():
                for message in pubsub.listen():
                    if message["type"] == "message":
                        try:
                            data = json.loads(message["data"])
                            self._handle_incoming_message(data)
                        except Exception as e:
                            self.logger.error(f"Error handling Redis message: {e}")

            thread = threading.Thread(target=listen, daemon=True)
            thread.start()
            self.logger.info("Redis listener started")

        except Exception as e:
            self.logger.error(f"Error starting Redis listener: {e}")

    def _start_rabbitmq_listener(self):
        """Start RabbitMQ listener"""
        try:
            channel = self.rabbitmq_connection.channel()
            exchange = "agent_communication"
            queue_name = f"agent_{self.agent_id}_queue"

            channel.exchange_declare(
                exchange=exchange, exchange_type="topic", durable=True
            )
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(
                exchange=exchange,
                queue=queue_name,
                routing_key=f"agent.{self.agent_id}",
            )
            channel.queue_bind(
                exchange=exchange, queue=queue_name, routing_key="broadcast"
            )
            channel.queue_bind(
                exchange=exchange, queue=queue_name, routing_key="status"
            )

            # Start consuming in a separate thread
            import threading

            def consume():
                try:
                    for method_frame, properties, body in channel.consume(queue_name):
                        try:
                            data = json.loads(body.decode())
                            self._handle_incoming_message(data)
                            channel.basic_ack(method_frame.delivery_tag)
                        except Exception as e:
                            self.logger.error(f"Error handling RabbitMQ message: {e}")
                            channel.basic_nack(method_frame.delivery_tag, requeue=False)
                except Exception as e:
                    self.logger.error(f"RabbitMQ consumer error: {e}")

            thread = threading.Thread(target=consume, daemon=True)
            thread.start()
            self.logger.info("RabbitMQ listener started")

        except Exception as e:
            self.logger.error(f"Error starting RabbitMQ listener: {e}")

    def _handle_incoming_message(self, message_data: Dict[str, Any]):
        """Handle incoming message and route to appropriate handler"""
        try:
            # Validate message
            if not MessageValidator.validate_message(message_data):
                self.logger.warning(f"Invalid message received: {message_data}")
                return

            # Create message object
            message = AgentMessage(
                message_id=message_data["message_id"],
                timestamp=message_data["timestamp"],
                sender_id=message_data["sender_id"],
                recipient_id=message_data.get("recipient_id"),
                message_type=message_data["message_type"],
                category=message_data.get("category", COMMAND_CATEGORIES["SYSTEM"]),
                priority=MessagePriority(
                    message_data.get("priority", MessagePriority.NORMAL.value)
                ),
                payload=message_data.get("payload", {}),
                correlation_id=message_data.get("correlation_id"),
                requires_response=message_data.get("requires_response", False),
            )

            # Route to appropriate handler
            handler = self.message_handlers.get(message.message_type)
            if handler:
                try:
                    start_time = time.time()
                    result = handler(message)
                    execution_time = time.time() - start_time

                    # Send response if required
                    if message.requires_response:
                        if result is not None:
                            self.send_response(
                                message,
                                True,
                                {"result": result},
                                execution_time=execution_time,
                            )
                        else:
                            self.send_response(
                                message, True, execution_time=execution_time
                            )

                except Exception as e:
                    self.logger.error(f"Error in message handler: {e}")
                    if message.requires_response:
                        self.send_response(
                            message,
                            False,
                            error_code="HANDLER_ERROR",
                            error_message=str(e),
                        )
            else:
                self.logger.warning(
                    f"No handler registered for message type: {message.message_type}"
                )

        except Exception as e:
            self.logger.error(f"Error handling incoming message: {e}")

    def stop(self):
        """Stop the communicator and clean up resources"""
        self.logger.info(f"Stopping communicator for {self.agent_id}")

        if self.rabbitmq_connection:
            try:
                self.rabbitmq_connection.close()
            except Exception as e:
                self.logger.error(f"Error closing RabbitMQ connection: {e}")

        # Clear response waiters
        self.response_waiters.clear()


# Flask integration
def create_flask_integration(communicator: CrossAgentCommunicator) -> Flask:
    """Create Flask app with cross-agent communication endpoints"""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = communicator.config.get(
        "secret_key", "default-secret-key"
    )

    @app.route("/api/agents/status", methods=["GET"])
    def get_agents_status():
        """Get status of all connected agents"""
        return jsonify(
            {
                "status": "success",
                "data": {
                    "connected_agents": list(communicator.connected_agents),
                    "total_agents": len(communicator.connected_agents),
                },
            }
        )

    @app.route("/api/agents/message", methods=["POST"])
    def send_agent_message():
        """Send a message to another agent"""
        try:
            data = request.get_json()
            required_fields = ["recipient_id", "message_type", "payload"]

            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            message_id = communicator.send_message(
                recipient_id=data["recipient_id"],
                message_type=data["message_type"],
                payload=data["payload"],
                category=data.get("category", COMMAND_CATEGORIES["SYSTEM"]),
                priority=MessagePriority(
                    data.get("priority", MessagePriority.NORMAL.value)
                ),
                requires_response=data.get("requires_response", False),
            )

            return jsonify({"status": "success", "data": {"message_id": message_id}})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/agents/broadcast", methods=["POST"])
    def broadcast_message():
        """Broadcast a message to all agents"""
        try:
            data = request.get_json()
            required_fields = ["message_type", "payload"]

            for field in required_fields:
                if field not in data:
                    return jsonify({"error": f"Missing required field: {field}"}), 400

            message_id = communicator.broadcast_message(
                message_type=data["message_type"],
                payload=data["payload"],
                category=data.get("category", COMMAND_CATEGORIES["SYSTEM"]),
                priority=MessagePriority(
                    data.get("priority", MessagePriority.NORMAL.value)
                ),
            )

            return jsonify({"status": "success", "data": {"message_id": message_id}})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


# FastAPI integration
def create_fastapi_integration(communicator: CrossAgentCommunicator) -> FastAPI:
    """Create FastAPI app with cross-agent communication endpoints"""
    app = FastAPI(title="Cross-Agent Communication API", version=PROTOCOL_VERSION)

    @app.get("/api/agents/status")
    async def get_agents_status():
        """Get status of all connected agents"""
        return {
            "status": "success",
            "data": {
                "connected_agents": list(communicator.connected_agents),
                "total_agents": len(communicator.connected_agents),
            },
        }

    @app.post("/api/agents/message")
    async def send_agent_message(data: Dict[str, Any]):
        """Send a message to another agent"""
        try:
            required_fields = ["recipient_id", "message_type", "payload"]

            for field in required_fields:
                if field not in data:
                    raise HTTPException(
                        status_code=400, detail=f"Missing required field: {field}"
                    )

            message_id = communicator.send_message(
                recipient_id=data["recipient_id"],
                message_type=data["message_type"],
                payload=data["payload"],
                category=data.get("category", COMMAND_CATEGORIES["SYSTEM"]),
                priority=MessagePriority(
                    data.get("priority", MessagePriority.NORMAL.value)
                ),
                requires_response=data.get("requires_response", False),
            )

            return {"status": "success", "data": {"message_id": message_id}}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/agents/broadcast")
    async def broadcast_message(data: Dict[str, Any]):
        """Broadcast a message to all agents"""
        try:
            required_fields = ["message_type", "payload"]

            for field in required_fields:
                if field not in data:
                    raise HTTPException(
                        status_code=400, detail=f"Missing required field: {field}"
                    )

            message_id = communicator.broadcast_message(
                message_type=data["message_type"],
                payload=data["message_type"],
                category=data.get("category", COMMAND_CATEGORIES["SYSTEM"]),
                priority=MessagePriority(
                    data.get("priority", MessagePriority.NORMAL.value)
                ),
            )

            return {"status": "success", "data": {"message_id": message_id}}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


# Utility functions
def create_agent_communicator(
    agent_id: str, config: Dict[str, Any] = None
) -> CrossAgentCommunicator:
    """Create a new agent communicator instance"""
    return CrossAgentCommunicator(agent_id, config)


def validate_message_format(message: Dict[str, Any]) -> bool:
    """Validate message format according to protocol"""
    return MessageValidator.validate_message(message)


def create_heartbeat_message(agent_id: str) -> Dict[str, Any]:
    """Create a heartbeat message"""
    return {
        "message_id": str(uuid.uuid4()),
        "timestamp": datetime.utcnow().isoformat(),
        "sender_id": agent_id,
        "message_type": MESSAGE_TYPES["HEARTBEAT"],
        "category": COMMAND_CATEGORIES["SYSTEM"],
        "priority": MessagePriority.LOW.value,
        "payload": {"agent_id": agent_id},
    }


# Protocol version and constants
__version__ = PROTOCOL_VERSION
__all__ = [
    "CrossAgentCommunicator",
    "AgentMessage",
    "AgentResponse",
    "AgentStatus",
    "MessagePriority",
    "AgentStatus",
    "MessageValidator",
    "AuthenticationManager",
    "create_flask_integration",
    "create_fastapi_integration",
    "create_agent_communicator",
    "validate_message_format",
    "create_heartbeat_message",
    "PROTOCOL_VERSION",
    "MESSAGE_TYPES",
    "COMMAND_CATEGORIES",
]
