#!/usr/bin/env python3
"""Tests for AgentHealthCoreMonitor health score calculation."""

from datetime import datetime
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from core.health.monitoring.health_monitoring_core import AgentHealthCoreMonitor
from core.health.monitoring.health_monitoring_metrics import (
    HealthMetric,
    HealthMetricType,
    HealthSnapshot,
    HealthStatus,
)


def test_calculate_health_score_no_counted_metrics():
    """When metrics exist but lack thresholds, default score is returned."""
    monitor = AgentHealthCoreMonitor()
    monitor.thresholds = {}

    metric = HealthMetric(
        agent_id="agent",
        metric_type=HealthMetricType.RESPONSE_TIME,
        value=500.0,
        unit="ms",
        timestamp=datetime.now(),
    )
    snapshot = HealthSnapshot(
        agent_id="agent",
        timestamp=datetime.now(),
        overall_status=HealthStatus.GOOD,
        health_score=0.0,
        metrics={HealthMetricType.RESPONSE_TIME: metric},
        alerts=[],
    )

    score = monitor._calculate_health_score(snapshot)
    assert score == 100.0
