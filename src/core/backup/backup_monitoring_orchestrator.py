#!/usr/bin/env python3
"""
Backup Monitoring Orchestrator - V2 Compliant Redirect
======================================================

This module redirects to the new modular backup monitoring system.
V2 COMPLIANT: Under 50 lines, simple import redirect.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

# Import all components from the new modular backup monitoring system
from .monitoring import (
    BackupInfo,
    BackupMonitor,
    BackupStatus,
    MonitoringStatus,
    BackupMetric,
    BackupMetricsCollector,
    MetricSummary,
    MetricType,
    BackupMonitoringSystem
)

# For backward compatibility
BackupMonitoringOrchestrator = BackupMonitoringSystem

__all__ = [
    "BackupInfo",
    "BackupMonitor",
    "BackupStatus", 
    "MonitoringStatus",
    "BackupMetric",
    "BackupMetricsCollector",
    "MetricSummary",
    "MetricType",
    "BackupMonitoringSystem",
    "BackupMonitoringOrchestrator"
]