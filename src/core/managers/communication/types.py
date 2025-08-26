#!/usr/bin/env python3
"""
Communication Types - V2 Modular Architecture
============================================

Type definitions and enums for the communication system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4H - Communication Manager Modularization
License: MIT
"""

from enum import Enum
from typing import Dict, Any, Optional, Union


class CommunicationTypes:
    """Communication system type definitions"""
    
    class MessageDirection(Enum):
        """Message direction enumeration"""
        INCOMING = "incoming"
        OUTGOING = "outgoing"
        BIDIRECTIONAL = "bidirectional"
    
    class ChannelStatus(Enum):
        """Channel status enumeration"""
        ACTIVE = "active"
        INACTIVE = "inactive"
        ERROR = "error"
        CLOSED = "closed"
        MAINTENANCE = "maintenance"
    
    class UnifiedMessagePriority(Enum):
        """Message priority enumeration"""
        LOW = "low"
        NORMAL = "normal"
        HIGH = "high"
        CRITICAL = "critical"
    
    class RoutingStrategy(Enum):
        """Routing strategy enumeration"""
        DIRECT = "direct"
        LOAD_BALANCED = "load_balanced"
        PRIORITY_BASED = "priority_based"
        PREDICTIVE = "predictive"
        FAILOVER = "failover"
    
    class OptimizationType(Enum):
        """Optimization type enumeration"""
        PERFORMANCE = "performance"
        RELIABILITY = "reliability"
        EFFICIENCY = "efficiency"
        COST = "cost"
        LATENCY = "latency"


class CommunicationConfig:
    """Communication system configuration constants"""
    
    # Default timeouts
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_RETRY_COUNT = 3
    DEFAULT_PING_INTERVAL = 30
    DEFAULT_PING_TIMEOUT = 10
    
    # Message limits
    MAX_MESSAGES = 10000
    MESSAGE_RETENTION_HOURS = 24
    
    # Connection limits
    MAX_CONCURRENT_CONNECTIONS = 100
    MAX_WEBSOCKET_CONNECTIONS = 50
    
    # Performance thresholds
    HIGH_ERROR_THRESHOLD = 10
    LOAD_BALANCE_THRESHOLD = 100
    SUCCESS_RATE_THRESHOLD = 0.95

