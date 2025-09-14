#!/usr/bin/env python3
"""
Dashboard Data Models - V2 Compliant Module
==========================================

Data models for swarm monitoring dashboard.
V2 Compliance: < 400 lines, single responsibility.

Author: Agent-3 (Infrastructure & DevOps Specialist)
Mission: V2 Compliance - Dashboard Modularization
License: MIT
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class AgentStatus(BaseModel):
    """Agent status model."""
    agent_id: str
    status: str
    last_updated: datetime
    current_mission: Optional[str] = None
    mission_status: Optional[str] = None
    coordinates: Optional[Dict[str, int]] = None
    performance_metrics: Optional[Dict[str, Any]] = None


class SwarmMetrics(BaseModel):
    """Swarm metrics model."""
    total_agents: int
    active_agents: int
    total_missions: int
    completed_missions: int
    active_missions: int
    performance_score: float
    last_updated: datetime


class ConsolidationProgress(BaseModel):
    """Consolidation progress model."""
    total_files: int
    active_files: int
    archive_files: int
    files_eliminated: int
    v2_violations: int
    v2_compliant_files: int
    progress_percentage: float
    last_updated: datetime


class Alert(BaseModel):
    """Alert model."""
    alert_id: str
    type: str
    severity: str
    message: str
    timestamp: datetime
    agent_id: Optional[str] = None
    resolved: bool = False


class DashboardData(BaseModel):
    """Complete dashboard data model."""
    swarm_metrics: SwarmMetrics
    agent_statuses: List[AgentStatus]
    consolidation_progress: ConsolidationProgress
    alerts: List[Alert]
    last_updated: datetime


class WebSocketMessage(BaseModel):
    """WebSocket message model."""
    type: str
    data: Dict[str, Any]
    timestamp: datetime


class DashboardConfig(BaseModel):
    """Dashboard configuration model."""
    refresh_interval: int = 5
    max_alerts: int = 100
    performance_threshold: float = 0.8
    auto_refresh: bool = True
    debug_mode: bool = False


# Export all models
__all__ = [
    "AgentStatus",
    "SwarmMetrics", 
    "ConsolidationProgress",
    "Alert",
    "DashboardData",
    "WebSocketMessage",
    "DashboardConfig"
]
