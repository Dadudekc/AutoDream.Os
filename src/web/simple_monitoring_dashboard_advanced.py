#!/usr/bin/env python3
"""
Simple Monitoring Dashboard - Advanced
=====================================

This module contains advanced monitoring dashboard functionality including
HTML generation, server management, and the main dashboard class.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Modularize simple_monitoring_dashboard.py for V2 compliance
License: MIT
"""

import logging
import socketserver

# Import core components
from .simple_monitoring_dashboard_core import SwarmMonitoringHandler

logger = logging.getLogger(__name__)


class AdvancedSwarmMonitoringHandler(SwarmMonitoringHandler):
    """Advanced HTTP request handler with enhanced HTML generation"""

    def generate_dashboard_html(self):
        """Generate the advanced dashboard HTML content"""
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


class SimpleSwarmDashboard:
    """Simple SWARM monitoring dashboard using only standard library"""

    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.httpd: socketserver.TCPServer | None = None
        self.is_running = False

    def start(self):
        """Start the dashboard server"""
        try:
            with socketserver.TCPServer(
                (self.host, self.port), AdvancedSwarmMonitoringHandler
            ) as httpd:
                self.httpd = httpd
                self.is_running = True

                logger.info("🐝 SWARM SIMPLE MONITORING DASHBOARD - Agent-7")
                print("=" * 60)
                logger.info("🚀 Dashboard started successfully!")
                logger.info(f"🌐 Access at: http://{self.host}:{self.port}")
                logger.info("📊 Features:")
                logger.info("  - Real-time agent status monitoring")
                logger.info("  - Consolidation progress tracking")
                logger.info("  - System status overview")
                logger.info("  - Auto-refresh every 30 seconds")
                print("=" * 60)
                logger.info("⏹️  Press Ctrl+C to stop the server")
                logger.info("")

                httpd.serve_forever()

        except KeyboardInterrupt:
            logger.info("\n🐝 Shutting down SWARM Monitoring Dashboard...")
            self.stop()
        except Exception as e:
            logger.info(f"❌ Error starting dashboard: {e}")
            self.stop()

    def stop(self):
        """Stop the dashboard server"""
        self.is_running = False
        if self.httpd:
            self.httpd.shutdown()
        logger.info("✅ Dashboard stopped successfully")


# Export advanced components
__all__ = ["AdvancedSwarmMonitoringHandler", "SimpleSwarmDashboard"]


if __name__ == "__main__":
    """Demonstrate module functionality with practical examples."""
    print("🐝 Simple Monitoring Dashboard - Advanced Module")
    print("=" * 50)
    print("✅ Advanced HTML generation loaded successfully")
    print("✅ Server management loaded successfully")
    print("✅ Main dashboard class loaded successfully")
    print("🐝 WE ARE SWARM - Advanced monitoring dashboard ready!")

    # Example usage
    dashboard = SimpleSwarmDashboard()
    print("✅ Dashboard instance created successfully")
    print("🚀 Ready to start monitoring server!")
