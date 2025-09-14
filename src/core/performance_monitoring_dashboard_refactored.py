"""Refactored Performance Monitoring Dashboard - V2 Compliant Version

This is a modular, V2-compliant version of the performance monitoring dashboard
that breaks down the original 1,038-line file into focused modules.

Author: Agent-8 (SSOT & System Integration Specialist)
V2 Compliance: < 300 lines, modular design, single responsibility
"""

import json
import logging
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any

from .performance import MetricsCollector, DashboardType, DashboardWidget

logger = logging.getLogger(__name__)


class PerformanceMonitoringDashboard:
    """
    V2-compliant performance monitoring dashboard system.
    
    This system provides real-time visualization of:
    - System performance metrics
    - Consolidation progress tracking
    - SLA compliance monitoring
    - Alert management and visualization
    """

    def __init__(self, dashboard_directory: str = "performance_dashboards"):
        """Initialize the performance monitoring dashboard."""
        self.dashboard_directory = Path(dashboard_directory)
        self.dashboard_directory.mkdir(exist_ok=True)
        
        # Core components
        self.metrics_collector = MetricsCollector()
        self.widgets: dict[str, DashboardWidget] = {}
        self.dashboards: dict[str, dict[str, Any]] = {}
        
        # Monitoring state
        self.is_monitoring = False
        self.monitoring_thread: threading.Thread | None = None
        self.collection_interval = 5.0  # seconds

    def start_monitoring(self) -> None:
        """Start continuous metrics collection."""
        if self.is_monitoring:
            logger.warning("Monitoring is already running")
            return
        
        self.is_monitoring = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info("Performance monitoring started")

    def stop_monitoring(self) -> None:
        """Stop continuous metrics collection."""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5.0)
        logger.info("Performance monitoring stopped")

    def _monitoring_loop(self) -> None:
        """Main monitoring loop that runs in a separate thread."""
        while self.is_monitoring:
            try:
                # Collect all metrics
                metrics = self.metrics_collector.get_all_metrics()
                
                # Update dashboards with new metrics
                self._update_dashboards(metrics)
                
                # Save dashboard data
                self._save_dashboard_data()
                
                time.sleep(self.collection_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(self.collection_interval)

    def _update_dashboards(self, metrics: list[Any]) -> None:
        """Update dashboard data with new metrics."""
        for metric in metrics:
            dashboard_type = self._get_dashboard_type_for_metric(metric)
            
            if dashboard_type not in self.dashboards:
                self.dashboards[dashboard_type] = {
                    'metrics': [],
                    'last_updated': datetime.now().isoformat(),
                    'widgets': []
                }
            
            # Add metric to appropriate dashboard
            self.dashboards[dashboard_type]['metrics'].append({
                'name': metric.name,
                'value': metric.value,
                'unit': metric.unit,
                'timestamp': metric.timestamp.isoformat(),
                'category': metric.category
            })

    def _get_dashboard_type_for_metric(self, metric: Any) -> str:
        """Determine which dashboard a metric belongs to."""
        category = getattr(metric, 'category', 'unknown')
        
        if category == 'system':
            return DashboardType.OPERATIONAL.value
        elif category == 'consolidation':
            return DashboardType.CONSOLIDATION.value
        elif category == 'application':
            return DashboardType.PERFORMANCE.value
        else:
            return DashboardType.OPERATIONAL.value

    def _save_dashboard_data(self) -> None:
        """Save dashboard data to files."""
        for dashboard_type, data in self.dashboards.items():
            dashboard_file = self.dashboard_directory / f"{dashboard_type}_dashboard.json"
            
            try:
                with open(dashboard_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, default=str)
            except Exception as e:
                logger.error(f"Failed to save dashboard {dashboard_type}: {e}")

    def create_widget(self, widget_id: str, title: str, widget_type: str, 
                     metrics: list[str] = None, config: dict[str, Any] = None) -> None:
        """Create a new dashboard widget."""
        widget = DashboardWidget(
            id=widget_id,
            title=title,
            widget_type=widget_type,
            metrics=metrics or [],
            config=config or {}
        )
        
        self.widgets[widget_id] = widget
        logger.info(f"Created widget: {widget_id}")

    def get_dashboard_data(self, dashboard_type: str) -> dict[str, Any]:
        """Get current dashboard data."""
        return self.dashboards.get(dashboard_type, {
            'metrics': [],
            'last_updated': datetime.now().isoformat(),
            'widgets': []
        })

    def get_metric_history(self, metric_name: str) -> list[dict[str, Any]]:
        """Get historical data for a specific metric."""
        history = self.metrics_collector.get_metric_history(metric_name)
        return [
            {
                'name': metric.name,
                'value': metric.value,
                'unit': metric.unit,
                'timestamp': metric.timestamp.isoformat(),
                'category': metric.category
            }
            for metric in history
        ]

    def export_dashboard_data(self, output_file: str = None) -> str:
        """Export all dashboard data to a JSON file."""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"dashboard_export_{timestamp}.json"
        
        export_data = {
            'dashboards': self.dashboards,
            'widgets': {k: {
                'id': v.id,
                'title': v.title,
                'widget_type': v.widget_type,
                'metrics': v.metrics,
                'config': v.config
            } for k, v in self.widgets.items()},
            'export_timestamp': datetime.now().isoformat()
        }
        
        output_path = self.dashboard_directory / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        logger.info(f"Dashboard data exported to {output_path}")
        return str(output_path)

    def get_system_status(self) -> dict[str, Any]:
        """Get overall system status summary."""
        current_metrics = self.metrics_collector.get_all_metrics()
        
        status = {
            'monitoring_active': self.is_monitoring,
            'total_metrics': len(current_metrics),
            'dashboards_count': len(self.dashboards),
            'widgets_count': len(self.widgets),
            'last_collection': self.metrics_collector.last_collection_time.isoformat(),
            'collection_interval': self.collection_interval
        }
        
        return status