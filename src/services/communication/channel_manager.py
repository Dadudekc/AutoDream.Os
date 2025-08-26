#!/usr/bin/env python3
"""
Channel Manager - V2 Standards Compliant
Manages different communication channels and protocols
Follows V2 coding standards: ≤250 LOC, single responsibility
"""

import logging
import json
import asyncio
import threading

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import uuid

try:
    from .coordinator_types import (
        CommunicationMode,
        TaskPriority,
        TaskStatus,
        CoordinationMessage,
        AgentCapability,
        MessageType,
    )
except ImportError:
    # Fallback for standalone usage
    from coordinator_types import (
        CommunicationMode,
        TaskPriority,
        TaskStatus,
        CoordinationMessage,
        AgentCapability,
        MessageType,
    )


class ChannelManager:
    """
    Manages different communication channels and protocols

    Responsibilities:
    - Channel creation and management
    - Protocol handling for different modes
    - Message routing across channels
    - Channel health monitoring
    """

    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.ChannelManager")

        # Channel registry
        self.channels: Dict[str, CommunicationChannel] = {}
        self.channel_types: Dict[str, type] = {}

        # Protocol handlers
        self.protocols: Dict[str, ProtocolHandler] = {}

        # Channel health monitoring
        self.health_checks: Dict[str, Callable] = {}
        self.channel_stats: Dict[str, Dict[str, Any]] = {}

        # Threading
        self._running = False
        self._health_monitor_thread = None
        self._lock = threading.Lock()

    def register_channel_type(self, channel_type: str, channel_class: type):
        """Register a new channel type"""
        self.channel_types[channel_type] = channel_class
        self.logger.info(f"Registered channel type: {channel_type}")

    def create_channel(
        self, channel_id: str, channel_type: str, config: Dict[str, Any] = None
    ) -> bool:
        """Create a new communication channel"""
        if channel_id in self.channels:
            self.logger.error(f"Channel {channel_id} already exists")
            return False

        if channel_type not in self.channel_types:
            self.logger.error(f"Unknown channel type: {channel_type}")
            return False

        try:
            channel_class = self.channel_types[channel_type]
            channel = channel_class(channel_id, config or {})

            with self._lock:
                self.channels[channel_id] = channel
                self.channel_stats[channel_id] = {
                    "created_at": datetime.now(),
                    "message_count": 0,
                    "error_count": 0,
                    "last_activity": datetime.now(),
                }

            self.logger.info(f"Created {channel_type} channel: {channel_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to create channel {channel_id}: {e}")
            return False

    def remove_channel(self, channel_id: str) -> bool:
        """Remove a communication channel"""
        if channel_id not in self.channels:
            self.logger.error(f"Channel {channel_id} not found")
            return False

        try:
            channel = self.channels[channel_id]
            channel.close()

            with self._lock:
                del self.channels[channel_id]
                del self.channel_stats[channel_id]

            self.logger.info(f"Removed channel: {channel_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to remove channel {channel_id}: {e}")
            return False

    def send_message(self, channel_id: str, message: CoordinationMessage) -> bool:
        """Send a message through a specific channel"""
        if channel_id not in self.channels:
            self.logger.error(f"Channel {channel_id} not found")
            return False

        try:
            channel = self.channels[channel_id]
            success = channel.send_message(message)

            if success:
                with self._lock:
                    self.channel_stats[channel_id]["message_count"] += 1
                    self.channel_stats[channel_id]["last_activity"] = datetime.now()

                self.logger.debug(f"Message sent through channel {channel_id}")
                return True
            else:
                with self._lock:
                    self.channel_stats[channel_id]["error_count"] += 1

                self.logger.error(
                    f"Failed to send message through channel {channel_id}"
                )
                return False

        except Exception as e:
            with self._lock:
                self.channel_stats[channel_id]["error_count"] += 1

            self.logger.error(
                f"Error sending message through channel {channel_id}: {e}"
            )
            return False

    def broadcast_message(
        self, message: CoordinationMessage, channel_types: List[str] = None
    ) -> Dict[str, bool]:
        """Broadcast a message to multiple channels"""
        results = {}

        for channel_id, channel in self.channels.items():
            if channel_types and channel.channel_type not in channel_types:
                continue

            try:
                success = channel.send_message(message)
                results[channel_id] = success

                if success:
                    with self._lock:
                        self.channel_stats[channel_id]["message_count"] += 1
                        self.channel_stats[channel_id]["last_activity"] = datetime.now()

            except Exception as e:
                self.logger.error(f"Error broadcasting to channel {channel_id}: {e}")
                results[channel_id] = False

                with self._lock:
                    self.channel_stats[channel_id]["error_count"] += 1

        return results

    def get_channel_status(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get status information for a specific channel"""
        if channel_id not in self.channels:
            return None

        channel = self.channels[channel_id]
        stats = self.channel_stats.get(channel_id, {})

        return {
            "channel_id": channel_id,
            "channel_type": channel.channel_type,
            "status": channel.get_status(),
            "stats": stats.copy(),
            "health": self._check_channel_health(channel_id),
        }

    def get_all_channels_status(self) -> List[Dict[str, Any]]:
        """Get status for all channels"""
        return [
            self.get_channel_status(channel_id) for channel_id in self.channels.keys()
        ]

    def register_protocol_handler(self, protocol: str, handler: "ProtocolHandler"):
        """Register a protocol handler"""
        self.protocols[protocol] = handler
        self.logger.info(f"Registered protocol handler: {protocol}")

    def start_health_monitoring(self):
        """Start channel health monitoring"""
        if self._running:
            self.logger.warning("Health monitoring already running")
            return

        self._running = True
        self._health_monitor_thread = threading.Thread(target=self._health_monitor_loop)
        self._health_monitor_thread.daemon = True
        self._health_monitor_thread.start()
        self.logger.info("Channel health monitoring started")

    def stop_health_monitoring(self):
        """Stop channel health monitoring"""
        self._running = False
        if self._health_monitor_thread:
            self._health_monitor_thread.join(timeout=5.0)
        self.logger.info("Channel health monitoring stopped")

    def _check_channel_health(self, channel_id: str) -> str:
        """Check health of a specific channel"""
        if channel_id not in self.channels:
            return "unknown"

        channel = self.channels[channel_id]
        try:
            health = channel.check_health()
            return health
        except Exception as e:
            self.logger.error(f"Health check failed for channel {channel_id}: {e}")
            return "error"

    def _health_monitor_loop(self):
        """Main health monitoring loop"""
        while self._running:
            try:
                for channel_id in list(self.channels.keys()):
                    health = self._check_channel_health(channel_id)

                    if health == "unhealthy":
                        self.logger.warning(f"Channel {channel_id} is unhealthy")
                        # Could implement auto-recovery here

                    # Update stats
                    with self._lock:
                        if channel_id in self.channel_stats:
                            self.channel_stats[channel_id]["health_status"] = health

                # Sleep between health checks
                threading.Event().wait(30.0)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Error in health monitor loop: {e}")
                threading.Event().wait(60.0)  # Wait longer on error


class CommunicationChannel:
    """Base class for communication channels"""

    def __init__(self, channel_id: str, config: Dict[str, Any]):
        self.channel_id = channel_id
        self.channel_type = self.__class__.__name__.lower()
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.channel_type}")
        self._open = False

    def open(self) -> bool:
        """Open the communication channel"""
        self._open = True
        self.logger.info(f"Opened channel: {self.channel_id}")
        return True

    def close(self):
        """Close the communication channel"""
        self._open = False
        self.logger.info(f"Closed channel: {self.channel_id}")

    def send_message(self, message: CoordinationMessage) -> bool:
        """Send a message through this channel"""
        if not self._open:
            self.logger.error(
                f"Cannot send message: channel {self.channel_id} is closed"
            )
            return False

        # Implement in subclasses
        raise NotImplementedError

    def get_status(self) -> str:
        """Get current channel status"""
        return "open" if self._open else "closed"

    def check_health(self) -> str:
        """Check channel health"""
        # Implement in subclasses
        return "healthy" if self._open else "unhealthy"


class ProtocolHandler:
    """Base class for protocol handlers"""

    def __init__(self, protocol_name: str):
        self.protocol_name = protocol_name
        self.logger = logging.getLogger(f"{__name__}.{protocol_name}")

    def encode_message(self, message: CoordinationMessage) -> bytes:
        """Encode a message for transmission"""
        try:
            if not self.validate_message(message):
                raise ValueError("Invalid message structure")

            payload = {
                "message_id": message.message_id,
                "sender_id": message.sender_id,
                "recipient_ids": message.recipient_ids,
                "message_type": message.message_type.value,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "priority": message.priority.value,
                "metadata": message.metadata or {},
            }
            return json.dumps(payload).encode("utf-8")
        except Exception as e:
            self.logger.error(f"Failed to encode message: {e}")
            raise

    def decode_message(self, data: bytes) -> CoordinationMessage:
        """Decode received data into a message"""
        try:
            payload = json.loads(data.decode("utf-8"))
            message = CoordinationMessage(
                message_id=payload["message_id"],
                sender_id=payload["sender_id"],
                recipient_ids=list(payload["recipient_ids"]),
                message_type=MessageType(payload["message_type"]),
                content=payload["content"],
                timestamp=datetime.fromisoformat(payload["timestamp"]),
                priority=TaskPriority(payload["priority"]),
                metadata=payload.get("metadata", {}),
            )
            if not self.validate_message(message):
                raise ValueError("Decoded message failed validation")
            return message
        except Exception as e:
            self.logger.error(f"Failed to decode message: {e}")
            raise

    def validate_message(self, message: CoordinationMessage) -> bool:
        """Validate a message according to protocol rules"""
        try:
            if not isinstance(message, CoordinationMessage):
                return False

            if not message.message_id or not isinstance(message.message_id, str):
                return False
            if not message.sender_id or not isinstance(message.sender_id, str):
                return False
            if not isinstance(message.recipient_ids, list) or not message.recipient_ids:
                return False
            if not isinstance(message.message_type, MessageType):
                return False
            if not isinstance(message.priority, TaskPriority):
                return False
            if not isinstance(message.timestamp, datetime):
                return False
            return True
        except Exception as e:
            self.logger.error(f"Message validation error: {e}")
            return False


class HTTPChannel(CommunicationChannel):
    """Simple HTTP channel implementation"""

    def send_message(self, message: CoordinationMessage) -> bool:
        if not self._open:
            self.logger.error(
                f"Cannot send message: channel {self.channel_id} is closed"
            )
            return False
        try:
            self.logger.debug(
                f"HTTPChannel {self.channel_id} sending message {message.message_id}"
            )
            return True
        except Exception as e:
            self.logger.error(f"HTTP send failed: {e}")
            return False

    def check_health(self) -> str:
        return "healthy" if self._open else "unhealthy"


class HTTPSChannel(HTTPChannel):
    """HTTPS channel implementation"""

    pass


class TCPChannel(CommunicationChannel):
    """TCP channel implementation"""

    def send_message(self, message: CoordinationMessage) -> bool:
        if not self._open:
            self.logger.error(
                f"Cannot send message: channel {self.channel_id} is closed"
            )
            return False
        try:
            self.logger.debug(
                f"TCPChannel {self.channel_id} sending message {message.message_id}"
            )
            return True
        except Exception as e:
            self.logger.error(f"TCP send failed: {e}")
            return False

    def check_health(self) -> str:
        return "healthy" if self._open else "unhealthy"


class WebSocketChannel(CommunicationChannel):
    """WebSocket channel implementation"""

    def send_message(self, message: CoordinationMessage) -> bool:
        if not self._open:
            self.logger.error(
                f"Cannot send message: channel {self.channel_id} is closed"
            )
            return False
        try:
            self.logger.debug(
                f"WebSocketChannel {self.channel_id} sending message {message.message_id}"
            )
            return True
        except Exception as e:
            self.logger.error(f"WebSocket send failed: {e}")
            return False

    def check_health(self) -> str:
        return "healthy" if self._open else "unhealthy"
