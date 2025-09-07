"""
Dashboard Engine - V2 Compliance Refactored
==========================================

Simplified core dashboard engine operations.
Refactored into modular architecture for V2 compliance.

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, List, Any, Optional

from .models import (
    PerformanceMetric,
    DashboardWidget,
    PerformanceAlert,
    DashboardConfig,
    PerformanceReport,
    MetricType,
)

# Import modular components
from .metric_manager import MetricManager
from .widget_manager import WidgetManager
from src.core.common.base_engine import BaseEngine


class DashboardEngine(BaseEngine):
    """Simplified core dashboard engine - V2 compliant."""

    def __init__(self) -> None:
        super().__init__()
        self.alerts: Dict[str, PerformanceAlert] = {}
        self.reports: Dict[str, PerformanceReport] = {}

        # Initialize modular components
        self.metric_manager = MetricManager()
        self.widget_manager = WidgetManager()

    # Delegate metric operations to MetricManager
    def add_metric(self, metric: PerformanceMetric) -> bool:
        """Add performance metric - simplified."""
        return self.metric_manager.add_metric(metric)

    def get_metric(self, metric_id: str) -> Optional[PerformanceMetric]:
        """Get performance metric by ID."""
        return self.metric_manager.get_metric(metric_id)

    def get_metrics_by_type(self, metric_type: MetricType) -> List[PerformanceMetric]:
        """Get metrics by type."""
        return self.metric_manager.get_metrics_by_type(metric_type)

    def update_metric(self, metric_id: str, updates: Dict[str, Any]) -> bool:
        """Update performance metric."""
        return self.metric_manager.update_metric(metric_id, updates)

    def remove_metric(self, metric_id: str) -> bool:
        """Remove performance metric."""
        return self.metric_manager.remove_metric(metric_id)

    def get_all_metrics(self) -> List[PerformanceMetric]:
        """Get all metrics."""
        return self.metric_manager.get_all_metrics()

    # Delegate widget operations to WidgetManager
    def add_widget(self, widget: DashboardWidget) -> bool:
        """Add dashboard widget - simplified."""
        return self.widget_manager.add_widget(widget)

    def get_widget(self, widget_id: str) -> Optional[DashboardWidget]:
        """Get dashboard widget by ID."""
        return self.widget_manager.get_widget(widget_id)

    def get_all_widgets(self) -> List[DashboardWidget]:
        """Get all widgets."""
        return self.widget_manager.get_all_widgets()

    def update_widget(self, widget_id: str, updates: Dict[str, Any]) -> bool:
        """Update dashboard widget."""
        return self.widget_manager.update_widget(widget_id, updates)

    def remove_widget(self, widget_id: str) -> bool:
        """Remove dashboard widget."""
        return self.widget_manager.remove_widget(widget_id)

    def add_config(self, config: DashboardConfig) -> bool:
        """Add dashboard configuration."""
        return self.widget_manager.add_config(config)

    def get_config(self, config_id: str) -> Optional[DashboardConfig]:
        """Get dashboard configuration by ID."""
        return self.widget_manager.get_config(config_id)

    def get_all_configs(self) -> List[DashboardConfig]:
        """Get all configurations."""
        return self.widget_manager.get_all_configs()

    def update_config(self, config_id: str, updates: Dict[str, Any]) -> bool:
        """Update dashboard configuration."""
        return self.widget_manager.update_config(config_id, updates)

    def remove_config(self, config_id: str) -> bool:
        """Remove dashboard configuration."""
        return self.widget_manager.remove_config(config_id)

    # Alert management
    def add_alert(self, alert: PerformanceAlert) -> bool:
        """Add performance alert - simplified."""
        try:
            if not alert or not alert.alert_id:
                self.logger.error("Invalid alert provided")
                return False

            self.alerts[alert.alert_id] = alert
            self.logger.info(f"Added alert: {alert.alert_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add alert: {e}")
            return False

    def get_alert(self, alert_id: str) -> Optional[PerformanceAlert]:
        """Get performance alert by ID."""
        return self.alerts.get(alert_id)

    def get_all_alerts(self) -> List[PerformanceAlert]:
        """Get all alerts."""
        return list(self.alerts.values())

    def remove_alert(self, alert_id: str) -> bool:
        """Remove performance alert."""
        try:
            if alert_id in self.alerts:
                del self.alerts[alert_id]
                self.logger.info(f"Removed alert: {alert_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove alert: {e}")
            return False

    # Report management
    def add_report(self, report: PerformanceReport) -> bool:
        """Add performance report - simplified."""
        try:
            if not report or not report.report_id:
                self.logger.error("Invalid report provided")
                return False

            self.reports[report.report_id] = report
            self.logger.info(f"Added report: {report.report_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add report: {e}")
            return False

    def get_report(self, report_id: str) -> Optional[PerformanceReport]:
        """Get performance report by ID."""
        return self.reports.get(report_id)

    def get_all_reports(self) -> List[PerformanceReport]:
        """Get all reports."""
        return list(self.reports.values())

    def remove_report(self, report_id: str) -> bool:
        """Remove performance report."""
        try:
            if report_id in self.reports:
                del self.reports[report_id]
                self.logger.info(f"Removed report: {report_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove report: {e}")
            return False

    # Status and summary methods
    def get_status(self) -> Dict[str, Any]:
        """Extend base status with dashboard-specific counters."""
        status = super().get_status()
        status.update(
            {
                "metrics_count": self.metric_manager.get_metrics_count(),
                "widgets_count": self.widget_manager.get_widgets_count(),
                "alerts_count": len(self.alerts),
                "reports_count": len(self.reports),
            }
        )
        return status

    def get_summary(self) -> Dict[str, Any]:
        """Get engine summary - simplified."""
        return {
            "metrics": self.metric_manager.get_metrics_summary(),
            "widgets": self.widget_manager.get_summary(),
            "alerts": {
                "total_alerts": len(self.alerts),
                "alert_levels": list(
                    set(alert.level.value for alert in self.alerts.values())
                ),
            },
            "reports": {
                "total_reports": len(self.reports),
                "report_types": list(
                    set(report.report_type for report in self.reports.values())
                ),
            },
        }

    def clear_resources(self) -> None:  # pragma: no cover - trivial
        """Clear all dashboard data."""
        self.metric_manager.clear_metrics()
        self.widget_manager.clear_all()
        self.alerts.clear()
        self.reports.clear()
        self.logger.info("Cleared all dashboard data")
