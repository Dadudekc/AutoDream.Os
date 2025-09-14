#!/usr/bin/env python3
"""
Consolidated Analytics Service - V2 Compliant
============================================

Consolidated analytics service coordinating all analytics components.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-3 (Infrastructure Specialist)
License: MIT
"""

import logging
import threading
from typing import Any, Dict, Optional

from .automated_reporting import AutomatedReportingSystem
from .metrics_collector import MetricsCollector
from .performance_dashboard import PerformanceDashboard
from .usage_analytics import UsageAnalyticsEngine

logger = logging.getLogger(__name__)


class ConsolidatedAnalyticsService:
    """Consolidated analytics service coordinating all analytics components."""

    def __init__(self):
        # Initialize components
        self.metrics_collector = MetricsCollector()
        self.usage_analytics = UsageAnalyticsEngine()
        self.performance_dashboard = PerformanceDashboard(
            self.metrics_collector, 
            self.usage_analytics
        )
        self.reporting_system = AutomatedReportingSystem(
            self.metrics_collector,
            self.usage_analytics,
            self.performance_dashboard
        )

        # Service state
        self._running = False
        self._collection_thread: Optional[threading.Thread] = None

    def start(self) -> None:
        """Start the analytics service."""
        try:
            self._running = True
            logger.info("Analytics service started")
        except Exception as e:
            logger.error(f"Failed to start analytics service: {e}")

    def stop(self) -> None:
        """Stop the analytics service."""
        try:
            self._running = False
            logger.info("Analytics service stopped")
        except Exception as e:
            logger.error(f"Failed to stop analytics service: {e}")

    def generate_report(self, report_type: str = "daily") -> Dict[str, Any]:
        """Generate analytics report."""
        try:
            return self.reporting_system.generate_business_intelligence_report(report_type)
        except Exception as e:
            logger.error(f"Failed to generate report: {e}")
            return {"status": "error", "error": str(e)}

    def get_dashboard_data(self, dashboard_type: str = "overview") -> Dict[str, Any]:
        """Get dashboard data."""
        try:
            return self.performance_dashboard.generate_dashboard_data(dashboard_type)
        except Exception as e:
            logger.error(f"Failed to get dashboard data: {e}")
            return {"status": "error", "error": str(e)}

    def collect_metric(self, metric_name: str, value: Any, **kwargs) -> None:
        """Collect a metric."""
        try:
            self.metrics_collector.collect_metric(metric_name, value, **kwargs)
        except Exception as e:
            logger.error(f"Failed to collect metric: {e}")

    def get_service_status(self) -> Dict[str, Any]:
        """Get service status."""
        return {
            "running": self._running,
            "metrics_count": len(self.metrics_collector.get_all_metric_names()),
            "collection_stats": self.metrics_collector.get_collection_stats()
        }


# Factory function
def create_consolidated_analytics_service() -> ConsolidatedAnalyticsService:
    """Factory function to create consolidated analytics service."""
    return ConsolidatedAnalyticsService()


# Global service instance
_global_analytics_service: Optional[ConsolidatedAnalyticsService] = None


def get_consolidated_analytics_service() -> ConsolidatedAnalyticsService:
    """Get or create the global consolidated analytics service instance."""
    global _global_analytics_service
    
    if _global_analytics_service is None:
        _global_analytics_service = create_consolidated_analytics_service()
    
    return _global_analytics_service


def get_analytics_service() -> ConsolidatedAnalyticsService:
    """Alias for get_consolidated_analytics_service."""
    return get_consolidated_analytics_service()


# Export
__all__ = [
    "ConsolidatedAnalyticsService", 
    "create_consolidated_analytics_service",
    "get_consolidated_analytics_service",
    "get_analytics_service"
]