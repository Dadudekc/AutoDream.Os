"""
Dashboard Frontend for Agent_Cellphone_V2_Repository
Real-time dashboard frontend with HTML, CSS, and JavaScript generation.
"""

import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartType(Enum):
    """Types of charts available for dashboard widgets."""
    LINE = "line"
    BAR = "bar"
    PIE = "pie"
    GAUGE = "gauge"
    AREA = "area"
    SCATTER = "scatter"
    HISTOGRAM = "histogram"
    HEATMAP = "heatmap"
    TABLE = "table"


@dataclass
class DashboardWidget:
    """Dashboard widget configuration."""
    widget_id: str
    title: str
    chart_type: ChartType
    metric_name: str
    refresh_interval: int = 5  # seconds
    width: int = 6  # grid columns (1-12)
    height: int = 4  # grid rows
    position_x: int = 0
    position_y: int = 0
    options: Dict[str, Any] = field(default_factory=dict)
    filters: Dict[str, str] = field(default_factory=dict)
    aggregation: str = "raw"  # raw, avg, max, min, sum
    time_range: int = 3600  # seconds (1 hour default)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""
    columns: int = 12
    rows: int = 8
    widget_spacing: int = 10
    responsive: bool = True
    theme: str = "dark"  # dark, light
    auto_refresh: bool = True
    refresh_interval: int = 5  # seconds


class DashboardFrontend:
    """Frontend generator for performance dashboard."""
    
    def __init__(self, websocket_url: Optional[str] = None):
        self.widgets: List[DashboardWidget] = []
        self.layout = DashboardLayout()
        self.websocket_url = websocket_url or "ws://localhost:8080/ws"
        self.title = "Agent Cellphone V2 - Performance Dashboard"
        
        logger.info("Dashboard frontend initialized")
    
    def add_widget(self, widget: DashboardWidget):
        """Add a widget to the dashboard."""
        self.widgets.append(widget)
        logger.info(f"Added widget: {widget.title} ({widget.chart_type.value})")
    
    def remove_widget(self, widget_id: str):
        """Remove a widget from the dashboard."""
        self.widgets = [w for w in self.widgets if w.widget_id != widget_id]
        logger.info(f"Removed widget: {widget_id}")
    
    def set_layout(self, layout: DashboardLayout):
        """Set dashboard layout configuration."""
        self.layout = layout
        logger.info(f"Updated layout: {layout.columns}x{layout.rows} grid")
    
    def generate_html(self) -> str:
        """Generate complete HTML for the dashboard."""
        widgets_html = self._generate_widgets_html()
        css = self._generate_css()
        javascript = self._generate_javascript()
        
        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/date-fns@2.29.3/index.min.js"></script>
    <style>
        {css}
    </style>
</head>
<body>
    <div class="dashboard-header">
        <h1>{self.title}</h1>
        <div class="dashboard-controls">
            <div class="connection-status" id="connection-status">
                <span class="status-dot" id="status-dot"></span>
                <span id="status-text">Connecting...</span>
            </div>
            <button id="refresh-btn" onclick="refreshDashboard()">Refresh</button>
            <button id="settings-btn" onclick="toggleSettings()">Settings</button>
        </div>
    </div>
    
    <div class="dashboard-container">
        {widgets_html}
    </div>
    
    <div class="dashboard-footer">
        <div class="footer-info">
            <span>Last Updated: <span id="last-updated">Never</span></span>
            <span>Active Alerts: <span id="alert-count">0</span></span>
            <span>Metrics: <span id="metrics-count">0</span></span>
        </div>
    </div>
    
    <!-- Settings Panel -->
    <div id="settings-panel" class="settings-panel hidden">
        <div class="settings-content">
            <h3>Dashboard Settings</h3>
            <div class="setting-group">
                <label>Theme:</label>
                <select id="theme-select" onchange="changeTheme()">
                    <option value="dark" {"selected" if self.layout.theme == "dark" else ""}>Dark</option>
                    <option value="light" {"selected" if self.layout.theme == "light" else ""}>Light</option>
                </select>
            </div>
            <div class="setting-group">
                <label>Auto Refresh:</label>
                <input type="checkbox" id="auto-refresh" {"checked" if self.layout.auto_refresh else ""} onchange="toggleAutoRefresh()">
            </div>
            <div class="setting-group">
                <label>Refresh Interval (seconds):</label>
                <input type="number" id="refresh-interval" value="{self.layout.refresh_interval}" min="1" max="300" onchange="updateRefreshInterval()">
            </div>
            <button onclick="toggleSettings()">Close</button>
        </div>
    </div>
    
    <script>
        {javascript}
    </script>
