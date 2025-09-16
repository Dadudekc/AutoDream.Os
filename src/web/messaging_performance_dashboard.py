#!/usr/bin/env python3
# Messaging Performance Dashboard - V2 Compliant
import logging
logger = logging.getLogger(__name__)

import asyncio
import json
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.messaging_performance_monitor import get_messaging_performance_monitor


class MessagingPerformanceDashboard:
    def __init__(self):
        self.app = FastAPI(title="Messaging Performance Dashboard", version="1.0.0")
        self.performance_monitor = get_messaging_performance_monitor()
        self.templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

        # Mount static files
        static_path = Path(__file__).parent / "static"
        static_path.mkdir(exist_ok=True)
        self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

        # Start performance monitoring
        self.performance_monitor.start_monitoring()

        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup FastAPI routes for messaging performance dashboard."""
        @self.app.get("/")
        async def dashboard():
            return {"message": "Messaging Performance Dashboard", "status": "operational"}

        @self.app.get("/metrics")
        async def get_metrics():
            return {"metrics": "performance data"}

# Initialize and use
    def _setup_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def messaging_performance_dashboard(request: Request):
            return self.templates.TemplateResponse(
                "messaging_performance.html",
                {"request": request, "title": "Messaging Performance Dashboard"}
            )

        @self.app.get("/api/messaging/metrics/current")
        async def get_current_metrics():
            try:
                metrics = self.performance_monitor.get_current_metrics()
                return JSONResponse(content={
                    "timestamp": metrics.timestamp.isoformat(),
                    "health_score": metrics.health_score,
                    "cpu_usage_percent": metrics.cpu_usage_percent,
                    "memory_usage_mb": metrics.memory_usage_mb,
                    "queue_depth": metrics.queue_depth,
                    "messages_per_second": metrics.messages_per_second,
                    "error_rate_percent": metrics.error_rate_percent,
                    "delivery_success_rate": metrics.delivery_success_rate,
                    "bottleneck_detected": metrics.bottleneck_detected,
                    "bottleneck_description": metrics.bottleneck_description,
                    "optimization_recommendations": metrics.optimization_recommendations
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/messaging/metrics/history")
        async def get_metrics_history(hours_back: int = 1):
            try:
                history = self.performance_monitor.get_metrics_history(hours_back)
                data = []
                for metrics in history:
                    data.append({
                        "timestamp": metrics.timestamp.isoformat(),
                        "health_score": metrics.health_score,
                        "cpu_usage_percent": metrics.cpu_usage_percent,
                        "memory_usage_mb": metrics.memory_usage_mb,
                        "queue_depth": metrics.queue_depth,
                        "messages_per_second": metrics.messages_per_second,
                        "error_rate_percent": metrics.error_rate_percent,
                        "delivery_success_rate": metrics.delivery_success_rate,
                        "bottleneck_detected": metrics.bottleneck_detected
                    })
                return JSONResponse(content={"history": data, "count": len(data)})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/messaging/performance/summary")
        async def get_performance_summary(hours_back: int = 24):
            """Get comprehensive performance summary."""
            try:
                summary = self.performance_monitor.get_performance_summary(hours_back)
                return JSONResponse(content=summary)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/messaging/bottlenecks/analysis")
        async def get_bottleneck_analysis():
            """Get bottleneck analysis and recommendations."""
            try:
                current_metrics = self.performance_monitor.get_current_metrics()
                patterns = self.performance_monitor._analyze_bottleneck_patterns()
                recommendations = self.performance_monitor._generate_optimization_recommendations(
                    self.performance_monitor.get_performance_summary(1)
                )

                return JSONResponse(content={
                    "current_bottlenecks": {
                        "detected": current_metrics.bottleneck_detected,
                        "description": current_metrics.bottleneck_description,
                        "recommendations": current_metrics.optimization_recommendations
                    },
                    "bottleneck_patterns": patterns,
                    "optimization_recommendations": recommendations
                })
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/messaging/optimization/report")
        async def get_optimization_report():
            """Generate comprehensive optimization report."""
            try:
                report = self.performance_monitor.generate_optimization_report()
                return JSONResponse(content=report)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/messaging/thresholds/update")
        async def update_thresholds(request: Request):
            """Update performance monitoring thresholds."""
            try:
                data = await request.json()
                self.performance_monitor.update_thresholds(data)
                return JSONResponse(content={"status": "thresholds_updated"})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.post("/api/messaging/metrics/record")
        async def record_custom_metrics(request: Request):
            """Record custom messaging metrics."""
            try:
                data = await request.json()
                metric_type = data.get("type")
                value = data.get("value", 0)
                success = data.get("success", True)

                if metric_type == "delivery":
                    self.performance_monitor.record_message_delivery(value, success)
                elif metric_type == "processing":
                    self.performance_monitor.record_message_processing(value)

                return JSONResponse(content={"status": "metric_recorded"})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

    def create_default_templates(self) -> None:
        """Create default HTML templates if they don't exist."""
        templates_dir = Path(__file__).parent / "templates"
        templates_dir.mkdir(exist_ok=True)

        # Create messaging performance dashboard template
        messaging_performance_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Messaging Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; color: #2563eb; }
        .metric-label { color: #6b7280; margin-top: 5px; }
        .health-good { color: #16a34a; }
        .health-warning { color: #ca8a04; }
        .health-critical { color: #dc2626; }
        .chart-container { height: 300px; margin: 20px 0; }
        .alert { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .recommendation { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .bottleneck-indicator { background: #fef3c7; border: 1px solid #fde047; color: #92400e; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin: 15px 0; }
        .status-item { text-align: center; padding: 10px; background: #f8fafc; border-radius: 4px; }
        .status-value { font-size: 1.2em; font-weight: bold; }
        .refresh-btn { background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; margin: 10px 5px; }
        .refresh-btn:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <h1>📡 Messaging Performance Dashboard</h1>

    <div style="margin-bottom: 20px;">
        <button class="refresh-btn" onclick="loadDashboard()">🔄 Refresh</button>
        <button class="refresh-btn" onclick="loadOptimizationReport()">📊 Optimization Report</button>
        <span id="last-updated">Last updated: -</span>
    </div>

    <div id="loading">Loading messaging performance data...</div>

    <div id="dashboard" style="display: none;">
        <!-- Health Overview -->
        <div class="dashboard">
            <div class="card">
                <h3>System Health</h3>
                <div class="metric">
                    <div class="metric-value" id="health-score">-</div>
                    <div class="metric-label">Health Score</div>
                </div>
                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-value" id="cpu-status">-</div>
                        <div>CPU (%)</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="memory-status">-</div>
                        <div>Memory (MB)</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="queue-status">-</div>
                        <div>Queue Depth</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="error-status">-</div>
                        <div>Error Rate (%)</div>
                    </div>
                </div>
            </div>

            <div class="card">
                <h3>Performance Metrics</h3>
                <div class="metric">
                    <div class="metric-value" id="throughput">-</div>
                    <div class="metric-label">Messages/sec</div>
                </div>
                <div class="status-grid">
                    <div class="status-item">
                        <div class="status-value" id="success-rate">-</div>
                        <div>Success Rate (%)</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="avg-delivery">-</div>
                        <div>Avg Delivery (s)</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="processed">-</div>
                        <div>Processed</div>
                    </div>
                    <div class="status-item">
                        <div class="status-value" id="errors">-</div>
                        <div>Errors</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Bottlenecks and Alerts -->
        <div id="bottlenecks-section" style="display: none;">
            <div class="card">
                <h3>🚨 Active Bottlenecks</h3>
                <div id="bottlenecks-container"></div>
            </div>
        </div>

        <div id="alerts-section" style="display: none;">
            <div class="card">
                <h3>⚠️ Performance Alerts</h3>
                <div id="alerts-container"></div>
            </div>
        </div>

        <!-- Charts -->
        <div class="dashboard">
            <div class="card">
                <h3>CPU Usage Trend</h3>
                <div class="chart-container">
                    <canvas id="cpuChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>Queue Depth Trend</h3>
                <div class="chart-container">
                    <canvas id="queueChart"></canvas>
                </div>
            </div>
        </div>

        <div class="dashboard">
            <div class="card">
                <h3>Throughput Trend</h3>
                <div class="chart-container">
                    <canvas id="throughputChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>Error Rate Trend</h3>
                <div class="chart-container">
                    <canvas id="errorChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Optimization Recommendations -->
        <div class="card">
            <h3>🎯 Optimization Recommendations</h3>
            <div id="recommendations-container">
                <p>Loading recommendations...</p>
            </div>
        </div>
    </div>

    <script>
        let cpuChart, queueChart, throughputChart, errorChart;
        let metricsHistory = [];
        const maxHistoryPoints = 50;

        async function loadDashboard() {
            try {
                // Load current metrics
                const metricsResponse = await fetch('/api/messaging/metrics/current');
                const currentMetrics = await metricsResponse.json();

                // Load recent history
                const historyResponse = await fetch('/api/messaging/metrics/history?hours_back=1');
                const historyData = await historyResponse.json();

                updateDashboard(currentMetrics, historyData.history);
                updateLastUpdated();

            } catch (error) {
                document.getElementById('loading').textContent = 'Error loading dashboard: ' + error.message;
            }
        }

        function updateDashboard(currentMetrics, history) {
            // Store history for charts
            metricsHistory = history.slice(-maxHistoryPoints);

            // Update health indicators
            updateHealthIndicators(currentMetrics);

            // Update metrics display
            updateMetricsDisplay(currentMetrics);

            // Show/hide bottlenecks and alerts
            updateBottlenecksAndAlerts(currentMetrics);

            // Update charts
            updateCharts();

            // Load recommendations
            loadRecommendations();

            // Show dashboard
            document.getElementById('loading').style.display = 'none';
            document.getElementById('dashboard').style.display = 'block';
        }

        function updateHealthIndicators(metrics) {
            const healthScore = metrics.health_score;
            const healthElement = document.getElementById('health-score');

            healthElement.textContent = healthScore.toFixed(1);

            // Color coding
            healthElement.className = 'metric-value';
            if (healthScore >= 80) {
                healthElement.classList.add('health-good');
            } else if (healthScore >= 60) {
                healthElement.classList.add('health-warning');
            } else {
                healthElement.classList.add('health-critical');
            }
        }

        function updateMetricsDisplay(metrics) {
            document.getElementById('cpu-status').textContent = metrics.cpu_usage_percent.toFixed(1);
            document.getElementById('memory-status').textContent = metrics.memory_usage_mb.toFixed(1);
            document.getElementById('queue-status').textContent = metrics.queue_depth;
            document.getElementById('error-status').textContent = metrics.error_rate_percent.toFixed(1);
            document.getElementById('throughput').textContent = metrics.messages_per_second.toFixed(1);
            document.getElementById('success-rate').textContent = metrics.delivery_success_rate.toFixed(1);
            document.getElementById('avg-delivery').textContent = 'N/A'; // Would need timing data
            document.getElementById('processed').textContent = metrics.messages_processed || 0;
            document.getElementById('errors').textContent = metrics.delivery_errors || 0;
        }

        function updateBottlenecksAndAlerts(metrics) {
            const bottlenecksSection = document.getElementById('bottlenecks-section');
            const alertsSection = document.getElementById('alerts-section');

            if (metrics.bottleneck_detected) {
                bottlenecksSection.style.display = 'block';
                const container = document.getElementById('bottlenecks-container');
                container.innerHTML = `
                    <div class="bottleneck-indicator">
                        <strong>${metrics.bottleneck_description}</strong>
                        <ul>
                            ${metrics.optimization_recommendations.map(rec => `<li>${rec}</li>`).join('')}
                        </ul>
                    </div>
                `;
            } else {
                bottlenecksSection.style.display = 'none';
            }

            // Check for critical thresholds
            const alerts = [];
            if (metrics.cpu_usage_percent > 80) alerts.push('High CPU usage detected');
            if (metrics.memory_usage_mb > 500) alerts.push('High memory usage detected');
            if (metrics.queue_depth > 1000) alerts.push('Queue depth critically high');
            if (metrics.error_rate_percent > 5) alerts.push('Error rate above threshold');

            if (alerts.length > 0) {
                alertsSection.style.display = 'block';
                const container = document.getElementById('alerts-container');
                container.innerHTML = alerts.map(alert =>
                    `<div class="alert">${alert}</div>`
                ).join('');
            } else {
                alertsSection.style.display = 'none';
            }
        }

        function updateCharts() {
            if (metricsHistory.length === 0) return;

            const labels = metricsHistory.map(m => new Date(m.timestamp).toLocaleTimeString());
            const cpuData = metricsHistory.map(m => m.cpu_usage_percent);
            const queueData = metricsHistory.map(m => m.queue_depth);
            const throughputData = metricsHistory.map(m => m.messages_per_second);
            const errorData = metricsHistory.map(m => m.error_rate_percent);

            // CPU Chart
            if (cpuChart) cpuChart.destroy();
            const cpuCtx = document.getElementById('cpuChart').getContext('2d');
            cpuChart = new Chart(cpuCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'CPU Usage (%)',
                        data: cpuData,
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            // Queue Chart
            if (queueChart) queueChart.destroy();
            const queueCtx = document.getElementById('queueChart').getContext('2d');
            queueChart = new Chart(queueCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Queue Depth',
                        data: queueData,
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            // Throughput Chart
            if (throughputChart) throughputChart.destroy();
            const throughputCtx = document.getElementById('throughputChart').getContext('2d');
            throughputChart = new Chart(throughputCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Messages/sec',
                        data: throughputData,
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            // Error Chart
            if (errorChart) errorChart.destroy();
            const errorCtx = document.getElementById('errorChart').getContext('2d');
            errorChart = new Chart(errorCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Error Rate (%)',
                        data: errorData,
                        borderColor: 'rgb(255, 205, 86)',
                        tension: 0.1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        }

        async function loadRecommendations() {
            try {
                const response = await fetch('/api/messaging/bottlenecks/analysis');
                const data = await response.json();

                const container = document.getElementById('recommendations-container');
                if (data.optimization_recommendations && data.optimization_recommendations.length > 0) {
                    container.innerHTML = data.optimization_recommendations.map(rec =>
                        `<div class="recommendation">${rec}</div>`
                    ).join('');
                } else {
                    container.innerHTML = '<p>No optimization recommendations at this time.</p>';
                }
            } catch (error) {
                document.getElementById('recommendations-container').innerHTML =
                    '<p>Error loading recommendations.</p>';
            }
        }

        async function loadOptimizationReport() {
            try {
                const response = await fetch('/api/messaging/optimization/report');
                const report = await response.json();

                console.log('Optimization Report:', report);
                alert('Optimization report generated! Check browser console for details.');
            } catch (error) {
                alert('Error generating optimization report: ' + error.message);
            }
        }

        function updateLastUpdated() {
            document.getElementById('last-updated').textContent =
                'Last updated: ' + new Date().toLocaleTimeString();
        }

        // Auto-refresh every 30 seconds
        setInterval(loadDashboard, 30000);

        // Load dashboard on page load
        loadDashboard();
    </script>
</body>
</html>
        """

        with open(templates_dir / "messaging_performance.html", "w") as f:
            f.write(messaging_performance_html)

    def start(self, host: str = "localhost", port: int = 8002) -> None:
        """Start the messaging performance dashboard web server."""
        logger.info(f"🚀 Starting Messaging Performance Dashboard on http://{host}:{port}")
        logger.info("📊 Dashboard Features:")
        logger.info("   - Real-time messaging performance metrics")
        logger.info("   - CPU, memory, and queue depth monitoring")
        logger.info("   - Bottleneck detection and alerts")
        logger.info("   - Throughput and error rate trending")
        logger.info("   - Optimization recommendations")
        logger.info("   - Interactive performance charts")

        uvicorn.run(self.app, host=host, port=port)

    def stop(self) -> None:
        """Stop the dashboard and performance monitoring."""
        if hasattr(self, 'performance_monitor'):
            self.performance_monitor.stop_monitoring()


def main():
    """Main entry point for messaging performance dashboard."""
    dashboard = MessagingPerformanceDashboard()
    dashboard.create_default_templates()

    try:
        # Start dashboard
        dashboard.start()
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down messaging performance dashboard...")
    finally:
        dashboard.stop()


if __name__ == "__main__":
    main()

