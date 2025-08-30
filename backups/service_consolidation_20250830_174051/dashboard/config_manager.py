
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env python3
"""
Configuration Manager - V2 Dashboard System

This module handles dashboard configuration import/export operations.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List
from .dashboard_types import DashboardConfig, DashboardLayout, ChartType
from .widget_factory import WidgetFactory


class ConfigManager:
    """Manages dashboard configuration import/export operations."""
    
    def __init__(self):
        self.widget_factory = WidgetFactory()
        self.logger = logging.getLogger(f"{__name__}.ConfigManager")
    
    def export_config(self, config: DashboardConfig, layout: DashboardLayout, widgets: List) -> Dict[str, Any]:
        """Export dashboard configuration."""
        return {
            "config": self._export_config_section(config),
            "layout": self._export_layout_section(layout),
            "widgets": self.widget_factory.export_widgets_config(widgets)
        }
    
    def import_config(self, config_data: Dict[str, Any], config: DashboardConfig, layout: DashboardLayout, widgets: List):
        """Import dashboard configuration."""
        try:
            self._import_config_section(config_data.get("config", {}), config)
            self._import_layout_section(config_data.get("layout", {}), layout)
            self._import_widgets_section(config_data.get("widgets", []), widgets)
            self.logger.info("Dashboard configuration imported successfully")
        except Exception as e:
            self.logger.error(f"Failed to import configuration: {e}")
            raise
    
    def _export_config_section(self, config: DashboardConfig) -> Dict[str, Any]:
        """Export configuration section."""
        return {
            "title": config.title,
            "websocket_url": config.websocket_url,
            "default_theme": config.default_theme,
            "default_refresh_interval": config.default_refresh_interval,
            "enable_notifications": config.enable_notifications,
            "enable_animations": config.enable_animations
        }
    
    def _export_layout_section(self, layout: DashboardLayout) -> Dict[str, Any]:
        """Export layout section."""
        return {
            "columns": layout.columns,
            "rows": layout.rows,
            "widget_spacing": layout.widget_spacing,
            "responsive": layout.responsive,
            "theme": layout.theme,
            "auto_refresh": layout.auto_refresh,
            "refresh_interval": layout.refresh_interval
        }
    
    def _import_config_section(self, config_data: Dict[str, Any], config: DashboardConfig):
        """Import configuration section."""
        if config_data:
            config.title = config_data.get("title", config.title)
            config.websocket_url = config_data.get("websocket_url", config.websocket_url)
            config.default_theme = config_data.get("default_theme", config.default_theme)
            config.default_refresh_interval = config_data.get("default_refresh_interval", config.default_refresh_interval)
            config.enable_notifications = config_data.get("enable_notifications", config.enable_notifications)
            config.enable_animations = config_data.get("enable_animations", config.enable_animations)
    
    def _import_layout_section(self, layout_data: Dict[str, Any], layout: DashboardLayout):
        """Import layout section."""
        if layout_data:
            layout.columns = layout_data.get("columns", layout.columns)
            layout.rows = layout_data.get("rows", layout.rows)
            layout.widget_spacing = layout_data.get("widget_spacing", layout.widget_spacing)
            layout.responsive = layout_data.get("responsive", layout.responsive)
            layout.theme = layout_data.get("theme", layout.theme)
            layout.auto_refresh = layout_data.get("auto_refresh", layout.auto_refresh)
            layout.refresh_interval = layout_data.get("refresh_interval", layout.refresh_interval)
    
    def _import_widgets_section(self, widgets_data: List[Dict[str, Any]], widgets: List):
        """Import widgets section."""
        if widgets_data:
            widgets.clear()
            for widget_data in widgets_data:
                try:
                    widget = self.widget_factory.create_widget_from_config(widget_data)
                    if self.widget_factory.validate_widget(widget):
                        widgets.append(widget)
                    else:
                        self.logger.warning(f"Invalid widget configuration: {widget_data}")
                except Exception as e:
                    self.logger.error(f"Failed to create widget from config: {e}")
    
    def validate_config(self, config_data: Dict[str, Any]) -> bool:
        """Validate configuration data."""
        try:
            required_sections = ["config", "layout", "widgets"]
            for section in required_sections:
                if section not in config_data:
                    self.logger.error(f"Missing required section: {section}")
                    return False
            
            # Validate config section
            config = config_data.get("config", {})
            if not config.get("title"):
                self.logger.error("Missing title in config section")
                return False
            
            # Validate layout section
            layout = config_data.get("layout", {})
            if layout.get("columns", 0) <= 0 or layout.get("rows", 0) <= 0:
                self.logger.error("Invalid layout dimensions")
                return False
            
            # Validate widgets section
            widgets = config_data.get("widgets", [])
            if not isinstance(widgets, list):
                self.logger.error("Widgets section must be a list")
                return False
            
            for widget_data in widgets:
                if not self._validate_widget_data(widget_data):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def _validate_widget_data(self, widget_data: Dict[str, Any]) -> bool:
        """Validate individual widget data."""
        required_fields = ["widget_id", "title", "chart_type", "metric_name"]
        for field in required_fields:
            if field not in widget_data:
                self.logger.error(f"Missing required field in widget: {field}")
                return False
        
        # Validate chart type
        try:
            ChartType(widget_data["chart_type"])
        except ValueError:
            self.logger.error(f"Invalid chart type: {widget_data['chart_type']}")
            return False
        
        return True


