#!/usr/bin/env python3
"""
JavaScript Utilities - V2 Dashboard System

This module provides utility functions for JavaScript generation.
Follows V2 coding standards: ≤200 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List
from .dashboard_types import DashboardWidget, DashboardLayout, DashboardConfig


class JavaScriptUtilities:
    """Provides utility functions for JavaScript generation"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.JavaScriptUtilities")
    
    def generate_config_js(self, widgets: List[DashboardWidget], layout: DashboardLayout, config: DashboardConfig) -> str:
        """Generate JavaScript configuration object."""
        widgets_config = []
        for widget in widgets:
            widget_config = {
                "id": widget.widget_id,
                "metric": widget.metric_name,
                "chart_type": widget.chart_type.value,
                "refresh_interval": widget.refresh_interval,
                "width": widget.width,
                "height": widget.height,
                "position_x": widget.position_x,
                "position_y": widget.position_y
            }
            widgets_config.append(widget_config)
        
        return f"""
// Dashboard Configuration
const DASHBOARD_CONFIG = {{
    title: "{config.title}",
    websocket_url: "{config.websocket_url}",
    layout: {{
        columns: {layout.columns},
        rows: {layout.rows},
        theme: "{layout.theme}",
        auto_refresh: {str(layout.auto_refresh).lower()},
        refresh_interval: {layout.refresh_interval}
    }},
    widgets: {widgets_config}
}};

// Global variables
let autoRefreshInterval = null;
let websocket = null;"""
    
    def generate_utility_functions(self) -> str:
        """Generate utility JavaScript functions."""
        return """
// Utility Functions
function showNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, { body: message });
    }
}

function log(message, level = 'info') {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] [${level.toUpperCase()}] ${message}`);
}

function updateLastUpdate(widgetId) {
    const element = document.getElementById(`last-update-${widgetId}`);
    if (element) {
        element.textContent = new Date().toLocaleTimeString();
    }
}

function showError(message) {
    log(message, 'error');
    showNotification('Dashboard Error', message);
}"""
    
    def generate_widget_functions(self) -> str:
        """Generate widget-related JavaScript functions."""
        return """
// Widget Functions
function refreshWidget(widgetId) {
    const widget = document.getElementById(`widget-${widgetId}`);
    if (widget) {
        widget.classList.add('refreshing');
        updateLastUpdate(widgetId);
        
        // Simulate refresh delay
        setTimeout(() => {
            widget.classList.remove('refreshing');
        }, 1000);
        
        log(`Widget ${widgetId} refreshed`);
    }
}

function toggleWidget(widgetId) {
    const widget = document.getElementById(`widget-${widgetId}`);
    if (widget) {
        widget.classList.toggle('collapsed');
        log(`Widget ${widgetId} toggled`);
    }
}

function initializeDashboard() {
    log('Initializing dashboard...');
    
    // Initialize all widgets
    DASHBOARD_CONFIG.widgets.forEach(widget => {
        const widgetElement = document.getElementById(`widget-${widget.id}`);
        if (widgetElement) {
            widgetElement.dataset.metric = widget.metric;
            widgetElement.dataset.refresh = widget.refresh_interval;
        }
    });
    
    log('Dashboard initialized successfully');
}"""
    
    def generate_theme_functions(self) -> str:
        """Generate theme-related JavaScript functions."""
        return """
// Theme Functions
function changeTheme() {
    const themeSelect = document.getElementById('theme-select');
    const newTheme = themeSelect.value;
    setTheme(newTheme);
}

function setTheme(theme) {
    document.body.className = `theme-${theme}`;
    localStorage.setItem('dashboard-theme', theme);
    DASHBOARD_CONFIG.layout.theme = theme;
    log(`Theme changed to ${theme}`);
}

function toggleSettings() {
    const panel = document.getElementById('settings-panel');
    panel.classList.toggle('visible');
}"""
    
    def generate_refresh_functions(self) -> str:
        """Generate refresh-related JavaScript functions."""
        return """
// Refresh Functions
function toggleAutoRefresh() {
    const checkbox = document.getElementById('auto-refresh');
    if (checkbox.checked) {
        startAutoRefresh();
    } else {
        stopAutoRefresh();
    }
}

function updateRefreshInterval() {
    const input = document.getElementById('refresh-interval');
    const newInterval = parseInt(input.value);
    
    if (newInterval > 0) {
        DASHBOARD_CONFIG.layout.refresh_interval = newInterval;
        
        if (autoRefreshInterval) {
            stopAutoRefresh();
            startAutoRefresh();
        }
        
        log(`Refresh interval updated to ${newInterval}s`);
    }
}

function startAutoRefresh() {
    stopAutoRefresh();
    autoRefreshInterval = setInterval(refreshDashboard, DASHBOARD_CONFIG.layout.refresh_interval * 1000);
    log('Auto-refresh started');
}

function stopAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
        autoRefreshInterval = null;
        log('Auto-refresh stopped');
    }
}

function refreshDashboard() {
    log('Refreshing dashboard...');
    DASHBOARD_CONFIG.widgets.forEach(widget => {
        refreshWidget(widget.id);
    });
}"""


