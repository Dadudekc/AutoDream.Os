#!/usr/bin/env python3
"""
Scaling Types - Agent Cellphone V2
==================================

Defines scaling-related enums and dataclasses.
Follows V2 standards: ≤50 LOC, SRP, OOP principles.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


class ScalingStrategy(Enum):
    """Horizontal scaling strategies"""
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    IP_HASH = "ip_hash"
    LEAST_RESPONSE_TIME = "least_response_time"
    CONSISTENT_HASH = "consistent_hash"


class ScalingStatus(Enum):
    """Scaling operation status"""
    IDLE = "idle"
    SCALING_UP = "scaling_up"
    SCALING_DOWN = "scaling_down"
    OPTIMIZING = "optimizing"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class LoadBalancerType(Enum):
    """Load balancer types"""
    APPLICATION = "application"
    NETWORK = "network"
    TRANSPORT = "transport"
    GLOBAL = "global"


@dataclass
class ScalingConfig:
    """Scaling configuration settings"""
    min_instances: int = 1
    max_instances: int = 10
    target_cpu_utilization: float = 70.0
    target_memory_utilization: float = 80.0
    scaling_cooldown: int = 300
    scaling_strategy: ScalingStrategy = ScalingStrategy.ROUND_ROBIN


@dataclass
class ScalingMetrics:
    """Scaling performance metrics"""
    current_instances: int
    target_instances: int
    cpu_utilization: float
    memory_utilization: float
    response_time: float
    throughput: float
    error_rate: float
    timestamp: float


@dataclass
class ScalingDecision:
    """Scaling decision data"""
    decision_id: str
    action: str
    reason: str
    current_metrics: ScalingMetrics
    target_metrics: ScalingMetrics
    confidence: float
    timestamp: float
