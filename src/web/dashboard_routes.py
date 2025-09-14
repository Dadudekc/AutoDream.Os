#!/usr/bin/env python3
"""
Dashboard FastAPI Routes - V2 Compliant Module
=============================================

FastAPI routes for swarm monitoring dashboard.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Dashboard Modularization
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from .dashboard_models import (
    AgentStatus,
    Alert,
    ConsolidationProgress,
    DashboardData,
    DashboardConfig,
    SwarmMetrics
)

# Setup logging
logger = logging.getLogger(__name__)

# Setup templates
templates = Jinja2Templates(directory="src/web/templates")

# Create router
router = APIRouter()


class DashboardRoutes:
    """Dashboard routes handler."""

    def __init__(self):
        """Initialize dashboard routes."""
        self.logger = logger

    def get_agent_statuses(self) -> List[AgentStatus]:
        """Get agent statuses from status files."""
        try:
            agent_statuses = []
            for i in range(1, 9):  # Agent-1 to Agent-8
                agent_id = f"Agent-{i}"
                status_file = Path(f"agent_workspaces/{agent_id}/status.json")
                
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    agent_status = AgentStatus(
                        agent_id=agent_id,
                        status=status_data.get('status', 'unknown'),
                        last_updated=datetime.fromisoformat(
                            status_data.get('last_updated', datetime.now().isoformat())
                        ),
                        current_mission=status_data.get('current_mission'),
                        mission_status=status_data.get('mission_status'),
                        coordinates=status_data.get('coordinates'),
                        performance_metrics=status_data.get('performance_metrics')
                    )
                    agent_statuses.append(agent_status)
                else:
                    # Create default status for missing agents
                    agent_status = AgentStatus(
                        agent_id=agent_id,
                        status='offline',
                        last_updated=datetime.now()
                    )
                    agent_statuses.append(agent_status)
            
            return agent_statuses
            
        except Exception as e:
            self.logger.error(f"Error getting agent statuses: {e}")
            return []

    def get_swarm_metrics(self) -> SwarmMetrics:
        """Get swarm metrics."""
        try:
            agent_statuses = self.get_agent_statuses()
            active_agents = sum(1 for agent in agent_statuses if agent.status == 'active')
            
            return SwarmMetrics(
                total_agents=8,
                active_agents=active_agents,
                total_missions=100,  # Placeholder
                completed_missions=85,  # Placeholder
                active_missions=15,  # Placeholder
                performance_score=0.85,  # Placeholder
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error getting swarm metrics: {e}")
            return SwarmMetrics(
                total_agents=8,
                active_agents=0,
                total_missions=0,
                completed_missions=0,
                active_missions=0,
                performance_score=0.0,
                last_updated=datetime.now()
            )

    def get_consolidation_progress(self) -> ConsolidationProgress:
        """Get consolidation progress."""
        try:
            # Count files (simplified)
            total_files = 0
            active_files = 0
            
            for root, dirs, files in Path('.').rglob('*.py'):
                if '.git' not in str(root) and '__pycache__' not in str(root):
                    total_files += 1
                    if 'archive' not in str(root):
                        active_files += 1
            
            return ConsolidationProgress(
                total_files=total_files,
                active_files=active_files,
                archive_files=total_files - active_files,
                files_eliminated=50,  # Placeholder
                v2_violations=63,  # From previous analysis
                v2_compliant_files=active_files - 63,
                progress_percentage=0.75,  # Placeholder
                last_updated=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error getting consolidation progress: {e}")
            return ConsolidationProgress(
                total_files=0,
                active_files=0,
                archive_files=0,
                files_eliminated=0,
                v2_violations=0,
                v2_compliant_files=0,
                progress_percentage=0.0,
                last_updated=datetime.now()
            )

    def get_alerts(self) -> List[Alert]:
        """Get current alerts."""
        try:
            # Placeholder alerts
            alerts = [
                Alert(
                    alert_id="v2_violation_1",
                    type="V2_COMPLIANCE",
                    severity="HIGH",
                    message="63 files exceed 400 lines (V2 violation)",
                    timestamp=datetime.now(),
                    resolved=False
                ),
                Alert(
                    alert_id="print_statements_1",
                    type="CODE_QUALITY",
                    severity="MEDIUM",
                    message="107 files contain print statements",
                    timestamp=datetime.now(),
                    resolved=False
                )
            ]
            return alerts
            
        except Exception as e:
            self.logger.error(f"Error getting alerts: {e}")
            return []


# Create routes handler instance
dashboard_routes = DashboardRoutes()


@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Serve dashboard home page."""
    try:
        return templates.TemplateResponse("dashboard.html", {"request": request})
    except Exception as e:
        logger.error(f"Error serving dashboard: {e}")
        raise HTTPException(status_code=500, detail="Dashboard error")


@router.get("/api/status")
async def get_dashboard_status():
    """Get dashboard status."""
    try:
        return JSONResponse({
            "status": "active",
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0"
        })
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(status_code=500, detail="Status error")


@router.get("/api/data")
async def get_dashboard_data():
    """Get complete dashboard data."""
    try:
        data = DashboardData(
            swarm_metrics=dashboard_routes.get_swarm_metrics(),
            agent_statuses=dashboard_routes.get_agent_statuses(),
            consolidation_progress=dashboard_routes.get_consolidation_progress(),
            alerts=dashboard_routes.get_alerts(),
            last_updated=datetime.now()
        )
        return JSONResponse(data.dict())
    except Exception as e:
        logger.error(f"Error getting dashboard data: {e}")
        raise HTTPException(status_code=500, detail="Data error")


@router.get("/api/agents")
async def get_agents():
    """Get agent statuses."""
    try:
        agents = dashboard_routes.get_agent_statuses()
        return JSONResponse([agent.dict() for agent in agents])
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        raise HTTPException(status_code=500, detail="Agents error")


@router.get("/api/metrics")
async def get_metrics():
    """Get swarm metrics."""
    try:
        metrics = dashboard_routes.get_swarm_metrics()
        return JSONResponse(metrics.dict())
    except Exception as e:
        logger.error(f"Error getting metrics: {e}")
        raise HTTPException(status_code=500, detail="Metrics error")


@router.get("/api/consolidation")
async def get_consolidation():
    """Get consolidation progress."""
    try:
        progress = dashboard_routes.get_consolidation_progress()
        return JSONResponse(progress.dict())
    except Exception as e:
        logger.error(f"Error getting consolidation: {e}")
        raise HTTPException(status_code=500, detail="Consolidation error")


@router.get("/api/alerts")
async def get_alerts():
    """Get alerts."""
    try:
        alerts = dashboard_routes.get_alerts()
        return JSONResponse([alert.dict() for alert in alerts])
    except Exception as e:
        logger.error(f"Error getting alerts: {e}")
        raise HTTPException(status_code=500, detail="Alerts error")


# Export router
__all__ = ["router", "DashboardRoutes"]
