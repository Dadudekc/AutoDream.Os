from __future__ import annotations

"""Data aggregation utilities for UnifiedFinancialAPI."""

from typing import Any, Dict


class DataAggregator:
    """Aggregates metrics across agents and requests."""

    def aggregate_system_health(
        self,
        registered_agents: Dict[str, Any],
        performance_metrics: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Compute system-wide health metrics."""
        total_agents = len(registered_agents)
        active_agents = sum(
            1 for agent in registered_agents.values() if agent.status == "ACTIVE"
        )

        total_requests = sum(
            metrics.get("total_requests", 0) for metrics in performance_metrics.values()
        )
        successful_requests = sum(
            metrics.get("successful_requests", 0)
            for metrics in performance_metrics.values()
        )
        failed_requests = sum(
            metrics.get("failed_requests", 0)
            for metrics in performance_metrics.values()
        )

        response_times = [
            metrics.get("average_response_time", 0.0)
            for metrics in performance_metrics.values()
            if metrics.get("average_response_time", 0.0) > 0
        ]
        average_response_time = (
            sum(response_times) / len(response_times) if response_times else 0.0
        )

        system_uptime = 99.9  # Placeholder for actual uptime calculation

        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "average_response_time": average_response_time,
            "system_uptime": system_uptime,
        }
