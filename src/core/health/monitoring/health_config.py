
# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration and data models for the new health monitoring system."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional


class HealthStatus(Enum):
    """Agent health status levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    WARNING = "warning"
    CRITICAL = "critical"
    OFFLINE = "offline"


class HealthMetricType(Enum):
    """Types of health metrics"""
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
    """Individual health metric data"""
    agent_id: str
    metric_type: HealthMetricType
    value: float
    unit: str
    timestamp: datetime
    threshold: Optional[float] = None
    status: HealthStatus = HealthStatus.GOOD


@dataclass
class HealthAlert:
    """Health alert information"""
    alert_id: str
    agent_id: str
    severity: str
    message: str
    metric_type: HealthMetricType
    current_value: float
    threshold: float
    timestamp: datetime
    acknowledged: bool = False
    resolved: bool = False


@dataclass
class HealthThreshold:
    """Health threshold configuration"""
    metric_type: HealthMetricType
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str


@dataclass
class HealthSnapshot:
    """Complete health snapshot for an agent"""
    agent_id: str
    timestamp: datetime
    overall_status: HealthStatus
    health_score: float  # 0-100
    metrics: Dict[HealthMetricType, HealthMetric] = field(default_factory=dict)
    alerts: List[HealthAlert] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


def initialize_default_thresholds() -> Dict[HealthMetricType, HealthThreshold]:
    """Create default health thresholds"""
    thresholds = [
        HealthThreshold(
            HealthMetricType.RESPONSE_TIME,
            warning_threshold=1000.0,
            critical_threshold=5000.0,
            unit="ms",
            description="Response time threshold",
        ),
        HealthThreshold(
            HealthMetricType.MEMORY_USAGE,
            warning_threshold=80.0,
            critical_threshold=95.0,
            unit="%",
            description="Memory usage threshold",
        ),
        HealthThreshold(
            HealthMetricType.CPU_USAGE,
            warning_threshold=85.0,
            critical_threshold=95.0,
            unit="%",
            description="CPU usage threshold",
        ),
        HealthThreshold(
            HealthMetricType.ERROR_RATE,
            warning_threshold=5.0,
            critical_threshold=15.0,
            unit="%",
            description="Error rate threshold",
        ),
        HealthThreshold(
            HealthMetricType.TASK_COMPLETION_RATE,
            warning_threshold=90.0,
            critical_threshold=75.0,
            unit="%",
            description="Task completion rate threshold",
        ),
        HealthThreshold(
            HealthMetricType.HEARTBEAT_FREQUENCY,
            warning_threshold=120.0,
            critical_threshold=300.0,
            unit="seconds",
            description="Heartbeat frequency threshold",
        ),
        HealthThreshold(
            HealthMetricType.CONTRACT_SUCCESS_RATE,
            warning_threshold=85.0,
            critical_threshold=70.0,
            unit="%",
            description="Contract success rate threshold",
        ),
        HealthThreshold(
            HealthMetricType.COMMUNICATION_LATENCY,
            warning_threshold=500.0,
            critical_threshold=2000.0,
            unit="ms",
            description="Communication latency threshold",
        ),
    ]
    return {t.metric_type: t for t in thresholds}
