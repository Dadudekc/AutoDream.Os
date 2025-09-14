#!/usr/bin/env python3
"""
Analytics Dashboard Web Interface - V2 Compliant
===============================================

Interactive web dashboard for advanced analytics and reporting system.
V2 COMPLIANT: Under 300 lines, single responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
from pathlib import Path

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.advanced_analytics_service import get_analytics_service
from .shared.dashboard_utilities import get_dashboard_utilities, get_system_metrics

logger = logging.getLogger(__name__)


class AnalyticsDashboardWeb:
    """Web interface for analytics dashboard."""

    def __init__(self):
        self.app = FastAPI(title="Advanced Analytics Dashboard", version="1.0.0")
        self.analytics_service = get_analytics_service()
        self.dashboard_utils = get_dashboard_utilities()
        self.templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

        # Mount static files
        static_path = Path(__file__).parent / "static"
        static_path.mkdir(exist_ok=True)
        self.app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

        self._setup_routes()

    def _setup_routes(self) -> None:
        """Setup FastAPI routes."""

        @self.app.get("/", response_class=HTMLResponse)
        async def dashboard_overview(request: Request):
            """Main dashboard overview page."""
            return self.templates.TemplateResponse(
                "dashboard.html", {"request": request, "title": "Analytics Dashboard"}
            )

        @self.app.get("/api/metrics")
        async def get_metrics():
            """Get system metrics."""
            try:
                metrics = get_system_metrics()
                return JSONResponse(content=metrics)
            except Exception as e:
                logger.error(f"Failed to get metrics: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/reports/{report_type}")
        async def get_report(report_type: str):
            """Get analytics report."""
            try:
                report = self.analytics_service.generate_report(report_type)
                return JSONResponse(content=report)
            except Exception as e:
                logger.error(f"Failed to generate report: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/dashboard/{dashboard_type}")
        async def get_dashboard_data(dashboard_type: str):
            """Get dashboard data."""
            try:
                data = self.analytics_service.get_dashboard_data(dashboard_type)
                return JSONResponse(content=data)
            except Exception as e:
                logger.error(f"Failed to get dashboard data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.app.get("/api/charts/{chart_type}")
        async def get_chart_data(chart_type: str):
            """Get chart data."""
            try:
                # Sample data for demonstration
                sample_data = [
                    {"label": "CPU", "value": 45.2},
                    {"label": "Memory", "value": 67.8},
                    {"label": "Disk", "value": 23.1}
                ]
                
                chart_data = self.dashboard_utils.generate_chart_data(sample_data, chart_type)
                return JSONResponse(content=chart_data)
            except Exception as e:
                logger.error(f"Failed to generate chart data: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    def run(self, host: str = "0.0.0.0", port: int = 8001):
        """Run the analytics dashboard server."""
        try:
            logger.info(f"Starting Analytics Dashboard on {host}:{port}")
            uvicorn.run(self.app, host=host, port=port)
        except Exception as e:
            logger.error(f"Failed to start dashboard: {e}")
            raise


def create_analytics_dashboard() -> AnalyticsDashboardWeb:
    """Factory function to create analytics dashboard."""
    return AnalyticsDashboardWeb()


def main():
    """Main entry point for running the analytics dashboard."""
    dashboard = create_analytics_dashboard()
    dashboard.run()


if __name__ == "__main__":
    main()

