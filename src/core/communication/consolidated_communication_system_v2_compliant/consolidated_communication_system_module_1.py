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