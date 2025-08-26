#!/usr/bin/env python3
"""
Performance Models - Data Structures and Enums
=============================================

Performance system data models, enums, and data structures.
Follows V2 standards: focused data models only.

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class PerformanceLevel(Enum):
    """Performance classification levels."""
    NOT_READY = "not_ready"
    BASIC = "basic"
    STANDARD = "standard"
    GOOD = "good"
    EXCELLENT = "excellent"
    ENTERPRISE_READY = "enterprise_ready"
    PRODUCTION_READY = "production_ready"


class ValidationSeverity(Enum):
    """Validation rule severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class BenchmarkType(Enum):
    """Types of performance benchmarks."""
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    NETWORK = "network"
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    CONCURRENCY = "concurrency"
    STRESS = "stress"
    LOAD = "load"
    END_TO_END = "end_to_end"


class MetricType(Enum):
    """Types of performance metrics."""
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class PerformanceMetric:
    """Individual performance metric."""
    name: str
    value: Union[int, float]
    unit: str
    metric_type: MetricType
    timestamp: datetime
    labels: Dict[str, str]
    description: str


@dataclass
class ValidationRule:
    """Performance validation rule definition."""
    rule_name: str
    metric_name: str
    threshold: float
    operator: str  # 'gt', 'lt', 'eq', 'gte', 'lte'
    severity: ValidationSeverity
    description: str
    enabled: bool = True


@dataclass
class ValidationThreshold:
    """Performance threshold configuration."""
    metric_name: str
    warning_threshold: float
    critical_threshold: float
    unit: str
    description: str


@dataclass
class ConnectionPool:
    """Connection pool definition"""
    name: str
    max_connections: int
    active_connections: int
    idle_connections: int
    total_connections: int
    wait_time: float
    utilization: float
    health_status: str


@dataclass
class BenchmarkResult:
    """Benchmark result definition"""
    id: str
    name: str
    component: str
    start_time: str
    end_time: str
    duration: float
    iterations: int
    metrics: Dict[str, float]
    success: bool
    error_message: Optional[str]


@dataclass
class SystemPerformanceReport:
    """Comprehensive system performance report."""
    report_id: str
    timestamp: datetime
    system_health: str
    overall_performance_level: PerformanceLevel
    metrics_summary: Dict[str, Any]
    validation_results: List[Dict[str, Any]]
    benchmarks: List[BenchmarkResult]
    recommendations: List[str]
    alerts: List[str]


@dataclass
class PerformanceConfig:
    """Performance system configuration."""
    system_name: str
    validation_rules: List[ValidationRule]
    thresholds: List[ValidationThreshold]
    benchmark_configs: Dict[str, Any]
    monitoring_interval: float
    alerting_enabled: bool
    reporting_enabled: bool
    auto_optimization: bool


@dataclass
class PerformanceAlert:
    """Performance alert definition."""
    alert_id: str
    timestamp: datetime
    severity: ValidationSeverity
    metric_name: str
    current_value: float
    threshold_value: float
    message: str
    component: str
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None


@dataclass
class PerformanceOptimization:
    """Performance optimization recommendation."""
    optimization_id: str
    timestamp: datetime
    component: str
    current_performance: float
    target_performance: float
    improvement_potential: float
    recommendation: str
    estimated_effort: str
    priority: str
    implemented: bool = False
    implemented_at: Optional[datetime] = None
    implemented_by: Optional[str] = None


@dataclass
class PerformanceTrend:
    """Performance trend analysis."""
    metric_name: str
    time_period: str
    trend_direction: str  # 'improving', 'stable', 'declining'
    change_rate: float
    confidence: float
    data_points: int
    start_value: float
    end_value: float
    analysis_date: datetime


@dataclass
class ResourceUtilization:
    """Resource utilization metrics."""
    resource_name: str
    resource_type: str
    current_usage: float
    max_capacity: float
    utilization_percentage: float
    status: str
    last_updated: datetime
    trend: Optional[PerformanceTrend] = None


@dataclass
class PerformanceBaseline:
    """Performance baseline for comparison."""
    baseline_id: str
    name: str
    description: str
    created_at: datetime
    metrics: Dict[str, float]
    conditions: Dict[str, Any]
    is_active: bool = True
    version: str = "1.0"
