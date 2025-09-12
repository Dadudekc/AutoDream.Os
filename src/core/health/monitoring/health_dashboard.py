#!/usr/bin/env python3
"""
🐝 AGENT-2 HEALTH MONITORING DASHBOARD
Web Interface for Real-Time System Health Visualization

This module provides a comprehensive web dashboard for monitoring:
- Real-time service availability and health status
- Performance metrics and resource usage charts
- Error rates and failure tracking
- Alert management and notifications
- Historical trends and analytics
"""

from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from flask import Flask, render_template_string, jsonify, request

from .health_monitoring_service import (
    HealthMonitoringService,
    HealthStatus,
    AlertSeverity,
    SystemHealthSnapshot
)


@dataclass
class DashboardWidget:
    """Represents a dashboard widget configuration."""
    id: str
    title: str
    widget_type: str  # 'chart', 'gauge', 'table', 'alert'
    data_source: str
    refresh_interval: int = 30
    size: Dict[str, int] = field(default_factory=lambda: {"width": 4, "height": 3})
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardLayout:
    """Dashboard layout configuration."""
    widgets: List[DashboardWidget] = field(default_factory=list)
    theme: str = "dark"
    refresh_interval: int = 30


class HealthMonitoringDashboard:
    """
    Web dashboard for health monitoring visualization.

    Provides real-time web interface with:
    - Service health status overview
    - Performance metrics charts
    - Resource usage gauges
    - Alert management interface
    - Historical trend analysis
    """

    def __init__(self, health_service: HealthMonitoringService, host: str = "0.0.0.0", port: int = 8080):
        self.health_service = health_service
        self.host = host
        self.port = port

        # Flask app
        self.app = Flask(__name__)
        self.app.secret_key = "health_monitoring_dashboard_secret"

        # Dashboard configuration
        self.layout = self._create_default_layout()

        # Web server control
        self.server_thread: Optional[threading.Thread] = None
        self.server_running = False

        # Setup routes
        self._setup_routes()

    def _create_default_layout(self) -> DashboardLayout:
        """Create default dashboard layout."""
        widgets = [
            DashboardWidget(
                id="overall_status",
                title="System Health Overview",
                widget_type="gauge",
                data_source="overall_status",
                refresh_interval=10
            ),
            DashboardWidget(
                id="service_status",
                title="Service Availability",
                widget_type="table",
                data_source="services",
                refresh_interval=30,
                size={"width": 6, "height": 4}
            ),
            DashboardWidget(
                id="performance_metrics",
                title="Performance Metrics",
                widget_type="chart",
                data_source="metrics",
                refresh_interval=30,
                size={"width": 8, "height": 4}
            ),
            DashboardWidget(
                id="resource_usage",
                title="Resource Usage",
                widget_type="chart",
                data_source="system_resources",
                refresh_interval=30,
                size={"width": 4, "height": 4}
            ),
            DashboardWidget(
                id="active_alerts",
                title="Active Alerts",
                widget_type="alert",
                data_source="alerts",
                refresh_interval=10,
                size={"width": 12, "height": 3}
            ),
            DashboardWidget(
                id="error_rates",
                title="Error Rate Trends",
                widget_type="chart",
                data_source="error_rates",
                refresh_interval=60,
                size={"width": 6, "height": 4}
            )
        ]

        return DashboardLayout(widgets=widgets)

    def _setup_routes(self) -> None:
        """Setup Flask routes."""

        @self.app.route('/')
        def dashboard():
            return render_template_string(self._get_dashboard_html(), layout=self.layout)

        @self.app.route('/api/health')
        def get_health_data():
            snapshot = self.health_service.get_health_snapshot()
            return jsonify(self._snapshot_to_dict(snapshot))

        @self.app.route('/api/metrics')
        def get_metrics():
            snapshot = self.health_service.get_health_snapshot()
            return jsonify({
                "metrics": [self._metric_to_dict(m) for m in snapshot.metrics.values()],
                "timestamp": datetime.now().isoformat()
            })

        @self.app.route('/api/alerts')
        def get_alerts():
            snapshot = self.health_service.get_health_snapshot()
            return jsonify({
                "alerts": [self._alert_to_dict(a) for a in snapshot.alerts],
                "total": len(snapshot.alerts),
                "critical": len([a for a in snapshot.alerts if hasattr(a, 'level') and str(a.level).upper() == 'CRITICAL']),
                "warning": len([a for a in snapshot.alerts if hasattr(a, 'level') and str(a.level).upper() == 'WARNING'])
            })

        @self.app.route('/api/history/<metric_name>')
        def get_metric_history(metric_name: str):
            # Get historical data for a specific metric
            history = []
            cutoff = datetime.now() - timedelta(hours=1)

            for metric in self.health_service.metrics_buffer:
                if (metric.name == metric_name and
                    metric.timestamp > cutoff):
                    history.append({
                        "timestamp": metric.timestamp.isoformat(),
                        "value": metric.value,
                        "unit": metric.unit
                    })

            return jsonify({
                "metric": metric_name,
                "history": history[-100:]  # Last 100 data points
            })

        @self.app.route('/api/services')
        def get_services():
            snapshot = self.health_service.get_health_snapshot()
            return jsonify({
                "services": {name: status.value for name, status in snapshot.services.items()},
                "timestamp": datetime.now().isoformat()
            })

        @self.app.route('/export')
        def export_data():
            filepath = self.health_service.export_health_data()
            return jsonify({"exported": filepath})

    def _snapshot_to_dict(self, snapshot: SystemHealthSnapshot) -> Dict[str, Any]:
        """Convert health snapshot to dictionary."""
        return {
            "timestamp": snapshot.timestamp.isoformat(),
            "overall_status": snapshot.overall_status.value,
            "services": {name: status.value for name, status in snapshot.services.items()},
            "metrics": {name: self._metric_to_dict(metric) for name, metric in snapshot.metrics.items()},
            "alerts": [self._alert_to_dict(alert) for alert in snapshot.alerts],
            "uptime_seconds": snapshot.uptime_seconds
        }

    def _metric_to_dict(self, metric) -> Dict[str, Any]:
        """Convert metric to dictionary."""
        return {
            "name": metric.name,
            "value": metric.value,
            "unit": metric.unit,
            "timestamp": metric.timestamp.isoformat(),
            "category": metric.category,
            "threshold_warning": metric.threshold_warning,
            "threshold_critical": metric.threshold_critical
        }

    def _alert_to_dict(self, alert) -> Dict[str, Any]:
        """Convert alert to dictionary."""
        return {
            "alert_id": alert.alert_id,
            "component": getattr(alert, 'component', {}).value if hasattr(alert, 'component') else 'unknown',
            "level": getattr(alert, 'level', {}).value if hasattr(alert, 'level') else 'unknown',
            "message": alert.message,
            "timestamp": alert.timestamp.isoformat(),
            "resolved": getattr(alert, 'resolved', False),
            "metadata": getattr(alert, 'metadata', {})
        }

    def _get_dashboard_html(self) -> str:
        """Get the main dashboard HTML template."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐝 System Health Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #1a1a1a; color: #ffffff; }
        .card { background-color: #2d2d2d; border: 1px solid #404040; margin-bottom: 20px; }
        .card-header { background-color: #404040; border-bottom: 1px solid #555; }
        .status-healthy { color: #28a745; }
        .status-warning { color: #ffc107; }
        .status-critical { color: #dc3545; }
        .status-unknown { color: #6c757d; }
        .alert-healthy { background-color: #d4edda; border-color: #c3e6cb; color: #155724; }
        .alert-warning { background-color: #fff3cd; border-color: #ffeaa7; color: #856404; }
        .alert-critical { background-color: #f8d7da; border-color: #f5c6cb; color: #721c24; }
        .metric-chart { height: 300px; }
        .gauge-container { display: flex; justify-content: center; align-items: center; height: 200px; }
    </style>
</head>
<body>
    <div class="container-fluid mt-4">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center mb-4">🐝 System Health Monitoring Dashboard</h1>
                <div id="overall-status" class="text-center mb-4">
                    <h3>System Status: <span id="system-status" class="status-unknown">Loading...</span></h3>
                    <div class="gauge-container">
                        <canvas id="overall-gauge" width="200" height="200"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Service Availability</h5>
                    </div>
                    <div class="card-body">
                        <div id="services-table">
                            <p class="text-center">Loading services...</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Resource Usage</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="resources-chart" class="metric-chart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Performance Metrics</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="performance-chart" class="metric-chart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Active Alerts</h5>
                    </div>
                    <div class="card-body">
                        <div id="alerts-container">
                            <p class="text-center">No active alerts</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5 class="mb-0">Error Rate Trends</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="error-chart" class="metric-chart"></canvas>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let charts = {};
        let lastUpdate = null;

        function updateDashboard() {
            fetch('/api/health')
                .then(response => response.json())
                .then(data => {
                    updateOverallStatus(data);
                    updateServicesTable(data.services);
                    updateResourceChart(data.metrics);
                    updatePerformanceChart(data.metrics);
                    updateAlerts(data.alerts);
                    updateErrorChart();

                    lastUpdate = new Date();
                    document.getElementById('last-update').textContent = lastUpdate.toLocaleTimeString();
                })
                .catch(error => console.error('Error updating dashboard:', error));
        }

        function updateOverallStatus(data) {
            const statusElement = document.getElementById('system-status');
            const status = data.overall_status.toLowerCase();

            statusElement.className = `status-${status}`;
            statusElement.textContent = data.overall_status;

            // Update gauge
            updateOverallGauge(data);
        }

        function updateOverallGauge(data) {
            const ctx = document.getElementById('overall-gauge').getContext('2d');

            if (charts.overallGauge) {
                charts.overallGauge.destroy();
            }

            const statusValue = getStatusValue(data.overall_status);
            const statusColor = getStatusColor(data.overall_status);

            charts.overallGauge = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    datasets: [{
                        data: [statusValue, 100 - statusValue],
                        backgroundColor: [statusColor, '#404040'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: false,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: { display: false },
                        tooltip: { enabled: false }
                    }
                }
            });
        }

        function updateServicesTable(services) {
            const container = document.getElementById('services-table');
            let html = '<table class="table table-dark table-sm"><thead><tr><th>Service</th><th>Status</th></tr></thead><tbody>';

            for (const [name, status] of Object.entries(services)) {
                const statusClass = `status-${status.toLowerCase()}`;
                html += `<tr><td>${name}</td><td><span class="${statusClass}">●</span> ${status}</td></tr>`;
            }

            html += '</tbody></table>';
            container.innerHTML = html;
        }

        function updateResourceChart(metrics) {
            const ctx = document.getElementById('resources-chart').getContext('2d');

            if (charts.resources) {
                charts.resources.destroy();
            }

            const cpuMetric = Object.values(metrics).find(m => m.name === 'cpu_usage');
            const memoryMetric = Object.values(metrics).find(m => m.name === 'memory_usage');
            const diskMetric = Object.values(metrics).find(m => m.name === 'disk_usage');

            charts.resources = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['CPU', 'Memory', 'Disk'],
                    datasets: [{
                        label: 'Usage (%)',
                        data: [
                            cpuMetric ? cpuMetric.value : 0,
                            memoryMetric ? memoryMetric.value : 0,
                            diskMetric ? diskMetric.value : 0
                        ],
                        backgroundColor: ['#007bff', '#28a745', '#ffc107']
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });
        }

        function updatePerformanceChart(metrics) {
            const ctx = document.getElementById('performance-chart').getContext('2d');

            if (charts.performance) {
                charts.performance.destroy();
            }

            const performanceMetrics = Object.values(metrics).filter(m =>
                m.category === 'system_performance'
            );

            charts.performance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: performanceMetrics.map(m => new Date(m.timestamp).toLocaleTimeString()),
                    datasets: [{
                        label: 'Performance Metrics',
                        data: performanceMetrics.map(m => m.value),
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0, 123, 255, 0.1)',
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        function updateAlerts(alerts) {
            const container = document.getElementById('alerts-container');

            if (alerts.length === 0) {
                container.innerHTML = '<p class="text-center text-muted">No active alerts</p>';
                return;
            }

            let html = '<div class="list-group">';
            alerts.forEach(alert => {
                const alertClass = `alert-${alert.level.toLowerCase()}`;
                const icon = getAlertIcon(alert.level);
                html += `
                    <div class="list-group-item ${alertClass}">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1">${icon} ${alert.component}</h6>
                            <small>${new Date(alert.timestamp).toLocaleString()}</small>
                        </div>
                        <p class="mb-1">${alert.message}</p>
                    </div>
                `;
            });
            html += '</div>';

            container.innerHTML = html;
        }

        function updateErrorChart() {
            const ctx = document.getElementById('error-chart').getContext('2d');

            if (charts.error) {
                charts.error.destroy();
            }

            // Mock error rate data - in real implementation, fetch from API
            charts.error = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({length: 24}, (_, i) => `${i}:00`),
                    datasets: [{
                        label: 'Error Rate (%)',
                        data: Array.from({length: 24}, () => Math.random() * 5),
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 10 }
                    }
                }
            });
        }

        function getStatusValue(status) {
            switch (status.toLowerCase()) {
                case 'healthy': return 100;
                case 'warning': return 75;
                case 'critical': return 25;
                default: return 50;
            }
        }

        function getStatusColor(status) {
            switch (status.toLowerCase()) {
                case 'healthy': return '#28a745';
                case 'warning': return '#ffc107';
                case 'critical': return '#dc3545';
                default: return '#6c757d';
            }
        }

        function getAlertIcon(level) {
            switch (level.toLowerCase()) {
                case 'critical': return '🚨';
                case 'warning': return '⚠️';
                case 'info': return 'ℹ️';
                default: return '❓';
            }
        }

        // Initial load and auto-refresh
        updateDashboard();
        setInterval(updateDashboard, 30000); // Update every 30 seconds
    </script>
</body>
</html>
        """

    def start_dashboard(self) -> None:
        """Start the web dashboard server."""
        if self.server_running:
            return

        self.server_running = True
        self.server_thread = threading.Thread(
            target=self._run_server,
            daemon=True,
            name="HealthDashboardServer"
        )
        self.server_thread.start()

        print(f"✅ Health monitoring dashboard started at http://{self.host}:{self.port}")

    def stop_dashboard(self) -> None:
        """Stop the web dashboard server."""
        self.server_running = False
        if hasattr(self.app, 'shutdown'):
            self.app.shutdown()

        if self.server_thread and self.server_thread.is_alive():
            self.server_thread.join(timeout=5)

        print("🛑 Health monitoring dashboard stopped")

    def _run_server(self) -> None:
        """Run the Flask server."""
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            print(f"❌ Dashboard server error: {e}")
            self.server_running = False
