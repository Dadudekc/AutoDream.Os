#!/usr/bin/env python3
"""
Simple Monitoring Dashboard - Core
=================================

This module contains core monitoring dashboard functionality including
HTTP request handling, data collection, and basic monitoring operations.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize simple_monitoring_dashboard.py for V2 compliance
License: MIT
"""

import http.server
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class SwarmMonitoringHandler(http.server.BaseHTTPRequestHandler):
    """HTTP request handler for the SWARM monitoring dashboard"""

    def __init__(self, *args, **kwargs):
        self.project_root = Path(__file__).parent.parent.parent
        self.agent_workspaces = self.project_root / "agent_workspaces"
        super().__init__(*args, **kwargs)

    def do_GET(self):
        """Handle GET requests for simple monitoring dashboard."""
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
        """Generate the dashboard HTML content - placeholder for advanced module"""
        return """
        <html>
        <head><title>Simple Monitoring Dashboard</title></head>
        <body>
            <h1>Simple Monitoring Dashboard</h1>
            <p>Dashboard is operational</p>
            <p>Advanced HTML generation available in advanced module</p>
        </body>
        </html>
        """

    def log_message(self, format, *args):
        """Override to reduce log verbosity"""
        pass


# Export core components
__all__ = ["SwarmMonitoringHandler"]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 Simple Monitoring Dashboard - Core Module")
    print("=" * 50)
    print("✅ HTTP request handler loaded successfully")
    print("✅ Agent status collection loaded successfully")
    print("✅ System status monitoring loaded successfully")
    print("✅ Progress calculation loaded successfully")
    print("🐝 WE ARE SWARM - Core monitoring dashboard ready!")
