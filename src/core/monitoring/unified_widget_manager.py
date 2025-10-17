"""
Unified Widget Manager - DUP-014 Consolidation
==============================================

Consolidates duplicate widget management from:
- src/core/managers/monitoring/widget_manager.py
- src/core/performance/unified_dashboard/widget_manager.py

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Integration & Core Systems Specialist
Mission: DUP-014 Metric/Widget Managers Consolidation
License: MIT
"""

import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field


class WidgetType(Enum):
    """Dashboard widget types."""
    CHART = "chart"
    TABLE = "table"
    METRIC = "metric"
    ALERT = "alert"
    CUSTOM = "custom"


@dataclass
class DashboardWidget:
    """Dashboard widget data structure."""
    widget_id: str
    widget_type: WidgetType
    title: str
    data_source: str
    config: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class UnifiedWidgetManager:
    """
    Unified widget management.
    
    Consolidates functionality from monitoring and unified_dashboard widget managers.
    Provides widget creation, configuration, and lifecycle management.
    """
    
    def __init__(self):
        """Initialize unified widget manager."""
        self.logger = logging.getLogger(__name__)
        self.widgets: Dict[str, DashboardWidget] = {}
    
    def create_widget(
        self,
        widget_type: WidgetType,
        title: str,
        data_source: str,
        config: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """
        Create a new widget.
        
        Args:
            widget_type: Type of widget
            title: Widget title
            data_source: Data source for widget
            config: Widget configuration
            
        Returns:
            Widget ID if successful, None otherwise
        """
        try:
            widget_id = str(uuid.uuid4())
            
            widget = DashboardWidget(
                widget_id=widget_id,
                widget_type=widget_type,
                title=title,
                data_source=data_source,
                config=config or {}
            )
            
            self.widgets[widget_id] = widget
            self.logger.info(f"Created widget: {widget_id} ({title})")
            
            return widget_id
            
        except Exception as e:
            self.logger.error(f"Failed to create widget: {e}")
            return None
    
    def get_widget(self, widget_id: str) -> Optional[DashboardWidget]:
        """Get widget by ID."""
        return self.widgets.get(widget_id)
    
    def get_all_widgets(self) -> List[DashboardWidget]:
        """Get all widgets."""
        return list(self.widgets.values())
    
    def get_widgets_by_type(self, widget_type: WidgetType) -> List[DashboardWidget]:
        """Get widgets of a specific type."""
        return [w for w in self.widgets.values() if w.widget_type == widget_type]
    
    def update_widget(self, widget_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update widget properties.
        
        Args:
            widget_id: ID of widget to update
            updates: Dictionary of properties to update
            
        Returns:
            True if successful, False otherwise
        """
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
        """Remove a widget."""
        try:
            if widget_id in self.widgets:
                del self.widgets[widget_id]
                self.logger.info(f"Removed widget: {widget_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Failed to remove widget: {e}")
            return False
    
    def clear_widgets(self) -> None:
        """Clear all widgets."""
        self.widgets.clear()
        self.logger.info("All widgets cleared")
    
    def get_widget_count(self) -> int:
        """Get total widget count."""
        return len(self.widgets)
    
    def get_widget_stats(self) -> Dict[str, Any]:
        """Get widget statistics."""
        stats = {
            "total_widgets": len(self.widgets),
            "by_type": {}
        }
        
        for widget_type in WidgetType:
            count = len([w for w in self.widgets.values() if w.widget_type == widget_type])
            if count > 0:
                stats["by_type"][widget_type.value] = count
        
        return stats

