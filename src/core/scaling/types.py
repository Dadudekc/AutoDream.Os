from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ScalingStrategy(Enum):
    """Available scaling strategies."""

    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    IP_HASH = "ip_hash"
    LEAST_RESPONSE_TIME = "least_response_time"
    CONSISTENT_HASH = "consistent_hash"


class ScalingStatus(Enum):
    """Possible status values for scaling actions."""

    IDLE = "idle"
    SCALING_UP = "scaling_up"
    SCALING_DOWN = "scaling_down"
    OPTIMIZING = "optimizing"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class ScalingConfig:
    """Configuration used by the scaling system."""

    min_instances: int = 1
    max_instances: int = 10
    target_cpu_utilization: float = 70.0
    target_memory_utilization: float = 80.0
    scaling_cooldown: int = 300
    scaling_strategy: ScalingStrategy = ScalingStrategy.ROUND_ROBIN


@dataclass
class ScalingMetrics:
    """Observed metrics used for scaling decisions."""

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
    """Decision produced by the scaling decider."""

    decision_id: str
    action: str
    reason: str
    current_metrics: ScalingMetrics
    confidence: float
    timestamp: float
