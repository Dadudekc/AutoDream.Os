"""Refactored Swarm Monitoring Dashboard - V2 Compliant Version

This is a modular, V2-compliant version of the swarm monitoring dashboard
that breaks down the original 989-line file into focused modules.

Author: Agent-7 (Web Development Specialist)
V2 Compliance: < 300 lines, modular design, single responsibility
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .swarm import SwarmDataService

logger = logging.getLogger(__name__)


class SwarmMonitoringDashboard:
    """
    V2-compliant web monitoring dashboard for SWARM operations.
    
    This dashboard provides real-time visualization of:
    - Agent status and coordination
    - System performance metrics
    - Consolidation progress tracking
    - Alert management
    """

    def __init__(self):
        """Initialize the swarm monitoring dashboard."""
        self.app = FastAPI(
            title="SWARM Monitoring Dashboard",
            description="Real-time monitoring dashboard for SWARM intelligence operations",
            version="2.0.0"
        )
        
        # Setup paths
        self.project_root = Path(__file__).parent.parent.parent
        self.templates_dir = self.project_root / "src" / "web" / "templates"
        self.static_dir = self.project_root / "src" / "web" / "static"
        
        # Initialize data service
        self.data_service = SwarmDataService(self.project_root)
        
        # WebSocket connections
        self.active_connections: list[WebSocket] = []
        
        # Setup routes
        self._setup_routes()
        self._setup_static_files()

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_home(request: Request):
            """Main dashboard page."""
            try:
                templates = Jinja2Templates(directory=str(self.templates_dir))
                return templates.TemplateResponse("swarm_dashboard.html", {
                    "request": request,
                    "title": "SWARM Monitoring Dashboard"
                })
            except Exception as e:
                logger.error(f"Error rendering dashboard: {e}")
                return HTMLResponse("<h1>SWARM Dashboard</h1><p>Dashboard loading...</p>")

        @self.app.get("/api/status")
        async def get_status():
            """Get overall system status."""
            try:
                return self.data_service.get_dashboard_summary()
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                raise HTTPException(status_code=500, detail="Error retrieving status")

        @self.app.get("/api/agents")
        async def get_agents():
            """Get agent statuses."""
            try:
                return self.data_service.get_agent_statuses()
            except Exception as e:
                logger.error(f"Error getting agents: {e}")
                raise HTTPException(status_code=500, detail="Error retrieving agents")

        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get system metrics."""
            try:
                return self.data_service.get_system_metrics()
            except Exception as e:
                logger.error(f"Error getting metrics: {e}")
                raise HTTPException(status_code=500, detail="Error retrieving metrics")

        @self.app.get("/api/alerts")
        async def get_alerts():
            """Get current alerts."""
            try:
                return self.data_service.get_alerts()
            except Exception as e:
                logger.error(f"Error getting alerts: {e}")
                raise HTTPException(status_code=500, detail="Error retrieving alerts")

        @self.app.post("/api/alerts/{alert_id}/resolve")
        async def resolve_alert(alert_id: str):
            """Resolve an alert."""
            try:
                success = self.data_service.resolve_alert(alert_id)
                if success:
                    await self._broadcast_update("alert_resolved", {"alert_id": alert_id})
                    return {"message": "Alert resolved successfully"}
                else:
                    raise HTTPException(status_code=404, detail="Alert not found")
            except Exception as e:
                logger.error(f"Error resolving alert: {e}")
                raise HTTPException(status_code=500, detail="Error resolving alert")

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            """WebSocket endpoint for real-time updates."""
            await websocket.accept()
            self.active_connections.append(websocket)
            
            try:
                while True:
                    # Keep connection alive and send periodic updates
                    await websocket.receive_text()
                    await self._send_dashboard_update(websocket)
            except WebSocketDisconnect:
                self.active_connections.remove(websocket)
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                if websocket in self.active_connections:
                    self.active_connections.remove(websocket)

    def _setup_static_files(self) -> None:
        """Setup static file serving."""
        if self.static_dir.exists():
            self.app.mount("/static", StaticFiles(directory=str(self.static_dir)), name="static")

    async def _send_dashboard_update(self, websocket: WebSocket) -> None:
        """Send dashboard update via WebSocket."""
        try:
            summary = self.data_service.get_dashboard_summary()
            await websocket.send_text(json.dumps({
                "type": "dashboard_update",
                "data": summary
            }))
        except Exception as e:
            logger.error(f"Error sending WebSocket update: {e}")

    async def _broadcast_update(self, update_type: str, data: dict[str, Any]) -> None:
        """Broadcast update to all connected WebSocket clients."""
        if not self.active_connections:
            return
        
        message = json.dumps({
            "type": update_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })
        
        disconnected = []
        for websocket in self.active_connections:
            try:
                await websocket.send_text(message)
            except Exception as e:
                logger.error(f"Error broadcasting to WebSocket: {e}")
                disconnected.append(websocket)
        
        # Remove disconnected clients
        for websocket in disconnected:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)

    def get_app(self) -> FastAPI:
        """Get the FastAPI application instance."""
        return self.app

    def add_test_alert(self) -> None:
        """Add a test alert for demonstration."""
        self.data_service.add_alert(
            level="info",
            message="Test alert from refactored dashboard",
            component="swarm_monitoring"
        )

    def get_connection_count(self) -> int:
        """Get the number of active WebSocket connections."""
        return len(self.active_connections)


# Factory function for creating the dashboard
def create_swarm_dashboard() -> SwarmMonitoringDashboard:
    """Create and return a new swarm monitoring dashboard instance."""
    return SwarmMonitoringDashboard()


# Main entry point for running the dashboard
if __name__ == "__main__":
    import uvicorn
    
    dashboard = create_swarm_dashboard()
    app = dashboard.get_app()
    
    # Add a test alert
    dashboard.add_test_alert()
    
    print("🐝 Starting SWARM Monitoring Dashboard...")
    print(f"📊 Dashboard will be available at: http://localhost:8000")
    print(f"🔌 WebSocket endpoint: ws://localhost:8000/ws")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")