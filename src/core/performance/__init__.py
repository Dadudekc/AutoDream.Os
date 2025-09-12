#!/usr/bin/env python3
"""
Performance Monitoring System - V2 Compliant Consolidation
=========================================================

Consolidated performance monitoring system providing unified dashboard functionality.
V2 COMPLIANT: This module consolidates 1014 lines into modular components.

Previously monolithic implementation refactored into focused modules:
- models/ (data models and enums)
- performance_orchestrator.py (main coordinator)

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from .performance_orchestrator import PerformanceMonitoringOrchestrator, create_performance_orchestrator
from .models import (
    Alert,
    AlertSeverity,
    AlertStatus,
    ConsolidationPhase,
    DashboardMetric,
    DashboardType,
    DashboardWidget,
    MetricType,
    PerformanceReport,
)

# Maintain backward compatibility by re-exporting key classes
__all__ = [
    # Main orchestrator
    "PerformanceMonitoringOrchestrator",
    "create_performance_orchestrator",

    # Models
    "DashboardMetric",
    "DashboardWidget",
    "ConsolidationPhase",
    "Alert",
    "PerformanceReport",

    # Enums
    "DashboardType",
    "MetricType",
    "AlertSeverity",
    "AlertStatus",
]

