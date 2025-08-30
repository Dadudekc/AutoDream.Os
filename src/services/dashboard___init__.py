#!/usr/bin/env python3
"""
Dashboard Module - V2 Dashboard System

This package provides comprehensive dashboard generation and management.
"""

from .dashboard_types import (
    ChartType, DashboardWidget, DashboardLayout, DashboardConfig
)
from .css_generator import CSSGenerator
from .html_generator import HTMLGenerator
from .js_utilities import JavaScriptUtilities
from .javascript_generator import JavaScriptGenerator
from .realtime_updater import RealTimeUpdater
from .widget_factory import WidgetFactory
from .config_manager import ConfigManager
from .file_generator import FileGenerator
from .dashboard_frontend import DashboardFrontend

__all__ = [
    'ChartType',
    'DashboardWidget',
    'DashboardLayout',
    'DashboardConfig',
    'CSSGenerator',
    'HTMLGenerator',
    'JavaScriptUtilities',
    'JavaScriptGenerator',
    'RealTimeUpdater',
    'WidgetFactory',
    'ConfigManager',
    'FileGenerator',
    'DashboardFrontend'
]

