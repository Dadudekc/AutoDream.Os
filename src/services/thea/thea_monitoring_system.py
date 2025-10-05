#!/usr/bin/env python3
"""
Thea Monitoring System - Unified Interface
==========================================

Unified interface for Thea monitoring system.
Provides backward compatibility and easy access to all monitoring components.

V2 Compliance: ≤400 lines, unified interface module
Author: Agent-6 (Quality Assurance Specialist)
"""

from .thea_monitoring_analytics import TheaMonitoringAnalytics
from .thea_monitoring_core import TheaMonitoringCore
from .thea_monitoring_models import PerformanceMetrics, SystemHealth


class TheaMonitoringSystem:
    """
    Unified Thea monitoring system.

    Integrates core monitoring, analytics, and reporting capabilities.
    """

    def __init__(self, log_dir: str = "logs/thea_monitoring"):
        """Initialize monitoring system."""
        self.core = TheaMonitoringCore(log_dir)
        self.analytics = TheaMonitoringAnalytics(
            self.core.performance_data, self.core.system_health_data
        )

    def start_monitoring(self) -> bool:
        """Start monitoring system."""
        return self.core.start_monitoring()

    def stop_monitoring(self) -> bool:
        """Stop monitoring system."""
        return self.core.stop_monitoring()

    def log_operation(
        self,
        operation: str,
        duration: float,
        success: bool,
        response_length: int = 0,
        error_message: str = None,
    ) -> None:
        """Log operation performance."""
        self.core.log_operation(operation, duration, success, response_length, error_message)

    def get_performance_summary(self, hours: int = 24) -> dict[str, Any]:
        """Get performance summary."""
        return self.analytics.get_performance_summary(hours)

    def get_system_health_summary(self, hours: int = 24) -> dict[str, Any]:
        """Get system health summary."""
        return self.analytics.get_system_health_summary(hours)

    def export_data(self, output_dir: str = "exports/thea_monitoring") -> dict[str, Any]:
        """Export monitoring data."""
        return self.analytics.export_data(output_dir)


def create_monitoring_system(log_dir: str = "logs/thea_monitoring") -> TheaMonitoringSystem:
    """Create Thea monitoring system instance."""
    return TheaMonitoringSystem(log_dir)


# Re-export all components for backward compatibility
__all__ = [
    "TheaMonitoringSystem",
    "TheaMonitoringCore",
    "TheaMonitoringAnalytics",
    "PerformanceMetrics",
    "SystemHealth",
    "create_monitoring_system",
]
