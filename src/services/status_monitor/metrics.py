"""Metric gathering utilities for the status monitor service."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

from .constants import DEFAULT_AGENT_IDS


@dataclass
class AgentMetrics:
    """Per-agent performance metrics."""

    agent_id: str
    status: str = "standby"
    last_activity: Optional[datetime] = None
    coordination_count: int = 0
    error_count: int = 0
    success_rate: float = 100.0
    response_time_avg: float = 0.0
    tasks_completed: int = 0
    tasks_failed: int = 0


class MetricsCollector:
    """Collect and update agent metrics."""

    def __init__(self) -> None:
        self.agent_metrics: Dict[str, AgentMetrics] = {
            agent_id: AgentMetrics(agent_id=agent_id) for agent_id in DEFAULT_AGENT_IDS
        }

    def update_agent_status(
        self, agent_id: str, status: str, activity_type: str = "coordination"
    ) -> None:
        """Update an agent's status and activity counts."""
        metrics = self.agent_metrics.get(agent_id)
        if not metrics:
            return
        metrics.status = status
        metrics.last_activity = datetime.now()
        if activity_type == "coordination":
            metrics.coordination_count += 1
        elif activity_type == "task_completion":
            metrics.tasks_completed += 1
        elif activity_type == "task_failure":
            metrics.tasks_failed += 1
        total_tasks = metrics.tasks_completed + metrics.tasks_failed
        if total_tasks:
            metrics.success_rate = (metrics.tasks_completed / total_tasks) * 100

    def record_agent_error(
        self, agent_id: str, error_message: str, log_dir: Path
    ) -> None:
        """Record an error for the given agent."""
        metrics = self.agent_metrics.get(agent_id)
        if not metrics:
            return
        metrics.error_count += 1
        log_dir.mkdir(exist_ok=True)
        with open(log_dir / f"{agent_id}_errors.log", "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {error_message}\n")

    def record_agent_response_time(self, agent_id: str, response_time: float) -> None:
        """Record response time for the given agent."""
        metrics = self.agent_metrics.get(agent_id)
        if not metrics:
            return
        if metrics.response_time_avg == 0.0:
            metrics.response_time_avg = response_time
        else:
            metrics.response_time_avg = (metrics.response_time_avg + response_time) / 2

    def get_agent_metrics(self, agent_id: str) -> Optional[Dict[str, object]]:
        """Return metrics for a specific agent as a dictionary."""
        metrics = self.agent_metrics.get(agent_id)
        if not metrics:
            return None
        return {
            "agent_id": metrics.agent_id,
            "status": metrics.status,
            "last_activity": (
                metrics.last_activity.isoformat() if metrics.last_activity else None
            ),
            "coordination_count": metrics.coordination_count,
            "error_count": metrics.error_count,
            "success_rate": metrics.success_rate,
            "response_time_avg": metrics.response_time_avg,
            "tasks_completed": metrics.tasks_completed,
            "tasks_failed": metrics.tasks_failed,
        }
