#!/usr/bin/env python3
"""
Dashboard JavaScript Generator - Agent Cellphone V2
=================================================

JavaScript generation functionality for the dashboard system.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, List

from .dashboard_core import DashboardCore, DashboardWidget, ChartType

logger = logging.getLogger(__name__)


class DashboardJSGenerator:
    """Generates JavaScript for dashboard functionality."""

    def __init__(self, dashboard: DashboardCore):
        self.dashboard = dashboard
        logger.info("Dashboard JavaScript generator initialized")

    def generate_main_js(self) -> str:
        """Generate the main JavaScript for the dashboard."""
        js = f"""
        // Dashboard Main JavaScript
        let dashboardConfig = {{
            websocketUrl: '{self.dashboard.websocket_url}',
            autoRefresh: {str(self.dashboard.layout.auto_refresh).lower()},
            refreshInterval: {self.dashboard.layout.refresh_interval} * 1000,
            theme: '{self.dashboard.layout.theme}'
        }};

        let charts = {{}};
        let websocket = null;
        let refreshTimer = null;

        {self._generate_initialization_js()}
        {self._generate_websocket_js()}
        {self._generate_chart_js()}
        {self._generate_ui_js()}
        {self._generate_utility_js()}
        """

        return js

    def _generate_initialization_js(self) -> str:
        """Generate JavaScript for dashboard initialization."""
        return """
        // Initialize dashboard when DOM is loaded
        document.addEventListener('DOMContentLoaded', function() {
            initializeDashboard();
            setupEventListeners();
            if (dashboardConfig.autoRefresh) {
                startAutoRefresh();
            }
        });

        function initializeDashboard() {
            console.log('Initializing dashboard...');
            updateConnectionStatus('Connecting...', 'connecting');
            initializeCharts();
            updateLastUpdated();
            updateMetricsCount();
        }

        function setupEventListeners() {
            // Refresh button
            document.getElementById('refresh-btn').addEventListener('click', refreshDashboard);

            // Settings button
            document.getElementById('settings-btn').addEventListener('click', toggleSettings);

            // Theme selector
            document.getElementById('theme-select').addEventListener('change', changeTheme);

            // Auto refresh toggle
            document.getElementById('auto-refresh').addEventListener('change', toggleAutoRefresh);

            // Refresh interval input
            document.getElementById('refresh-interval').addEventListener('change', updateRefreshInterval);
        }

        function initializeCharts() {
            const widgets = document.querySelectorAll('.widget');
            widgets.forEach(widget => {
                const widgetId = widget.id.replace('widget-', '');
                const chartCanvas = widget.querySelector('.chart-canvas');
                if (chartCanvas) {
                    createChart(widgetId, chartCanvas);
                }
            });
        }"""

    def _generate_websocket_js(self) -> str:
        """Generate JavaScript for WebSocket functionality."""
        return """
        function connectWebSocket() {
            try {
                websocket = new WebSocket(dashboardConfig.websocketUrl);

                websocket.onopen = function(event) {
                    console.log('WebSocket connected');
                    updateConnectionStatus('Connected', 'connected');
                };

                websocket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    handleWebSocketMessage(data);
                };

                websocket.onclose = function(event) {
                    console.log('WebSocket disconnected');
                    updateConnectionStatus('Disconnected', 'disconnected');
                    // Attempt to reconnect after 5 seconds
                    setTimeout(connectWebSocket, 5000);
                };

                websocket.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    updateConnectionStatus('Error', 'disconnected');
                };

            } catch (error) {
                console.error('Failed to create WebSocket:', error);
                updateConnectionStatus('Failed', 'disconnected');
            }
        }

        function handleWebSocketMessage(data) {
            if (data.type === 'metric_update') {
                updateMetric(data.widget_id, data.value, data.timestamp);
            } else if (data.type === 'alert') {
                showAlert(data.message, data.level);
            } else if (data.type === 'status_update') {
                updateSystemStatus(data.status);
            }
        }

        function updateMetric(widgetId, value, timestamp) {
            const widget = document.getElementById(`widget-${widgetId}`);
            if (!widget) return;

            const chart = charts[widgetId];
            if (chart) {
                updateChartData(chart, value, timestamp);
            }

            updateWidgetStatus(widgetId, 'Updated', timestamp);
        }"""

    def _generate_chart_js(self) -> str:
        """Generate JavaScript for chart functionality."""
        return """
        function createChart(widgetId, canvas) {
            const ctx = canvas.getContext('2d');
            const widget = document.getElementById(`widget-${widgetId}`);
            const chartType = getChartType(widget);

            let chart;

            switch (chartType) {
                case 'line':
                    chart = createLineChart(ctx, widgetId);
                    break;
                case 'bar':
                    chart = createBarChart(ctx, widgetId);
                    break;
                case 'pie':
                    chart = createPieChart(ctx, widgetId);
                    break;
                case 'gauge':
                    chart = createGaugeChart(ctx, widgetId);
                    break;
                case 'table':
                    chart = createTableChart(widgetId);
                    break;
                default:
                    console.warn(`Unsupported chart type: ${chartType}`);
                    return;
            }

            charts[widgetId] = chart;
            console.log(`Chart created for widget ${widgetId}`);
        }

        function getChartType(widget) {
            // Extract chart type from widget data attributes or content
            const chartCanvas = widget.querySelector('.chart-canvas');
            if (chartCanvas.classList.contains('pie-chart')) return 'pie';
            if (widget.querySelector('.gauge-container')) return 'gauge';
            if (widget.querySelector('.data-table')) return 'table';

            // Default to line chart
            return 'line';
        }

        function createLineChart(ctx, widgetId) {
            return new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Metric',
                        data: [],
                        borderColor: '#4a9eff',
                        backgroundColor: 'rgba(74, 158, 255, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        function createBarChart(ctx, widgetId) {
            return new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Metric',
                        data: [],
                        backgroundColor: '#4a9eff'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function createPieChart(ctx, widgetId) {
            return new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Value 1', 'Value 2', 'Value 3'],
                    datasets: [{
                        data: [30, 40, 30],
                        backgroundColor: ['#4a9eff', '#00c851', '#ffbb33']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function createGaugeChart(ctx, widgetId) {
            // Simple gauge implementation
            const gaugeValue = document.getElementById(`gauge-value-${widgetId}`);
            if (gaugeValue) {
                gaugeValue.textContent = '0';
            }
            return { type: 'gauge', update: updateGaugeValue };
        }

        function createTableChart(widgetId) {
            const table = document.getElementById(`table-${widgetId}`);
            if (table) {
                return { type: 'table', element: table, update: updateTableData };
            }
            return null;
        }

        function updateChartData(chart, value, timestamp) {
            if (chart.type === 'gauge') {
                chart.update(value);
            } else if (chart.type === 'table') {
                chart.update(value, timestamp);
            } else {
                // Chart.js charts
                const timeLabel = new Date(timestamp).toLocaleTimeString();
                chart.data.labels.push(timeLabel);
                chart.data.datasets[0].data.push(value);

                // Keep only last 20 data points
                if (chart.data.labels.length > 20) {
                    chart.data.labels.shift();
                    chart.data.datasets[0].data.shift();
                }

                chart.update();
            }
        }"""

    def _generate_ui_js(self) -> str:
        """Generate JavaScript for UI interactions."""
        return """
        function refreshDashboard() {
            console.log('Refreshing dashboard...');
            updateLastUpdated();

            // Refresh all widgets
            Object.keys(charts).forEach(widgetId => {
                refreshWidget(widgetId);
            });

            // Update metrics count
            updateMetricsCount();
        }

        function refreshWidget(widgetId) {
            const widget = document.getElementById(`widget-${widgetId}`);
            if (!widget) return;

            updateWidgetStatus(widgetId, 'Refreshing...', null);

            // Simulate data refresh (replace with actual API call)
            setTimeout(() => {
                const randomValue = Math.random() * 100;
                updateMetric(widgetId, randomValue, Date.now());
            }, 1000);
        }

        function toggleSettings() {
            const panel = document.getElementById('settings-panel');
            panel.classList.toggle('hidden');
        }

        function changeTheme() {
            const themeSelect = document.getElementById('theme-select');
            const newTheme = themeSelect.value;

            // Update theme in dashboard config
            dashboardConfig.theme = newTheme;

            // Apply theme change (this would typically reload the page or update CSS)
            console.log(`Theme changed to: ${newTheme}`);

            // For now, just show a message
            showAlert(`Theme changed to ${newTheme}`, 'info');
        }

        function toggleAutoRefresh() {
            const checkbox = document.getElementById('auto-refresh');
            dashboardConfig.autoRefresh = checkbox.checked;

            if (dashboardConfig.autoRefresh) {
                startAutoRefresh();
            } else {
                stopAutoRefresh();
            }
        }

        function updateRefreshInterval() {
            const input = document.getElementById('refresh-interval');
            const newInterval = parseInt(input.value) * 1000;

            if (newInterval >= 1000 && newInterval <= 300000) {
                dashboardConfig.refreshInterval = newInterval;

                if (dashboardConfig.autoRefresh) {
                    stopAutoRefresh();
                    startAutoRefresh();
                }
            }
        }

        function startAutoRefresh() {
            if (refreshTimer) {
                clearInterval(refreshTimer);
            }

            refreshTimer = setInterval(() => {
                refreshDashboard();
            }, dashboardConfig.refreshInterval);

            console.log(`Auto refresh started with ${dashboardConfig.refreshInterval}ms interval`);
        }

        function stopAutoRefresh() {
            if (refreshTimer) {
                clearInterval(refreshTimer);
                refreshTimer = null;
                console.log('Auto refresh stopped');
            }
        }"""

    def _generate_utility_js(self) -> str:
        """Generate JavaScript utility functions."""
        return """
        function updateConnectionStatus(text, status) {
            const statusText = document.getElementById('status-text');
            const statusDot = document.getElementById('status-dot');

            if (statusText) statusText.textContent = text;
            if (statusDot) {
                statusDot.className = `status-dot ${status}`;
            }
        }

        function updateWidgetStatus(widgetId, status, timestamp) {
            const statusElement = document.getElementById(`status-${widgetId}`);
            const updatedElement = document.getElementById(`updated-${widgetId}`);

            if (statusElement) statusElement.textContent = status;
            if (updatedElement && timestamp) {
                updatedElement.textContent = new Date(timestamp).toLocaleTimeString();
            }
        }

        function updateLastUpdated() {
            const element = document.getElementById('last-updated');
            if (element) {
                element.textContent = new Date().toLocaleString();
            }
        }

        function updateMetricsCount() {
            const element = document.getElementById('metrics-count');
            if (element) {
                element.textContent = Object.keys(charts).length;
            }
        }

        function updateAlertCount(count) {
            const element = document.getElementById('alert-count');
            if (element) {
                element.textContent = count;
            }
        }

        function showAlert(message, level = 'info') {
            console.log(`Alert [${level}]: ${message}`);
            // Implement alert display logic here
        }

        function updateSystemStatus(status) {
            console.log('System status update:', status);
            // Implement system status update logic here
        }

        function updateGaugeValue(value) {
            // Update gauge display
            const gaugeValue = document.querySelector('.gauge-value');
            if (gaugeValue) {
                gaugeValue.textContent = Math.round(value);
            }
        }

        function updateTableData(value, timestamp) {
            // Update table data
            const table = document.querySelector('.data-table tbody');
            if (table) {
                const row = table.insertRow();
                row.insertCell(0).textContent = new Date(timestamp).toLocaleString();
                row.insertCell(1).textContent = value.toFixed(2);
                row.insertCell(2).textContent = 'units';

                // Keep only last 10 rows
                while (table.rows.length > 10) {
                    table.deleteRow(1);
                }
            }
        }

        // Export functions for external use
        window.dashboardAPI = {{
            refreshDashboard,
            refreshWidget,
            toggleSettings,
            changeTheme,
            toggleAutoRefresh,
            updateRefreshInterval
        }};"""

    def generate_widget_config_js(self) -> str:
        """Generate JavaScript for widget configuration."""
        return """
        function configureWidget(widgetId) {
            const modal = document.getElementById(`config-modal-${widgetId}`);
            if (modal) {
                modal.classList.remove('hidden');
            }
        }

        function closeWidgetConfig(widgetId) {
            const modal = document.getElementById(`config-modal-${widgetId}`);
            if (modal) {
                modal.classList.add('hidden');
            }
        }

        function saveWidgetConfig(widgetId) {
            // Get configuration values
            const title = document.getElementById(`config-title-${widgetId}`).value;
            const refresh = document.getElementById(`config-refresh-${widgetId}`).value;
            const width = document.getElementById(`config-width-${widgetId}`).value;
            const height = document.getElementById(`config-height-${widgetId}`).value;

            // Update widget configuration (this would typically send to backend)
            console.log(`Saving config for widget ${widgetId}:`, { title, refresh, width, height });

            // Close modal
            closeWidgetConfig(widgetId);

            // Show success message
            showAlert('Widget configuration saved', 'success');
        }"""

    def export_js_file(self, filepath: str) -> bool:
        """Export JavaScript to a file."""
        try:
            js_content = self.generate_main_js()
            with open(filepath, "w") as f:
                f.write(js_content)
            logger.info(f"JavaScript exported to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Failed to export JavaScript: {e}")
            return False
