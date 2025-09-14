"""
Recommendation Engine System - V2 Compliant Module
=================================================

System-wide recommendation functionality for optimization.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import logging
from typing import Any

from ..vector_integration_models import (
    OptimizationRecommendation,
    PerformanceMetrics,
    create_optimization_recommendation,
)


class RecommendationEngineSystem:
    """System-wide recommendation functionality."""

    def __init__(self, base_engine, logger=None):
        """Initialize system recommendations with base engine reference."""
        self.base_engine = base_engine
        self.logger = logger or logging.getLogger(__name__)

    def _generate_system_recommendations(
        self, metrics_data: list[PerformanceMetrics]
    ) -> list[OptimizationRecommendation]:
        """Generate system-wide optimization recommendations."""
        recommendations = []

        try:
            # Calculate overall system metrics
            metric_summaries = self._calculate_metric_summaries(metrics_data)

            # Check for resource optimization opportunities
            resource_rec = self._check_resource_optimization(metric_summaries)
            if resource_rec:
                recommendations.append(resource_rec)

            # Check for performance optimization opportunities
            perf_rec = self._check_performance_optimization(metric_summaries)
            if perf_rec:
                recommendations.append(perf_rec)

            # Check for scalability recommendations
            scale_rec = self._check_scalability_optimization(metric_summaries)
            if scale_rec:
                recommendations.append(scale_rec)

            self.logger.info(f"Generated {len(recommendations)} system-wide recommendations")

        except Exception as e:
            self.logger.error(f"Error generating system recommendations: {e}")

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
                    }

        except Exception as e:
            self.logger.error(f"Error calculating metric summaries: {e}")

        return summaries

    def _check_resource_optimization(
        self, metric_summaries: dict[str, dict[str, Any]]
    ) -> OptimizationRecommendation | None:
        """Check for resource optimization opportunities."""
        try:
            # Look for high memory usage
            memory_metrics = [name for name in metric_summaries.keys() if "memory" in name.lower()]
            if memory_metrics:
                for metric_name in memory_metrics:
                    avg_value = metric_summaries[metric_name].get("average", 0)
                    if avg_value > 1000:  # Example threshold
                        return self._create_metric_recommendation(
                            metric_name,
                            "resource",
                            f"High memory usage detected in {metric_name}. Consider memory optimization.",
                        )

            # Look for high CPU usage
            cpu_metrics = [name for name in metric_summaries.keys() if "cpu" in name.lower()]
            if cpu_metrics:
                for metric_name in cpu_metrics:
                    avg_value = metric_summaries[metric_name].get("average", 0)
                    if avg_value > 80:  # Example threshold
                        return self._create_metric_recommendation(
                            metric_name,
                            "resource",
                            f"High CPU usage detected in {metric_name}. Consider CPU optimization.",
                        )

        except Exception as e:
            self.logger.error(f"Error checking resource optimization: {e}")

        return None

    def _check_performance_optimization(
        self, metric_summaries: dict[str, dict[str, Any]]
    ) -> OptimizationRecommendation | None:
        """Check for performance optimization opportunities."""
        try:
            # Look for slow response times
            response_metrics = [
                name
                for name in metric_summaries.keys()
                if "response" in name.lower() or "latency" in name.lower()
            ]
            if response_metrics:
                for metric_name in response_metrics:
                    avg_value = metric_summaries[metric_name].get("average", 0)
                    if avg_value > 1000:  # Example threshold (1 second)
                        return self._create_metric_recommendation(
                            metric_name,
                            "performance",
                            f"Slow response time detected in {metric_name}. Consider performance optimization.",
                        )

        except Exception as e:
            self.logger.error(f"Error checking performance optimization: {e}")

        return None

    def _check_scalability_optimization(
        self, metric_summaries: dict[str, dict[str, Any]]
    ) -> OptimizationRecommendation | None:
        """Check for scalability optimization opportunities."""
        try:
            # Look for throughput metrics
            throughput_metrics = [
                name for name in metric_summaries.keys() if "throughput" in name.lower()
            ]
            if throughput_metrics:
                for metric_name in throughput_metrics:
                    avg_value = metric_summaries[metric_name].get("average", 0)
                    if avg_value < 100:  # Example threshold
                        return self._create_metric_recommendation(
                            metric_name,
                            "scalability",
                            f"Low throughput detected in {metric_name}. Consider scalability improvements.",
                        )

        except Exception as e:
            self.logger.error(f"Error checking scalability optimization: {e}")

        return None

    def _create_metric_recommendation(
        self, metric_name: str, rec_type: str = "performance", description: str = ""
    ) -> OptimizationRecommendation:
        """Create a metric-based recommendation."""
        return create_optimization_recommendation(
            title=f"{rec_type.title()} optimization for {metric_name}",
            description=description,
            category=rec_type,
            priority="medium",
            impact="medium",
        )
