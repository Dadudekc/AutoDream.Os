"""
Agent Health Monitor - Main Interface

This module provides a clean interface to the refactored health monitoring
system. All core functionality has been extracted into focused modules
following SRP principles.

The refactored system includes:
- Core monitoring orchestration (monitoring_new.core)
- Health metrics collection (metrics.collector)
- Alerting utilities (alerting.*)
- Reporting and analytics (reporting.generator)
"""

from .health.monitoring_new.core import AgentHealthCoreMonitor
from .health.metrics.collector import HealthMetricsCollector
from .health.alerting import (
    generate_alert,
    send_alert_notifications,
    check_escalations,
)
from .health.reporting.generator import HealthReportingGenerator

# Re-export main classes for backward compatibility
__all__ = [
    'AgentHealthCoreMonitor',
    'HealthMetricsCollector',
    'HealthReportingGenerator',
    'generate_alert',
    'send_alert_notifications',
    'check_escalations',
]

# Convenience function to get a fully configured health monitoring system
def create_health_monitor(config=None):
    """
    Create a fully configured health monitoring system with all components.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        tuple: (core_monitor, metrics_collector, reporting_generator)
    """
    core_monitor = AgentHealthCoreMonitor()
    metrics_collector = HealthMetricsCollector()
    reporting_generator = HealthReportingGenerator()

    return core_monitor, metrics_collector, reporting_generator
