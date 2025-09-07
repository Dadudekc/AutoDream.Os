from __future__ import annotations

"""Metric data structures for decision tracking."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

from ..decision_types import DecisionType


@dataclass
class DecisionMetrics:
    """Centralized decision performance metrics."""

    metrics_id: str
    decision_type: DecisionType
    name: str = ""
    description: str = ""
    current_value: float = 0.0
    target_value: float = 0.0
    unit: str = ""
    is_active: bool = True
    total_decisions: int = 0
    successful_decisions: int = 0
    failed_decisions: int = 0
    average_confidence: float = 0.0
    average_execution_time: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)
    total_execution_time: float = 0.0
    confidence_history: List[float] = field(default_factory=list)
    execution_time_history: List[float] = field(default_factory=list)
    success_rate_threshold: float = 0.8
    execution_time_threshold: float = 5.0
    confidence_threshold: float = 0.7


@dataclass
class MetricsSnapshot:
    """Snapshot of decision metrics at a point in time."""

    snapshot_id: str
    timestamp: str
    total_decisions: int
    successful_decisions: int
    failed_decisions: int
    average_decision_time: float
    success_rate: float
    performance_score: float
    metrics_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PerformanceAlert:
    """Performance alert for decision metrics."""

    alert_id: str
    alert_type: str
    severity: str
    message: str
    threshold_value: float
    current_value: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    acknowledged: bool = False
    resolved: bool = False
