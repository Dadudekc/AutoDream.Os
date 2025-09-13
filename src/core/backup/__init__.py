#!/usr/bin/env python3
"""
Backup Monitoring System - V2 Compliant Consolidation
====================================================

Consolidated backup monitoring system providing unified monitoring functionality.
V2 COMPLIANT: This module consolidates 993 lines into modular components.

Previously monolithic implementation refactored into focused modules:
- models/ (data models and enums)
- database/ (database management)
- alerts/ (alert system)
- backup_monitoring_orchestrator.py (main coordinator)

All modules are V2 compliant (<300 lines, focused responsibilities).

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from .alerts import BackupAlertSystem
from .backup_monitoring_orchestrator import (
    BackupMonitoringOrchestrator,
    create_backup_monitoring_orchestrator,
    start_backup_monitoring,
)
from .database import BackupMonitoringDatabase
from .models import (
    Alert,
    AlertHistory,
    AlertSeverity,
    AlertStatus,
    AlertType,
    HealthCheck,
    HealthCheckStatus,
    HealthCheckType,
    MetricType,
    MonitoringConfig,
    MonitoringDashboard,
    MonitoringMetric,
    MonitoringStatus,
)

# Maintain backward compatibility
__all__ = [
    # Main orchestrator
    "BackupMonitoringOrchestrator",
    "create_backup_monitoring_orchestrator",
    "start_backup_monitoring",
    # Database
    "BackupMonitoringDatabase",
    # Alert system
    "BackupAlertSystem",
    # Models and enums
    "Alert",
    "AlertHistory",
    "AlertSeverity",
    "AlertStatus",
    "AlertType",
    "HealthCheck",
    "HealthCheckStatus",
    "HealthCheckType",
    "MetricType",
    "MonitoringConfig",
    "MonitoringDashboard",
    "MonitoringMetric",
    "MonitoringStatus",
]
