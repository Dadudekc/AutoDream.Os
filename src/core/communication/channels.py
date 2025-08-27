"""Channel definitions and enums for communication system."""
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict


class ChannelType(Enum):
    """Supported communication channel types."""
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
    """Represents a configured communication channel."""
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
