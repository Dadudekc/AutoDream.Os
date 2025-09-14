#!/usr/bin/env python3
"""
Swarm Monitoring Dashboard - V2 Compliant Orchestrator
====================================================

Main dashboard orchestrator for swarm monitoring.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Dashboard Modularization
License: MIT
"""

import asyncio
import logging
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .dashboard_routes import router as dashboard_router
from .dashboard_websocket import dashboard_websocket

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("swarm_dashboard.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


class SwarmDashboard:
    """Main swarm monitoring dashboard."""

    def __init__(self):
        """Initialize dashboard."""
        self.app = FastAPI(
            title="Swarm Monitoring Dashboard",
            description="Real-time monitoring for SWARM operations",
            version="2.0.0"
        )
        self.logger = logger
        self._setup_routes()
        self._setup_static_files()

    def _setup_routes(self) -> None:
        """Setup dashboard routes."""
        # Include dashboard routes
        self.app.include_router(dashboard_router, prefix="/dashboard")
        
        # WebSocket endpoint
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket):
            await dashboard_websocket.websocket_endpoint(websocket)

        # Health check
        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy",
                "service": "swarm_dashboard",
                "version": "2.0.0"
            }

    def _setup_static_files(self) -> None:
        """Setup static file serving."""
        try:
            # Mount static files if directory exists
            static_dir = Path("src/web/static")
            if static_dir.exists():
                self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
                self.logger.info("Static files mounted at /static")
            else:
                self.logger.warning("Static directory not found: src/web/static")
        except Exception as e:
            self.logger.error(f"Error setting up static files: {e}")

    async def start_broadcast_updates(self) -> None:
        """Start WebSocket broadcast updates."""
        try:
            await dashboard_websocket.start_broadcast_updates()
            self.logger.info("WebSocket broadcast updates started")
        except Exception as e:
            self.logger.error(f"Error starting broadcast updates: {e}")

    async def stop_broadcast_updates(self) -> None:
        """Stop WebSocket broadcast updates."""
        try:
            await dashboard_websocket.stop_broadcast_updates()
            self.logger.info("WebSocket broadcast updates stopped")
        except Exception as e:
            self.logger.error(f"Error stopping broadcast updates: {e}")

    def get_app(self) -> FastAPI:
        """Get FastAPI application."""
        return self.app

    def get_connection_count(self) -> int:
        """Get number of active WebSocket connections."""
        return dashboard_websocket.get_connection_count()


def create_dashboard() -> SwarmDashboard:
    """Create dashboard instance."""
    return SwarmDashboard()


async def main():
    """Main entry point for dashboard."""
    import uvicorn
    
    dashboard = create_dashboard()
    
    # Start broadcast updates
    await dashboard.start_broadcast_updates()
    
    try:
        # Run dashboard
        config = uvicorn.Config(
            app=dashboard.get_app(),
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    except KeyboardInterrupt:
        logger.info("Dashboard shutdown requested")
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
    finally:
        # Stop broadcast updates
        await dashboard.stop_broadcast_updates()
        logger.info("Dashboard shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Dashboard interrupted by user")
    except Exception as e:
        logger.error(f"Dashboard startup error: {e}")
        sys.exit(1)
