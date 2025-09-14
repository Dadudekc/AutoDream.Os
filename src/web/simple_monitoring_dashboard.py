#!/usr/bin/env python3
"""
🐝 SIMPLE SWARM MONITORING DASHBOARD - Agent-7
Lightweight web monitoring interface using only standard library

Real-time monitoring dashboard for SWARM operations without external dependencies.
Provides agent status tracking, consolidation progress, and basic monitoring.
"""

import http.server
import json
import socketserver
from datetime import datetime
from pathlib import Path


class SwarmMonitoringHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the SWARM monitoring dashboard"""

    def __init__(self, *args, **kwargs):
        self.project_root = Path(__file__).parent.parent.parent
        self.agent_workspaces = self.project_root / "agent_workspaces"
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests for simple monitoring dashboard."""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Simple HTML response
        html = """
        <html>
        <head><title>Simple Monitoring Dashboard</title></head>
        <body>
            <h1>Simple Monitoring Dashboard</h1>
            <p>Dashboard is operational</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Simple_Monitoring_Dashboard(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

        """Handle GET requests"""
        try:
            if self.path == "/":
                self.serve_dashboard()
            elif self.path == "/api/agents/status":
                self.serve_agents_status()
            elif self.path == "/api/system/status":
                self.serve_system_status()
            elif self.path == "/api/consolidation/progress":
                self.serve_consolidation_progress()
            elif self.path.startswith("/static/"):
                self.serve_static_file()
            else:
                self.send_error(404, "Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def serve_dashboard(self):
        """Serve the main dashboard HTML"""
        html_content = self.generate_dashboard_html()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def serve_agents_status(self):
        """Serve agent status data as JSON"""
        try:
            agents_data = self.get_agents_status()
            response = {
                "timestamp": datetime.now().isoformat(),
                "agents": agents_data,
                "total_agents": len(agents_data),
                "active_agents": len([a for a in agents_data if a.get("status") != "OFFLINE"]),
            }
            self.send_json_response(response)
        except Exception as e:
            self.send_json_response({"error": str(e), "timestamp": datetime.now().isoformat()})

    def serve_system_status(self):
        """Serve basic system status"""
        try:
            system_info = {
                "timestamp": datetime.now().isoformat(),
                "server_status": "RUNNING",
                "uptime": "Monitoring Active",
                "monitoring_mode": "SIMPLE_MODE",
            }
            self.send_json_response(system_info)
        except Exception as e:
            self.send_json_response({"error": str(e)})

    def serve_consolidation_progress(self):
        """Serve consolidation progress data"""
        try:
            progress_data = self.calculate_consolidation_progress()
            self.send_json_response(progress_data)
        except Exception as e:
            self.send_json_response({"error": str(e)})

    def serve_static_file(self):
        """Serve static files (if any)"""
        self.send_error(404, "Static files not available in simple mode")

    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))

    def get_agents_status(self):
        """Get status of all agents from their status.json files"""
        agents_status = []

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status_file = self.agent_workspaces / agent_id / "status.json"

            try:
                if status_file.exists():
                    with open(status_file, encoding="utf-8") as f:
                        data = json.load(f)

                    agent_status = {
                        "agent_id": agent_id,
                        "status": data.get("status", "UNKNOWN"),
                        "current_phase": data.get("current_phase", "UNKNOWN"),
                        "last_updated": data.get("last_updated", datetime.now().isoformat()),
                        "current_mission": data.get("current_mission"),
                        "mission_priority": data.get("mission_priority"),
                        "progress_percentage": data.get("progress_percentage"),
                        "active_tasks": len(data.get("current_tasks", [])),
                        "completed_tasks": len(data.get("completed_tasks", [])),
                    }
                    agents_status.append(agent_status)
                else:
                    agents_status.append(
                        {
                            "agent_id": agent_id,
                            "status": "OFFLINE",
                            "current_phase": "UNKNOWN",
                            "last_updated": datetime.now().isoformat(),
                            "active_tasks": 0,
                            "completed_tasks": 0,
                        }
                    )

            except Exception as e:
                agents_status.append(
                    {
                        "agent_id": agent_id,
                        "status": "ERROR",
                        "current_phase": "UNKNOWN",
                        "last_updated": datetime.now().isoformat(),
                        "active_tasks": 0,
                        "completed_tasks": 0,
                        "error": str(e),
                    }
                )

        return agents_status

    def calculate_consolidation_progress(self):
        """Calculate overall consolidation progress"""
        try:
            agents_status = self.get_agents_status()

            total_progress = 0
            active_tasks = 0
            completed_tasks = 0
            active_agents = 0

            for agent in agents_status:
                progress = agent.get("progress_percentage", 0)
                if progress:
                    total_progress += progress
                    active_agents += 1

                active_tasks += agent.get("active_tasks", 0)
                completed_tasks += agent.get("completed_tasks", 0)

            average_progress = total_progress / max(active_agents, 1)

            return {
                "timestamp": datetime.now().isoformat(),
                "overall_progress": round(average_progress, 1),
                "active_agents": active_agents,
                "total_active_tasks": active_tasks,
                "total_completed_tasks": completed_tasks,
                "total_agents": len(agents_status),
            }

        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "overall_progress": 0,
                "active_agents": 0,
            }

    def generate_dashboard_html(self):
        """Generate the dashboard HTML content"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐝 SWARM Monitoring Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3rem;
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }

        .agent-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 12px;
            border-left: 4px solid #28a745;
            font-size: 0.9rem;
        }

        .agent-card.offline {
            border-left-color: #dc3545;
            opacity: 0.7;
        }

        .agent-card.error {
            border-left-color: #ffc107;
        }

        .agent-id {
            font-weight: bold;
            margin-bottom: 5px;
        }

        .agent-status {
            color: #666;
            font-size: 0.8rem;
        }

        .progress-bar {
            width: 100%;
            height: 20px;
            background: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745, #20c997);
            transition: width 0.3s ease;
        }

        .metric {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
            margin: 5px 0;
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #667eea;
        }

        .metric-label {
            font-size: 0.9rem;
            color: #666;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: white;
            opacity: 0.8;
        }

        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }

        .refresh-btn:hover {
            background: #5a67d8;
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐝 SWARM Monitoring Dashboard</h1>
            <p>Real-time monitoring for SWARM intelligence operations</p>
            <p><small>Simple Mode - Agent-7 Web Monitoring Interface</small></p>
            <button class="refresh-btn" onclick="refreshData()">🔄 Refresh Data</button>
            <div id="last-update">Last updated: <span id="update-time">-</span></div>
        </div>

        <div class="dashboard-grid">
            <!-- Agent Status Card -->
            <div class="card">
                <h3>🤖 Agent Status</h3>
                <div id="agent-status" class="status-grid">
                    <div class="agent-card">
                        <div class="agent-id">Loading...</div>
                        <div class="agent-status">Please refresh</div>
                    </div>
                </div>
            </div>

            <!-- System Status Card -->
            <div class="card">
                <h3>📊 System Status</h3>
                <div id="system-status">
                    <div class="metric">
                        <div class="metric-value" id="server-status">RUNNING</div>
                        <div class="metric-label">Server Status</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value" id="active-agents">-</div>
                        <div class="metric-label">Active Agents</div>
                    </div>
                </div>
            </div>

            <!-- Consolidation Progress Card -->
            <div class="card">
                <h3>📈 Consolidation Progress</h3>
                <div class="progress-bar">
                    <div id="progress-fill" class="progress-fill" style="width: 0%"></div>
                </div>
                <div id="progress-text">Loading progress...</div>
                <div id="consolidation-details">
                    <div class="metric">
                        <div class="metric-value" id="total-tasks">-</div>
                        <div class="metric-label">Total Tasks</div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>🐝 SWARM Intelligence Operations - Agent-7 Simple Web Monitoring Interface</p>
        <p>Real-time monitoring for maximum coordination efficiency</p>
    </div>

    <script>
        let lastUpdateTime = new Date();

        // Load data on page load
        document.addEventListener('DOMContentLoaded', function() {
            refreshData();
            // Auto-refresh every 30 seconds
            setInterval(refreshData, 30000);
        });

        async function refreshData() {
            try {
                // Fetch agent status
                const agentsResponse = await fetch('/api/agents/status');
                const agentsData = await agentsResponse.json();

                // Fetch system status
                const systemResponse = await fetch('/api/system/status');
                const systemData = await systemResponse.json();

                // Fetch consolidation progress
                const progressResponse = await fetch('/api/consolidation/progress');
                const progressData = await progressResponse.json();

                // Update UI
                updateAgentStatus(agentsData);
                updateSystemStatus(systemData);
                updateProgress(progressData);
                updateTimestamp(agentsData.timestamp);

            } catch (error) {
                console.error('Error refreshing data:', error);
                document.getElementById('agent-status').innerHTML =
                    '<div class="agent-card error"><div class="agent-id">Error</div><div class="agent-status">Failed to load data</div></div>';
            }
        }

        function updateAgentStatus(data) {
            const container = document.getElementById('agent-status');
            const agents = data.agents || [];

            if (agents.length === 0) {
                container.innerHTML = '<div class="agent-card"><div class="agent-id">No agents found</div></div>';
                return;
            }

            container.innerHTML = agents.map(agent => {
                const statusClass = agent.status === 'OFFLINE' ? 'offline' :
                                  agent.status === 'ERROR' ? 'error' : '';
                return `
                    <div class="agent-card ${statusClass}">
                        <div class="agent-id">${agent.agent_id}</div>
                        <div class="agent-status">${agent.status}</div>
                        <div style="font-size: 0.7rem; color: #888; margin-top: 3px;">
                            Tasks: ${agent.active_tasks || 0}/${(agent.active_tasks || 0) + (agent.completed_tasks || 0)}
                        </div>
                    </div>
                `;
            }).join('');
        }

        function updateSystemStatus(data) {
            document.getElementById('server-status').textContent = data.server_status || 'UNKNOWN';
            document.getElementById('active-agents').textContent = data.monitoring_mode || 'SIMPLE';
        }

        function updateProgress(data) {
            const fill = document.getElementById('progress-fill');
            const text = document.getElementById('progress-text');
            const details = document.getElementById('consolidation-details');

            if (data.error) {
                text.textContent = `Error: ${data.error}`;
                return;
            }

            const percentage = data.overall_progress || 0;
            fill.style.width = `${percentage}%`;
            text.textContent = `${percentage}% Complete - ${data.active_agents || 0}/${data.total_agents || 8} Agents`;

            document.getElementById('total-tasks').textContent =
                (data.total_active_tasks || 0) + (data.total_completed_tasks || 0);
        }

        function updateTimestamp(timestamp) {
            const timeElement = document.getElementById('update-time');
            timeElement.textContent = new Date(timestamp).toLocaleString();
            lastUpdateTime = new Date(timestamp);
        }
    </script>
</body>
</html>"""

    def log_message(self, format, *args):
        """Override to reduce log verbosity"""
        pass


class SimpleSwarmDashboard:
    """Simple SWARM monitoring dashboard using only standard library"""

    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.httpd = None
        self.is_running = False

    def start(self):
        """Start the dashboard server"""
        try:
            with socketserver.TCPServer((self.host, self.port), SwarmMonitoringHandler) as httpd:
                self.httpd = httpd
                self.is_running = True

                print("🐝 SWARM SIMPLE MONITORING DASHBOARD - Agent-7")
                print("=" * 60)
                print("🚀 Dashboard started successfully!")
                print(f"🌐 Access at: http://{self.host}:{self.port}")
                print("📊 Features:")
                print("  - Real-time agent status monitoring")
                print("  - Consolidation progress tracking")
                print("  - System status overview")
                print("  - Auto-refresh every 30 seconds")
                print("=" * 60)
                print("⏹️  Press Ctrl+C to stop the server")
                print()

                httpd.serve_forever()

        except KeyboardInterrupt:
            print("\n🐝 Shutting down SWARM Monitoring Dashboard...")
            self.stop()
        except Exception as e:
            print(f"❌ Error starting dashboard: {e}")
            self.stop()

    def stop(self):
        """Stop the dashboard server"""
        self.is_running = False
        if self.httpd:
            self.httpd.shutdown()
        print("✅ Dashboard stopped successfully")


if __name__ == "__main__":
    dashboard = SimpleSwarmDashboard()
    dashboard.start()
