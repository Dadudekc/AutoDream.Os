"""
Agent Health Monitoring Package

This package contains modules for comprehensive agent health monitoring,
including core monitoring, metrics collection, alerting, and reporting.
"""

from .monitoring_new.core import (
    AgentHealthCoreMonitor,
    HealthStatus,
    HealthMetricType,
    HealthMetric,
    HealthSnapshot,
    HealthAlert,
    HealthThreshold,
)

from .metrics import (
    MetricSourceAdapter,
    SystemMetricsAdapter,
    MetricAggregator,
    AsyncScheduler,
    CollectorFacade,
    Metric,
)

from .alerting import (
    HealthAlertingManager,
    AlertSeverity,
    AlertStatus,
    NotificationChannel,
    EscalationLevel,
    AlertRule,
    NotificationConfig,
    EscalationPolicy,
)

from .reporting import (
    HealthReportingGenerator,
    ReportType,
    ReportFormat,
    ReportConfig,
    HealthReport,
    ReportGenerator,
    ReportFormatter,
    ReportDelivery,
)

__all__ = [
    # Core Monitoring
    "AgentHealthCoreMonitor",
    "HealthStatus",
    "HealthMetricType",
    "HealthMetric",
    "HealthSnapshot",
    "HealthAlert",
    "HealthThreshold",

    # Metrics Collection
    "MetricSourceAdapter",
    "SystemMetricsAdapter",
    "MetricAggregator",
    "AsyncScheduler",
    "CollectorFacade",
    "Metric",

    # Alerting
    "HealthAlertingManager",
    "AlertSeverity",
    "AlertStatus",
    "NotificationChannel",
    "EscalationLevel",
    "AlertRule",
    "NotificationConfig",
    "EscalationPolicy",

    # Reporting
    "HealthReportingGenerator",
    "ReportType",
    "ReportFormat",
    "ReportConfig",
    "HealthReport",
    "ReportGenerator",
    "ReportFormatter",
    "ReportDelivery",
]

__version__ = "1.0.0"
__author__ = "Agent-5 (Business Intelligence & Trading Specialist)"
__description__ = "Comprehensive agent health monitoring system"
