#!/usr/bin/env python3
"""
Analytics Package - V2 Compliant Modular BI System
==================================================

Modular business intelligence analytics system with clean architecture.
All components are V2 compliant with focused responsibilities under 300 lines.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

# Import all analytics components for easy access
from .automated_reporting import AutomatedReportingSystem, create_automated_reporting_system
from .consolidated_analytics_service import (
    ConsolidatedAnalyticsService,
    get_analytics_service,
    get_consolidated_analytics_service,
)
from .metrics_collector import MetricsCollector, create_metrics_collector
from .performance_dashboard import PerformanceDashboard, create_performance_dashboard
from .usage_analytics import UsageAnalyticsEngine, create_usage_analytics_engine

# Export all public interfaces
__all__ = [
    # Main service
    "ConsolidatedAnalyticsService",
    "get_consolidated_analytics_service",
    "get_analytics_service",

    # Core components
    "MetricsCollector",
    "UsageAnalyticsEngine",
    "PerformanceDashboard",
    "AutomatedReportingSystem",

    # Factory functions
    "create_metrics_collector",
    "create_usage_analytics_engine",
    "create_performance_dashboard",
    "create_automated_reporting_system",
]

