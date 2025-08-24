"""
Agent Health Monitor - Main Interface

This module provides a clean interface to the refactored health monitoring system.
All core functionality has been extracted into focused modules following SRP principles.

The refactored system includes:
- Core monitoring orchestration (monitoring_new.core)
- Health metrics collection (metrics.collector)
- Alerting and notifications (alerting.manager)
- Reporting and analytics (reporting.generator)
"""

from .health.monitoring_new.core import AgentHealthCoreMonitor
from .health.metrics.collector import HealthMetricsCollector
from .health.alerting.manager import HealthAlertingManager
from .health.reporting.generator import HealthReportingGenerator

# Re-export main classes for backward compatibility
__all__ = [
    'AgentHealthCoreMonitor',
    'HealthMetricsCollector', 
    'HealthAlertingManager',
    'HealthReportingGenerator'
]

# Convenience function to get a fully configured health monitoring system
def create_health_monitor(config=None):
    """
    Create a fully configured health monitoring system with all components.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        tuple: (core_monitor, metrics_collector, alerting_manager, reporting_generator)
    """
    core_monitor = AgentHealthCoreMonitor()
    metrics_collector = HealthMetricsCollector()
    alerting_manager = HealthAlertingManager()
    reporting_generator = HealthReportingGenerator()
    
    return core_monitor, metrics_collector, alerting_manager, reporting_generator
