"""Health monitoring metric models and enums."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class HealthStatus(Enum):
    """Agent health status levels."""

    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class HealthMetricType(Enum):
    """Types of health metrics tracked for agents."""

    RESPONSE_TIME = "response_time"
    MEMORY_USAGE = "memory_usage"
    CPU_USAGE = "cpu_usage"
    ERROR_RATE = "error_rate"
    TASK_COMPLETION_RATE = "task_completion_rate"
    HEARTBEAT_FREQUENCY = "heartbeat_frequency"
    CONTRACT_SUCCESS_RATE = "contract_success_rate"
    COMMUNICATION_LATENCY = "communication_latency"


@dataclass
class HealthMetric:
    """Individual health metric data."""

    agent_id: str
    metric_type: HealthMetricType
    value: float
    unit: str
    timestamp: datetime
    threshold: Optional[float] = None
    status: HealthStatus = HealthStatus.GOOD


@dataclass
class HealthSnapshot:
    """Complete health snapshot for an agent."""

    agent_id: str
    timestamp: datetime
    overall_status: HealthStatus
    health_score: float  # 0-100
    metrics: Dict[HealthMetricType, HealthMetric] = field(default_factory=dict)
    alerts: List["HealthAlert"] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)

