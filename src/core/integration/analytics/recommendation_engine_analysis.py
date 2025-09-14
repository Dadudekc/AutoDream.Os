"""
Recommendation Engine Analysis - V2 Compliant Module
===================================================

Analysis functionality for optimization recommendation generation.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Any

from ..vector_integration_models import (
    OptimizationRecommendation,
    PerformanceMetrics,
    TrendAnalysis,
)


class RecommendationEngineAnalysis:
    """Analysis functionality for recommendation engine."""

    def __init__(self, base_engine, logger=None):
        """Initialize analysis with base engine reference."""
        self.base_engine = base_engine
        self.logger = logger or logging.getLogger(__name__)

    def _generate_metric_recommendations(
        self, metrics_data: list[PerformanceMetrics], trends: dict[str, TrendAnalysis]
    ) -> list[OptimizationRecommendation]:
        """Generate recommendations based on metric analysis."""
        recommendations = []

        try:
            # Calculate metric summaries
            metric_summaries = self._calculate_metric_summaries(metrics_data)

            # Analyze each metric for recommendations
            for metric_name, summary in metric_summaries.items():
                metric_recs = self._analyze_metric_for_recommendations(
                    metric_name, summary, trends.get(metric_name)
                )
                recommendations.extend(metric_recs)

            self.logger.info(f"Generated {len(recommendations)} metric-based recommendations")

        except Exception as e:
            self.logger.error(f"Error generating metric recommendations: {e}")

        return recommendations

    def _analyze_metric_for_recommendations(
        self, metric_name: str, summary: dict[str, Any], trend: TrendAnalysis | None
    ) -> list[OptimizationRecommendation]:
        """Analyze a specific metric for recommendations."""
        recommendations = []

        try:
            values = summary.get("values", [])
            if not values:
                return recommendations

            # Check for high volatility
            if self._is_highly_volatile(values):
                rec = self._create_metric_recommendation(
                    metric_name,
                    "stability",
                    f"High volatility detected in {metric_name}. Consider implementing smoothing or caching.",
                )
                recommendations.append(rec)

            # Check for performance issues
            avg_value = summary.get("average", 0)
            if avg_value > summary.get("threshold", 1000):  # Example threshold
                rec = self._create_metric_recommendation(
                    metric_name,
                    "performance",
                    f"High average value for {metric_name}. Consider optimization.",
                )
                recommendations.append(rec)

            # Check for trend-based recommendations
            if trend and trend.trend_direction == "increasing":
                rec = self._create_metric_recommendation(
                    metric_name,
                    "trend",
                    f"Increasing trend in {metric_name}. Monitor for potential issues.",
                )
                recommendations.append(rec)

        except Exception as e:
            self.logger.error(f"Error analyzing metric {metric_name}: {e}")

        return recommendations

    def _calculate_metric_summaries(
        self, metrics_data: list[PerformanceMetrics]
    ) -> dict[str, dict[str, Any]]:
        """Calculate summaries for all metrics."""
        summaries = {}

        try:
            # Group metrics by name
            metric_groups = {}
            for metric in metrics_data:
                name = metric.metric_name
                if name not in metric_groups:
                    metric_groups[name] = []
                metric_groups[name].append(metric.value)

            # Calculate summaries for each metric
            for metric_name, values in metric_groups.items():
                if values:
                    summaries[metric_name] = {
                        "values": values,
                        "average": sum(values) / len(values),
                        "min": min(values),
                        "max": max(values),
                        "count": len(values),
                        "threshold": 1000,  # Example threshold
                    }

        except Exception as e:
            self.logger.error(f"Error calculating metric summaries: {e}")

        return summaries

    def _is_highly_volatile(self, values: list[float]) -> bool:
        """Check if values are highly volatile."""
        if len(values) < 2:
            return False

        try:
            # Calculate coefficient of variation
            mean_val = sum(values) / len(values)
            if mean_val == 0:
                return False

            variance = sum((x - mean_val) ** 2 for x in values) / len(values)
            std_dev = variance**0.5
            cv = std_dev / mean_val

            # Consider highly volatile if CV > 0.5
            return cv > 0.5

        except Exception:
            return False
