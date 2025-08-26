#!/usr/bin/env python3
"""
Communication Models - V2 Modular Architecture
=============================================

Data models and structures for the communication system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, Optional


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


@dataclass
class ChannelStats:
    """Channel statistics and metrics"""
    channel_id: str
    total_messages: int
    successful_messages: int
    failed_messages: int
    last_activity: str
    uptime_percentage: float
    average_response_time: float
    error_rate: float


@dataclass
class MessageMetrics:
    """Message processing metrics"""
    total_processed: int
    successful_delivery: int
    failed_delivery: int
    average_processing_time: float
    queue_size: int
    retry_count: int

