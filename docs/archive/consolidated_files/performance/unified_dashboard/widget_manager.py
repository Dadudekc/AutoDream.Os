"""
Dashboard Widget Manager - V2 Compliance Module
==============================================

Widget management functionality for dashboard engine.

V2 Compliance: < 300 lines, single responsibility, widget management.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import logging
from datetime import datetime
from typing import Any

from .models import DashboardConfig, DashboardWidget

logger = logging.getLogger(__name__)


class WidgetManager:
    """Widget management functionality."""

    def __init__(self):
        """Initialize widget manager."""
        self.logger = logger
        self.widgets: dict[str, DashboardWidget] = {}
        self.configs: dict[str, DashboardConfig] = {}

    def add_widget(self, widget: DashboardWidget) -> bool:
        """Add dashboard widget."""
        try:
            if not widget or not widget.widget_id:
                self.logger.error("Invalid widget provided")
                return False

            self.widgets[widget.widget_id] = widget
            self.logger.info(f"Added widget: {widget.widget_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add widget: {e}")
            return False

    def get_widget(self, widget_id: str) -> DashboardWidget | None:
        """Get dashboard widget by ID."""
        return self.widgets.get(widget_id)

    def get_all_widgets(self) -> list[DashboardWidget]:
        """Get all widgets."""
        return list(self.widgets.values())

    def update_widget(self, widget_id: str, updates: dict[str, Any]) -> bool:
        """Update dashboard widget."""
        try:
            if widget_id not in self.widgets:
                self.logger.error(f"Widget not found: {widget_id}")
                return False

            widget = self.widgets[widget_id]
            for key, value in updates.items():
                if hasattr(widget, key):
                    setattr(widget, key, value)

            widget.updated_at = datetime.now()
            self.logger.info(f"Updated widget: {widget_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update widget: {e}")
            return False

    def remove_widget(self, widget_id: str) -> bool:
        """Remove dashboard widget."""
        try:
            if widget_id in self.widgets:
                del self.widgets[widget_id]
                self.logger.info(f"Removed widget: {widget_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove widget: {e}")
            return False

    def add_config(self, config: DashboardConfig) -> bool:
        """Add dashboard configuration."""
        try:
            if not config or not config.config_id:
                self.logger.error("Invalid config provided")
                return False

            self.configs[config.config_id] = config
            self.logger.info(f"Added config: {config.config_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add config: {e}")
            return False

    def get_config(self, config_id: str) -> DashboardConfig | None:
        """Get dashboard configuration by ID."""
        return self.configs.get(config_id)

    def get_all_configs(self) -> list[DashboardConfig]:
        """Get all configurations."""
        return list(self.configs.values())

    def update_config(self, config_id: str, updates: dict[str, Any]) -> bool:
        """Update dashboard configuration."""
        try:
            if config_id not in self.configs:
                self.logger.error(f"Config not found: {config_id}")
                return False

            config = self.configs[config_id]
            for key, value in updates.items():
                if hasattr(config, key):
                    setattr(config, key, value)

            config.updated_at = datetime.now()
            self.logger.info(f"Updated config: {config_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to update config: {e}")
            return False

    def remove_config(self, config_id: str) -> bool:
        """Remove dashboard configuration."""
        try:
            if config_id in self.configs:
                del self.configs[config_id]
                self.logger.info(f"Removed config: {config_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove config: {e}")
            return False

    def get_widgets_count(self) -> int:
        """Get total widgets count."""
        return len(self.widgets)

    def get_configs_count(self) -> int:
        """Get total configs count."""
        return len(self.configs)

    def clear_all(self) -> None:
        """Clear all widgets and configs."""
        self.widgets.clear()
        self.configs.clear()
        self.logger.info("Cleared all widgets and configs")

    def get_summary(self) -> dict[str, Any]:
        """Get widgets and configs summary."""
        return {
            "total_widgets": len(self.widgets),
            "total_configs": len(self.configs),
            "widget_types": list({widget.widget_type for widget in self.widgets.values()}),
            "last_updated": max(
                (widget.updated_at for widget in self.widgets.values()), default=None
            ),
        }