</body>
</html>"""
        
        return html_template
    
    def _generate_widgets_html(self) -> str:
        """Generate HTML for dashboard widgets."""
        widgets_html = ""
        
        for widget in self.widgets:
            widget_html = f"""
            <div class="widget" id="widget-{widget.widget_id}" 
                 style="grid-column: span {widget.width}; grid-row: span {widget.height};">
                <div class="widget-header">
                    <h3 class="widget-title">{widget.title}</h3>
                    <div class="widget-controls">
                        <button onclick="refreshWidget('{widget.widget_id}')" title="Refresh">↻</button>
                        <button onclick="configureWidget('{widget.widget_id}')" title="Configure">⚙</button>
                    </div>
                </div>
                <div class="widget-content">
                    {self._generate_widget_content(widget)}
                </div>
                <div class="widget-footer">
                    <span class="widget-status" id="status-{widget.widget_id}">Loading...</span>
                    <span class="widget-updated" id="updated-{widget.widget_id}">Never</span>
                </div>
            </div>
            """
            widgets_html += widget_html
        
        return widgets_html
    
    def _generate_widget_content(self, widget: DashboardWidget) -> str:
        """Generate content for a specific widget based on its type."""
        if widget.chart_type in [ChartType.LINE, ChartType.BAR, ChartType.AREA, ChartType.SCATTER]:
            return f'<canvas id="chart-{widget.widget_id}" class="chart-canvas"></canvas>'
        
        elif widget.chart_type == ChartType.PIE:
            return f'<canvas id="chart-{widget.widget_id}" class="chart-canvas pie-chart"></canvas>'
        
        elif widget.chart_type == ChartType.GAUGE:
            return f'''
            <div class="gauge-container" id="gauge-{widget.widget_id}">
                <canvas id="chart-{widget.widget_id}" class="gauge-canvas"></canvas>
                <div class="gauge-value" id="gauge-value-{widget.widget_id}">0</div>
                <div class="gauge-unit" id="gauge-unit-{widget.widget_id}">%</div>
            </div>
            '''
        
        elif widget.chart_type == ChartType.TABLE:
            return f'''
            <div class="table-container">
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
            </div>
            '''
        
        elif widget.chart_type == ChartType.HEATMAP:
            return f'<div id="heatmap-{widget.widget_id}" class="heatmap-container"></div>'
        
        else:
            return f'<div class="widget-placeholder">Chart type {widget.chart_type.value} not implemented</div>'
    
    def _generate_css(self) -> str:
        """Generate CSS styles for the dashboard."""
        theme_colors = {
            "dark": {
                "bg": "#1a1a1a",
                "surface": "#2d2d2d",
                "primary": "#4a9eff",
                "text": "#ffffff",
                "text_secondary": "#b0b0b0",
                "border": "#404040",
                "success": "#00c851",
                "warning": "#ffbb33",
                "danger": "#ff4444"
            },
            "light": {
                "bg": "#f5f5f5",
                "surface": "#ffffff",
                "primary": "#2196f3",
                "text": "#333333",
                "text_secondary": "#666666",
                "border": "#e0e0e0",
                "success": "#4caf50",
                "warning": "#ff9800",
                "danger": "#f44336"
            }
        }
        
        colors = theme_colors[self.layout.theme]
        
        css = f"""
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: {colors['bg']};
            color: {colors['text']};
            line-height: 1.6;
        }}
        
        .dashboard-header {{
            background-color: {colors['surface']};
            border-bottom: 1px solid {colors['border']};
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .dashboard-header h1 {{
            color: {colors['primary']};
            font-size: 1.5rem;
            font-weight: 600;
        }}
        
        .dashboard-controls {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .connection-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .status-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
            background-color: {colors['warning']};
            animation: pulse 2s infinite;
        }}
        
        .status-dot.connected {{
            background-color: {colors['success']};
            animation: none;
        }}
        
        .status-dot.disconnected {{
            background-color: {colors['danger']};
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        button {{
            background-color: {colors['primary']};
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background-color 0.3s;
        }}
        
        button:hover {{
            opacity: 0.8;
        }}
        
        .dashboard-container {{
            padding: 2rem;
            display: grid;
            grid-template-columns: repeat({self.layout.columns}, 1fr);
            grid-template-rows: repeat({self.layout.rows}, minmax(200px, 1fr));
            gap: {self.layout.widget_spacing}px;
            min-height: calc(100vh - 140px);
        }}
        
        .widget {{
            background-color: {colors['surface']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            transition: box-shadow 0.3s;
        }}
        
        .widget:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .widget-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid {colors['border']};
        }}
        
        .widget-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {colors['text']};
        }}
        
        .widget-controls {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .widget-controls button {{
            background: none;
            border: 1px solid {colors['border']};
            color: {colors['text_secondary']};
            padding: 0.25rem 0.5rem;
            font-size: 0.8rem;
            border-radius: 4px;
        }}
        
        .widget-content {{
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        
        .chart-canvas {{
            max-width: 100%;
            max-height: 100%;
        }}
        
        .gauge-container {{
            position: relative;
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }}
        
        .gauge-canvas {{
            width: 150px;
            height: 150px;
        }}
        
        .gauge-value {{
            position: absolute;
            font-size: 2rem;
            font-weight: bold;
            color: {colors['primary']};
        }}
        
        .gauge-unit {{
            position: absolute;
            bottom: 30%;
            font-size: 0.9rem;
            color: {colors['text_secondary']};
        }}
        
        .table-container {{
            width: 100%;
            height: 100%;
            overflow: auto;
        }}
        
        .data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}
        
        .data-table th,
        .data-table td {{
            padding: 0.5rem;
            text-align: left;
            border-bottom: 1px solid {colors['border']};
        }}
        
        .data-table th {{
            background-color: {colors['bg']};
            font-weight: 600;
            position: sticky;
            top: 0;
        }}
        
        .widget-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 0.5rem;
            padding-top: 0.5rem;
            border-top: 1px solid {colors['border']};
            font-size: 0.8rem;
            color: {colors['text_secondary']};
        }}
        
        .dashboard-footer {{
            background-color: {colors['surface']};
            border-top: 1px solid {colors['border']};
            padding: 1rem 2rem;
            text-align: center;
        }}
        
        .footer-info {{
            display: flex;
            justify-content: center;
            gap: 2rem;
            font-size: 0.9rem;
            color: {colors['text_secondary']};
        }}
        
        .settings-panel {{
            position: fixed;
            top: 0;
            right: 0;
            width: 300px;
            height: 100vh;
            background-color: {colors['surface']};
            border-left: 1px solid {colors['border']};
            padding: 2rem;
            transform: translateX(100%);
            transition: transform 0.3s;
            z-index: 1000;
        }}
        
        .settings-panel.visible {{
            transform: translateX(0);
        }}
        
        .settings-content h3 {{
            margin-bottom: 1.5rem;
            color: {colors['primary']};
        }}
        
        .setting-group {{
            margin-bottom: 1rem;
        }}
        
        .setting-group label {{
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }}
        
        .setting-group input,
        .setting-group select {{
            width: 100%;
            padding: 0.5rem;
            border: 1px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['bg']};
            color: {colors['text']};
        }}
        
        .hidden {{
            display: none;
        }}
        
        .widget-placeholder {{
            display: flex;
            align-items: center;
            justify-content: center;
            color: {colors['text_secondary']};
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .dashboard-container {{
                grid-template-columns: 1fr;
                padding: 1rem;
            }}
            
            .widget {{
                grid-column: span 1 !important;
            }}
            
            .dashboard-header {{
                padding: 1rem;
            }}
            
            .dashboard-controls {{
                flex-direction: column;
                gap: 0.5rem;
            }}
        }}
        """
        
        return css
    
    def generate_javascript(self) -> str:
        """Generate JavaScript for the dashboard."""
        widget_configs = []
        for widget in self.widgets:
            config = {
                "id": widget.widget_id,
                "title": widget.title,
                "chart_type": widget.chart_type.value,
                "metric_name": widget.metric_name,
                "refresh_interval": widget.refresh_interval,
                "aggregation": widget.aggregation,
                "time_range": widget.time_range,
                "options": widget.options,
                "filters": widget.filters
            }
            widget_configs.append(config)
        
        javascript = f"""
        // Dashboard Configuration
        const DASHBOARD_CONFIG = {{
            websocket_url: '{self.websocket_url}',
            widgets: {json.dumps(widget_configs, indent=2)},
            layout: {{
                auto_refresh: {str(self.layout.auto_refresh).lower()},
                refresh_interval: {self.layout.refresh_interval},
                theme: '{self.layout.theme}'
            }}
        }};
        
        // Global variables
        let websocket = null;
        let charts = {{}};
        let isConnected = false;
        let autoRefreshInterval = null;
        let lastUpdateTime = null;
        
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {{
            initializeDashboard();
        }});
        
        function initializeDashboard() {{
            console.log('Initializing dashboard...');
            
            // Initialize WebSocket connection
            connectWebSocket();
            
            // Initialize charts
            initializeCharts();
            
            // Start auto-refresh if enabled
            if (DASHBOARD_CONFIG.layout.auto_refresh) {{
                startAutoRefresh();
            }}
            
            // Initialize theme
            setTheme(DASHBOARD_CONFIG.layout.theme);
        }}
        
        function connectWebSocket() {{
            console.log('Connecting to WebSocket:', DASHBOARD_CONFIG.websocket_url);
            
            try {{
                websocket = new WebSocket(DASHBOARD_CONFIG.websocket_url);
                
                websocket.onopen = function(event) {{
                    console.log('WebSocket connected');
                    isConnected = true;
                    updateConnectionStatus(true);
                    
                    // Subscribe to all metrics
                    DASHBOARD_CONFIG.widgets.forEach(widget => {{
                        subscribeToMetric(widget.metric_name);
                    }});
                    
                    // Request initial data
                    requestMetricsData();
                }};
                
                websocket.onmessage = function(event) {{
                    try {{
                        const data = JSON.parse(event.data);
                        handleWebSocketMessage(data);
                    }} catch (error) {{
                        console.error('Error parsing WebSocket message:', error);
                    }}
                }};
                
                websocket.onclose = function(event) {{
                    console.log('WebSocket disconnected');
                    isConnected = false;
                    updateConnectionStatus(false);
                    
                    // Attempt to reconnect after 5 seconds
                    setTimeout(connectWebSocket, 5000);
                }};
                
                websocket.onerror = function(error) {{
                    console.error('WebSocket error:', error);
                    updateConnectionStatus(false);
                }};
            }} catch (error) {{
                console.error('Error creating WebSocket:', error);
                updateConnectionStatus(false);
            }}
        }}
        
        function handleWebSocketMessage(data) {{
            console.log('Received WebSocket message:', data.type);
            
            switch (data.type) {{
                case 'connection':
                    console.log('Connection confirmed:', data.connection_id);
                    break;
                
                case 'metrics_update':
                case 'metrics_data':
                    updateChartsWithData(data.data);
                    updateLastUpdateTime();
                    break;
                
                case 'alert':
                    handleAlert(data.data);
                    break;
                
                case 'subscription_confirmed':
                    console.log('Subscribed to metric:', data.metric_name);
                    break;
                
                default:
                    console.log('Unknown message type:', data.type);
            }}
        }}
        
        function subscribeToMetric(metricName) {{
            if (websocket && websocket.readyState === WebSocket.OPEN) {{
                websocket.send(JSON.stringify({{
                    type: 'subscribe',
                    metric_name: metricName
                }}));
            }}
        }}
        
        function requestMetricsData() {{
            if (websocket && websocket.readyState === WebSocket.OPEN) {{
                const metricNames = DASHBOARD_CONFIG.widgets.map(w => w.metric_name);
                websocket.send(JSON.stringify({{
                    type: 'get_metrics',
                    metric_names: metricNames
                }}));
            }}
        }}
        
        function initializeCharts() {{
            DASHBOARD_CONFIG.widgets.forEach(widget => {{
                initializeChart(widget);
            }});
        }}
        
        function initializeChart(widget) {{
            const canvas = document.getElementById(`chart-${{widget.id}}`);
            if (!canvas) {{
                console.warn(`Canvas not found for widget: ${{widget.id}}`);
                return;
            }}
            
            const ctx = canvas.getContext('2d');
            
            let chartConfig = {{
                type: widget.chart_type,
                data: {{
                    labels: [],
                    datasets: [{{
                        label: widget.title,
                        data: [],
                        borderColor: '#4a9eff',
                        backgroundColor: 'rgba(74, 158, 255, 0.1)',
                        borderWidth: 2,
                        fill: widget.chart_type === 'area'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{
                            type: 'time',
                            time: {{
                                unit: 'minute'
                            }}
                        }},
                        y: {{
                            beginAtZero: true
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            display: true
                        }}
                    }},
                    ...widget.options
                }}
            }};
            
            // Special handling for different chart types
            if (widget.chart_type === 'gauge') {{
                chartConfig = createGaugeConfig(widget);
            }} else if (widget.chart_type === 'pie') {{
                chartConfig = createPieConfig(widget);
            }}
            
            try {{
                charts[widget.id] = new Chart(ctx, chartConfig);
                updateWidgetStatus(widget.id, 'Ready');
            }} catch (error) {{
                console.error(`Error creating chart for widget ${{widget.id}}:`, error);
                updateWidgetStatus(widget.id, 'Error');
            }}
        }}
        
        function createGaugeConfig(widget) {{
            return {{
                type: 'doughnut',
                data: {{
                    datasets: [{{
                        data: [0, 100],
                        backgroundColor: ['#4a9eff', '#e0e0e0'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    circumference: Math.PI,
                    rotation: Math.PI,
                    cutout: '80%',
                    plugins: {{
                        legend: {{
                            display: false
                        }},
                        tooltip: {{
                            enabled: false
                        }}
                    }}
                }}
            }};
        }}
        
        function createPieConfig(widget) {{
            return {{
                type: 'pie',
                data: {{
                    labels: [],
                    datasets: [{{
                        data: [],
                        backgroundColor: [
                            '#4a9eff', '#00c851', '#ffbb33', '#ff4444',
                            '#9c27b0', '#ff9800', '#2196f3', '#4caf50'
                        ]
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            position: 'right'
                        }}
                    }}
                }}
            }};
        }}
        
        function updateChartsWithData(metricsData) {{
            DASHBOARD_CONFIG.widgets.forEach(widget => {{
                const metricData = metricsData[widget.metric_name];
                if (metricData) {{
                    updateChart(widget, metricData);
                    updateWidgetStatus(widget.id, 'Updated');
                }}
            }});
        }}
        
        function updateChart(widget, metricData) {{
            const chart = charts[widget.id];
            if (!chart) return;
            
            if (widget.chart_type === 'gauge') {{
                updateGauge(widget, metricData);
            }} else if (widget.chart_type === 'table') {{
                updateTable(widget, metricData);
            }} else {{
                updateTimeSeriesChart(chart, metricData);
            }}
        }}
        
        function updateGauge(widget, metricData) {{
            const chart = charts[widget.id];
            const value = metricData.value || 0;
            const maxValue = widget.options.max_value || 100;
            
            chart.data.datasets[0].data = [value, maxValue - value];
            chart.update('none');
            
            // Update gauge value display
            const valueElement = document.getElementById(`gauge-value-${{widget.id}}`);
            const unitElement = document.getElementById(`gauge-unit-${{widget.id}}`);
            
            if (valueElement) {{
                valueElement.textContent = Math.round(value);
            }}
            if (unitElement) {{
                unitElement.textContent = metricData.unit || '';
            }}
        }}
        
        function updateTable(widget, metricData) {{
            const table = document.getElementById(`table-${{widget.id}}`);
            if (!table) return;
            
            const tbody = table.querySelector('tbody');
            
            // Add new row
            const row = tbody.insertRow(0);
            row.insertCell(0).textContent = new Date(metricData.timestamp * 1000).toLocaleTimeString();
            row.insertCell(1).textContent = metricData.value;
            row.insertCell(2).textContent = metricData.unit || '';
            
            // Keep only last 10 rows
            while (tbody.rows.length > 10) {{
                tbody.deleteRow(tbody.rows.length - 1);
            }}
        }}
        
        function updateTimeSeriesChart(chart, metricData) {{
            const now = new Date(metricData.timestamp * 1000);
            
            chart.data.labels.push(now);
            chart.data.datasets[0].data.push(metricData.value);
            
            // Keep only last 50 data points
            if (chart.data.labels.length > 50) {{
                chart.data.labels.shift();
                chart.data.datasets[0].data.shift();
            }}
            
            chart.update('none');
        }}
        
        function updateConnectionStatus(connected) {{
            const statusDot = document.getElementById('status-dot');
            const statusText = document.getElementById('status-text');
            
            if (connected) {{
                statusDot.className = 'status-dot connected';
                statusText.textContent = 'Connected';
            }} else {{
                statusDot.className = 'status-dot disconnected';
                statusText.textContent = 'Disconnected';
            }}
        }}
        
        function updateWidgetStatus(widgetId, status) {{
            const statusElement = document.getElementById(`status-${{widgetId}}`);
            if (statusElement) {{
                statusElement.textContent = status;
            }}
        }}
        
        function updateLastUpdateTime() {{
            lastUpdateTime = new Date();
            const element = document.getElementById('last-updated');
            if (element) {{
                element.textContent = lastUpdateTime.toLocaleTimeString();
            }}
        }}
        
        function handleAlert(alertData) {{
            console.warn('Alert received:', alertData);
            
            // Update alert count
            const alertCountElement = document.getElementById('alert-count');
            if (alertCountElement) {{
                const currentCount = parseInt(alertCountElement.textContent) || 0;
                alertCountElement.textContent = currentCount + 1;
            }}
            
            // Show notification (if supported)
            if ('Notification' in window && Notification.permission === 'granted') {{
                new Notification(`Alert: ${{alertData.rule_name}}`, {{
                    body: alertData.message,
                    icon: '/static/alert-icon.png'
                }});
            }}
        }}
        
        function refreshDashboard() {{
            console.log('Refreshing dashboard...');
            requestMetricsData();
        }}
        
        function refreshWidget(widgetId) {{
            console.log('Refreshing widget:', widgetId);
            const widget = DASHBOARD_CONFIG.widgets.find(w => w.id === widgetId);
            if (widget && websocket && websocket.readyState === WebSocket.OPEN) {{
                websocket.send(JSON.stringify({{
                    type: 'get_metrics',
                    metric_names: [widget.metric_name]
                }}));
            }}
        }}
        
        function configureWidget(widgetId) {{
            console.log('Configure widget:', widgetId);
            // TODO: Implement widget configuration
            alert('Widget configuration not yet implemented');
        }}
        
        function toggleSettings() {{
            const panel = document.getElementById('settings-panel');
            panel.classList.toggle('visible');
        }}
        
        function changeTheme() {{
            const themeSelect = document.getElementById('theme-select');
            const newTheme = themeSelect.value;
            setTheme(newTheme);
        }}
        
        function setTheme(theme) {{
            document.body.className = `theme-${{theme}}`;
            localStorage.setItem('dashboard-theme', theme);
        }}
        
        function toggleAutoRefresh() {{
            const checkbox = document.getElementById('auto-refresh');
            if (checkbox.checked) {{
                startAutoRefresh();
            }} else {{
                stopAutoRefresh();
            }}
        }}
        
        function updateRefreshInterval() {{
            const input = document.getElementById('refresh-interval');
            const newInterval = parseInt(input.value);
            
            if (newInterval > 0) {{
                DASHBOARD_CONFIG.layout.refresh_interval = newInterval;
                
                if (autoRefreshInterval) {{
                    stopAutoRefresh();
                    startAutoRefresh();
                }}
            }}
        }}
        
        function startAutoRefresh() {{
            stopAutoRefresh();
            autoRefreshInterval = setInterval(refreshDashboard, DASHBOARD_CONFIG.layout.refresh_interval * 1000);
        }}
        
        function stopAutoRefresh() {{
            if (autoRefreshInterval) {{
                clearInterval(autoRefreshInterval);
                autoRefreshInterval = null;
            }}
        }}
        
        // Request notification permission
        if ('Notification' in window && Notification.permission === 'default') {{
            Notification.requestPermission();
        }}
        """
        
        return javascript


class RealTimeUpdater:
    """Real-time updater for dashboard components."""
    
    def __init__(self):
        self.websocket = None
        self.update_callbacks: List[Callable] = []
        
        logger.info("Real-time updater initialized")
    
    def add_update_callback(self, callback: Callable):
        """Add callback for real-time updates."""
        self.update_callbacks.append(callback)
    
    async def send_update(self, data: Dict[str, Any]):
        """Send update through WebSocket."""
        if self.websocket:
            try:
                await self.websocket.send(json.dumps(data))
            except Exception as e:
                logger.error(f"Error sending WebSocket update: {e}")
    
    def trigger_callbacks(self, data: Dict[str, Any]):
        """Trigger all update callbacks."""
        for callback in self.update_callbacks:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in update callback: {e}")


# Export all classes
__all__ = [
    'ChartType', 'DashboardWidget', 'DashboardLayout',
    'DashboardFrontend', 'RealTimeUpdater'
]
