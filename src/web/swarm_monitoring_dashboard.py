#!/usr/bin/env python3
"""
🐝 SWARM MONITORING DASHBOARD - Agent-7
Web Monitoring Interface for Swarm Intelligence Operations

Real-time monitoring dashboard for SWARM operations, providing:
- Agent status tracking and coordination
- Performance metrics visualization
- Consolidation progress monitoring
- Alert management and notifications
- Real-time communication monitoring

Author: Agent-7 (Web Development Specialist)
Phase: Mission Execution Phase
Assignment: Web Monitoring Interface (90 min)
"""

import asyncio
import json
import logging
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    psutil = None
    PSUTIL_AVAILABLE = False

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('swarm_monitoring_dashboard.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AgentStatus(BaseModel):
    """Agent status model"""
    agent_id: str
    status: str
    current_phase: str
    last_updated: datetime
    current_mission: Optional[str] = None
    mission_priority: Optional[str] = None
    progress_percentage: Optional[float] = None
    active_tasks: List[str] = []
    completed_tasks: List[str] = []
    coordination_status: Dict[str, Any] = {}


class Alert(BaseModel):
    """Alert model"""
    alert_id: str
    level: str
    message: str
    component: str
    timestamp: datetime
    resolved: bool = False


class SwarmMonitoringDashboard:
    """
    Web monitoring dashboard for SWARM operations.

    This dashboard provides real-time visualization of:
    - Agent status and coordination
    - System performance metrics
    - Consolidation progress tracking
    - Alert management
    - Communication monitoring
    """

    def __init__(self):
        self.app = FastAPI(
            title="SWARM Monitoring Dashboard",
            description="Real-time monitoring dashboard for SWARM intelligence operations",
            version="1.0.0"
        )

        # Setup paths
        self.project_root = Path(__file__).parent.parent.parent
        self.templates_dir = self.project_root / "src" / "web" / "templates"
        self.static_dir = self.project_root / "src" / "web" / "static"
        self.agent_workspaces = self.project_root / "agent_workspaces"

        # Create directories if they don't exist
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.static_dir.mkdir(parents=True, exist_ok=True)

        # Setup templates and static files
        self.templates = Jinja2Templates(directory=str(self.templates_dir))
        self.app.mount("/static", StaticFiles(directory=str(self.static_dir)), name="static")

        # Data storage
        self.connected_clients: List[WebSocket] = []
        self.agent_status_cache: Dict[str, AgentStatus] = {}
        self.alerts: List[Alert] = []
        self.system_metrics: Dict[str, Any] = {}
        self.is_running = False
        self.monitoring_thread: Optional[threading.Thread] = None

        # Setup routes
        self._setup_routes()

    def _setup_routes(self):
        """Setup FastAPI routes"""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard page"""
            return self.templates.TemplateResponse("dashboard.html", {
                "request": request,
                "title": "SWARM Monitoring Dashboard",
                "timestamp": datetime.now().isoformat()
            })

        @self.app.get("/api/agents/status")
        async def get_agents_status():
            """Get status of all agents"""
            try:
                agents_status = await self._get_all_agents_status()
                return JSONResponse(content={
                    "timestamp": datetime.now().isoformat(),
                    "agents": [agent.dict() for agent in agents_status],
                    "total_agents": len(agents_status),
                    "active_agents": len([a for a in agents_status if a.status != "OFFLINE"])
                })
            except Exception as e:
                logger.error(f"Error getting agents status: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/system/metrics")
        async def get_system_metrics():
            """Get system performance metrics"""
            try:
                metrics = await self._get_system_metrics()
                return JSONResponse(content={
                    "timestamp": datetime.now().isoformat(),
                    "metrics": metrics
                })
            except Exception as e:
                logger.error(f"Error getting system metrics: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/alerts")
        async def get_alerts(resolved: bool = False, limit: int = 50):
            """Get active alerts"""
            try:
                filtered_alerts = [alert for alert in self.alerts
                                 if alert.resolved == resolved][:limit]
                return JSONResponse(content={
                    "timestamp": datetime.now().isoformat(),
                    "alerts": [alert.dict() for alert in filtered_alerts],
                    "total": len(filtered_alerts)
                })
            except Exception as e:
                logger.error(f"Error getting alerts: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/consolidation/progress")
        async def get_consolidation_progress():
            """Get consolidation progress across all agents"""
            try:
                progress = await self._calculate_consolidation_progress()
                return JSONResponse(content={
                    "timestamp": datetime.now().isoformat(),
                    "progress": progress
                })
            except Exception as e:
                logger.error(f"Error getting consolidation progress: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.websocket("/ws/updates")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates"""
            await websocket.accept()
            self.connected_clients.append(websocket)
            try:
                while True:
                    # Send periodic updates
                    data = await self._get_dashboard_data()
                    await websocket.send_json(data)
                    await asyncio.sleep(5)  # Update every 5 seconds
            except WebSocketDisconnect:
                self.connected_clients.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if websocket in self.connected_clients:
                    self.connected_clients.remove(websocket)

        @self.app.post("/api/alerts/{alert_id}/resolve")
        async def resolve_alert(alert_id: str):
            """Resolve an alert"""
            try:
                for alert in self.alerts:
                    if alert.alert_id == alert_id:
                        alert.resolved = True
                        alert.timestamp = datetime.now()
                        await self._broadcast_update()
                        return JSONResponse(content={"status": "resolved"})
                raise HTTPException(status_code=404, detail="Alert not found")
            except Exception as e:
                logger.error(f"Error resolving alert: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    async def _get_all_agents_status(self) -> List[AgentStatus]:
        """Get status of all agents from their status.json files"""
        agents_status = []

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            status_file = self.agent_workspaces / agent_id / "status.json"

            try:
                if status_file.exists():
                    with open(status_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    # Convert timestamp strings to datetime
                    last_updated = datetime.fromisoformat(data.get('last_updated', datetime.now().isoformat()))

                    agent_status = AgentStatus(
                        agent_id=agent_id,
                        status=data.get('status', 'UNKNOWN'),
                        current_phase=data.get('current_phase', 'UNKNOWN'),
                        last_updated=last_updated,
                        current_mission=data.get('current_mission'),
                        mission_priority=data.get('mission_priority'),
                        progress_percentage=data.get('progress_percentage'),
                        active_tasks=data.get('current_tasks', []),
                        completed_tasks=data.get('completed_tasks', []),
                        coordination_status=data.get('coordination_status', {})
                    )
                    agents_status.append(agent_status)
                else:
                    # Agent offline or no status file
                    agent_status = AgentStatus(
                        agent_id=agent_id,
                        status="OFFLINE",
                        current_phase="UNKNOWN",
                        last_updated=datetime.now(),
                        active_tasks=[],
                        completed_tasks=[],
                        coordination_status={}
                    )
                    agents_status.append(agent_status)

            except Exception as e:
                logger.error(f"Error reading status for {agent_id}: {e}")
                agent_status = AgentStatus(
                    agent_id=agent_id,
                    status="ERROR",
                    current_phase="UNKNOWN",
                    last_updated=datetime.now(),
                    active_tasks=[],
                    completed_tasks=[],
                    coordination_status={"error": str(e)}
                )
                agents_status.append(agent_status)

        return agents_status

    async def _get_system_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        try:
            if not PSUTIL_AVAILABLE:
                # Return basic metrics when psutil is not available
                return {
                    "cpu_usage": 0,
                    "memory_usage": 0,
                    "memory_used": 0,
                    "memory_total": 0,
                    "disk_usage": 0,
                    "disk_used": 0,
                    "disk_total": 0,
                    "process_memory": 0,
                    "psutil_available": False,
                    "timestamp": datetime.now().isoformat()
                }

            # CPU and memory metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Process information
            process = psutil.Process()
            process_memory = process.memory_info()

            metrics = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_used": memory.used,
                "memory_total": memory.total,
                "disk_usage": disk.percent,
                "disk_used": disk.used,
                "disk_total": disk.total,
                "process_memory": process_memory.rss,
                "psutil_available": True,
                "timestamp": datetime.now().isoformat()
            }

            self.system_metrics = metrics
            return metrics

        except Exception as e:
            logger.error(f"Error getting system metrics: {e}")
            return {
                "error": str(e),
                "psutil_available": PSUTIL_AVAILABLE,
                "timestamp": datetime.now().isoformat()
            }

    async def _calculate_consolidation_progress(self) -> Dict[str, Any]:
        """Calculate overall consolidation progress"""
        try:
            agents_status = await self._get_all_agents_status()

            total_progress = 0
            active_tasks = 0
            completed_tasks = 0

            for agent in agents_status:
                if agent.progress_percentage:
                    total_progress += agent.progress_percentage
                active_tasks += len(agent.active_tasks)
                completed_tasks += len(agent.completed_tasks)

            average_progress = total_progress / len(agents_status) if agents_status else 0

            return {
                "overall_progress": average_progress,
                "active_agents": len([a for a in agents_status if a.status != "OFFLINE"]),
                "total_active_tasks": active_tasks,
                "total_completed_tasks": completed_tasks,
                "agent_breakdown": [
                    {
                        "agent_id": agent.agent_id,
                        "progress": agent.progress_percentage or 0,
                        "active_tasks": len(agent.active_tasks),
                        "completed_tasks": len(agent.completed_tasks)
                    }
                    for agent in agents_status
                ]
            }

        except Exception as e:
            logger.error(f"Error calculating consolidation progress: {e}")
            return {"error": str(e)}

    async def _get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data for WebSocket updates"""
        try:
            agents_status = await self._get_all_agents_status()
            system_metrics = await self._get_system_metrics()
            consolidation_progress = await self._calculate_consolidation_progress()

            return {
                "timestamp": datetime.now().isoformat(),
                "agents": [agent.dict() for agent in agents_status],
                "system_metrics": system_metrics,
                "consolidation_progress": consolidation_progress,
                "active_alerts": [alert.dict() for alert in self.alerts if not alert.resolved],
                "total_alerts": len([a for a in self.alerts if not a.resolved])
            }

        except Exception as e:
            logger.error(f"Error getting dashboard data: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e)
            }

    async def _broadcast_update(self):
        """Broadcast updates to all connected WebSocket clients"""
        if not self.connected_clients:
            return

        data = await self._get_dashboard_data()

        disconnected_clients = []
        for client in self.connected_clients:
            try:
                await client.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting to client: {e}")
                disconnected_clients.append(client)

        # Remove disconnected clients
        for client in disconnected_clients:
            if client in self.connected_clients:
                self.connected_clients.remove(client)

    def start_monitoring(self):
        """Start the monitoring system"""
        if self.is_running:
            logger.warning("Monitoring already running")
            return

        self.is_running = True
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info("🚀 Swarm monitoring dashboard started")

    def stop_monitoring(self):
        """Stop the monitoring system"""
        self.is_running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        logger.info("⏹️ Swarm monitoring dashboard stopped")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_running:
            try:
                # Update system metrics
                asyncio.run(self._get_system_metrics())

                # Check for agent status changes
                asyncio.run(self._check_agent_status_changes())

                # Broadcast updates
                asyncio.run(self._broadcast_update())

                time.sleep(30)  # Update every 30 seconds

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(5)

    async def _check_agent_status_changes(self):
        """Check for changes in agent status"""
        try:
            current_agents = await self._get_all_agents_status()

            for agent in current_agents:
                if agent.agent_id not in self.agent_status_cache:
                    # New agent or first check
                    self.agent_status_cache[agent.agent_id] = agent
                else:
                    # Check for status changes
                    cached = self.agent_status_cache[agent.agent_id]
                    if (cached.status != agent.status or
                        cached.current_mission != agent.current_mission):
                        logger.info(f"📊 Status change detected for {agent.agent_id}")
                        self.agent_status_cache[agent.agent_id] = agent

        except Exception as e:
            logger.error(f"Error checking agent status changes: {e}")

    def create_html_template(self):
        """Create the HTML template for the dashboard"""
        template_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SWARM Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
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
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            color: white;
        }

        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }

        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }

        .card {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }

        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 10px;
        }

        .agent-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 15px;
            border-left: 4px solid #28a745;
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
            font-size: 1.1rem;
            margin-bottom: 5px;
        }

        .agent-status {
            font-size: 0.9rem;
            color: #666;
        }

        .agent-mission {
            font-size: 0.8rem;
            color: #888;
            margin-top: 5px;
        }

        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }

        .metric {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }

        .metric-value {
            font-size: 2rem;
            font-weight: bold;
            color: #667eea;
        }

        .metric-label {
            font-size: 0.9rem;
            color: #666;
            margin-top: 5px;
        }

        .alert-list {
            max-height: 300px;
            overflow-y: auto;
        }

        .alert-item {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            background: #fff3cd;
            border-left: 4px solid #ffc107;
        }

        .alert-item.error {
            background: #f8d7da;
            border-left-color: #dc3545;
        }

        .alert-item.info {
            background: #d1ecf1;
            border-left-color: #17a2b8;
        }

        .alert-message {
            font-weight: bold;
        }

        .alert-time {
            font-size: 0.8rem;
            color: #666;
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

        .chart-container {
            position: relative;
            height: 300px;
            margin: 20px 0;
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            color: white;
            opacity: 0.8;
        }

        @media (max-width: 768px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }

            .header h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🐝 SWARM Monitoring Dashboard</h1>
            <p>Real-time monitoring for SWARM intelligence operations</p>
            <div id="last-update">Last updated: <span id="update-time">-</span></div>
        </div>

        <div class="dashboard-grid">
            <!-- Agent Status Card -->
            <div class="card">
                <h3>🤖 Agent Status</h3>
                <div id="agent-status" class="status-grid">
                    <div class="loading">Loading agent status...</div>
                </div>
            </div>

            <!-- System Metrics Card -->
            <div class="card">
                <h3>📊 System Metrics</h3>
                <div id="system-metrics" class="metrics-grid">
                    <div class="loading">Loading system metrics...</div>
                </div>
            </div>

            <!-- Consolidation Progress Card -->
            <div class="card">
                <h3>📈 Consolidation Progress</h3>
                <div class="progress-bar">
                    <div id="progress-fill" class="progress-fill" style="width: 0%"></div>
                </div>
                <div id="progress-text">0% Complete</div>
                <div id="consolidation-details" class="metrics-grid">
                    <div class="loading">Loading consolidation details...</div>
                </div>
            </div>

            <!-- Alerts Card -->
            <div class="card">
                <h3>🚨 Active Alerts</h3>
                <div id="alerts-list" class="alert-list">
                    <div class="loading">Loading alerts...</div>
                </div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="dashboard-grid">
            <div class="card">
                <h3>📊 Agent Activity Chart</h3>
                <div class="chart-container">
                    <canvas id="agent-activity-chart"></canvas>
                </div>
            </div>

            <div class="card">
                <h3>⚡ System Performance Chart</h3>
                <div class="chart-container">
                    <canvas id="system-performance-chart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>🐝 SWARM Intelligence Operations - Agent-7 Web Monitoring Interface</p>
        <p>Real-time monitoring for maximum coordination efficiency</p>
    </div>

    <script>
        // Global variables
        let agentActivityChart;
        let systemPerformanceChart;
        let lastUpdateTime = new Date();

        // Initialize charts
        function initializeCharts() {
            const agentCtx = document.getElementById('agent-activity-chart').getContext('2d');
            agentActivityChart = new Chart(agentCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Active', 'Idle', 'Offline'],
                    datasets: [{
                        data: [0, 0, 8],
                        backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });

            const systemCtx = document.getElementById('system-performance-chart').getContext('2d');
            systemPerformanceChart = new Chart(systemCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'CPU Usage (%)',
                        data: [],
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        tension: 0.4
                    }, {
                        label: 'Memory Usage (%)',
                        data: [],
                        borderColor: '#764ba2',
                        backgroundColor: 'rgba(118, 75, 162, 0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            max: 100
                        }
                    }
                }
            });
        }

        // Update agent status display
        function updateAgentStatus(agents) {
            const container = document.getElementById('agent-status');
            const activeCount = agents.filter(a => a.status !== 'OFFLINE').length;
            const idleCount = agents.filter(a => a.status === 'IDLE').length;
            const offlineCount = agents.filter(a => a.status === 'OFFLINE').length;

            // Update chart
            agentActivityChart.data.datasets[0].data = [activeCount, idleCount, offlineCount];
            agentActivityChart.update();

            // Update agent cards
            container.innerHTML = agents.map(agent => `
                <div class="agent-card ${agent.status.toLowerCase()}">
                    <div class="agent-id">${agent.agent_id}</div>
                    <div class="agent-status">Status: ${agent.status}</div>
                    ${agent.current_mission ? `<div class="agent-mission">${agent.current_mission.substring(0, 30)}...</div>` : ''}
                </div>
            `).join('');
        }

        // Update system metrics display
        function updateSystemMetrics(metrics) {
            const container = document.getElementById('system-metrics');

            if (metrics.error) {
                container.innerHTML = `<div class="metric">Error loading metrics: ${metrics.error}</div>`;
                return;
            }

            container.innerHTML = `
                <div class="metric">
                    <div class="metric-value">${metrics.cpu_usage.toFixed(1)}%</div>
                    <div class="metric-label">CPU Usage</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${metrics.memory_usage.toFixed(1)}%</div>
                    <div class="metric-label">Memory Usage</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${(metrics.memory_used / (1024**3)).toFixed(1)}GB</div>
                    <div class="metric-label">Memory Used</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${(metrics.disk_usage).toFixed(1)}%</div>
                    <div class="metric-label">Disk Usage</div>
                </div>
            `;

            // Update performance chart
            const now = new Date().toLocaleTimeString();
            if (systemPerformanceChart.data.labels.length > 10) {
                systemPerformanceChart.data.labels.shift();
                systemPerformanceChart.data.datasets[0].data.shift();
                systemPerformanceChart.data.datasets[1].data.shift();
            }
            systemPerformanceChart.data.labels.push(now);
            systemPerformanceChart.data.datasets[0].data.push(metrics.cpu_usage);
            systemPerformanceChart.data.datasets[1].data.push(metrics.memory_usage);
            systemPerformanceChart.update();
        }

        // Update consolidation progress
        function updateConsolidationProgress(progress) {
            const fill = document.getElementById('progress-fill');
            const text = document.getElementById('progress-text');
            const details = document.getElementById('consolidation-details');

            if (progress.error) {
                text.textContent = `Error: ${progress.error}`;
                return;
            }

            const percentage = progress.overall_progress.toFixed(1);
            fill.style.width = `${percentage}%`;
            text.textContent = `${percentage}% Complete - ${progress.active_agents}/8 Agents Active`;

            details.innerHTML = `
                <div class="metric">
                    <div class="metric-value">${progress.total_active_tasks}</div>
                    <div class="metric-label">Active Tasks</div>
                </div>
                <div class="metric">
                    <div class="metric-value">${progress.total_completed_tasks}</div>
                    <div class="metric-label">Completed Tasks</div>
                </div>
            `;
        }

        // Update alerts display
        function updateAlerts(alerts) {
            const container = document.getElementById('alerts-list');

            if (alerts.length === 0) {
                container.innerHTML = '<div class="alert-item info">No active alerts</div>';
                return;
            }

            container.innerHTML = alerts.map(alert => `
                <div class="alert-item ${alert.level.toLowerCase()}">
                    <div class="alert-message">${alert.message}</div>
                    <div class="alert-time">${new Date(alert.timestamp).toLocaleString()}</div>
                </div>
            `).join('');
        }

        // Update timestamp
        function updateTimestamp(timestamp) {
            const timeElement = document.getElementById('update-time');
            timeElement.textContent = new Date(timestamp).toLocaleString();
            lastUpdateTime = new Date(timestamp);
        }

        // WebSocket connection
        let websocket;

        function connectWebSocket() {
            websocket = new WebSocket('ws://localhost:8000/ws/updates');

            websocket.onopen = function(event) {
                console.log('WebSocket connected');
            };

            websocket.onmessage = function(event) {
                const data = JSON.parse(event.data);

                updateTimestamp(data.timestamp);
                updateAgentStatus(data.agents || []);
                updateSystemMetrics(data.system_metrics || {});
                updateConsolidationProgress(data.consolidation_progress || {});
                updateAlerts(data.active_alerts || []);
            };

            websocket.onclose = function(event) {
                console.log('WebSocket disconnected, reconnecting...');
                setTimeout(connectWebSocket, 5000);
            };

            websocket.onerror = function(error) {
                console.error('WebSocket error:', error);
            };
        }

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeCharts();
            connectWebSocket();
        });
    </script>
</body>
</html>
        """

        template_file = self.templates_dir / "dashboard.html"
        with open(template_file, 'w', encoding='utf-8') as f:
            f.write(template_content)

        logger.info(f"✅ HTML template created at {template_file}")

    def run(self, host: str = "0.0.0.0", port: int = 8000):
        """Run the dashboard server"""
        import uvicorn

        self.create_html_template()
        self.start_monitoring()

        logger.info(f"🚀 Starting SWARM Monitoring Dashboard on http://{host}:{port}")
        logger.info("🐝 Dashboard features:")
        logger.info("  - Real-time agent status monitoring")
        logger.info("  - System performance metrics")
        logger.info("  - Consolidation progress tracking")
        logger.info("  - Alert management")
        logger.info("  - WebSocket live updates")

        try:
            uvicorn.run(self.app, host=host, port=port)
        finally:
            self.stop_monitoring()


if __name__ == "__main__":
    dashboard = SwarmMonitoringDashboard()
    dashboard.run()
