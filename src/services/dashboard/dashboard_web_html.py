#!/usr/bin/env python3
"""
Swarm Coordination Dashboard Web Interface
==========================================
Web interface components and HTML generation for the Swarm Coordination Dashboard.
Provides the frontend HTML, CSS, and JavaScript for the dashboard.
Author: Agent-8 (Documentation Specialist)
License: MIT
"""
from typing import Dict, List, Any
def generate_dashboard_html() -> str:
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
