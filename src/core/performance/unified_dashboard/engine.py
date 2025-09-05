"""
Dashboard Engine - KISS Simplified
=================================

Simplified core dashboard engine operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined engine logic.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import time
from .models import (
    PerformanceMetric, DashboardWidget, PerformanceAlert, DashboardConfig,
    PerformanceReport, MetricType, AlertLevel, DashboardStatus
)


class DashboardEngine:
    """Simplified core dashboard engine."""
    
    def __init__(self):
        """Initialize dashboard engine."""
        self.logger = logging.getLogger(__name__)
        self.metrics: Dict[str, PerformanceMetric] = {}
        self.widgets: Dict[str, DashboardWidget] = {}
        self.alerts: Dict[str, PerformanceAlert] = {}
        self.configs: Dict[str, DashboardConfig] = {}
        self.reports: Dict[str, PerformanceReport] = {}
        self.is_initialized = False
        self.status = DashboardStatus.INACTIVE
    
    def initialize(self) -> bool:
        """Initialize the engine - simplified."""
        try:
            self.is_initialized = True
            self.status = DashboardStatus.ACTIVE
            self.logger.info("Dashboard Engine initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Dashboard Engine: {e}")
            return False
    
    def add_metric(self, metric: PerformanceMetric) -> bool:
        """Add performance metric - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine not initialized")
            
            self.metrics[metric.metric_id] = metric
            self.logger.debug(f"Added metric: {metric.metric_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding metric: {e}")
            return False
    
    def get_metric(self, metric_id: str) -> Optional[PerformanceMetric]:
        """Get performance metric - simplified."""
        return self.metrics.get(metric_id)
    
    def get_metrics(self, metric_type: MetricType = None, hours: int = 24) -> List[PerformanceMetric]:
        """Get metrics - simplified."""
        try:
            if not self.is_initialized:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            metrics = list(self.metrics.values())
            
            # Filter by time
            metrics = [m for m in metrics if m.timestamp >= cutoff_time]
            
            # Filter by type if specified
            if metric_type:
                metrics = [m for m in metrics if m.metric_type == metric_type]
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error getting metrics: {e}")
            return []
    
    def add_widget(self, widget: DashboardWidget) -> bool:
        """Add dashboard widget - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine not initialized")
            
            self.widgets[widget.widget_id] = widget
            self.logger.debug(f"Added widget: {widget.widget_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding widget: {e}")
            return False
    
    def get_widget(self, widget_id: str) -> Optional[DashboardWidget]:
        """Get dashboard widget - simplified."""
        return self.widgets.get(widget_id)
    
    def get_widgets(self) -> List[DashboardWidget]:
        """Get all widgets - simplified."""
        return list(self.widgets.values())
    
    def add_alert(self, alert: PerformanceAlert) -> bool:
        """Add performance alert - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine not initialized")
            
            self.alerts[alert.alert_id] = alert
            self.logger.debug(f"Added alert: {alert.alert_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding alert: {e}")
            return False
    
    def get_alerts(self, alert_level: AlertLevel = None, hours: int = 24) -> List[PerformanceAlert]:
        """Get alerts - simplified."""
        try:
            if not self.is_initialized:
                return []
            
            cutoff_time = datetime.now() - timedelta(hours=hours)
            alerts = list(self.alerts.values())
            
            # Filter by time
            alerts = [a for a in alerts if a.timestamp >= cutoff_time]
            
            # Filter by level if specified
            if alert_level:
                alerts = [a for a in alerts if a.level == alert_level]
            
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error getting alerts: {e}")
            return []
    
    def create_report(self, report_type: str, hours: int = 24) -> Optional[PerformanceReport]:
        """Create performance report - simplified."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Engine not initialized")
            
            # Get metrics and alerts for the time period
            metrics = self.get_metrics(hours=hours)
            alerts = self.get_alerts(hours=hours)
            
            # Create report
            report = PerformanceReport(
                report_id=f"report_{int(time.time())}",
                report_type=report_type,
                generated_at=datetime.now(),
                time_range_hours=hours,
                metrics_count=len(metrics),
                alerts_count=len(alerts),
                system_health=self._calculate_system_health(metrics, alerts)
            )
            
            self.reports[report.report_id] = report
            return report
            
        except Exception as e:
            self.logger.error(f"Error creating report: {e}")
            return None
    
    def _calculate_system_health(self, metrics: List[PerformanceMetric], 
                                alerts: List[PerformanceAlert]) -> str:
        """Calculate system health - simplified."""
        try:
            critical_alerts = len([a for a in alerts if a.level == AlertLevel.CRITICAL])
            warning_alerts = len([a for a in alerts if a.level == AlertLevel.WARNING])
            
            if critical_alerts > 0:
                return "critical"
            elif warning_alerts > 5:
                return "warning"
            elif warning_alerts > 0:
                return "degraded"
            else:
                return "healthy"
                
        except Exception:
            return "unknown"
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """Get engine statistics - simplified."""
        return {
            "is_initialized": self.is_initialized,
            "status": self.status.value,
            "metrics_count": len(self.metrics),
            "widgets_count": len(self.widgets),
            "alerts_count": len(self.alerts),
            "reports_count": len(self.reports)
        }
    
    def cleanup_old_data(self, max_age_hours: int = 24) -> int:
        """Cleanup old data - simplified."""
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned = 0
            
            # Cleanup old metrics
            old_metrics = [mid for mid, metric in self.metrics.items() 
                          if metric.timestamp < cutoff_time]
            for mid in old_metrics:
                del self.metrics[mid]
                cleaned += 1
            
            # Cleanup old alerts
            old_alerts = [aid for aid, alert in self.alerts.items() 
                         if alert.timestamp < cutoff_time]
            for aid in old_alerts:
                del self.alerts[aid]
                cleaned += 1
            
            if cleaned > 0:
                self.logger.info(f"Cleaned up {cleaned} old data entries")
            
            return cleaned
            
        except Exception as e:
            self.logger.error(f"Error cleaning up data: {e}")
            return 0
    
    def get_recent_reports(self, limit: int = 10) -> List[PerformanceReport]:
        """Get recent reports - simplified."""
        try:
            reports = list(self.reports.values())
            reports.sort(key=lambda r: r.generated_at, reverse=True)
            return reports[:limit]
            
        except Exception as e:
            self.logger.error(f"Error getting recent reports: {e}")
            return []
    
    def cleanup_old_reports(self, cutoff_time: datetime) -> int:
        """Cleanup old reports - simplified."""
        try:
            old_reports = [rid for rid, report in self.reports.items() 
                          if report.generated_at < cutoff_time]
            for rid in old_reports:
                del self.reports[rid]
            
            return len(old_reports)
            
        except Exception as e:
            self.logger.error(f"Error cleaning up reports: {e}")
            return 0
    
    def shutdown(self) -> bool:
        """Shutdown engine - simplified."""
        try:
            self.is_initialized = False
            self.status = DashboardStatus.INACTIVE
            self.metrics.clear()
            self.widgets.clear()
            self.alerts.clear()
            self.configs.clear()
            self.reports.clear()
            self.logger.info("Dashboard Engine shutdown")
            return True
        except Exception as e:
            self.logger.error(f"Error during shutdown: {e}")
            return False