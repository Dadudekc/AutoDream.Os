from datetime import datetime
from typing import Any, Dict, Iterable

from .constants import (
from .metrics import AgentMetrics
from dataclasses import dataclass, field

"""Health calculations for the status monitor service."""


    ERROR_PENALTY,
    WARNING_PENALTY,
    MIN_ACTIVE_AGENTS,
    LOW_ACTIVE_AGENT_PENALTY,
)


@dataclass
class SystemHealth:
    """Aggregated system health details."""

    total_agents: int
    active_agents: int = 0
    system_status: str = "initializing"
    overall_health_score: float = 100.0
    critical_issues: int = 0
    warnings: int = 0
    last_health_check: datetime = field(default_factory=datetime.now)


def assess_system_health(
    agent_metrics: Iterable[AgentMetrics], health: SystemHealth
) -> SystemHealth:
    """Update system health based on agent metrics."""
    active_agents = sum(1 for m in agent_metrics if m.status == "active")
    total_errors = sum(m.error_count for m in agent_metrics)
    total_warnings = sum(1 for m in agent_metrics if m.success_rate < 90.0)

    health_score = 100.0
    if total_errors:
        health_score -= total_errors * ERROR_PENALTY
    if total_warnings:
        health_score -= total_warnings * WARNING_PENALTY
    if active_agents < MIN_ACTIVE_AGENTS:
        health_score -= LOW_ACTIVE_AGENT_PENALTY
    health_score = max(0.0, health_score)

    if health_score >= 90:
        system_status = "healthy"
    elif health_score >= 70:
        system_status = "warning"
    elif health_score >= 50:
        system_status = "critical"
    else:
        system_status = "failing"

    health.active_agents = active_agents
    health.system_status = system_status
    health.overall_health_score = health_score
    health.critical_issues = total_errors
    health.warnings = total_warnings
    health.last_health_check = datetime.now()
    return health


def get_system_summary(
    agent_metrics: Dict[str, AgentMetrics], health: SystemHealth
) -> Dict[str, Any]:
    """Generate a full system summary."""
    agent_status_summary = {
        agent_id: {
            "status": m.status,
            "success_rate": m.success_rate,
            "error_count": m.error_count,
            "last_activity": m.last_activity.isoformat() if m.last_activity else None,
        }
        for agent_id, m in agent_metrics.items()
    }
    overall_metrics = {
        "total_coordinations": sum(
            m.coordination_count for m in agent_metrics.values()
        ),
        "total_errors": sum(m.error_count for m in agent_metrics.values()),
        "total_tasks": sum(
            m.tasks_completed + m.tasks_failed for m in agent_metrics.values()
        ),
        "average_success_rate": (
            sum(m.success_rate for m in agent_metrics.values()) / len(agent_metrics)
            if agent_metrics
            else 0.0
        ),
    }
    return {
        "system_health": {
            "status": health.system_status,
            "health_score": health.overall_health_score,
            "active_agents": health.active_agents,
            "total_agents": health.total_agents,
            "critical_issues": health.critical_issues,
            "warnings": health.warnings,
            "last_health_check": health.last_health_check.isoformat(),
        },
        "agent_status": agent_status_summary,
        "overall_metrics": overall_metrics,
    }
