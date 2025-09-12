#!/usr/bin/env python3
"""
Analytics Dashboard Web Interface
==================================

Interactive web dashboard for advanced analytics and reporting system.
Provides real-time visualizations, performance monitoring, and business intelligence insights.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

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

from services.advanced_analytics_service import get_analytics_service


class AnalyticsDashboardWeb:
    """Web interface for analytics dashboard."""

    def __init__(self):
        self.app = FastAPI(title="Advanced Analytics Dashboard", version="1.0.0")
        self.analytics_service = get_analytics_service()
        self.templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

        # Mount static files
        static_path = Path(__file__).parent / "static"
        static_path.mkdir(exist_ok=True)
        self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_overview(request: Request):
            """Main dashboard overview page."""
            return self.templates.TemplateResponse(
                "dashboard.html",
                {"request": request, "title": "Analytics Dashboard"}
            )

        @self.app.get("/api/dashboard/{dashboard_type}")
        async def get_dashboard_data(dashboard_type: str):
            """Get dashboard data by type."""
            try:
                data = self.analytics_service.get_dashboard_data(dashboard_type)
                return JSONResponse(content=data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/analytics/usage")
        async def get_usage_analytics(agent_id: Optional[str] = None, hours_back: int = 24):
            """Get usage analytics data."""
            try:
                data = self.analytics_service.get_usage_analytics(agent_id, hours_back)
                return JSONResponse(content=data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/reports/{report_type}")
        async def generate_report(report_type: str):
            """Generate automated report."""
            try:
                report = self.analytics_service.generate_report(report_type)
                return JSONResponse(content=report)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/metrics/{metric_name}")
        async def get_metric_data(metric_name: str, hours_back: int = 1):
            """Get specific metric data."""
            try:
                data = self.analytics_service.get_metrics_stats(metric_name, hours_back)
                return JSONResponse(content=data)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/health")
        async def get_service_health():
            """Get service health status."""
            try:
                status = self.analytics_service.get_service_status()
                return JSONResponse(content=status)
            except Exception as e:
                raise HTTPException(status_code=500, detail={"error": str(e)})

        @self.app.post("/api/metrics/custom")
        async def collect_custom_metric(request: Request):
            """Collect a custom metric."""
            try:
                data = await request.json()
                metric_name = data.get("name")
                value = data.get("value")
                tags = data.get("tags", {})

                if not metric_name or value is None:
                    raise HTTPException(status_code=400, detail="Missing name or value")

                self.analytics_service.collect_custom_metric(metric_name, value, tags)
                return JSONResponse(content={"status": "collected"})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/performance", response_class=HTMLResponse)
        async def performance_dashboard(request: Request):
            """Performance dashboard page."""
            return self.templates.TemplateResponse(
                "performance.html",
                {"request": request, "title": "Performance Dashboard"}
            )

        @self.app.get("/usage", response_class=HTMLResponse)
        async def usage_dashboard(request: Request):
            """Usage analytics dashboard page."""
            return self.templates.TemplateResponse(
                "usage.html",
                {"request": request, "title": "Usage Analytics"}
            )

        @self.app.get("/reports", response_class=HTMLResponse)
        async def reports_page(request: Request):
            """Reports page."""
            return self.templates.TemplateResponse(
                "reports.html",
                {"request": request, "title": "Business Intelligence Reports"}
            )

    def start(self, host: str = "localhost", port: int = 8001) -> None:
        """Start the dashboard web server."""
        print(f"🚀 Starting Analytics Dashboard on http://{host}:{port}")
        print("📊 Dashboard Types Available:")
        print("   - Overview: http://localhost:8001/")
        print("   - Performance: http://localhost:8001/performance")
        print("   - Usage: http://localhost:8001/usage")
        print("   - Reports: http://localhost:8001/reports")

        uvicorn.run(self.app, host=host, port=port)

    def create_default_templates(self) -> None:
        """Create default HTML templates if they don't exist."""
        templates_dir = Path(__file__).parent / "templates"
        templates_dir.mkdir(exist_ok=True)

        # Create dashboard template
        dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { text-align: center; }
        .metric-value { font-size: 2em; font-weight: bold; color: #2563eb; }
        .metric-label { color: #6b7280; margin-top: 5px; }
        .chart-container { height: 300px; margin: 20px 0; }
        .alert { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 10px; border-radius: 4px; margin: 10px 0; }
        .insight { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <h1>🐝 Advanced Analytics Dashboard</h1>

    <div id="loading">Loading dashboard data...</div>
    <div id="dashboard" style="display: none;">
        <div class="dashboard">
            <div class="card">
                <h3>System Health</h3>
                <div class="metric">
                    <div class="metric-value" id="health-score">-</div>
                    <div class="metric-label">Health Score</div>
                </div>
            </div>

            <div class="card">
                <h3>System Efficiency</h3>
                <div class="metric">
                    <div class="metric-value" id="efficiency">-</div>
                    <div class="metric-label">Tasks per Activity</div>
                </div>
            </div>

            <div class="card">
                <h3>Error Rate</h3>
                <div class="metric">
                    <div class="metric-value" id="error-rate">-</div>
                    <div class="metric-label">Error Rate (%)</div>
                </div>
            </div>

            <div class="card">
                <h3>Active Agents</h3>
                <div class="metric">
                    <div class="metric-value" id="active-agents">8</div>
                    <div class="metric-label">Total Agents</div>
                </div>
            </div>
        </div>

        <div class="dashboard">
            <div class="card">
                <h3>Agent Activity (Last Hour)</h3>
                <div class="chart-container">
                    <canvas id="activityChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>System Efficiency Trend</h3>
                <div class="chart-container">
                    <canvas id="efficiencyChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card">
            <h3>System Alerts</h3>
            <div id="alerts-container"></div>
        </div>

        <div class="card">
            <h3>AI Insights</h3>
            <div id="insights-container"></div>
        </div>
    </div>

    <script>
        let activityChart, efficiencyChart;

        async function loadDashboard() {
            try {
                const response = await fetch('/api/dashboard/overview');
                const data = await response.json();

                if (data.error) {
                    document.getElementById('loading').textContent = 'Error loading dashboard: ' + data.error;
                    return;
                }

                // Update metrics
                document.getElementById('health-score').textContent = data.kpis.agent_health_score.toFixed(1);
                document.getElementById('efficiency').textContent = data.kpis.system_efficiency.toFixed(2);
                document.getElementById('error-rate').textContent = (data.kpis.error_rate * 100).toFixed(1);
                document.getElementById('active-agents').textContent = data.kpis.active_agents;

                // Create charts
                createActivityChart(data.charts.agent_activity);
                createEfficiencyChart(data.charts.system_efficiency_trend);

                // Display alerts
                displayAlerts(data.alerts);

                // Display insights
                displayInsights(data.insights);

                // Show dashboard
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';

            } catch (error) {
                document.getElementById('loading').textContent = 'Error loading dashboard: ' + error.message;
            }
        }

        function createActivityChart(chartData) {
            const ctx = document.getElementById('activityChart').getContext('2d');
            activityChart = new Chart(ctx, {
                type: 'bar',
                data: chartData.data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { beginAtZero: true }
                    }
                }
            });
        }

        function createEfficiencyChart(chartData) {
            const ctx = document.getElementById('efficiencyChart').getContext('2d');
            efficiencyChart = new Chart(ctx, {
                type: 'line',
                data: chartData.data,
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function displayAlerts(alerts) {
            const container = document.getElementById('alerts-container');
            container.innerHTML = '';

            if (!alerts || alerts.length === 0) {
                container.innerHTML = '<p>No active alerts</p>';
                return;
            }

            alerts.forEach(alert => {
                const alertDiv = document.createElement('div');
                alertDiv.className = 'alert';
                alertDiv.innerHTML = `<strong>${alert.level.toUpperCase()}:</strong> ${alert.message}`;
                container.appendChild(alertDiv);
            });
        }

        function displayInsights(insights) {
            const container = document.getElementById('insights-container');
            container.innerHTML = '';

            if (!insights || insights.length === 0) {
                container.innerHTML = '<p>No insights available</p>';
                return;
            }

            insights.forEach(insight => {
                const insightDiv = document.createElement('div');
                insightDiv.className = 'insight';
                insightDiv.innerHTML = `<strong>💡</strong> ${insight}`;
                container.appendChild(insightDiv);
            });
        }

        // Auto-refresh every 30 seconds
        setInterval(loadDashboard, 30000);

        // Load dashboard on page load
        loadDashboard();
    </script>
</body>
</html>
        """

        with open(templates_dir / "dashboard.html", "w") as f:
            f.write(dashboard_html)

        # Create performance dashboard template
        performance_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; margin: 20px 0; }
        .metric { text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px; }
        .metric-value { font-size: 1.5em; font-weight: bold; color: #2563eb; }
        .metric-label { color: #6b7280; font-size: 0.9em; margin-top: 5px; }
        .chart-container { height: 300px; margin: 20px 0; }
        .recommendations { background: #fefce8; border: 1px solid #fde047; padding: 15px; border-radius: 6px; margin: 15px 0; }
    </style>
</head>
<body>
    <h1>⚡ Performance Dashboard</h1>

    <div id="loading">Loading performance data...</div>
    <div id="dashboard" style="display: none;">
        <div class="metric-grid">
            <div class="metric">
                <div class="metric-value" id="cpu-usage">-</div>
                <div class="metric-label">CPU Usage (%)</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="memory-usage">-</div>
                <div class="metric-label">Memory Usage (%)</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="response-time">-</div>
                <div class="metric-label">Avg Response (ms)</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="throughput">-</div>
                <div class="metric-label">Requests/sec</div>
            </div>
        </div>

        <div class="dashboard">
            <div class="card">
                <h3>CPU Usage Trend</h3>
                <div class="chart-container">
                    <canvas id="cpuChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>Memory Usage Trend</h3>
                <div class="chart-container">
                    <canvas id="memoryChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card">
            <h3>Performance Recommendations</h3>
            <div id="recommendations-container" class="recommendations">
                <p>Loading recommendations...</p>
            </div>
        </div>
    </div>

    <script>
        let cpuChart, memoryChart;

        async function loadPerformanceDashboard() {
            try {
                const response = await fetch('/api/dashboard/performance');
                const data = await response.json();

                if (data.error) {
                    document.getElementById('loading').textContent = 'Error loading performance data: ' + data.error;
                    return;
                }

                // Update metrics
                document.getElementById('cpu-usage').textContent = '65.2';
                document.getElementById('memory-usage').textContent = '72.1';
                document.getElementById('response-time').textContent = '145';
                document.getElementById('throughput').textContent = '23.4';

                // Create charts (placeholder data)
                createCpuChart();
                createMemoryChart();

                // Display recommendations
                displayRecommendations();

                // Show dashboard
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';

            } catch (error) {
                document.getElementById('loading').textContent = 'Error loading performance data: ' + error.message;
            }
        }

        function createCpuChart() {
            const ctx = document.getElementById('cpuChart').getContext('2d');
            cpuChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['5m ago', '4m ago', '3m ago', '2m ago', '1m ago', 'now'],
                    datasets: [{
                        label: 'CPU Usage (%)',
                        data: [45, 52, 48, 61, 55, 65],
                        borderColor: 'rgb(255, 99, 132)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function createMemoryChart() {
            const ctx = document.getElementById('memoryChart').getContext('2d');
            memoryChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['5m ago', '4m ago', '3m ago', '2m ago', '1m ago', 'now'],
                    datasets: [{
                        label: 'Memory Usage (%)',
                        data: [62, 65, 58, 72, 68, 72],
                        borderColor: 'rgb(54, 162, 235)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function displayRecommendations() {
            const container = document.getElementById('recommendations-container');
            container.innerHTML = `
                <ul>
                    <li><strong>CPU Optimization:</strong> Consider load balancing for Agent-4 processing spikes</li>
                    <li><strong>Memory Management:</strong> Implement periodic cleanup of cached agent states</li>
                    <li><strong>Response Time:</strong> Optimize database queries for agent status lookups</li>
                    <li><strong>Throughput:</strong> Scale message routing workers for peak loads</li>
                </ul>
            `;
        }

        // Auto-refresh every 30 seconds
        setInterval(loadPerformanceDashboard, 30000);

        // Load dashboard on page load
        loadPerformanceDashboard();
    </script>
</body>
</html>
        """

        with open(templates_dir / "performance.html", "w") as f:
            f.write(performance_html)

        # Create usage analytics template
        usage_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Usage Analytics</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(500px, 1fr)); gap: 20px; }
        .card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .metric { text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px; }
        .metric-value { font-size: 1.8em; font-weight: bold; color: #2563eb; }
        .metric-label { color: #6b7280; font-size: 0.9em; margin-top: 5px; }
        .chart-container { height: 300px; margin: 20px 0; }
        .ranking { background: #f0fdf4; border: 1px solid #bbf7d0; padding: 15px; border-radius: 6px; margin: 10px 0; }
        .ranking h4 { margin: 0 0 10px 0; color: #166534; }
        .ranking-item { display: flex; justify-content: space-between; margin: 5px 0; }
    </style>
</head>
<body>
    <h1>📊 Usage Analytics Dashboard</h1>

    <div id="loading">Loading usage analytics...</div>
    <div id="dashboard" style="display: none;">
        <div class="metric-grid">
            <div class="metric">
                <div class="metric-value" id="total-activity">-</div>
                <div class="metric-label">Total Activities (24h)</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="total-tasks">-</div>
                <div class="metric-label">Tasks Completed (24h)</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="system-efficiency">-</div>
                <div class="metric-label">System Efficiency</div>
            </div>
            <div class="metric">
                <div class="metric-value" id="error-rate">-</div>
                <div class="metric-label">Error Rate (%)</div>
            </div>
        </div>

        <div class="dashboard">
            <div class="card">
                <h3>Agent Activity Distribution</h3>
                <div class="chart-container">
                    <canvas id="activityChart"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>Efficiency Distribution</h3>
                <div class="chart-container">
                    <canvas id="efficiencyChart"></canvas>
                </div>
            </div>
        </div>

        <div class="card">
            <h3>Agent Rankings</h3>
            <div class="ranking">
                <h4>🏆 Most Active Agents</h4>
                <div id="most-active-list"></div>
            </div>
            <div class="ranking">
                <h4>⚡ Most Efficient Agents</h4>
                <div id="most-efficient-list"></div>
            </div>
        </div>
    </div>

    <script>
        let activityChart, efficiencyChart;

        async function loadUsageAnalytics() {
            try {
                const response = await fetch('/api/analytics/usage');
                const data = await response.json();

                if (data.error) {
                    document.getElementById('loading').textContent = 'Error loading usage analytics: ' + data.error;
                    return;
                }

                // Update metrics
                document.getElementById('total-activity').textContent = data.system_metrics.total_system_activity;
                document.getElementById('total-tasks').textContent = data.system_metrics.total_system_tasks;
                document.getElementById('system-efficiency').textContent = data.system_metrics.system_efficiency.toFixed(2);
                document.getElementById('error-rate').textContent = (data.system_metrics.system_error_rate * 100).toFixed(1);

                // Create charts (placeholder data for now)
                createActivityChart();
                createEfficiencyChart();

                // Display rankings
                displayRankings(data.agent_rankings);

                // Show dashboard
                document.getElementById('loading').style.display = 'none';
                document.getElementById('dashboard').style.display = 'block';

            } catch (error) {
                document.getElementById('loading').textContent = 'Error loading usage analytics: ' + error.message;
            }
        }

        function createActivityChart() {
            const ctx = document.getElementById('activityChart').getContext('2d');
            activityChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8'],
                    datasets: [{
                        label: 'Activities (24h)',
                        data: [45, 52, 38, 67, 41, 39, 28, 35],
                        backgroundColor: 'rgba(54, 162, 235, 0.6)'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: { y: { beginAtZero: true } }
                }
            });
        }

        function createEfficiencyChart() {
            const ctx = document.getElementById('efficiencyChart').getContext('2d');
            efficiencyChart = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8'],
                    datasets: [{
                        label: 'Efficiency Ratio',
                        data: [1.2, 1.4, 0.9, 1.6, 1.3, 1.1, 0.8, 1.0],
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        }

        function displayRankings(rankings) {
            // Most active
            const activeList = document.getElementById('most-active-list');
            activeList.innerHTML = rankings.most_active_agents.map(agent =>
                `<div class="ranking-item"><span>${agent.agent}</span><span>${agent.activities} activities</span></div>`
            ).join('');

            // Most efficient
            const efficientList = document.getElementById('most-efficient-list');
            efficientList.innerHTML = rankings.most_efficient_agents.map(agent =>
                `<div class="ranking-item"><span>${agent.agent}</span><span>${agent.efficiency.toFixed(2)} efficiency</span></div>`
            ).join('');
        }

        // Auto-refresh every 60 seconds
        setInterval(loadUsageAnalytics, 60000);

        // Load analytics on page load
        loadUsageAnalytics();
    </script>
</body>
</html>
        """

        with open(templates_dir / "usage.html", "w") as f:
            f.write(usage_html)

        # Create reports template
        reports_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Business Intelligence Reports</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .report-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin: 20px 0; }
        .report-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); cursor: pointer; transition: transform 0.2s; }
        .report-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.15); }
        .report-icon { font-size: 2em; margin-bottom: 10px; }
        .report-title { font-size: 1.2em; font-weight: bold; margin-bottom: 10px; }
        .report-desc { color: #6b7280; margin-bottom: 15px; }
        .generate-btn { background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .generate-btn:hover { background: #1d4ed8; }
        .report-content { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin: 20px 0; display: none; }
        .metric-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .metric { text-align: center; padding: 15px; background: #f8fafc; border-radius: 6px; }
        .metric-value { font-size: 1.5em; font-weight: bold; color: #2563eb; }
        .metric-label { color: #6b7280; font-size: 0.9em; margin-top: 5px; }
        .insights { background: #f0fdf4; border: 1px solid #bbf7d0; padding: 15px; border-radius: 6px; margin: 15px 0; }
        .recommendations { background: #fefce8; border: 1px solid #fde047; padding: 15px; border-radius: 6px; margin: 15px 0; }
    </style>
</head>
<body>
    <h1>📈 Business Intelligence Reports</h1>

    <div class="report-grid">
        <div class="report-card" onclick="generateReport('daily')">
            <div class="report-icon">📊</div>
            <div class="report-title">Daily Business Intelligence</div>
            <div class="report-desc">24-hour system performance, efficiency metrics, and key insights</div>
            <button class="generate-btn">Generate Daily Report</button>
        </div>

        <div class="report-card" onclick="generateReport('weekly')">
            <div class="report-icon">📈</div>
            <div class="report-title">Weekly Analytics Report</div>
            <div class="report-desc">7-day trends, performance analysis, and strategic recommendations</div>
            <button class="generate-btn">Generate Weekly Report</button>
        </div>

        <div class="report-card" onclick="generateReport('monthly')">
            <div class="report-icon">🎯</div>
            <div class="report-title">Monthly Business Intelligence</div>
            <div class="report-desc">30-day comprehensive analysis with ROI metrics and future planning</div>
            <button class="generate-btn">Generate Monthly Report</button>
        </div>
    </div>

    <div id="report-content" class="report-content"></div>

    <script>
        let currentReport = null;

        async function generateReport(type) {
            const contentDiv = document.getElementById('report-content');
            contentDiv.style.display = 'block';
            contentDiv.innerHTML = '<h3>Generating report...</h3><p>Please wait...</p>';

            try {
                const response = await fetch(`/api/reports/${type}`);
                const report = await response.json();

                if (report.error) {
                    contentDiv.innerHTML = `<h3>Error</h3><p>${report.error}</p>`;
                    return;
                }

                displayReport(report, type);
                currentReport = report;

            } catch (error) {
                contentDiv.innerHTML = `<h3>Error</h3><p>Failed to generate report: ${error.message}</p>`;
            }
        }

        function displayReport(report, type) {
            const contentDiv = document.getElementById('report-content');

            let html = `<h2>${type.charAt(0).toUpperCase() + type.slice(1)} Business Intelligence Report</h2>`;
            html += `<p><strong>Generated:</strong> ${new Date(report.generated_at).toLocaleString()}</p>`;
            html += `<p><strong>Period:</strong> ${report.period}</p>`;

            if (report.executive_summary) {
                html += `
                <h3>Executive Summary</h3>
                <div class="metric-grid">
                    <div class="metric">
                        <div class="metric-value">${report.executive_summary.system_efficiency.toFixed(2)}</div>
                        <div class="metric-label">System Efficiency</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${(report.executive_summary.error_rate * 100).toFixed(1)}%</div>
                        <div class="metric-label">Error Rate</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${report.executive_summary.tasks_completed}</div>
                        <div class="metric-label">Tasks Completed</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">${report.executive_summary.active_agents}</div>
                        <div class="metric-label">Active Agents</div>
                    </div>
                </div>`;
            }

            if (report.key_insights && report.key_insights.length > 0) {
                html += '<div class="insights"><h3>AI Insights</h3><ul>';
                report.key_insights.forEach(insight => {
                    html += `<li>${insight}</li>`;
                });
                html += '</ul></div>';
            }

            if (report.recommendations && report.recommendations.length > 0) {
                html += '<div class="recommendations"><h3>Strategic Recommendations</h3><ul>';
                report.recommendations.forEach(rec => {
                    html += `<li>${rec}</li>`;
                });
                html += '</ul></div>';
            }

            if (report.agent_performance) {
                html += '<h3>Agent Performance Rankings</h3>';
                html += '<h4>Most Active Agents</h4><ul>';
                report.agent_performance.most_active_agents.forEach(agent => {
                    html += `<li>${agent.agent}: ${agent.activities} activities</li>`;
                });
                html += '</ul>';

                html += '<h4>Most Efficient Agents</h4><ul>';
                report.agent_performance.most_efficient_agents.forEach(agent => {
                    html += `<li>${agent.agent}: ${agent.efficiency.toFixed(2)} efficiency ratio</li>`;
                });
                html += '</ul>';
            }

            contentDiv.innerHTML = html;
        }
    </script>
</body>
</html>
        """

        with open(templates_dir / "reports.html", "w") as f:
            f.write(reports_html)


def main():
    """Main entry point for analytics dashboard."""
    dashboard = AnalyticsDashboardWeb()
    dashboard.create_default_templates()

    # Start analytics service
    analytics_service = get_analytics_service()
    analytics_service.start()

    try:
        # Start web dashboard
        dashboard.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down analytics dashboard...")
    finally:
        analytics_service.stop()


if __name__ == "__main__":
    main()
