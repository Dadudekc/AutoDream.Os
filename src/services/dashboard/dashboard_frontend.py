#!/usr/bin/env python3
"""
Dashboard Frontend - V2 Dashboard System

This is the refactored main system that orchestrates dashboard generation.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging
from typing import List, Optional, Dict, Any
from pathlib import Path

from .dashboard_types import (
    DashboardWidget, DashboardLayout, DashboardConfig, ChartType
)
from .html_generator import HTMLGenerator
from .javascript_generator import JavaScriptGenerator
from .realtime_updater import RealTimeUpdater
from .widget_factory import WidgetFactory
from .config_manager import ConfigManager
from .file_generator import FileGenerator


class DashboardFrontend:
    """
    Refactored frontend generator for performance dashboard
    
    Responsibilities:
    - Orchestrate dashboard generation
    - Coordinate between specialized components
    - Provide unified interface for dashboard creation
    """

    def __init__(self, websocket_url: Optional[str] = None):
        # Initialize configuration
        self.config = DashboardConfig()
        if websocket_url:
            self.config.websocket_url = websocket_url
        
        # Initialize components
        self.html_generator = HTMLGenerator(self.config)
        self.javascript_generator = JavaScriptGenerator(self.config)
        self.realtime_updater = RealTimeUpdater(self.config.websocket_url)
        self.widget_factory = WidgetFactory()
        self.config_manager = ConfigManager()
        self.file_generator = FileGenerator(self.html_generator, self.javascript_generator)
        
        # Dashboard state
        self.widgets: List[DashboardWidget] = []
        self.layout = DashboardLayout()
        
        self.logger = logging.getLogger(f"{__name__}.DashboardFrontend")
        self.logger.info("Dashboard frontend initialized")

    def add_widget(self, widget: DashboardWidget):
        """Add a widget to the dashboard."""
        if self.widget_factory.validate_widget(widget):
            self.widgets.append(widget)
            self.logger.info(f"Added widget: {widget.title} ({widget.chart_type.value})")
        else:
            self.logger.error(f"Invalid widget configuration: {widget.widget_id}")

    def remove_widget(self, widget_id: str):
        """Remove a widget from the dashboard."""
        self.widgets = [w for w in self.widgets if w.widget_id != widget_id]
        self.logger.info(f"Removed widget: {widget_id}")

    def set_layout(self, layout: DashboardLayout):
        """Set dashboard layout configuration."""
        self.layout = layout
        self.logger.info(f"Updated layout: {layout.columns}x{layout.rows} grid")

    def generate_html(self) -> str:
        """Generate complete HTML for the dashboard."""
        try:
            self.logger.info("Generating dashboard HTML")
            html = self.html_generator.generate_html(self.widgets, self.layout)
            self.logger.info("Dashboard HTML generated successfully")
            return html
        except Exception as e:
            self.logger.error(f"Failed to generate HTML: {e}")
            raise

    def generate_javascript(self) -> str:
        """Generate JavaScript for the dashboard."""
        try:
            self.logger.info("Generating dashboard JavaScript")
            javascript = self.javascript_generator.generate_javascript(self.widgets, self.layout)
            self.logger.info("Dashboard JavaScript generated successfully")
            return javascript
        except Exception as e:
            self.logger.error(f"Failed to generate JavaScript: {e}")
            raise

    def generate_dashboard_files(self, output_dir: str = "dashboard_output") -> Dict[str, str]:
        """Generate all dashboard files and save to directory."""
        return self.file_generator.generate_dashboard_files(self.widgets, self.layout, output_dir)

    def create_sample_widgets(self) -> List[DashboardWidget]:
        """Create sample widgets for testing."""
        sample_widgets = self.widget_factory.create_sample_widgets()
        
        for widget in sample_widgets:
            self.add_widget(widget)
        
        self.logger.info(f"Created {len(sample_widgets)} sample widgets")
        return sample_widgets

    def get_widget_summary(self) -> Dict[str, Any]:
        """Get summary of all widgets."""
        return self.widget_factory.get_widget_summary(self.widgets)

    def export_config(self) -> Dict[str, Any]:
        """Export dashboard configuration."""
        return self.config_manager.export_config(self.config, self.layout, self.widgets)

    def import_config(self, config_data: Dict[str, Any]):
        """Import dashboard configuration."""
        if self.config_manager.validate_config(config_data):
            self.config_manager.import_config(config_data, self.config, self.layout, self.widgets)
        else:
            raise ValueError("Invalid configuration data")

    def get_status(self) -> Dict[str, Any]:
        """Get dashboard system status."""
        return {
            "widgets_count": len(self.widgets),
            "layout": f"{self.layout.columns}x{self.layout.rows}",
            "theme": self.layout.theme,
            "auto_refresh": self.layout.auto_refresh,
            "websocket_status": self.realtime_updater.get_connection_status()
        }
