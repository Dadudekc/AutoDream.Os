#!/usr/bin/env python3
"""
HTML Generator - V2 Dashboard System

This module handles HTML generation for dashboard components.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List
from .dashboard_types import DashboardWidget, DashboardLayout, DashboardConfig
from .css_generator import CSSGenerator


class HTMLGenerator:
    """Handles HTML generation for dashboard components"""
    
    def __init__(self, config: DashboardConfig):
        self.config = config
        self.css_generator = CSSGenerator()
        self.logger = logging.getLogger(f"{__name__}.HTMLGenerator")
    
    def generate_html(self, widgets: List[DashboardWidget], layout: DashboardLayout) -> str:
        """Generate complete HTML for the dashboard."""
        widgets_html = self._generate_widgets_html(widgets)
        css = self.css_generator.generate_css(layout)
        responsive_css = self.css_generator.generate_responsive_css(layout)
        animation_css = self.css_generator.generate_animation_css()
        javascript = self._generate_javascript_placeholder()
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.title}</title>
    <style>{css}{responsive_css}{animation_css}</style>
</head>
<body class="theme-{layout.theme}">
    <div class="dashboard-container">
        <header class="dashboard-header">
            <h1>{self.config.title}</h1>
            <div class="header-controls">
                <button onclick="toggleSettings()" class="btn btn-secondary">Settings</button>
                <select id="theme-select" onchange="changeTheme()">
                    <option value="dark" {'selected' if layout.theme == 'dark' else ''}>Dark Theme</option>
                    <option value="light" {'selected' if layout.theme == 'light' else ''}>Light Theme</option>
                </select>
            </div>
        </header>
        
        <div class="dashboard-grid" style="grid-template-columns: repeat({layout.columns}, 1fr);">
            {widgets_html}
        </div>
        
        <div id="settings-panel" class="settings-panel">
            <h3>Dashboard Settings</h3>
            <div class="setting-group">
                <label>
                    <input type="checkbox" id="auto-refresh" {'checked' if layout.auto_refresh else ''} onchange="toggleAutoRefresh()">
                    Auto Refresh
                </label>
                <label>
                    Refresh Interval (seconds):
                    <input type="number" id="refresh-interval" value="{layout.refresh_interval}" min="1" max="300" onchange="updateRefreshInterval()">
                </label>
            </div>
        </div>
    </div>
    
    <script>{javascript}</script>
</body>
</html>"""
        
        return html_template
    
    def _generate_widgets_html(self, widgets: List[DashboardWidget]) -> str:
        """Generate HTML for all dashboard widgets."""
        if not widgets:
            return '<div class="no-widgets">No widgets configured</div>'
        
        widgets_html = []
        for widget in widgets:
            widget_html = self._generate_widget_content(widget)
            widgets_html.append(widget_html)
        
        return '\n'.join(widgets_html)
    
    def _generate_widget_content(self, widget: DashboardWidget) -> str:
        """Generate HTML content for a single widget."""
        grid_style = f"grid-column: span {widget.width}; grid-row: span {widget.height};"
        position_style = f"grid-column-start: {widget.position_x + 1}; grid-row-start: {widget.position_y + 1};"
        
        widget_html = f"""<div class="widget widget-{widget.chart_type.value}" 
                         id="widget-{widget.widget_id}" 
                         style="{grid_style} {position_style}"
                         data-metric="{widget.metric_name}"
                         data-refresh="{widget.refresh_interval}">
            <div class="widget-header">
                <h3>{widget.title}</h3>
                <div class="widget-controls">
                    <button onclick="refreshWidget('{widget.widget_id}')" class="btn btn-small">Refresh</button>
                    <button onclick="toggleWidget('{widget.widget_id}')" class="btn btn-small">Toggle</button>
                </div>
            </div>
            <div class="widget-content">
                <div class="chart-container" id="chart-{widget.widget_id}">
                    <div class="chart-placeholder">
                        <span class="chart-type">{widget.chart_type.value.title()} Chart</span>
                        <span class="metric-name">{widget.metric_name}</span>
                    </div>
                </div>
            </div>
            <div class="widget-footer">
                <span class="refresh-info">Refreshes every {widget.refresh_interval}s</span>
                <span class="last-update">Last update: <span id="last-update-{widget.widget_id}">Never</span></span>
            </div>
        </div>"""
        
        return widget_html
    
    def _generate_javascript_placeholder(self) -> str:
        """Generate placeholder JavaScript (actual JS will be in separate module)."""
        return """
        // JavaScript functionality will be loaded from separate module
        console.log('Dashboard HTML generated successfully');
        """

