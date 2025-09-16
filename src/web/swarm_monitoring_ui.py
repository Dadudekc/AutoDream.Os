#!/usr/bin/env python3
"""
Swarm Monitoring UI - Web interface components
==============================================

Web UI components extracted from swarm_monitoring_dashboard.py
V2 compliant: ≤400 lines, focused responsibility
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .swarm_monitoring_core import SwarmMonitoringCore

logger = logging.getLogger(__name__)


class WebSocketManager:
    """WebSocket connection manager."""

    def __init__(self):
        """Initialize WebSocket manager."""
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        """Accept WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"WebSocket connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove WebSocket connection."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, data: dict[str, Any]) -> None:
        """Broadcast data to all connected clients."""
        if not self.active_connections:
            return

        message = json.dumps(data, default=str)
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                logger.error(f"Failed to send WebSocket message: {e}")
                disconnected.append(connection)

        # Remove disconnected connections
        for connection in disconnected:
            self.disconnect(connection)


class SwarmMonitoringUI:
    """Swarm monitoring web interface."""

    def __init__(self, core: SwarmMonitoringCore):
        """Initialize monitoring UI."""
        self.core = core
        self.app = FastAPI(title="Swarm Monitoring Dashboard")
        self.websocket_manager = WebSocketManager()
        self.templates = Jinja2Templates(directory="templates")

        self._setup_routes()
        self._start_background_tasks()

        logger.info("Swarm monitoring UI initialized")

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard(request: Request):
            """Main dashboard page."""
            return self.templates.TemplateResponse(
                "dashboard.html", {"request": request, "title": "Swarm Monitoring Dashboard"}
            )

        @self.app.get("/api/agents")
        async def get_agents():
            """Get all agents status."""
            return {"agents": [agent.dict() for agent in self.core.agents.values()]}

        @self.app.get("/api/agents/{agent_id}")
        async def get_agent(agent_id: str):
            """Get specific agent status."""
            if agent_id not in self.core.agents:
                raise HTTPException(status_code=404, detail="Agent not found")
            return self.core.agents[agent_id].dict()

        @self.app.post("/api/agents/{agent_id}/status")
        async def update_agent_status(agent_id: str, status_data: dict[str, Any]):
            """Update agent status."""
            success = self.core.update_agent_status(agent_id, status_data)
            if success:
                await self._broadcast_update(
                    "agent_status", {"agent_id": agent_id, "status": status_data}
                )
                return {"success": True}
            else:
                raise HTTPException(status_code=500, detail="Failed to update status")

        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get system metrics."""
            return self.core.get_metrics_summary()

        @self.app.get("/api/metrics/history")
        async def get_metrics_history():
            """Get metrics history."""
            return {"metrics": [metric.dict() for metric in self.core.metrics_history[-100:]]}

        @self.app.get("/api/alerts")
        async def get_alerts():
            """Get all alerts."""
            return {"alerts": [alert.dict() for alert in self.core.alerts]}

        @self.app.get("/api/alerts/active")
        async def get_active_alerts():
            """Get active alerts."""
            return {"alerts": [alert.dict() for alert in self.core.get_active_alerts()]}

        @self.app.post("/api/alerts/{alert_id}/resolve")
        async def resolve_alert(alert_id: str):
            """Resolve alert."""
            success = self.core.resolve_alert(alert_id)
            if success:
                await self._broadcast_update("alert_resolved", {"alert_id": alert_id})
                return {"success": True}
            else:
                raise HTTPException(status_code=404, detail="Alert not found")

        @self.app.get("/api/summary")
        async def get_summary():
            """Get system summary."""
            return {
                "agents": self.core.get_agent_summary(),
                "metrics": self.core.get_metrics_summary(),
                "health": self.core.get_health_status(),
                "alerts": {
                    "total": len(self.core.alerts),
                    "active": len(self.core.get_active_alerts()),
                },
            }

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await self.websocket_manager.connect(websocket)
            try:
                while True:
                    # Keep connection alive
                    await websocket.receive_text()
            except WebSocketDisconnect:
                self.websocket_manager.disconnect(websocket)

    async def _broadcast_update(self, update_type: str, data: dict[str, Any]) -> None:
        """Broadcast update to all connected clients."""
        message = {"type": update_type, "timestamp": datetime.now().isoformat(), "data": data}
        await self.websocket_manager.broadcast(message)

    def _start_background_tasks(self) -> None:
        """Start background monitoring tasks."""

        @self.app.on_event("startup")
        async def startup_event():
            """Start background tasks on startup."""
            asyncio.create_task(self._metrics_collector())
            asyncio.create_task(self._health_monitor())
            logger.info("Background tasks started")

        @self.app.on_event("shutdown")
        async def shutdown_event():
            """Cleanup on shutdown."""
            logger.info("Shutting down monitoring UI")

    async def _metrics_collector(self) -> None:
        """Background metrics collection."""
        while True:
            try:
                metrics = self.core.get_system_metrics()
                await self._broadcast_update("metrics", metrics.dict())
                await asyncio.sleep(5)  # Collect every 5 seconds
            except Exception as e:
                logger.error(f"Metrics collection error: {e}")
                await asyncio.sleep(10)

    async def _health_monitor(self) -> None:
        """Background health monitoring."""
        while True:
            try:
                health = self.core.get_health_status()

                # Create alerts for health issues
                if health["status"] == "critical":
                    self.core.create_alert(
                        "critical",
                        f"System health critical: {health['health_score']}%",
                        "health_monitor",
                    )
                elif health["status"] == "degraded":
                    self.core.create_alert(
                        "warning",
                        f"System health degraded: {health['health_score']}%",
                        "health_monitor",
                    )

                await self._broadcast_update("health", health)
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Health monitoring error: {e}")
                await asyncio.sleep(60)

    def get_app(self) -> FastAPI:
        """Get FastAPI application."""
        return self.app


def create_monitoring_app(workspace_path: str = "agent_workspaces") -> FastAPI:
    """Create monitoring application."""
    core = SwarmMonitoringCore(workspace_path)
    ui = SwarmMonitoringUI(core)
    return ui.get_app()


if __name__ == "__main__":
    import uvicorn

    app = create_monitoring_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
