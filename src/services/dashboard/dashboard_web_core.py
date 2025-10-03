#!/usr/bin/env python3
"""
Swarm Coordination Dashboard Web Core
=====================================

Core HTTP request handling and API logic for the Swarm Coordination Dashboard.
Provides the main request processing and response generation functionality.

Author: Agent-8 (Documentation Specialist)
License: MIT
"""

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from .swarm_coordination_dashboard import SwarmCoordinationDashboard


class DashboardWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard web interface"""

    def __init__(self, dashboard, *args, **kwargs):
        self.dashboard = dashboard
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == "/":
            self._serve_dashboard()
        elif self.path == "/api/status":
            self._serve_api_status()
        elif self.path == "/api/agents":
            self._serve_api_agents()
        elif self.path == "/api/tasks":
            self._serve_api_tasks()
        elif self.path == "/api/messages":
            self._serve_api_messages()
        elif self.path == "/api/alerts":
            self._serve_api_alerts()
        else:
            self._serve_404()

    def do_POST(self):
        """Handle POST requests"""
        if self.path == "/api/acknowledge-alert":
            self._handle_acknowledge_alert()
        elif self.path == "/api/update-agent":
            self._handle_update_agent()
        else:
            self._serve_404()

    def _serve_dashboard(self):
        """Serve main dashboard HTML"""
        from .dashboard_web_html import generate_dashboard_html

        html_content = generate_dashboard_html()
        self._send_response(200, "text/html", html_content)

    def _serve_api_status(self):
        """Serve API status endpoint"""
        data = self.dashboard.get_dashboard_data()
        self._send_json_response(200, data)

    def _serve_api_agents(self):
        """Serve API agents endpoint"""
        agents = self.dashboard.get_all_agent_status()
        data = {
            agent_id: {
                "agent_id": agent.agent_id,
                "status": agent.status.value,
                "current_task": agent.current_task,
                "last_activity": agent.last_activity.isoformat(),
                "performance_score": agent.performance_score,
                "message_count": agent.message_count,
                "error_count": agent.error_count,
            }
            for agent_id, agent in agents.items()
        }
        self._send_json_response(200, data)

    def _serve_api_tasks(self):
        """Serve API tasks endpoint"""
        tasks = self.dashboard.get_all_task_status()
        data = {
            task_id: {
                "task_id": task.task_id,
                "title": task.title,
                "status": task.status.value,
                "assigned_agent": task.assigned_agent,
                "priority": task.priority,
                "progress": task.progress,
                "updated_at": task.updated_at.isoformat(),
            }
            for task_id, task in tasks.items()
        }
        self._send_json_response(200, data)

    def _serve_api_messages(self):
        """Serve API messages endpoint"""
        messages = self.dashboard.get_recent_messages(50)
        self._send_json_response(200, messages)

    def _serve_api_alerts(self):
        """Serve API alerts endpoint"""
        alerts = self.dashboard.get_alerts()
        self._send_json_response(200, alerts)

    def _handle_acknowledge_alert(self):
        """Handle alert acknowledgment"""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        alert_id = data.get("alert_id")
        if alert_id:
            self.dashboard.acknowledge_alert(alert_id)
            self._send_json_response(200, {"status": "success"})
        else:
            self._send_json_response(400, {"error": "Missing alert_id"})

    def _handle_update_agent(self):
        """Handle agent status update"""
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode("utf-8"))

        agent_id = data.get("agent_id")
        status = data.get("status")
        current_task = data.get("current_task")

        if agent_id and status:
            from .swarm_coordination_dashboard import AgentStatus

            agent_status = AgentStatus(status)
            self.dashboard.update_agent_status(agent_id, agent_status, current_task)
            self._send_json_response(200, {"status": "success"})
        else:
            self._send_json_response(400, {"error": "Missing required fields"})

    def _serve_404(self):
        """Serve 404 error"""
        self._send_response(404, "text/plain", "Not Found")

    def _send_response(self, status_code: int, content_type: str, content: str):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _send_json_response(self, status_code: int, data: Any):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2)
        self._send_response(status_code, "application/json", json_data)

    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass


class DashboardWebServer:
    """Web server for the dashboard interface"""

    def __init__(
        self, dashboard: SwarmCoordinationDashboard, host: str = "localhost", port: int = 8080
    ):
        self.dashboard = dashboard
        self.host = host
        self.port = port
        self.server = None
        self.thread = None

    def start(self):
        """Start the web server"""

        def handler(*args, **kwargs):
            return DashboardWebHandler(self.dashboard, *args, **kwargs)

        self.server = HTTPServer((self.host, self.port), handler)
        self.thread = threading.Thread(
            target=self.server.serve_forever, daemon=True, daemon=True, daemon=True
        )
        self.thread.daemon = True
        self.thread.start()

        print(f"🚀 Swarm Coordination Dashboard started at http://{self.host}:{self.port}")

    def stop(self):
        """Stop the web server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 Swarm Coordination Dashboard stopped")
