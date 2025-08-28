#!/usr/bin/env python3
"""
Real-Time Performance Dashboard - PERF-001 Contract

Advanced real-time performance monitoring dashboard with live updates,
performance alerts, and trend visualization.

Author: Agent-6 (PERFORMANCE OPTIMIZATION MANAGER)
Contract: PERF-001 - Advanced Performance Metrics Implementation
Status: EXECUTION_IN_PROGRESS
"""

import os
import sys
import time
import json
import logging
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import webbrowser
import http.server
import socketserver
import urllib.parse

# Add current directory to path for imports
CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from advanced_performance_metrics import AdvancedMetricsCollector, RealTimeMonitor


class PerformanceDashboard:
    """Real-time performance monitoring dashboard"""
    
    def __init__(self, port: int = 8080):
        self.logger = logging.getLogger(f"{__name__}.PerformanceDashboard")
        self.port = port
        self.server = None
        self.server_thread = None
        self.dashboard_active = False
        
        # Initialize metrics system
        self.metrics_collector = AdvancedMetricsCollector()
        self.monitor = RealTimeMonitor(self.metrics_collector)
        
        # Dashboard data
        self.dashboard_data = {
            "last_update": datetime.now().isoformat(),
            "system_status": "initializing",
            "performance_metrics": {},
            "alerts": [],
            "trends": {},
            "overall_score": 0.0
        }
        
        self.logger.info("🚀 Performance Dashboard initialized")
    
    def start_dashboard(self):
        """Start the performance dashboard"""
        if not self.dashboard_active:
            self.dashboard_active = True
            
            # Start metrics collection
            self.monitor.start_monitoring()
            
            # Start web server
            self._start_web_server()
            
            # Start dashboard update loop
            self._start_update_loop()
            
            self.logger.info("✅ Performance Dashboard started")
    
    def stop_dashboard(self):
        """Stop the performance dashboard"""
        self.dashboard_active = False
        
        # Stop monitoring
        self.monitor.stop_monitoring()
        
        # Stop web server
        if self.server:
            self.server.shutdown()
        
        self.logger.info("⏹️ Performance Dashboard stopped")
    
    def _start_web_server(self):
        """Start the web server for the dashboard"""
        try:
            # Create custom request handler
            handler = self._create_request_handler()
            
            # Start server in separate thread
            self.server_thread = threading.Thread(target=self._run_server, args=(handler,), daemon=True)
            self.server_thread.start()
            
            self.logger.info(f"🌐 Web server started on port {self.port}")
            
        except Exception as e:
            self.logger.error(f"Failed to start web server: {e}")
    
    def _run_server(self, handler):
        """Run the web server"""
        try:
            with socketserver.TCPServer(("", self.port), handler) as httpd:
                self.server = httpd
                httpd.serve_forever()
        except Exception as e:
            self.logger.error(f"Web server error: {e}")
    
    def _create_request_handler(self):
        """Create custom HTTP request handler"""
        
        class DashboardRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                self.dashboard = self
                super().__init__(*args, **kwargs)
            
            def do_GET(self):
                """Handle GET requests"""
                try:
                    if self.path == '/':
                        # Serve main dashboard
                        self._serve_dashboard()
                    elif self.path == '/api/metrics':
                        # Serve metrics API
                        self._serve_metrics_api()
                    elif self.path == '/api/alerts':
                        # Serve alerts API
                        self._serve_alerts_api()
                    elif self.path == '/api/status':
                        # Serve status API
                        self._serve_status_api()
                    else:
                        # Serve static files
                        super().do_GET()
                except Exception as e:
                    self.logger.error(f"Request handler error: {e}")
                    self.send_error(500, str(e))
            
            def _serve_dashboard(self):
                """Serve the main dashboard HTML"""
                html_content = self._generate_dashboard_html()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            
            def _serve_metrics_api(self):
                """Serve metrics data as JSON"""
                try:
                    metrics = self.dashboard.metrics_collector.get_metrics_summary()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(metrics, default=str).encode('utf-8'))
                except Exception as e:
                    self.send_error(500, str(e))
            
            def _serve_alerts_api(self):
                """Serve alerts data as JSON"""
                try:
                    alerts = self.dashboard.monitor.get_alerts()
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(alerts, default=str).encode('utf-8'))
                except Exception as e:
                    self.send_error(500, str(e))
            
            def _serve_status_api(self):
                """Serve dashboard status as JSON"""
                try:
                    status = {
                        "dashboard_active": self.dashboard.dashboard_active,
                        "metrics_active": self.dashboard.metrics_collector.collection_active,
                        "monitoring_active": self.dashboard.monitor.monitoring_active,
                        "last_update": self.dashboard.dashboard_data["last_update"],
                        "overall_score": self.dashboard.dashboard_data["overall_score"]
                    }
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps(status, default=str).encode('utf-8'))
                except Exception as e:
                    self.send_error(500, str(e))
            
            def _generate_dashboard_html(self):
                """Generate the main dashboard HTML"""
                return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Performance Dashboard - PERF-001</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            margin: 10px 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        .metric-card h3 {{
            margin: 0 0 15px 0;
            color: #fff;
            font-size: 1.3em;
        }}
        .metric-value {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        .metric-label {{
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 10px;
        }}
        .trend-indicator {{
            display: inline-block;
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 0.8em;
            font-weight: bold;
            margin-left: 10px;
        }}
        .trend-increasing {{ background: #ff6b6b; }}
        .trend-decreasing {{ background: #51cf66; }}
        .trend-stable {{ background: #74c0fc; }}
        .alerts-section {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .alert-item {{
            background: rgba(255,107,107,0.2);
            border-left: 4px solid #ff6b6b;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
        }}
        .status-bar {{
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            margin-bottom: 20px;
        }}
        .refresh-info {{
            text-align: center;
            opacity: 0.7;
            font-size: 0.9em;
            margin-top: 20px;
        }}
        .overall-score {{
            text-align: center;
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .score-excellent {{ color: #51cf66; }}
        .score-good {{ color: #74c0fc; }}
        .score-warning {{ color: #ffd43b; }}
        .score-critical {{ color: #ff6b6b; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Advanced Performance Dashboard</h1>
            <p>PERF-001 Contract - Real-Time System Monitoring</p>
            <p>Agent-6 (PERFORMANCE OPTIMIZATION MANAGER)</p>
        </div>
        
        <div class="status-bar">
            <strong>Dashboard Status:</strong> <span id="dashboard-status">Loading...</span> | 
            <strong>Last Update:</strong> <span id="last-update">Loading...</span>
        </div>
        
        <div class="overall-score">
            <div id="overall-score">--</div>
            <div style="font-size: 0.3em; opacity: 0.8;">Overall Performance Score</div>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <h3>🖥️ CPU Performance</h3>
                <div class="metric-label">Current Usage</div>
                <div class="metric-value" id="cpu-usage">--</div>
                <div class="metric-label">Trend: <span id="cpu-trend" class="trend-indicator trend-stable">--</span></div>
            </div>
            
            <div class="metric-card">
                <h3>💾 Memory Performance</h3>
                <div class="metric-label">Current Usage</div>
                <div class="metric-value" id="memory-usage">--</div>
                <div class="metric-label">Trend: <span id="memory-trend" class="trend-indicator trend-stable">--</span></div>
            </div>
            
            <div class="metric-card">
                <h3>💿 Disk Performance</h3>
                <div class="metric-label">Current Usage</div>
                <div class="metric-value" id="disk-usage">--</div>
                <div class="metric-label">Trend: <span id="disk-trend" class="trend-indicator trend-stable">--</span></div>
            </div>
            
            <div class="metric-card">
                <h3>🌐 Network Performance</h3>
                <div class="metric-label">Active Connections</div>
                <div class="metric-value" id="network-connections">--</div>
                <div class="metric-label">Status: <span id="network-status">--</span></div>
            </div>
        </div>
        
        <div class="alerts-section">
            <h3>🚨 Performance Alerts</h3>
            <div id="alerts-container">
                <div style="opacity: 0.7;">No alerts currently active</div>
            </div>
        </div>
        
        <div class="refresh-info">
            Dashboard updates automatically every 2 seconds | 
            <button onclick="location.reload()" style="background: rgba(255,255,255,0.2); border: none; color: white; padding: 8px 16px; border-radius: 5px; cursor: pointer;">🔄 Refresh</button>
        </div>
    </div>
    
    <script>
        // Dashboard update functionality
        function updateDashboard() {{
            // Update metrics
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {{
                    if (data.status === 'active') {{
                        const snapshot = data.latest_snapshot;
                        
                        // Update CPU metrics
                        if (snapshot.cpu_metrics && snapshot.cpu_metrics.usage_percent !== undefined) {{
                            document.getElementById('cpu-usage').textContent = 
                                snapshot.cpu_metrics.usage_percent.toFixed(1) + '%';
                        }}
                        
                        // Update memory metrics
                        if (snapshot.memory_metrics && snapshot.memory_metrics.used_percent !== undefined) {{
                            document.getElementById('memory-usage').textContent = 
                                snapshot.memory_metrics.used_percent.toFixed(1) + '%';
                        }}
                        
                        // Update disk metrics
                        if (snapshot.disk_metrics && snapshot.disk_metrics.used_percent !== undefined) {{
                            document.getElementById('disk-usage').textContent = 
                                snapshot.disk_metrics.used_percent.toFixed(1) + '%';
                        }}
                        
                        // Update network metrics
                        if (snapshot.network_metrics && snapshot.network_metrics.active_connections !== undefined) {{
                            document.getElementById('network-connections').textContent = 
                                snapshot.network_metrics.active_connections;
                        }}
                        
                        // Update trends
                        if (data.trends) {{
                            updateTrend('cpu-trend', data.trends.cpu);
                            updateTrend('memory-trend', data.trends.memory);
                            updateTrend('disk-trend', data.trends.disk);
                        }}
                        
                        // Update overall score
                        if (snapshot.overall_score !== undefined) {{
                            const scoreElement = document.getElementById('overall-score');
                            scoreElement.textContent = snapshot.overall_score.toFixed(1);
                            
                            // Update score color
                            scoreElement.className = 'overall-score';
                            if (snapshot.overall_score >= 80) {{
                                scoreElement.classList.add('score-excellent');
                            }} else if (snapshot.overall_score >= 60) {{
                                scoreElement.classList.add('score-good');
                            }} else if (snapshot.overall_score >= 40) {{
                                scoreElement.classList.add('score-warning');
                            }} else {{
                                scoreElement.classList.add('score-critical');
                            }}
                        }}
                    }}
                }})
                .catch(error => console.error('Error fetching metrics:', error));
            
            // Update alerts
            fetch('/api/alerts')
                .then(response => response.json())
                .then(alerts => {{
                    updateAlerts(alerts);
                }})
                .catch(error => console.error('Error fetching alerts:', error));
            
            // Update status
            fetch('/api/status')
                .then(response => response.json())
                .then(status => {{
                    document.getElementById('dashboard-status').textContent = 
                        status.dashboard_active ? 'Active' : 'Inactive';
                    document.getElementById('last-update').textContent = 
                        new Date(status.last_update).toLocaleTimeString();
                }})
                .catch(error => console.error('Error fetching status:', error));
        }}
        
        function updateTrend(elementId, trend) {{
            const element = document.getElementById(elementId);
            if (element) {{
                element.textContent = trend || 'stable';
                element.className = 'trend-indicator';
                
                if (trend === 'increasing') {{
                    element.classList.add('trend-increasing');
                }} else if (trend === 'decreasing') {{
                    element.classList.add('trend-decreasing');
                }} else {{
                    element.classList.add('trend-stable');
                }}
            }}
        }}
        
        function updateAlerts(alerts) {{
            const container = document.getElementById('alerts-container');
            if (alerts && alerts.length > 0) {{
                container.innerHTML = alerts.map(alert => `
                    <div class="alert-item">
                        <strong>${{alert.metric_type}}:</strong> ${{alert.message}} 
                        <span style="opacity: 0.7;">(${{new Date(alert.timestamp).toLocaleTimeString()}})</span>
                    </div>
                `).join('');
            }} else {{
                container.innerHTML = '<div style="opacity: 0.7;">No alerts currently active</div>';
            }}
        }}
        
        // Update dashboard every 2 seconds
        setInterval(updateDashboard, 2000);
        
        // Initial update
        updateDashboard();
    </script>
</body>
</html>
                """
        
        # Set the dashboard reference
        DashboardRequestHandler.dashboard = self
        return DashboardRequestHandler
    
    def _start_update_loop(self):
        """Start the dashboard update loop"""
        def update_loop():
            while self.dashboard_active:
                try:
                    # Update dashboard data
                    self._update_dashboard_data()
                    time.sleep(2)  # Update every 2 seconds
                except Exception as e:
                    self.logger.error(f"Dashboard update error: {e}")
                    time.sleep(2)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def _update_dashboard_data(self):
        """Update dashboard data with latest metrics"""
        try:
            # Get latest metrics
            metrics_summary = self.metrics_collector.get_metrics_summary()
            
            if metrics_summary.get("status") == "active":
                self.dashboard_data.update({
                    "last_update": datetime.now().isoformat(),
                    "system_status": "active",
                    "performance_metrics": metrics_summary.get("latest_snapshot", {}),
                    "trends": metrics_summary.get("trends", {}),
                    "overall_score": metrics_summary.get("latest_snapshot", {}).get("overall_score", 0.0)
                })
            else:
                self.dashboard_data.update({
                    "last_update": datetime.now().isoformat(),
                    "system_status": "inactive",
                    "performance_metrics": {},
                    "trends": {},
                    "overall_score": 0.0
                })
            
            # Get latest alerts
            alerts = self.monitor.get_alerts()
            self.dashboard_data["alerts"] = alerts
            
        except Exception as e:
            self.logger.error(f"Failed to update dashboard data: {e}")
    
    def open_browser(self):
        """Open dashboard in default web browser"""
        try:
            url = f"http://localhost:{self.port}"
            webbrowser.open(url)
            self.logger.info(f"🌐 Dashboard opened in browser: {url}")
        except Exception as e:
            self.logger.error(f"Failed to open browser: {e}")


def main():
    """Main execution function for Performance Dashboard"""
    print("🚀 Performance Dashboard - PERF-001 Contract")
    print("=" * 60)
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize dashboard
    dashboard = PerformanceDashboard(port=8080)
    
    print("✅ Performance Dashboard initialized successfully")
    
    try:
        # Start dashboard
        print("\n🚀 Starting Performance Dashboard...")
        dashboard.start_dashboard()
        
        # Wait a moment for startup
        time.sleep(2)
        
        # Open in browser
        print("\n🌐 Opening dashboard in browser...")
        dashboard.open_browser()
        
        print("\n📊 Dashboard is now running!")
        print("📍 URL: http://localhost:8080")
        print("⏹️  Press Ctrl+C to stop...")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Stopping Performance Dashboard...")
    finally:
        dashboard.stop_dashboard()
        print("✅ Performance Dashboard stopped")


if __name__ == "__main__":
    main()
