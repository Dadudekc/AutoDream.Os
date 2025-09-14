"""Data models for swarm monitoring dashboard."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AgentStatus(BaseModel):
    """Agent status model."""
    agent_id: str
    status: str
    current_phase: str
    last_updated: datetime
    current_mission: str | None = None
    mission_priority: str | None = None
    progress_percentage: float | None = None
    active_tasks: list[str] = []
    completed_tasks: list[str] = []
    coordination_status: dict[str, Any] = {}


class Alert(BaseModel):
    """Alert model."""
    alert_id: str
    level: str
    message: str
    component: str
    timestamp: datetime
    resolved: bool = False


class SystemMetrics(BaseModel):
    """System metrics model."""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: dict[str, int]
    timestamp: datetime


class ConsolidationProgress(BaseModel):
    """Consolidation progress model."""
    phase: str
    progress_percentage: float
    files_processed: int
    total_files: int
    estimated_completion: datetime | None = None
    current_task: str | None = None