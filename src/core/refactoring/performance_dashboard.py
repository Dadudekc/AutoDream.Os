#!/usr/bin/env python3
"""
Refactoring Performance Dashboard - Agent-5
==========================================

This module provides a comprehensive dashboard for visualizing and monitoring
refactoring performance metrics in real-time.

Features:
- Real-time metrics visualization
- Interactive charts and graphs
- Performance alerts and notifications
- Historical trend analysis
- Customizable dashboard layouts
- Export capabilities for reports

Author: Agent-5 (REFACTORING MANAGER)
Contract: REFACTOR-003
Status: In Progress
"""

import os
import sys
import json
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import traceback

sys.path.append(str(Path(__file__).parent.parent.parent))
from core.managers.base_manager import BaseManager
from core.refactoring.refactoring_performance_metrics import (
    RefactoringPerformanceMetrics, MetricType, MetricCategory
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DashboardWidgetType(Enum):
    """Types of dashboard widgets"""
    METRICS_OVERVIEW = "metrics_overview"
    PERFORMANCE_CHART = "performance_chart"
    QUALITY_METRICS = "quality_metrics"
    TREND_ANALYSIS = "trend_analysis"
    ALERTS_PANEL = "alerts_panel"
    BASELINE_COMPARISON = "baseline_comparison"
    REAL_TIME_MONITORING = "real_time_monitoring"

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    SUCCESS = "success"

@dataclass
class DashboardWidget:
    """Individual dashboard widget configuration"""
    widget_id: str
    widget_type: DashboardWidgetType
    title: str
    position: Tuple[int, int]  # (row, column)
    size: Tuple[int, int]  # (width, height)
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    refresh_interval: int = 30  # seconds

@dataclass
class PerformanceAlert:
    """Performance alert configuration"""
    alert_id: str
    title: str
    message: str
    severity: AlertSeverity
    timestamp: datetime
    metric_name: str
    threshold_value: float
    current_value: float
    acknowledged: bool = False
    resolved: bool = False

@dataclass
class DashboardLayout:
    """Dashboard layout configuration"""
    layout_id: str
    name: str
    description: str
    widgets: List[DashboardWidget]
    created_at: datetime
    updated_at: datetime
    is_default: bool = False

class RefactoringPerformanceDashboard(BaseManager):
    """
    Comprehensive dashboard for monitoring and visualizing refactoring performance metrics.
    
    This dashboard provides:
    - Real-time metrics visualization
    - Interactive charts and graphs
    - Performance alerts and notifications
    - Historical trend analysis
    - Customizable dashboard layouts
    - Export capabilities for reports
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the refactoring performance dashboard"""
        super().__init__(config or {})
        self.metrics_system = RefactoringPerformanceMetrics()
        self.widgets: List[DashboardWidget] = []
        self.alerts: List[PerformanceAlert] = []
        self.layouts: List[DashboardLayout] = []
        self.dashboard_config = self._initialize_dashboard_config()
        self._initialize_default_layout()
        self._start_monitoring()
    
    def _initialize_dashboard_config(self) -> Dict[str, Any]:
        """Initialize dashboard configuration"""
        return {
            "auto_refresh_enabled": True,
            "refresh_interval": 30,  # seconds
            "max_alerts": 100,
            "alert_retention_days": 7,
            "chart_colors": [
                "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
                "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
            ],
            "thresholds": {
                "complexity_warning": 10,
                "complexity_critical": 20,
                "maintainability_warning": 0.6,
                "maintainability_critical": 0.4,
                "duplication_warning": 0.15,
                "duplication_critical": 0.25,
                "duration_warning": 300,  # 5 minutes
                "duration_critical": 600   # 10 minutes
            }
        }
    
    def _initialize_default_layout(self):
        """Initialize the default dashboard layout"""
        default_widgets = [
            DashboardWidget(
                widget_id="overview_metrics",
                widget_type=DashboardWidgetType.METRICS_OVERVIEW,
                title="Metrics Overview",
                position=(0, 0),
                size=(4, 2),
                config={"show_summary": True, "show_trends": True}
            ),
            DashboardWidget(
                widget_id="performance_chart",
                widget_type=DashboardWidgetType.PERFORMANCE_CHART,
                title="Performance Trends",
                position=(0, 2),
                size=(4, 3),
                config={"chart_type": "line", "time_range": "24h"}
            ),
            DashboardWidget(
                widget_id="quality_metrics",
                widget_type=DashboardWidgetType.QUALITY_METRICS,
                title="Code Quality Metrics",
                position=(2, 0),
                size=(2, 2),
                config={"show_complexity": True, "show_maintainability": True}
            ),
            DashboardWidget(
                widget_id="alerts_panel",
                widget_type=DashboardWidgetType.ALERTS_PANEL,
                title="Performance Alerts",
                position=(2, 2),
                size=(2, 3),
                config={"max_alerts": 10, "show_acknowledged": False}
            ),
            DashboardWidget(
                widget_id="baseline_comparison",
                widget_type=DashboardWidgetType.BASELINE_COMPARISON,
                title="Baseline Comparison",
                position=(4, 0),
                size=(4, 2),
                config={"baseline_name": "Default Baseline"}
            )
        ]
        
        default_layout = DashboardLayout(
            layout_id="default_layout",
            name="Default Dashboard",
            description="Standard dashboard layout for refactoring performance monitoring",
            widgets=default_widgets,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_default=True
        )
        
        self.layouts.append(default_layout)
        self.widgets = default_widgets.copy()
    
    def _start_monitoring(self):
        """Start the monitoring system"""
        logger.info("Starting dashboard monitoring system")
        # In a real implementation, this would start background tasks
        # For now, we'll simulate monitoring through manual calls
    
    def get_metrics_overview(self) -> Dict[str, Any]:
        """Get overview of current metrics"""
        try:
            # Get current system health
            health = self.metrics_system.get_system_health()
            
            # Get recent metrics summary
            recent_report = self.metrics_system.generate_metrics_report(
                time_range=(datetime.now() - timedelta(hours=24), datetime.now())
            )
            
            # Calculate key performance indicators
            kpis = self._calculate_kpis(recent_report)
            
            overview = {
                "timestamp": datetime.now().isoformat(),
                "system_health": health,
                "recent_metrics": {
                    "total_operations": recent_report.summary.get("total_operations", 0),
                    "average_duration": recent_report.summary.get("average_duration", 0),
                    "total_metrics": recent_report.summary.get("metrics_count", 0)
                },
                "key_performance_indicators": kpis,
                "active_alerts": len([a for a in self.alerts if not a.resolved]),
                "last_activity": health.get("last_activity")
            }
            
            return overview
            
        except Exception as e:
            logger.error(f"Error getting metrics overview: {e}")
            return {"error": str(e)}
    
    def _calculate_kpis(self, report) -> Dict[str, Any]:
        """Calculate key performance indicators from metrics report"""
        kpis = {}
        
        try:
            # Performance efficiency KPI
            if report.summary.get("total_duration") and report.summary.get("total_operations"):
                avg_duration = report.summary["total_duration"] / report.summary["total_operations"]
                kpis["performance_efficiency"] = {
                    "value": avg_duration,
                    "unit": "seconds",
                    "status": "good" if avg_duration < 300 else "warning" if avg_duration < 600 else "critical"
                }
            
            # Code quality KPI
            if hasattr(report, 'detailed_metrics') and report.detailed_metrics:
                quality_scores = []
                for snapshot in report.detailed_metrics:
                    for metric in snapshot.metrics:
                        if metric.name == "maintainability_index" and isinstance(metric.value, (int, float)):
                            quality_scores.append(metric.value)
                
                if quality_scores:
                    avg_quality = sum(quality_scores) / len(quality_scores)
                    kpis["code_quality"] = {
                        "value": avg_quality,
                        "unit": "score",
                        "status": "good" if avg_quality > 0.7 else "warning" if avg_quality > 0.5 else "critical"
                    }
            
            # Productivity KPI
            if report.summary.get("total_operations"):
                operations_per_hour = report.summary["total_operations"] / 24  # Assuming 24-hour period
                kpis["productivity"] = {
                    "value": operations_per_hour,
                    "unit": "operations/hour",
                    "status": "good" if operations_per_hour > 2 else "warning" if operations_per_hour > 1 else "critical"
                }
                
        except Exception as e:
            logger.error(f"Error calculating KPIs: {e}")
        
        return kpis
    
    def get_performance_chart_data(self, chart_type: str = "line", 
                                  time_range: str = "24h") -> Dict[str, Any]:
        """Get data for performance charts"""
        try:
            # Calculate time range
            end_time = datetime.now()
            if time_range == "1h":
                start_time = end_time - timedelta(hours=1)
            elif time_range == "6h":
                start_time = end_time - timedelta(hours=6)
            elif time_range == "24h":
                start_time = end_time - timedelta(hours=24)
            elif time_range == "7d":
                start_time = end_time - timedelta(days=7)
            else:
                start_time = end_time - timedelta(hours=24)
            
            # Get metrics for the time range
            report = self.metrics_system.generate_metrics_report(
                time_range=(start_time, end_time)
            )
            
            # Prepare chart data
            chart_data = {
                "chart_type": chart_type,
                "time_range": time_range,
                "labels": [],
                "datasets": {}
            }
            
            # Group metrics by timestamp
            time_series = {}
            for snapshot in report.detailed_metrics:
                timestamp = snapshot.timestamp.strftime("%H:%M")
                chart_data["labels"].append(timestamp)
                
                for metric in snapshot.metrics:
                    if isinstance(metric.value, (int, float)):
                        if metric.name not in time_series:
                            time_series[metric.name] = []
                        time_series[metric.name].append(metric.value)
            
            # Create datasets for each metric
            for metric_name, values in time_series.items():
                if len(values) == len(chart_data["labels"]):
                    chart_data["datasets"][metric_name] = {
                        "label": metric_name.replace("_", " ").title(),
                        "data": values,
                        "borderColor": self.dashboard_config["chart_colors"][len(chart_data["datasets"]) % len(self.dashboard_config["chart_colors"])],
                        "fill": False
                    }
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Error getting performance chart data: {e}")
            return {"error": str(e)}
    
    def get_quality_metrics(self) -> Dict[str, Any]:
        """Get current code quality metrics"""
        try:
            # Get recent quality metrics
            recent_report = self.metrics_system.generate_metrics_report(
                time_range=(datetime.now() - timedelta(hours=6), datetime.now())
            )
            
            quality_metrics = {
                "timestamp": datetime.now().isoformat(),
                "metrics": {},
                "status": "unknown"
            }
            
            # Aggregate quality metrics
            quality_data = {}
            for snapshot in recent_report.detailed_metrics:
                for metric in snapshot.metrics:
                    if metric.name in ["complexity", "maintainability_index", "duplication_percentage"]:
                        if metric.name not in quality_data:
                            quality_data[metric.name] = []
                        if isinstance(metric.value, (int, float)):
                            quality_data[metric.name].append(metric.value)
            
            # Calculate averages and determine status
            overall_status = "good"
            for metric_name, values in quality_data.items():
                if values:
                    avg_value = sum(values) / len(values)
                    quality_metrics["metrics"][metric_name] = {
                        "current": avg_value,
                        "average": avg_value,
                        "status": self._get_metric_status(metric_name, avg_value)
                    }
                    
                    # Update overall status
                    if quality_metrics["metrics"][metric_name]["status"] == "critical":
                        overall_status = "critical"
                    elif quality_metrics["metrics"][metric_name]["status"] == "warning" and overall_status != "critical":
                        overall_status = "warning"
            
            quality_metrics["status"] = overall_status
            return quality_metrics
            
        except Exception as e:
            logger.error(f"Error getting quality metrics: {e}")
            return {"error": str(e)}
    
    def _get_metric_status(self, metric_name: str, value: float) -> str:
        """Get status for a metric based on thresholds"""
        thresholds = self.dashboard_config["thresholds"]
        
        if metric_name == "complexity":
            if value <= thresholds["complexity_warning"]:
                return "good"
            elif value <= thresholds["complexity_critical"]:
                return "warning"
            else:
                return "critical"
        elif metric_name == "maintainability_index":
            if value >= thresholds["maintainability_critical"]:
                return "good"
            elif value >= thresholds["maintainability_warning"]:
                return "warning"
            else:
                return "critical"
        elif metric_name == "duplication_percentage":
            if value <= thresholds["duplication_warning"]:
                return "good"
            elif value <= thresholds["duplication_critical"]:
                return "warning"
            else:
                return "critical"
        
        return "unknown"
    
    def get_alerts_panel(self, max_alerts: int = 10, 
                         show_acknowledged: bool = False) -> Dict[str, Any]:
        """Get current performance alerts"""
        try:
            # Filter alerts based on parameters
            filtered_alerts = []
            for alert in self.alerts:
                if not show_acknowledged and alert.acknowledged:
                    continue
                filtered_alerts.append(alert)
            
            # Sort by severity and timestamp
            filtered_alerts.sort(key=lambda x: (
                {"critical": 3, "warning": 2, "info": 1, "success": 0}[x.severity.value],
                x.timestamp
            ), reverse=True)
            
            # Limit number of alerts
            filtered_alerts = filtered_alerts[:max_alerts]
            
            alerts_data = {
                "timestamp": datetime.now().isoformat(),
                "total_alerts": len(self.alerts),
                "active_alerts": len([a for a in self.alerts if not a.resolved]),
                "alerts": [
                    {
                        "id": alert.alert_id,
                        "title": alert.title,
                        "message": alert.message,
                        "severity": alert.severity.value,
                        "timestamp": alert.timestamp.isoformat(),
                        "metric_name": alert.metric_name,
                        "threshold_value": alert.threshold_value,
                        "current_value": alert.current_value,
                        "acknowledged": alert.acknowledged,
                        "resolved": alert.resolved
                    }
                    for alert in filtered_alerts
                ]
            }
            
            return alerts_data
            
        except Exception as e:
            logger.error(f"Error getting alerts panel: {e}")
            return {"error": str(e)}
    
    def get_baseline_comparison(self, baseline_name: str = "Default Baseline") -> Dict[str, Any]:
        """Get comparison data against a specific baseline"""
        try:
            # Get current metrics
            current_metrics = self.get_quality_metrics()
            
            # Compare against baseline
            comparison = self.metrics_system.compare_against_baseline(
                baseline_name, current_metrics.get("metrics", {})
            )
            
            # Format comparison data for dashboard
            comparison_data = {
                "timestamp": datetime.now().isoformat(),
                "baseline_name": baseline_name,
                "comparison": comparison,
                "summary": {
                    "total_metrics": len(comparison.get("differences", {})),
                    "improvements": len(comparison.get("improvements", {})),
                    "regressions": len(comparison.get("regressions", {})),
                    "unchanged": len(comparison.get("differences", {})) - 
                               len(comparison.get("improvements", {})) - 
                               len(comparison.get("regressions", {}))
                }
            }
            
            return comparison_data
            
        except Exception as e:
            logger.error(f"Error getting baseline comparison: {e}")
            return {"error": str(e)}
    
    def create_alert(self, title: str, message: str, severity: AlertSeverity,
                    metric_name: str, threshold_value: float, current_value: float) -> str:
        """Create a new performance alert"""
        alert_id = f"alert_{int(time.time())}_{metric_name}"
        
        alert = PerformanceAlert(
            alert_id=alert_id,
            title=title,
            message=message,
            severity=severity,
            timestamp=datetime.now(),
            metric_name=metric_name,
            threshold_value=threshold_value,
            current_value=current_value
        )
        
        self.alerts.append(alert)
        
        # Limit total alerts
        if len(self.alerts) > self.dashboard_config["max_alerts"]:
            self.alerts = self.alerts[-self.dashboard_config["max_alerts"]:]
        
        logger.info(f"Created alert: {title} ({severity.value})")
        return alert_id
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge a performance alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                logger.info(f"Acknowledged alert: {alert_id}")
                return True
        return False
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve a performance alert"""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.resolved = True
                logger.info(f"Resolved alert: {alert_id}")
                return True
        return False
    
    def create_custom_layout(self, name: str, description: str, 
                           widgets: List[DashboardWidget]) -> str:
        """Create a custom dashboard layout"""
        layout_id = f"layout_{int(time.time())}"
        
        layout = DashboardLayout(
            layout_id=layout_id,
            name=name,
            description=description,
            widgets=widgets,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.layouts.append(layout)
        logger.info(f"Created custom layout: {name}")
        return layout_id
    
    def switch_layout(self, layout_id: str) -> bool:
        """Switch to a different dashboard layout"""
        layout = next((l for l in self.layouts if l.layout_id == layout_id), None)
        if layout:
            self.widgets = layout.widgets.copy()
            logger.info(f"Switched to layout: {layout.name}")
            return True
        return False
    
    def export_dashboard_data(self, output_path: str, format: str = "json") -> bool:
        """Export dashboard data to external format"""
        try:
            if format.lower() == "json":
                export_data = {
                    "export_timestamp": datetime.now().isoformat(),
                    "dashboard_config": self.dashboard_config,
                    "current_layout": {
                        "layout_id": next((l.layout_id for l in self.layouts if l.is_default), "unknown"),
                        "widgets": [
                            {
                                "widget_id": w.widget_id,
                                "widget_type": w.widget_type.value,
                                "title": w.title,
                                "position": w.position,
                                "size": w.size,
                                "enabled": w.enabled
                            }
                            for w in self.widgets
                        ]
                    },
                    "alerts": [
                        {
                            "id": a.alert_id,
                            "title": a.title,
                            "message": a.message,
                            "severity": a.severity.value,
                            "timestamp": a.timestamp.isoformat(),
                            "metric_name": a.metric_name,
                            "threshold_value": a.threshold_value,
                            "current_value": a.current_value,
                            "acknowledged": a.acknowledged,
                            "resolved": a.resolved
                        }
                        for a in self.alerts
                    ],
                    "layouts": [
                        {
                            "layout_id": l.layout_id,
                            "name": l.name,
                            "description": l.description,
                            "is_default": l.is_default,
                            "created_at": l.created_at.isoformat(),
                            "updated_at": l.updated_at.isoformat()
                        }
                        for l in self.layouts
                    ]
                }
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, default=str)
                
                logger.info(f"Exported dashboard data to {output_path}")
                return True
                
            else:
                logger.error(f"Unsupported export format: {format}")
                return False
                
        except Exception as e:
            logger.error(f"Error exporting dashboard data: {e}")
            return False
    
    def cleanup_old_alerts(self, max_age_days: int = None):
        """Clean up old alerts"""
        if max_age_days is None:
            max_age_days = self.dashboard_config["alert_retention_days"]
        
        cutoff_date = datetime.now() - timedelta(days=max_age_days)
        
        original_count = len(self.alerts)
        self.alerts = [
            alert for alert in self.alerts
            if alert.timestamp > cutoff_date
        ]
        removed_count = original_count - len(self.alerts)
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old alerts")
    
    def get_dashboard_status(self) -> Dict[str, Any]:
        """Get overall dashboard status"""
        return {
            "status": "active",
            "widgets_count": len(self.widgets),
            "active_widgets": len([w for w in self.widgets if w.enabled]),
            "layouts_count": len(self.layouts),
            "current_layout": next((l.name for l in self.layouts if l.is_default), "unknown"),
            "alerts_count": len(self.alerts),
            "active_alerts": len([a for a in self.alerts if not a.resolved]),
            "last_refresh": datetime.now().isoformat(),
            "metrics_system_health": self.metrics_system.get_system_health()
        }

async def demo_performance_dashboard():
    """Demonstrate the refactoring performance dashboard"""
    print("🚀 Refactoring Performance Dashboard Demo")
    print("=" * 50)
    
    # Initialize the dashboard
    dashboard = RefactoringPerformanceDashboard()
    
    # Get metrics overview
    overview = dashboard.get_metrics_overview()
    print(f"Metrics Overview: {overview.get('recent_metrics', {})}")
    
    # Get performance chart data
    chart_data = dashboard.get_performance_chart_data("line", "24h")
    print(f"Chart Data: {len(chart_data.get('datasets', {}))} datasets")
    
    # Get quality metrics
    quality_metrics = dashboard.get_quality_metrics()
    print(f"Quality Metrics Status: {quality_metrics.get('status', 'unknown')}")
    
    # Get alerts panel
    alerts_data = dashboard.get_alerts_panel()
    print(f"Active Alerts: {alerts_data.get('active_alerts', 0)}")
    
    # Get baseline comparison
    baseline_comparison = dashboard.get_baseline_comparison()
    print(f"Baseline Comparison: {baseline_comparison.get('summary', {})}")
    
    # Get dashboard status
    status = dashboard.get_dashboard_status()
    print(f"Dashboard Status: {status.get('status', 'unknown')}")
    
    print("\n✅ Demo completed successfully!")

if __name__ == "__main__":
    asyncio.run(demo_performance_dashboard())
