#!/usr/bin/env python3
"""
Multicast Routing System Models
===============================

Data models, enums, and dataclasses for the multicast routing system.

**Author:** Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
**Contract:** COORD-012 - Advanced Coordination Protocol Implementation
**Status:** MODULARIZED
**Target:** 1000+ msg/sec throughput (10x improvement)
"""

import asyncio
import threading
import time
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional, Callable, Set, Union
import uuid
import json
import hashlib

class MessageType(Enum):
    """Message types for multicast routing"""
    
    BROADCAST = "broadcast"           # Send to all agents
    MULTICAST = "multicast"          # Send to specific group
    UNICAST = "unicast"              # Send to single agent
    PRIORITY = "priority"            # High priority message
    BULK = "bulk"                    # Bulk data transfer
    CONTROL = "control"              # System control message


class MessagePriority(Enum):
    """Message priority levels"""
    
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5


class RoutingStrategy(Enum):
    """Multicast routing strategies"""
    
    ROUND_ROBIN = "round_robin"           # Distribute messages evenly
    PRIORITY_BASED = "priority_based"     # Route by message priority
    LOAD_BALANCED = "load_balanced"       # Balance load across agents
    GEOGRAPHIC = "geographic"             # Route by geographic proximity
    ADAPTIVE = "adaptive"                 # Dynamically adjust routing


@dataclass
class Message:
    """Represents a message for multicast routing"""
    
    message_id: str
    sender_id: str
    message_type: MessageType
    priority: MessagePriority
    content: Any
    recipients: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: int = 300  # Time to live in seconds
    retry_count: int = 0
    max_retries: int = 3
    status: str = "pending"
    routing_path: List[str] = field(default_factory=list)
    delivery_confirmations: Set[str] = field(default_factory=set)


@dataclass
class MessageBatch:
    """Represents a batch of messages for efficient routing"""
    
    batch_id: str
    messages: List[Message] = field(default_factory=list)
    strategy: RoutingStrategy = RoutingStrategy.ADAPTIVE
    max_size: int = 50
    priority_threshold: Optional[MessagePriority] = None
    time_window: Optional[float] = None  # seconds
    status: str = "pending"
    start_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    success_count: int = 0
    failure_count: int = 0
    total_processing_time: float = 0.0
    throughput: float = 0.0  # messages per second


@dataclass
class RoutingNode:
    """Represents a routing node in the multicast network"""
    
    node_id: str
    agent_id: str
    capabilities: List[str] = field(default_factory=list)
    load: float = 0.0  # Current load (0.0 to 1.0)
    latency: float = 0.0  # Network latency in milliseconds
    throughput: float = 0.0  # Messages per second capacity
    status: str = "active"
    last_heartbeat: datetime = field(default_factory=datetime.now)
    routing_table: Dict[str, List[str]] = field(default_factory=dict)


@dataclass
class RoutingMetrics:
    """Performance metrics for routing operations"""
    
    total_messages: int = 0
    completed_messages: int = 0
    failed_messages: int = 0
    current_throughput: float = 0.0
    average_latency: float = 0.0
    success_rate: float = 0.0
    batch_efficiency: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class BatchConfiguration:
    """Configuration for message batching"""
    
    max_batch_size: int = 50
    batch_timeout: float = 10.0  # seconds
    priority_threshold: Optional[MessagePriority] = None
    time_window: Optional[float] = None
    strategy: RoutingStrategy = RoutingStrategy.ADAPTIVE


@dataclass
class NetworkTopology:
    """Network topology information for routing"""
    
    nodes: Dict[str, RoutingNode] = field(default_factory=dict)
    connections: Dict[str, List[str]] = field(default_factory=dict)
    routing_table: Dict[str, List[str]] = field(default_factory=dict)
    load_distribution: Dict[str, float] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)
