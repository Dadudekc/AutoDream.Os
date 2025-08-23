#!/usr/bin/env python3
"""
JavaScript Generator - V2 Dashboard System

This module handles JavaScript generation for dashboard functionality.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging
from typing import List
from .dashboard_types import DashboardWidget, DashboardLayout, DashboardConfig
from .js_utilities import JavaScriptUtilities


class JavaScriptGenerator:
    """Handles JavaScript generation for dashboard functionality"""
    
    def __init__(self, config: DashboardConfig):
        self.config = config
        self.js_utils = JavaScriptUtilities()
        self.logger = logging.getLogger(f"{__name__}.JavaScriptGenerator")
    
    def generate_javascript(self, widgets: List[DashboardWidget], layout: DashboardLayout) -> str:
        """Generate complete JavaScript for the dashboard."""
        config_js = self.js_utils.generate_config_js(widgets, layout, self.config)
        utility_functions = self.js_utils.generate_utility_functions()
        widget_functions = self.js_utils.generate_widget_functions()
        theme_functions = self.js_utils.generate_theme_functions()
        refresh_functions = self.js_utils.generate_refresh_functions()
        
        javascript = f"""{config_js}

{utility_functions}

{widget_functions}

{theme_functions}

{refresh_functions}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {{
    initializeDashboard();
    if (DASHBOARD_CONFIG.layout.auto_refresh) {{
        startAutoRefresh();
    }}
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {{
        Notification.requestPermission();
    }}
}});"""
        
        return javascript
