#!/usr/bin/env python3
"""
Multicast Routing System Package
================================

Modularized multicast routing system package.

**Author:** Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
**Contract:** COORD-012 - Advanced Coordination Protocol Implementation
**Status:** MODULARIZED
**Target:** 1000+ msg/sec throughput (10x improvement)
"""

from .models import (
    MessageType,
    MessagePriority,
    RoutingStrategy,
    Message,
    MessageBatch,
    RoutingNode,
    RoutingMetrics,
    BatchConfiguration,
    NetworkTopology
)

from .routing_engine import MulticastRoutingEngine
from .batch_processor import MessageBatchProcessor
from .main import MulticastRoutingSystem

__version__ = "2.0.0"
__author__ = "Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)"
__status__ = "MODULARIZED"

__all__ = [
    'MessageType',
    'MessagePriority',
    'RoutingStrategy',
    'Message',
    'MessageBatch',
    'RoutingNode',
    'RoutingMetrics',
    'BatchConfiguration',
    'NetworkTopology',
    'MulticastRoutingEngine',
    'MessageBatchProcessor',
    'MulticastRoutingSystem'
]
