#!/usr/bin/env python3
"""
Usage Analytics Engine - V2 Compliant Module
===========================================

Advanced usage analytics and behavioral insights engine for business intelligence.
V2 COMPLIANT: Under 300 lines, focused responsibility.

Author: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

import logging
import statistics
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List

from .metrics_collector import MetricDataPoint, MetricsCollector

logger = logging.getLogger(__name__)


class UsageAnalyticsEngine:
    """Advanced usage analytics and behavioral insights engine."""

    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.user_sessions = defaultdict(list)
        self.feature_usage = defaultdict(int)
        self.error_patterns = defaultdict(int)
        self.performance_patterns = defaultdict(list)

    def analyze_agent_usage(self, agent_id: str, hours_back: int = 24) -> Dict[str, Any]:

EXAMPLE USAGE:
==============

# Import the service
from src.services.analytics.usage_analytics import Usage_AnalyticsService

# Initialize service
service = Usage_AnalyticsService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Usage_AnalyticsService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

        """Analyze usage patterns for a specific agent."""
        # Get agent activity metrics
        activity_data = self.metrics_collector.get_metric_data(f"agent.{agent_id}.activity", hours_back)
        task_data = self.metrics_collector.get_metric_data(f"agent.{agent_id}.tasks_completed", hours_back)
        error_data = self.metrics_collector.get_metric_data(f"agent.{agent_id}.errors", hours_back)

        # Calculate usage metrics
        total_activity = len(activity_data)
        total_tasks = sum(dp.value for dp in task_data if isinstance(dp.value, (int, float)))
        total_errors = sum(dp.value for dp in error_data if isinstance(dp.value, (int, float)))

        # Calculate efficiency metrics
        efficiency = total_tasks / max(total_activity, 1)
        error_rate = total_errors / max(total_tasks, 1)

        # Analyze patterns
        peak_hours = self._find_peak_usage_hours(activity_data)
        task_completion_trend = self._analyze_task_completion_trend(task_data)

        return {
            "agent_id": agent_id,
            "analysis_period_hours": hours_back,
            "usage_metrics": {
                "total_activities": total_activity,
                "tasks_completed": total_tasks,
                "errors_encountered": total_errors,
                "efficiency_ratio": efficiency,
                "error_rate": error_rate
            },
            "patterns": {
                "peak_usage_hours": peak_hours,
                "task_completion_trend": task_completion_trend,
                "activity_distribution": self._calculate_activity_distribution(activity_data)
            },
            "insights": self._generate_usage_insights(agent_id, efficiency, error_rate, peak_hours)
        }

    def analyze_system_usage(self, hours_back: int = 24) -> Dict[str, Any]:
        """Analyze overall system usage patterns."""
        # Get system-wide metrics
        all_agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        agent_analyses = {}

        total_system_activity = 0
        total_system_tasks = 0
        total_system_errors = 0

        for agent_id in all_agents:
            agent_analysis = self.analyze_agent_usage(agent_id, hours_back)
            agent_analyses[agent_id] = agent_analysis

            # Aggregate system metrics
            metrics = agent_analysis["usage_metrics"]
            total_system_activity += metrics["total_activities"]
            total_system_tasks += metrics["tasks_completed"]
            total_system_errors += metrics["errors_encountered"]

        # Calculate system efficiency
        system_efficiency = total_system_tasks / max(total_system_activity, 1)
        system_error_rate = total_system_errors / max(total_system_tasks, 1)

        # Identify most active agents
        most_active = sorted(
            agent_analyses.items(),
            key=lambda x: x[1]["usage_metrics"]["total_activities"],
            reverse=True
        )[:3]

        # Identify highest efficiency agents
        most_efficient = sorted(
            agent_analyses.items(),
            key=lambda x: x[1]["usage_metrics"]["efficiency_ratio"],
            reverse=True
        )[:3]

        return {
            "analysis_period_hours": hours_back,
            "system_metrics": {
                "total_agents": len(all_agents),
                "total_system_activity": total_system_activity,
                "total_system_tasks": total_system_tasks,
                "total_system_errors": total_system_errors,
                "system_efficiency": system_efficiency,
                "system_error_rate": system_error_rate
            },
            "agent_rankings": {
                "most_active_agents": [{"agent": agent, "activities": data["usage_metrics"]["total_activities"]}
                                     for agent, data in most_active],
                "most_efficient_agents": [{"agent": agent, "efficiency": data["usage_metrics"]["efficiency_ratio"]}
                                        for agent, data in most_efficient]
            },
            "system_insights": self._generate_system_insights(system_efficiency, system_error_rate, agent_analyses)
        }

    def _find_peak_usage_hours(self, activity_data: List[MetricDataPoint]) -> List[int]:
        """Find peak usage hours from activity data."""
        hour_counts = defaultdict(int)

        for dp in activity_data:
            hour_counts[dp.timestamp.hour] += 1

        # Return top 3 peak hours
        return sorted(hour_counts.keys(), key=lambda h: hour_counts[h], reverse=True)[:3]

    def _analyze_task_completion_trend(self, task_data: List[MetricDataPoint]) -> str:
        """Analyze task completion trend."""
        if len(task_data) < 10:
            return "insufficient_data"

        # Extract task completion values
        values = [dp.value for dp in task_data if isinstance(dp.value, (int, float))]

        if len(values) < 10:
            return "insufficient_data"

        return self.metrics_collector._calculate_trend(values)

    def _calculate_activity_distribution(self, activity_data: List[MetricDataPoint]) -> Dict[str, int]:
        """Calculate activity distribution by hour."""
        distribution = defaultdict(int)

        for dp in activity_data:
            hour = dp.timestamp.hour
            if 6 <= hour < 12:
                distribution["morning"] += 1
            elif 12 <= hour < 18:
                distribution["afternoon"] += 1
            elif 18 <= hour < 22:
                distribution["evening"] += 1
            else:
                distribution["night"] += 1

        return dict(distribution)

    def _generate_usage_insights(self, agent_id: str, efficiency: float,
                               error_rate: float, peak_hours: List[int]) -> List[str]:
        """Generate usage insights for an agent."""
        insights = []

        if efficiency > 1.5:
            insights.append(f"High efficiency: {efficiency:.2f} tasks per activity - excellent performance")
        elif efficiency < 0.8:
            insights.append(f"Low efficiency: {efficiency:.2f} tasks per activity - optimization needed")

        if error_rate > 0.1:
            insights.append(f"High error rate: {error_rate:.2%} - focus on error reduction")
        elif error_rate < 0.01:
            insights.append(f"Low error rate: {error_rate:.2%} - excellent reliability")

        if peak_hours:
            insights.append(f"Peak activity hours: {', '.join(map(str, peak_hours))}")

        return insights

    def _generate_system_insights(self, system_efficiency: float, system_error_rate: float,
                                agent_analyses: Dict[str, Any]) -> List[str]:
        """Generate system-wide usage insights."""
        insights = []

        if system_efficiency > 1.2:
            insights.append("High system efficiency - swarm operating optimally")
        elif system_efficiency < 0.9:
            insights.append("Low system efficiency - coordination improvements needed")

        # Check for agent imbalances
        efficiencies = [data["usage_metrics"]["efficiency_ratio"] for data in agent_analyses.values()]
        if efficiencies:
            efficiency_std = statistics.stdev(efficiencies) if len(efficiencies) > 1 else 0
            if efficiency_std > 0.3:
                insights.append("High efficiency variance between agents - workload balancing opportunity")

        if system_error_rate > 0.05:
            insights.append("Elevated system error rate - quality improvements recommended")

        return insights


# Factory function for dependency injection
def create_usage_analytics_engine(metrics_collector: MetricsCollector) -> UsageAnalyticsEngine:
    """Factory function to create usage analytics engine with dependency injection."""
    return UsageAnalyticsEngine(metrics_collector)


# Export for DI
__all__ = ["UsageAnalyticsEngine", "create_usage_analytics_engine"]
