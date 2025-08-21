#!/usr/bin/env python3
"""
Unified Health Models - Consolidated Health Data Structures

This module provides unified health models to eliminate duplication.
Follows Single Responsibility Principle - only health data structures.
Architecture: Single Responsibility Principle - health models only
LOC: Target 200 lines (under 300 limit)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum


class HealthStatus(Enum):
    """Health status definitions"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"
    DEGRADED = "degraded"
    OFFLINE = "offline"


class HealthMetricType(Enum):
    """Health metric types"""
    SYSTEM_HEALTH = "system_health"
    AGENT_HEALTH = "agent_health"
    SERVICE_HEALTH = "service_health"
    NETWORK_HEALTH = "network_health"
    DATABASE_HEALTH = "database_health"
    PERFORMANCE_HEALTH = "performance_health"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


@dataclass
class HealthMetric:
    """Unified health metric definition"""
    metric_id: str
    metric_type: HealthMetricType
    name: str
    value: float
    unit: str
    status: HealthStatus
    timestamp: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthSnapshot:
    """Health snapshot at a point in time"""
    snapshot_id: str
    timestamp: float
    overall_status: HealthStatus
    metrics: Dict[str, HealthMetric]
    system_info: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthAlert:
    """Health alert definition"""
    alert_id: str
    severity: AlertSeverity
    title: str
    description: str
    metric_id: str
    current_value: float
    threshold_value: float
    timestamp: float
    acknowledged: bool = False
    resolved: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthThreshold:
    """Health threshold definition"""
    metric_type: HealthMetricType
    warning_threshold: float
    critical_threshold: float
    unit: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthReport:
    """Comprehensive health report"""
    report_id: str
    timestamp: float
    time_period: str
    overall_status: HealthStatus
    summary: Dict[str, Any]
    metrics: List[HealthMetric]
    alerts: List[HealthAlert]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthCheck:
    """Health check definition"""
    check_id: str
    name: str
    description: str
    check_type: str
    timeout: float
    retry_count: int
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class HealthCheckResult:
    """Health check result"""
    check_id: str
    timestamp: float
    success: bool
    response_time: float
    status: HealthStatus
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
