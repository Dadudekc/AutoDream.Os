"""Common workflow metrics and results structures."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class OptimizationMetrics:
    """Metrics for measuring optimization improvements."""
    startup_time_reduction: float = 0.0
    message_throughput_improvement: float = 0.0
    coordination_latency_reduction: float = 0.0
    resource_utilization_improvement: float = 0.0
    batch_processing_efficiency: float = 0.0
    parallel_initialization_gain: float = 0.0


@dataclass
class WorkflowOptimizationResult:
    """Result of workflow optimization."""
    optimization_id: str
    timestamp: str
    original_metrics: Dict[str, Any]
    optimized_metrics: Dict[str, Any]
    improvement_percentage: float
    optimization_strategies_applied: List[str]
    quality_validation_passed: bool
    next_phase_ready: bool
