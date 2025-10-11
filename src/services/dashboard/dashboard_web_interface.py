#!/usr/bin/env python3
"""
Swarm Coordination Dashboard Web Interface
==========================================

Web-based interface for the Swarm Coordination Dashboard.
Provides real-time visualization of agent status, tasks, and performance.

Author: Agent-2 (Architecture & Design Specialist) + Agent-4 (Captain)
License: MIT
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

from .swarm_coordination_dashboard import SwarmCoordinationDashboard

class DashboardWebHandler(BaseHTTPRequestHandler):
    """HTTP request handler for dashboard web interface"""
    
    def __init__(self, dashboard, *args, **kwargs):
        self.dashboard = dashboard
        super().__init__(*args, **kwargs)
        
    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self._serve_dashboard()
        elif self.path == '/api/status':
            self._serve_api_status()
        elif self.path == '/api/agents':
            self._serve_api_agents()
        elif self.path == '/api/tasks':
            self._serve_api_tasks()
        elif self.path == '/api/messages':
            self._serve_api_messages()
        elif self.path == '/api/alerts':
            self._serve_api_alerts()
        else:
            self._serve_404()
            
    def do_POST(self):
        """Handle POST requests"""
        if self.path == '/api/acknowledge-alert':
            self._handle_acknowledge_alert()
        elif self.path == '/api/update-agent':
            self._handle_update_agent()
        else:
            self._serve_404()
            
    def _serve_dashboard(self):
        """Serve main dashboard HTML"""
        html_content = self._generate_dashboard_html()
        self._send_response(200, 'text/html', html_content)
        
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
                "error_count": agent.error_count
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
                "updated_at": task.updated_at.isoformat()
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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        alert_id = data.get('alert_id')
        if alert_id:
            self.dashboard.acknowledge_alert(alert_id)
            self._send_json_response(200, {"status": "success"})
        else:
            self._send_json_response(400, {"error": "Missing alert_id"})
            
    def _handle_update_agent(self):
        """Handle agent status update"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        agent_id = data.get('agent_id')
        status = data.get('status')
        current_task = data.get('current_task')
        
        if agent_id and status:
            from .swarm_coordination_dashboard import AgentStatus
            agent_status = AgentStatus(status)
            self.dashboard.update_agent_status(agent_id, agent_status, current_task)
            self._send_json_response(200, {"status": "success"})
        else:
            self._send_json_response(400, {"error": "Missing required fields"})
            
    def _serve_404(self):
        """Serve 404 error"""
        self._send_response(404, 'text/plain', 'Not Found')
        
    def _send_response(self, status_code: int, content_type: str, content: str):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
        
    def _send_json_response(self, status_code: int, data: Any):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2)
        self._send_response(status_code, 'application/json', json_data)
        
    def _generate_dashboard_html(self) -> str:
        """Generate dashboard HTML"""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Swarm Coordination Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        .header h1 {
            color: #2c3e50;
            font-size: 2.5em;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .header p {
            color: #7f8c8d;
            text-align: center;
            font-size: 1.1em;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease;
        }
        
        .card:hover {
            transform: translateY(-5px);
        }
        
        .card h2 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.5em;
        }
        
        .agent-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .agent-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #3498db;
        }
        
        .agent-card.active {
            border-left-color: #27ae60;
        }
        
        .agent-card.working {
            border-left-color: #f39c12;
        }
        
        .agent-card.error {
            border-left-color: #e74c3c;
        }
        
        .agent-card.offline {
            border-left-color: #95a5a6;
        }
        
        .agent-id {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .agent-status {
            color: #7f8c8d;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        
        .agent-task {
            color: #34495e;
            font-size: 0.85em;
        }
        
        .task-list {
            max-height: 300px;
            overflow-y: auto;
        }
        
        .task-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
            border-left: 4px solid #3498db;
        }
        
        .task-item.completed {
            border-left-color: #27ae60;
        }
        
        .task-item.in-progress {
            border-left-color: #f39c12;
        }
        
        .task-title {
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        
        .task-meta {
            color: #7f8c8d;
            font-size: 0.85em;
        }
        
        .progress-bar {
            width: 100%;
            height: 8px;
            background: #ecf0f1;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 5px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #3498db, #2ecc71);
            transition: width 0.3s ease;
        }
        
        .alert-list {
            max-height: 200px;
            overflow-y: auto;
        }
        
        .alert-item {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        }
        
        .alert-item.error {
            background: #f8d7da;
            border-color: #f5c6cb;
        }
        
        .alert-item.warning {
            background: #fff3cd;
            border-color: #ffeaa7;
        }
        
        .alert-item.info {
            background: #d1ecf1;
            border-color: #bee5eb;
        }
        
        .refresh-btn {
            background: linear-gradient(45deg, #3498db, #2ecc71);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
            margin: 10px;
        }
        
        .refresh-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        
        .status-indicator {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-active { background: #27ae60; }
        .status-working { background: #f39c12; }
        .status-error { background: #e74c3c; }
        .status-offline { background: #95a5a6; }
        
        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
            
            .agent-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐝 Swarm Coordination Dashboard</h1>
            <p>Real-time monitoring and coordination for Team Alpha</p>
            <button class="refresh-btn" onclick="refreshDashboard()">🔄 Refresh</button>
        </div>
        
        <div class="dashboard-grid">
            <div class="card">
                <h2>🤖 Agent Status</h2>
                <div class="agent-grid" id="agent-grid">
                    <!-- Agent cards will be populated here -->
                </div>
            </div>
            
            <div class="card">
                <h2>📋 Active Tasks</h2>
                <div class="task-list" id="task-list">
                    <!-- Task items will be populated here -->
                </div>
            </div>
            
            <div class="card">
                <h2>🚨 Alerts</h2>
                <div class="alert-list" id="alert-list">
                    <!-- Alert items will be populated here -->
                </div>
            </div>
            
            <div class="card">
                <h2>📊 Summary</h2>
                <div id="summary-stats">
                    <!-- Summary statistics will be populated here -->
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function refreshDashboard() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    updateAgentGrid(data.agents);
                    updateTaskList(data.tasks);
                    updateAlertList(data.alerts);
                    updateSummaryStats(data.summary);
                })
                .catch(error => console.error('Error refreshing dashboard:', error));
        }
        
        function updateAgentGrid(agents) {
            const grid = document.getElementById('agent-grid');
            grid.innerHTML = '';
            
            Object.values(agents).forEach(agent => {
                const card = document.createElement('div');
                card.className = `agent-card ${agent.status}`;
                card.innerHTML = `
                    <div class="agent-id">${agent.agent_id}</div>
                    <div class="agent-status">
                        <span class="status-indicator status-${agent.status}"></span>
                        ${agent.status.toUpperCase()}
                    </div>
                    <div class="agent-task">${agent.current_task || 'No active task'}</div>
                    <div class="agent-task">Score: ${agent.performance_score}%</div>
                `;
                grid.appendChild(card);
            });
        }
        
        function updateTaskList(tasks) {
            const list = document.getElementById('task-list');
            list.innerHTML = '';
            
            Object.values(tasks).forEach(task => {
                const item = document.createElement('div');
                item.className = `task-item ${task.status}`;
                item.innerHTML = `
                    <div class="task-title">${task.title}</div>
                    <div class="task-meta">
                        ${task.assigned_agent} • ${task.priority} • ${task.progress}%
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%"></div>
                    </div>
                `;
                list.appendChild(item);
            });
        }
        
        function updateAlertList(alerts) {
            const list = document.getElementById('alert-list');
            list.innerHTML = '';
            
            if (alerts.length === 0) {
                list.innerHTML = '<div style="text-align: center; color: #7f8c8d;">No active alerts</div>';
                return;
            }
            
            alerts.forEach(alert => {
                const item = document.createElement('div');
                item.className = `alert-item ${alert.type}`;
                item.innerHTML = `
                    <div style="font-weight: bold;">${alert.type.toUpperCase()}</div>
                    <div>${alert.message}</div>
                    <div style="font-size: 0.8em; color: #7f8c8d; margin-top: 5px;">
                        ${new Date(alert.timestamp).toLocaleString()}
                    </div>
                `;
                list.appendChild(item);
            });
        }
        
        function updateSummaryStats(summary) {
            const stats = document.getElementById('summary-stats');
            stats.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                    <div style="text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: #3498db;">${summary.active_agents}</div>
                        <div style="color: #7f8c8d;">Active Agents</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: #27ae60;">${summary.completed_tasks}</div>
                        <div style="color: #7f8c8d;">Completed Tasks</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: #f39c12;">${summary.completion_rate.toFixed(1)}%</div>
                        <div style="color: #7f8c8d;">Completion Rate</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2em; font-weight: bold; color: #e74c3c;">${summary.pending_alerts}</div>
                        <div style="color: #7f8c8d;">Pending Alerts</div>
                    </div>
                </div>
            `;
        }
        
        // Auto-refresh every 5 seconds
        setInterval(refreshDashboard, 5000);
        
        // Initial load
        refreshDashboard();
    </script>
</body>
</html>
        """
        
    def log_message(self, format, *args):
        """Override to suppress default logging"""
        pass

class DashboardWebServer:
    """Web server for the dashboard interface"""
    
    def __init__(self, dashboard: SwarmCoordinationDashboard, host: str = "localhost", port: int = 8080):
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
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True
        self.thread.start()
        
        print(f"🚀 Swarm Coordination Dashboard started at http://{self.host}:{self.port}")
        
    def stop(self):
        """Stop the web server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 Swarm Coordination Dashboard stopped")


