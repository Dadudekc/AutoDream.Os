#!/usr/bin/env python3
"""
Cross-Agent Communication Protocol
Simplified orchestrator coordinating authentication, routing, handshake,
and logging modules.
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional, Callable
import uuid

from .authentication import AuthenticationManager
from .logging_utils import get_logger
from .routing import MessageRouter
from .handshake import HandshakeNegotiator

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


@dataclass
class AgentMessage:
    """Standardized message format for cross-agent communication."""

    message_id: str
    timestamp: str
    sender_id: str
    recipient_id: Optional[str]
    message_type: str
    payload: Dict[str, Any]
    requires_response: bool = False

    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


@dataclass
class AgentResponse:
    """Standardized response format for cross-agent communication."""

    response_id: str
    original_message_id: str
    timestamp: str
    sender_id: str
    recipient_id: str
    success: bool
    payload: Dict[str, Any] | None = None

    def __post_init__(self):
        if not self.response_id:
            self.response_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat()


class CrossAgentCommunicator:
    """Coordinates authentication, routing, handshake, and logging."""

    def __init__(self, agent_id: str, config: Dict[str, Any] | None = None):
        self.agent_id = agent_id
        self.config = config or {}
        self.logger = get_logger(f"CrossAgentCommunicator.{agent_id}")
        self.auth_manager = AuthenticationManager(self.config.get("secret_key"))
        self.router = MessageRouter(self.logger, self._send_response_internal)
        self.handshake = HandshakeNegotiator(
            self.auth_manager, PROTOCOL_VERSION, self.logger
        )

    def register_message_handler(
        self, message_type: str, handler: Callable[[Dict[str, Any]], Any]
    ):
        self.router.register_handler(message_type, handler)

    def route_message(self, message: Dict[str, Any]):
        """Route a message through the internal router."""
        self.router.route(message)

    def send_message(
        self,
        recipient_id: str,
        message_type: str,
        payload: Dict[str, Any] | None = None,
        requires_response: bool = False,
    ):
        """Create and route a message to the appropriate handler."""
        message = AgentMessage(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            sender_id=self.agent_id,
            recipient_id=recipient_id,
            message_type=message_type,
            payload=payload or {},
            requires_response=requires_response,
        )
        self.logger.info(f"Sending {message_type} to {recipient_id}")
        self.route_message(asdict(message))

    def _send_response_internal(
        self,
        original_message: Dict[str, Any],
        success: bool,
        payload: Dict[str, Any] | None = None,
    ):
        response = AgentResponse(
            response_id=str(uuid.uuid4()),
            original_message_id=original_message["message_id"],
            timestamp=datetime.utcnow().isoformat(),
            sender_id=self.agent_id,
            recipient_id=original_message["sender_id"],
            success=success,
            payload=payload or {},
        )
        self.logger.info(
            f"Responding to {original_message['sender_id']} with success={success}"
        )
        return asdict(response)

    def negotiate_handshake(self, peer_id: str, token: str, version: str) -> bool:
        """Perform a handshake negotiation with another agent."""
        return self.handshake.negotiate(peer_id, token, version)
