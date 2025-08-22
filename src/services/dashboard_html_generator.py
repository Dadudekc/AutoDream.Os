#!/usr/bin/env python3
"""
Dashboard HTML Generator - Agent Cellphone V2
============================================

HTML generation functionality for the dashboard system.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import logging
from typing import List

from .dashboard_core import DashboardCore, DashboardWidget, ChartType

logger = logging.getLogger(__name__)


class DashboardHTMLGenerator:
    """Generates HTML for dashboard components."""
    
    def __init__(self, dashboard: DashboardCore):
        self.dashboard = dashboard
        logger.info("Dashboard HTML generator initialized")
    
    def generate_main_html(self) -> str:
        """Generate the main HTML structure for the dashboard."""
        widgets_html = self._generate_widgets_html()
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.dashboard.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/date-fns@2.29.3/index.min.js"></script>
    <link rel="stylesheet" href="dashboard_styles.css">
</head>
<body>
    {self._generate_header_html()}
    
    <div class="dashboard-container">
        {widgets_html}
    </div>
    
    {self._generate_footer_html()}
    {self._generate_settings_panel_html()}
    
    <script src="dashboard_script.js"></script>
</body>
</html>"""
        
        return html_template
    
    def _generate_header_html(self) -> str:
        """Generate the dashboard header HTML."""
        return f"""<div class="dashboard-header">
    <h1>{self.dashboard.title}</h1>
    <div class="dashboard-controls">
        <div class="connection-status" id="connection-status">
            <span class="status-dot" id="status-dot"></span>
            <span id="status-text">Connecting...</span>
        </div>
        <button id="refresh-btn" onclick="refreshDashboard()">Refresh</button>
        <button id="settings-btn" onclick="toggleSettings()">Settings</button>
    </div>
</div>"""
    
    def _generate_footer_html(self) -> str:
        """Generate the dashboard footer HTML."""
        return """<div class="dashboard-footer">
    <div class="footer-info">
        <span>Last Updated: <span id="last-updated">Never</span></span>
        <span>Active Alerts: <span id="alert-count">0</span></span>
        <span>Metrics: <span id="metrics-count">0</span></span>
    </div>
</div>"""
    
    def _generate_settings_panel_html(self) -> str:
        """Generate the settings panel HTML."""
        theme_selected = "selected" if self.dashboard.layout.theme == "dark" else ""
        light_selected = "selected" if self.dashboard.layout.theme == "light" else ""
        auto_refresh_checked = "checked" if self.dashboard.layout.auto_refresh else ""
        
        return f"""<div id="settings-panel" class="settings-panel hidden">
    <div class="settings-content">
        <h3>Dashboard Settings</h3>
        <div class="setting-group">
            <label>Theme:</label>
            <select id="theme-select" onchange="changeTheme()">
                <option value="dark" {theme_selected}>Dark</option>
                <option value="light" {light_selected}>Light</option>
            </select>
        </div>
        <div class="setting-group">
            <label>Auto Refresh:</label>
            <input type="checkbox" id="auto-refresh" {auto_refresh_checked} onchange="toggleAutoRefresh()">
        </div>
        <div class="setting-group">
            <label>Refresh Interval (seconds):</label>
            <input type="number" id="refresh-interval" value="{self.dashboard.layout.refresh_interval}" min="1" max="300" onchange="updateRefreshInterval()">
        </div>
        <button onclick="toggleSettings()">Close</button>
    </div>
</div>"""
    
    def _generate_widgets_html(self) -> str:
        """Generate HTML for all dashboard widgets."""
        widgets_html = ""
        
        for widget in self.dashboard.widgets:
            widget_html = self._generate_single_widget_html(widget)
            widgets_html += widget_html
        
        return widgets_html
    
    def _generate_single_widget_html(self, widget: DashboardWidget) -> str:
        """Generate HTML for a single widget."""
        widget_html = f"""
        <div class="widget" id="widget-{widget.widget_id}" 
             style="grid-column: span {widget.width}; grid-row: span {widget.height};">
            {self._generate_widget_header_html(widget)}
            {self._generate_widget_content_html(widget)}
            {self._generate_widget_footer_html(widget)}
        </div>
        """
        return widget_html
    
    def _generate_widget_header_html(self, widget: DashboardWidget) -> str:
        """Generate the header HTML for a widget."""
        return f"""<div class="widget-header">
    <h3 class="widget-title">{widget.title}</h3>
    <div class="widget-controls">
        <button onclick="refreshWidget('{widget.widget_id}')" title="Refresh">↻</button>
        <button onclick="configureWidget('{widget.widget_id}')" title="Configure">⚙</button>
    </div>
</div>"""
    
    def _generate_widget_content_html(self, widget: DashboardWidget) -> str:
        """Generate the content HTML for a widget based on its chart type."""
        if widget.chart_type in [ChartType.LINE, ChartType.BAR, ChartType.AREA, ChartType.SCATTER]:
            return f'<canvas id="chart-{widget.widget_id}" class="chart-canvas"></canvas>'
        
        elif widget.chart_type == ChartType.PIE:
            return f'<canvas id="chart-{widget.widget_id}" class="chart-canvas pie-chart"></canvas>'
        
        elif widget.chart_type == ChartType.GAUGE:
            return self._generate_gauge_html(widget)
        
        elif widget.chart_type == ChartType.TABLE:
            return self._generate_table_html(widget)
        
        elif widget.chart_type == ChartType.HEATMAP:
            return f'<div id="heatmap-{widget.widget_id}" class="heatmap-container"></div>'
        
        else:
            return f'<div class="widget-placeholder">Chart type {widget.chart_type.value} not implemented</div>'
    
    def _generate_gauge_html(self, widget: DashboardWidget) -> str:
        """Generate HTML for gauge chart widgets."""
        return f"""<div class="gauge-container" id="gauge-{widget.widget_id}">
    <canvas id="chart-{widget.widget_id}" class="gauge-canvas"></canvas>
    <div class="gauge-value" id="gauge-value-{widget.widget_id}">0</div>
    <div class="gauge-unit" id="gauge-unit-{widget.widget_id}">%</div>
</div>"""
    
    def _generate_table_html(self, widget: DashboardWidget) -> str:
        """Generate HTML for table widgets."""
        return f"""<div class="table-container">
    <table id="table-{widget.widget_id}" class="data-table">
        <thead>
            <tr>
                <th>Timestamp</th>
                <th>Value</th>
                <th>Unit</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>
</div>"""
    
    def _generate_widget_footer_html(self, widget: DashboardWidget) -> str:
        """Generate the footer HTML for a widget."""
        return f"""<div class="widget-footer">
    <span class="widget-status" id="status-{widget.widget_id}">Loading...</span>
    <span class="widget-updated" id="updated-{widget.widget_id}">Never</span>
</div>"""
    
    def generate_widget_config_html(self, widget: DashboardWidget) -> str:
        """Generate HTML for widget configuration modal."""
        return f"""<div id="config-modal-{widget.widget_id}" class="config-modal hidden">
    <div class="config-content">
        <h3>Configure {widget.title}</h3>
        <div class="config-group">
            <label>Title:</label>
            <input type="text" id="config-title-{widget.widget_id}" value="{widget.title}">
        </div>
        <div class="config-group">
            <label>Refresh Interval (seconds):</label>
            <input type="number" id="config-refresh-{widget.widget_id}" value="{widget.refresh_interval}" min="1" max="300">
        </div>
        <div class="config-group">
            <label>Width (columns):</label>
            <input type="number" id="config-width-{widget.widget_id}" value="{widget.width}" min="1" max="12">
        </div>
        <div class="config-group">
            <label>Height (rows):</label>
            <input type="number" id="config-height-{widget.widget_id}" value="{widget.height}" min="1" max="8">
        </div>
        <div class="config-buttons">
            <button onclick="saveWidgetConfig('{widget.widget_id}')">Save</button>
            <button onclick="closeWidgetConfig('{widget.widget_id}')">Cancel</button>
        </div>
    </div>
</div>"""
    
    def generate_standalone_html(self, include_inline_styles: bool = False) -> str:
        """Generate standalone HTML with optional inline styles."""
        if include_inline_styles:
            # This would include CSS inline - implementation depends on CSS generator
            return self.generate_main_html()
        else:
            return self.generate_main_html()
