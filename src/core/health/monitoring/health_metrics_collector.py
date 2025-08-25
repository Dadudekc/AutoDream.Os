import logging
from datetime import datetime
from typing import Dict, Optional

from .health_monitoring_metrics import (
    HealthMetric,
    HealthMetricType,
    HealthSnapshot,
    HealthStatus,
)

logger = logging.getLogger(__name__)


class HealthMetricsCollector:
    """Collects and records health metrics for agents."""

    def __init__(self, health_data: Dict[str, HealthSnapshot]):
        self.health_data = health_data

    def collect_metrics(self) -> None:
        """Hook for external metric collection.

        In production this would gather metrics from running agents. The
        default implementation is a stub to keep the collector focused solely on
        recording duties.
        """

    def record_metric(
        self,
        agent_id: str,
        metric_type: HealthMetricType,
        value: float,
        unit: str,
        threshold: Optional[float] = None,
    ) -> None:
        """Record a health metric for an agent."""
        if agent_id not in self.health_data:
            self.health_data[agent_id] = HealthSnapshot(
                agent_id=agent_id,
                timestamp=datetime.now(),
                overall_status=HealthStatus.GOOD,
                health_score=100.0,
            )

        snapshot = self.health_data[agent_id]
        metric = HealthMetric(
            agent_id=agent_id,
            metric_type=metric_type,
            value=value,
            unit=unit,
            timestamp=datetime.now(),
            threshold=threshold,
        )
        snapshot.metrics[metric_type] = metric
        snapshot.timestamp = datetime.now()
        logger.debug(
            "Recorded metric %s for %s: %s%s",
            metric_type.value,
            agent_id,
            value,
            unit,
        )

    def get_agent_health(self, agent_id: str) -> Optional[HealthSnapshot]:
        """Retrieve health snapshot for a specific agent."""
        return self.health_data.get(agent_id)

    def get_all_health(self) -> Dict[str, HealthSnapshot]:
        """Return a copy of all health data."""
        return self.health_data.copy()
