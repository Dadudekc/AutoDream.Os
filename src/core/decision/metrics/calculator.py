from __future__ import annotations

"""Calculation helpers for decision metrics."""

from datetime import datetime
from typing import Any, Dict, List

from .definitions import DecisionMetrics


def update_metrics(metrics: DecisionMetrics, success: bool, execution_time: float, confidence: float) -> None:
    """Update metrics with a new decision result."""
    metrics.total_decisions += 1
    if success:
        metrics.successful_decisions += 1
    else:
        metrics.failed_decisions += 1

    metrics.total_execution_time += execution_time
    metrics.execution_time_history.append(execution_time)
    metrics.confidence_history.append(confidence)

    metrics.average_execution_time = metrics.total_execution_time / metrics.total_decisions
    metrics.average_confidence = sum(metrics.confidence_history) / len(metrics.confidence_history)
    metrics.last_updated = datetime.now()


def get_success_rate(metrics: DecisionMetrics) -> float:
    """Return current success rate."""
    if metrics.total_decisions == 0:
        return 0.0
    return metrics.successful_decisions / metrics.total_decisions


def get_performance_score(metrics: DecisionMetrics) -> float:
    """Calculate overall performance score."""
    success_rate = get_success_rate(metrics)
    time_score = max(0.0, 1.0 - (metrics.average_execution_time / 10.0))
    confidence_score = metrics.average_confidence
    return (success_rate * 0.4) + (time_score * 0.3) + (confidence_score * 0.3)


def check_alerts(metrics: DecisionMetrics) -> List[str]:
    """Check for performance alerts."""
    alerts: List[str] = []
    if get_success_rate(metrics) < metrics.success_rate_threshold:
        alerts.append(
            f"Success rate {get_success_rate(metrics):.2%} below threshold {metrics.success_rate_threshold:.2%}"
        )
    if metrics.average_execution_time > metrics.execution_time_threshold:
        alerts.append(
            f"Average execution time {metrics.average_execution_time:.2f}s above threshold {metrics.execution_time_threshold:.2f}s"
        )
    if metrics.average_confidence < metrics.confidence_threshold:
        alerts.append(
            f"Average confidence {metrics.average_confidence:.2f} below threshold {metrics.confidence_threshold:.2f}"
        )
    return alerts


def get_summary(metrics: DecisionMetrics) -> Dict[str, Any]:
    """Return a metrics summary."""
    return {
        "metrics_id": metrics.metrics_id,
        "decision_type": metrics.decision_type.value,
        "total_decisions": metrics.total_decisions,
        "successful_decisions": metrics.successful_decisions,
        "failed_decisions": metrics.failed_decisions,
        "success_rate": get_success_rate(metrics),
        "average_execution_time": metrics.average_execution_time,
        "average_confidence": metrics.average_confidence,
        "performance_score": get_performance_score(metrics),
        "alerts": check_alerts(metrics),
        "last_updated": metrics.last_updated.isoformat(),
        "current_value": metrics.current_value,
        "target_value": metrics.target_value,
        "unit": metrics.unit,
        "name": metrics.name,
        "description": metrics.description,
    }
