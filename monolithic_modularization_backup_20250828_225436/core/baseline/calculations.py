"""Measurement calculation utilities for baselines."""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from .data_handler import (
    BaselineComparison,
    BaselineMetric,
    PerformanceBaseline,
)


def compare_against_baseline(
    baseline: PerformanceBaseline, current_metrics: Dict[str, float]
) -> Optional[BaselineComparison]:
    """Compare current metrics against a baseline and return a comparison."""

    metric_comparisons: Dict[str, Dict[str, float]] = {}
    improvements = []
    regressions = []
    total_score = 0.0
    total_weight = 0.0

    for name, current_value in current_metrics.items():
        baseline_metric: BaselineMetric | None = baseline.metrics.get(name)
        if not baseline_metric:
            continue
        baseline_value = baseline_metric.value
        difference = current_value - baseline_value
        percentage_change = (
            (difference / baseline_value * 100) if baseline_value else 0.0
        )
        is_improvement = difference > 0
        score = (
            1.0
            if baseline_value and abs(percentage_change) <= 10
            else max(0.0, 1.0 - abs(percentage_change) / 100)
        )
        metric_comparisons[name] = {
            "baseline_value": baseline_value,
            "current_value": current_value,
            "difference": difference,
            "percentage_change": percentage_change,
            "score": score,
            "weight": baseline_metric.weight,
            "unit": baseline_metric.unit,
        }
        if is_improvement:
            improvements.append(name)
        else:
            regressions.append(name)
        total_score += score * baseline_metric.weight
        total_weight += baseline_metric.weight

    if total_weight == 0.0:
        return None

    overall_score = total_score / total_weight
    return BaselineComparison(
        baseline_id=baseline.baseline_id,
        comparison_timestamp=datetime.now(),
        overall_score=overall_score,
        metric_comparisons=metric_comparisons,
        improvements=improvements,
        regressions=regressions,
        recommendations=[],
        confidence_level="low",
    )


__all__ = ["compare_against_baseline"]
