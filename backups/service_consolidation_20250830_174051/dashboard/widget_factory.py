#!/usr/bin/env python3
"""
Widget Factory - V2 Dashboard System

This module handles widget creation, management, and configuration.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List, Dict, Any
from .dashboard_types import DashboardWidget, ChartType


class WidgetFactory:
    """Factory for creating and managing dashboard widgets."""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.WidgetFactory")
    
    def create_sample_widgets(self) -> List[DashboardWidget]:
        """Create sample widgets for testing."""
        return [
            DashboardWidget(
                widget_id="cpu_usage",
                title="CPU Usage",
                chart_type=ChartType.GAUGE,
                metric_name="cpu_percentage",
                refresh_interval=5,
                width=4, height=3, position_x=0, position_y=0
            ),
            DashboardWidget(
                widget_id="memory_usage",
                title="Memory Usage",
                chart_type=ChartType.BAR,
                metric_name="memory_percentage",
                refresh_interval=5,
                width=4, height=3, position_x=4, position_y=0
            ),
            DashboardWidget(
                widget_id="network_traffic",
                title="Network Traffic",
                chart_type=ChartType.LINE,
                metric_name="network_bytes",
                refresh_interval=10,
                width=4, height=3, position_x=8, position_y=0
            ),
            DashboardWidget(
                widget_id="disk_io",
                title="Disk I/O",
                chart_type=ChartType.AREA,
                metric_name="disk_operations",
                refresh_interval=15,
                width=6, height=4, position_x=0, position_y=3
            ),
            DashboardWidget(
                widget_id="system_health",
                title="System Health",
                chart_type=ChartType.TABLE,
                metric_name="health_status",
                refresh_interval=30,
                width=6, height=4, position_x=6, position_y=3
            )
        ]
    
    def create_widget_from_config(self, config: Dict[str, Any]) -> DashboardWidget:
        """Create a widget from configuration dictionary."""
        try:
            chart_type = ChartType(config["chart_type"])
            return DashboardWidget(
                widget_id=config["widget_id"],
                title=config["title"],
                chart_type=chart_type,
                metric_name=config["metric_name"],
                refresh_interval=config.get("refresh_interval", 5),
                width=config.get("width", 6),
                height=config.get("height", 4),
                position_x=config.get("position_x", 0),
                position_y=config.get("position_y", 0),
                options=config.get("options", {}),
                filters=config.get("filters", {}),
                aggregation=config.get("aggregation", "raw"),
                time_range=config.get("time_range", 3600)
            )
        except Exception as e:
            self.logger.error(f"Failed to create widget from config: {e}")
            raise
    
    def get_widget_summary(self, widgets: List[DashboardWidget]) -> Dict[str, Any]:
        """Get summary of all widgets."""
        if not widgets:
            return {"error": "No widgets configured"}
        
        summary = {
            "total_widgets": len(widgets),
            "chart_types": self._count_chart_types(widgets),
            "refresh_intervals": self._count_refresh_intervals(widgets),
            "total_width": sum(w.width for w in widgets),
            "total_height": sum(w.height for w in widgets)
        }
        
        return summary
    
    def _count_chart_types(self, widgets: List[DashboardWidget]) -> Dict[str, int]:
        """Count chart types in widgets."""
        chart_types = {}
        for widget in widgets:
            chart_type = widget.chart_type.value
            chart_types[chart_type] = chart_types.get(chart_type, 0) + 1
        return chart_types
    
    def _count_refresh_intervals(self, widgets: List[DashboardWidget]) -> Dict[str, int]:
        """Count refresh intervals in widgets."""
        intervals = {}
        for widget in widgets:
            interval = str(widget.refresh_interval)
            intervals[interval] = intervals.get(interval, 0) + 1
        return intervals
    
    def export_widgets_config(self, widgets: List[DashboardWidget]) -> List[Dict[str, Any]]:
        """Export widgets configuration."""
        return [
            {
                "widget_id": w.widget_id,
                "title": w.title,
                "chart_type": w.chart_type.value,
                "metric_name": w.metric_name,
                "refresh_interval": w.refresh_interval,
                "width": w.width,
                "height": w.height,
                "position_x": w.position_x,
                "position_y": w.position_y,
                "options": w.options,
                "filters": w.filters,
                "aggregation": w.aggregation,
                "time_range": w.time_range
            }
            for w in widgets
        ]
    
    def validate_widget(self, widget: DashboardWidget) -> bool:
        """Validate widget configuration."""
        try:
            # Check required fields
            if not widget.widget_id or not widget.title or not widget.metric_name:
                return False
            
            # Check dimensions
            if widget.width <= 0 or widget.height <= 0:
                return False
            
            # Check refresh interval
            if widget.refresh_interval <= 0:
                return False
            
            # Check position
            if widget.position_x < 0 or widget.position_y < 0:
                return False
            
            return True
            
        except Exception:
            return False


