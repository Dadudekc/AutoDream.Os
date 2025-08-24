#!/usr/bin/env python3
"""
Dashboard Core Classes - Agent Cellphone V2
==========================================

Core dashboard classes and enums for the dashboard system.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class ChartType(Enum):
    """Types of charts available for dashboard widgets."""

    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    GAUGE = "gauge"
    AREA = "area"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    TABLE = "table"


@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""

    widget_id: str
    title: str
    chart_type: ChartType
    metric_name: str
    refresh_interval: int = 5  # seconds
    width: int = 6  # grid columns (1-12)
    height: int = 4  # grid rows
    position_x: int = 0
    position_y: int = 0
    options: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation: str = "raw"  # raw, avg, max, min, sum
    time_range: int = 3600  # seconds (1 hour default)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""

    columns: int = 12
    rows: int = 8
    widget_spacing: int = 10
    responsive: bool = True
    theme: str = "dark"  # dark, light
    auto_refresh: bool = True
    refresh_interval: int = 5  # seconds


class DashboardCore:
    """Core dashboard management functionality."""

    def __init__(self, websocket_url: Optional[str] = None):
        self.widgets: List[DashboardWidget] = []
        self.layout = DashboardLayout()
        self.websocket_url = websocket_url or "ws://localhost:8080/ws"
        self.title = "Agent Cellphone V2 - Performance Dashboard"

        logger.info("Dashboard core initialized")

    def add_widget(self, widget: DashboardWidget):
        """Add a widget to the dashboard."""
        self.widgets.append(widget)
        logger.info(f"Added widget: {widget.title} ({widget.chart_type.value})")

    def remove_widget(self, widget_id: str):
        """Remove a widget from the dashboard."""
        self.widgets = [w for w in self.widgets if w.widget_id != widget_id]
        logger.info(f"Removed widget: {widget_id}")

    def set_layout(self, layout: DashboardLayout):
        """Set dashboard layout configuration."""
        self.layout = layout
        logger.info(f"Updated layout: {layout.columns}x{layout.rows} grid")

    def get_widget(self, widget_id: str) -> Optional[DashboardWidget]:
        """Get a widget by ID."""
        for widget in self.widgets:
            if widget.widget_id == widget_id:
                return widget
        return None

    def get_widgets_by_type(self, chart_type: ChartType) -> List[DashboardWidget]:
        """Get all widgets of a specific chart type."""
        return [w for w in self.widgets if w.chart_type == chart_type]

    def get_widgets_by_category(self, category: str) -> List[DashboardWidget]:
        """Get widgets by category (if implemented in widget options)."""
        return [w for w in self.widgets if w.options.get("category") == category]

    def clear_widgets(self):
        """Remove all widgets from the dashboard."""
        self.widgets.clear()
        logger.info("All widgets cleared")

    def get_widget_count(self) -> int:
        """Get the total number of widgets."""
        return len(self.widgets)

    def validate_layout(self) -> bool:
        """Validate that all widgets fit within the layout grid."""
        total_width = sum(widget.width for widget in self.widgets)
        max_height = (
            max(widget.height for widget in self.widgets) if self.widgets else 0
        )

        if total_width > self.layout.columns:
            logger.warning(
                f"Total widget width ({total_width}) exceeds layout columns ({self.layout.columns})"
            )
            return False

        if max_height > self.layout.rows:
            logger.warning(
                f"Widget height ({max_height}) exceeds layout rows ({self.layout.rows})"
            )
            return False

        return True

    def export_config(self) -> Dict[str, Any]:
        """Export dashboard configuration as dictionary."""
        return {
            "title": self.title,
            "websocket_url": self.websocket_url,
            "layout": {
                "columns": self.layout.columns,
                "rows": self.layout.rows,
                "widget_spacing": self.layout.widget_spacing,
                "responsive": self.layout.responsive,
                "theme": self.layout.theme,
                "auto_refresh": self.layout.auto_refresh,
                "refresh_interval": self.layout.refresh_interval,
            },
            "widgets": [
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
                    "time_range": w.time_range,
                }
                for w in self.widgets
            ],
        }

    def import_config(self, config: Dict[str, Any]):
        """Import dashboard configuration from dictionary."""
        self.title = config.get("title", self.title)
        self.websocket_url = config.get("websocket_url", self.websocket_url)

        if "layout" in config:
            layout_config = config["layout"]
            self.layout = DashboardLayout(
                columns=layout_config.get("columns", 12),
                rows=layout_config.get("rows", 8),
                widget_spacing=layout_config.get("widget_spacing", 10),
                responsive=layout_config.get("responsive", True),
                theme=layout_config.get("theme", "dark"),
                auto_refresh=layout_config.get("auto_refresh", True),
                refresh_interval=layout_config.get("refresh_interval", 5),
            )

        if "widgets" in config:
            self.widgets.clear()
            for widget_config in config["widgets"]:
                try:
                    chart_type = ChartType(widget_config["chart_type"])
                    widget = DashboardWidget(
                        widget_id=widget_config["widget_id"],
                        title=widget_config["title"],
                        chart_type=chart_type,
                        metric_name=widget_config["metric_name"],
                        refresh_interval=widget_config.get("refresh_interval", 5),
                        width=widget_config.get("width", 6),
                        height=widget_config.get("height", 4),
                        position_x=widget_config.get("position_x", 0),
                        position_y=widget_config.get("position_y", 0),
                        options=widget_config.get("options", {}),
                        filters=widget_config.get("filters", {}),
                        aggregation=widget_config.get("aggregation", "raw"),
                        time_range=widget_config.get("time_range", 3600),
                    )
                    self.widgets.append(widget)
                except (KeyError, ValueError) as e:
                    logger.error(
                        f"Failed to import widget {widget_config.get('widget_id', 'unknown')}: {e}"
                    )

        logger.info(f"Imported configuration with {len(self.widgets)} widgets")
