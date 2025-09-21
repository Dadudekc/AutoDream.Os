#!/usr/bin/env python3
"""
V3-010: Web Dashboard Components
===============================

Dashboard components for web dashboard system.
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .web_dashboard_models import DashboardConfig, DashboardComponent

logger = logging.getLogger(__name__)


class WebDashboardComponents:
    """Dashboard components for web dashboard system."""
    
    def __init__(self, config: DashboardConfig):
        """Initialize dashboard components."""
        self.config = config
    
    def create_agent_status_component(self) -> Dict[str, Any]:
        """Create agent status component."""
        try:
            logger.info("Creating agent status component...")
            
            component = {
                "id": "agent-status",
                "title": "Agent Status",
                "type": "table",
                "position": {"x": 0, "y": 0, "w": 6, "h": 4},
                "data_source": "/api/v1/agents",
                "refresh_interval": self.config.refresh_interval,
                "columns": [
                    {"key": "agent_id", "label": "Agent ID", "sortable": True},
                    {"key": "status", "label": "Status", "sortable": True},
                    {"key": "current_task", "label": "Current Task", "sortable": False},
                    {"key": "last_activity", "label": "Last Activity", "sortable": True},
                    {"key": "performance", "label": "Performance", "sortable": True}
                ],
                "filters": [
                    {"key": "status", "type": "select", "options": ["active", "inactive", "error"]},
                    {"key": "agent_id", "type": "text", "placeholder": "Filter by Agent ID"}
                ],
                "actions": [
                    {"name": "refresh", "label": "Refresh", "icon": "refresh"},
                    {"name": "export", "label": "Export", "icon": "download"}
                ],
                "styling": {
                    "theme": self.config.theme,
                    "responsive": self.config.responsive
                }
            }
            
            logger.info("Agent status component created successfully")
            return component
            
        except Exception as e:
            logger.error(f"Error creating agent status component: {e}")
            return {}
    
    def create_v3_pipeline_component(self) -> Dict[str, Any]:
        """Create V3 pipeline component."""
        try:
            logger.info("Creating V3 pipeline component...")
            
            component = {
                "id": "v3-pipeline",
                "title": "V3 Pipeline Status",
                "type": "pipeline",
                "position": {"x": 6, "y": 0, "w": 6, "h": 4},
                "data_source": "/api/v1/v3-contracts",
                "refresh_interval": self.config.refresh_interval,
                "pipeline_stages": [
                    {"id": "v3-001", "name": "Cloud Infrastructure", "status": "completed"},
                    {"id": "v3-004", "name": "Distributed Tracing", "status": "completed"},
                    {"id": "v3-007", "name": "ML Pipeline", "status": "completed"},
                    {"id": "v3-010", "name": "Web Dashboard", "status": "in_progress"}
                ],
                "visualization": {
                    "type": "flowchart",
                    "orientation": "horizontal",
                    "show_labels": True,
                    "show_status": True
                },
                "interactions": [
                    {"action": "click", "handler": "show_contract_details"},
                    {"action": "hover", "handler": "show_contract_tooltip"}
                ],
                "styling": {
                    "theme": self.config.theme,
                    "colors": {
                        "completed": "#4CAF50",
                        "in_progress": "#FF9800",
                        "pending": "#9E9E9E",
                        "failed": "#F44336"
                    }
                }
            }
            
            logger.info("V3 pipeline component created successfully")
            return component
            
        except Exception as e:
            logger.error(f"Error creating V3 pipeline component: {e}")
            return {}
    
    def create_system_health_component(self) -> Dict[str, Any]:
        """Create system health component."""
        try:
            logger.info("Creating system health component...")
            
            component = {
                "id": "system-health",
                "title": "System Health",
                "type": "metrics",
                "position": {"x": 0, "y": 4, "w": 6, "h": 3},
                "data_source": "/api/v1/system-health",
                "refresh_interval": self.config.refresh_interval,
                "metrics": [
                    {
                        "name": "CPU Usage",
                        "value": 0,
                        "unit": "%",
                        "threshold": 80,
                        "trend": "stable"
                    },
                    {
                        "name": "Memory Usage",
                        "value": 0,
                        "unit": "%",
                        "threshold": 85,
                        "trend": "stable"
                    },
                    {
                        "name": "Disk Usage",
                        "value": 0,
                        "unit": "%",
                        "threshold": 90,
                        "trend": "stable"
                    },
                    {
                        "name": "Network I/O",
                        "value": 0,
                        "unit": "MB/s",
                        "threshold": 100,
                        "trend": "stable"
                    }
                ],
                "visualization": {
                    "type": "gauge",
                    "show_thresholds": True,
                    "show_trends": True,
                    "animate": True
                },
                "alerts": {
                    "enabled": True,
                    "threshold_warning": True,
                    "threshold_critical": True
                },
                "styling": {
                    "theme": self.config.theme,
                    "colors": {
                        "normal": "#4CAF50",
                        "warning": "#FF9800",
                        "critical": "#F44336"
                    }
                }
            }
            
            logger.info("System health component created successfully")
            return component
            
        except Exception as e:
            logger.error(f"Error creating system health component: {e}")
            return {}
    
    def create_real_time_component(self) -> Dict[str, Any]:
        """Create real-time component."""
        try:
            logger.info("Creating real-time component...")
            
            component = {
                "id": "real-time",
                "title": "Real-Time Activity",
                "type": "stream",
                "position": {"x": 6, "y": 4, "w": 6, "h": 3},
                "data_source": "/ws/activity",
                "refresh_interval": 1000,  # Real-time updates
                "stream_config": {
                    "max_items": 100,
                    "auto_scroll": True,
                    "show_timestamps": True,
                    "filter_duplicates": True
                },
                "message_types": [
                    {"type": "agent_message", "color": "#2196F3", "icon": "message"},
                    {"type": "task_completion", "color": "#4CAF50", "icon": "check"},
                    {"type": "error", "color": "#F44336", "icon": "error"},
                    {"type": "system_event", "color": "#FF9800", "icon": "event"}
                ],
                "filters": [
                    {"key": "message_type", "type": "select", "multiple": True},
                    {"key": "agent_id", "type": "select", "multiple": True},
                    {"key": "time_range", "type": "range", "default": "1h"}
                ],
                "actions": [
                    {"name": "clear", "label": "Clear", "icon": "clear"},
                    {"name": "pause", "label": "Pause", "icon": "pause"},
                    {"name": "export", "label": "Export", "icon": "download"}
                ],
                "styling": {
                    "theme": self.config.theme,
                    "font_size": "small",
                    "show_avatars": True
                }
            }
            
            logger.info("Real-time component created successfully")
            return component
            
        except Exception as e:
            logger.error(f"Error creating real-time component: {e}")
            return {}
    
    def create_configuration_component(self) -> Dict[str, Any]:
        """Create configuration component."""
        try:
            logger.info("Creating configuration component...")
            
            component = {
                "id": "configuration",
                "title": "Configuration",
                "type": "form",
                "position": {"x": 0, "y": 7, "w": 12, "h": 3},
                "data_source": "/api/v1/configuration",
                "refresh_interval": 0,  # No auto-refresh for forms
                "form_fields": [
                    {
                        "name": "dashboard_title",
                        "label": "Dashboard Title",
                        "type": "text",
                        "value": self.config.title,
                        "required": True
                    },
                    {
                        "name": "theme",
                        "label": "Theme",
                        "type": "select",
                        "options": ["light", "dark", "auto"],
                        "value": self.config.theme,
                        "required": True
                    },
                    {
                        "name": "refresh_interval",
                        "label": "Refresh Interval (ms)",
                        "type": "number",
                        "value": self.config.refresh_interval,
                        "min": 1000,
                        "max": 60000,
                        "required": True
                    },
                    {
                        "name": "enable_websockets",
                        "label": "Enable WebSockets",
                        "type": "checkbox",
                        "value": self.config.enable_websockets
                    },
                    {
                        "name": "enable_real_time",
                        "label": "Enable Real-Time Updates",
                        "type": "checkbox",
                        "value": self.config.enable_real_time
                    }
                ],
                "actions": [
                    {"name": "save", "label": "Save", "type": "primary", "icon": "save"},
                    {"name": "reset", "label": "Reset", "type": "secondary", "icon": "refresh"},
                    {"name": "export", "label": "Export Config", "type": "secondary", "icon": "download"}
                ],
                "validation": {
                    "required_fields": ["dashboard_title", "theme", "refresh_interval"],
                    "custom_validators": ["validate_refresh_interval"]
                },
                "styling": {
                    "theme": self.config.theme,
                    "layout": "grid",
                    "columns": 2
                }
            }
            
            logger.info("Configuration component created successfully")
            return component
            
        except Exception as e:
            logger.error(f"Error creating configuration component: {e}")
            return {}



