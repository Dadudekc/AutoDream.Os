#!/usr/bin/env python3
"""
Dashboard Models - Data Models for Swarm Monitoring Dashboard
===========================================================

Data models and schemas for the swarm monitoring dashboard.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel


class AgentStatus(BaseModel):
    """Agent status model."""

    agent_id: str
    status: str
    last_activity: datetime
    coordinates: dict[str, int] | None = None
    performance_metrics: dict[str, Any] | None = None


class SystemMetrics(BaseModel):
    """System metrics model."""

    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_io: dict[str, int]
    timestamp: datetime


class SwarmMetrics(BaseModel):
    """Swarm metrics model."""

    total_agents: int
    active_agents: int
    total_messages: int
    coordination_efficiency: float
    system_health: str
    timestamp: datetime


class DashboardData(BaseModel):
    """Complete dashboard data model."""

    agents: list[AgentStatus]
    system_metrics: SystemMetrics
    swarm_metrics: SwarmMetrics
    last_updated: datetime

