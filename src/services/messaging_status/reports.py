"""
Messaging Status Reports
========================

Reporting engine for messaging status data.
V2 Compliance: < 300 lines, single responsibility, report generation.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from .models import (
    StatusEntry,
    StatusType,
    StatusSummary,
    AgentStatus,
    PerformanceMetrics,
)
from .analytics import StatusAnalytics


class StatusReporter:
    """Reporting engine for messaging status data."""

    def __init__(self, analytics: StatusAnalytics):
        """Initialize reporter with analytics engine."""
        self.analytics = analytics

    def generate_status_report(
        self, time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive status report."""
        performance_metrics = self.analytics.get_performance_metrics(time_window)
        agent_stats = self.analytics.get_agent_statistics(time_window)
        error_analysis = self.analytics.get_error_analysis(time_window)

        return {
            "timestamp": datetime.now().isoformat(),
            "time_window": str(time_window) if time_window else "all_time",
            "summary": {
                "total_messages": performance_metrics.total_requests,
                "successful_messages": (
                    performance_metrics.total_requests - performance_metrics.error_count
                ),
                "failed_messages": performance_metrics.error_count,
                "success_rate": 100 - performance_metrics.error_rate,
                "average_response_time": performance_metrics.average_response_time,
            },
            "performance_metrics": {
                "average_response_time": performance_metrics.average_response_time,
                "max_response_time": performance_metrics.max_response_time,
                "min_response_time": performance_metrics.min_response_time,
                "error_rate": performance_metrics.error_rate,
            },
            "agent_statistics": agent_stats,
            "error_analysis": error_analysis,
        }

    def generate_agent_report(
        self, agent_id: str, time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Generate report for specific agent."""
        agent_stats = self.analytics.get_agent_statistics(time_window)
        agent_data = agent_stats.get(agent_id, {})

        if not agent_data:
            return {
                "agent_id": agent_id,
                "timestamp": datetime.now().isoformat(),
                "status": "no_data",
                "message": f"No data found for agent {agent_id}",
            }

        return {
            "agent_id": agent_id,
            "timestamp": datetime.now().isoformat(),
            "time_window": str(time_window) if time_window else "all_time",
            "statistics": agent_data,
            "success_rate": self.analytics.get_agent_success_rate(
                agent_id, time_window
            ),
            "is_online": (
                agent_data.get("last_activity", datetime.min)
                > datetime.now() - timedelta(hours=1)
            ),
        }

    def generate_performance_report(
        self, time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Generate performance-focused report."""
        performance_metrics = self.analytics.get_performance_metrics(time_window)

        # Performance rating based on metrics
        performance_rating = self._calculate_performance_rating(performance_metrics)

        return {
            "timestamp": datetime.now().isoformat(),
            "time_window": str(time_window) if time_window else "all_time",
            "performance_rating": performance_rating,
            "metrics": {
                "average_response_time": performance_metrics.average_response_time,
                "max_response_time": performance_metrics.max_response_time,
                "min_response_time": performance_metrics.min_response_time,
                "total_requests": performance_metrics.total_requests,
                "error_count": performance_metrics.error_count,
                "error_rate": performance_metrics.error_rate,
            },
            "recommendations": self._generate_performance_recommendations(
                performance_metrics
            ),
        }

    def generate_error_report(
        self, time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Generate error-focused report."""
        error_analysis = self.analytics.get_error_analysis(time_window)

        return {
            "timestamp": datetime.now().isoformat(),
            "time_window": str(time_window) if time_window else "all_time",
            "error_summary": {
                "total_errors": error_analysis["total_errors"],
                "error_rate": error_analysis["error_rate"],
            },
            "common_errors": error_analysis["common_errors"],
            "error_trends": error_analysis["error_trends"],
            "recommendations": self._generate_error_recommendations(error_analysis),
        }

    def generate_daily_summary(self) -> Dict[str, Any]:
        """Generate daily summary report."""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        time_window = datetime.now() - today

        return self.generate_status_report(time_window)

    def generate_weekly_summary(self) -> Dict[str, Any]:
        """Generate weekly summary report."""
        week_ago = datetime.now() - timedelta(days=7)
        time_window = datetime.now() - week_ago

        return self.generate_status_report(time_window)

    def _calculate_performance_rating(self, metrics: PerformanceMetrics) -> str:
        """Calculate performance rating based on metrics."""
        if metrics.error_rate > 10:
            return "poor"
        elif metrics.error_rate > 5:
            return "fair"
        elif metrics.average_response_time > 5.0:
            return "good"
        elif metrics.average_response_time > 2.0:
            return "very_good"
        else:
            return "excellent"

    def _generate_performance_recommendations(
        self, metrics: PerformanceMetrics
    ) -> List[str]:
        """Generate performance recommendations."""
        recommendations = []

        if metrics.error_rate > 10:
            recommendations.append(
                "High error rate detected. Review error logs and fix underlying issues."
            )

        if metrics.average_response_time > 5.0:
            recommendations.append(
                "Slow response times detected. Consider performance optimization."
            )

        if metrics.max_response_time > 10.0:
            recommendations.append(
                "Very slow requests detected. Investigate timeout issues."
            )

        if metrics.total_requests < 10:
            recommendations.append("Low request volume. Consider load testing.")

        if not recommendations:
            recommendations.append(
                "Performance metrics look good. Continue monitoring."
            )

        return recommendations

    def _generate_error_recommendations(
        self, error_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate error recommendations."""
        recommendations = []

        if error_analysis["error_rate"] > 10:
            recommendations.append("High error rate. Implement better error handling.")

        if error_analysis["common_errors"]:
            top_error = error_analysis["common_errors"][0]
            recommendations.append(
                f"Most common error: {top_error[0]} ({top_error[1]} occurrences). Focus on fixing this issue."
            )

        if error_analysis["error_trends"]:
            recent_errors = error_analysis["error_trends"][-3:]  # Last 3 hours
            if len(recent_errors) >= 2:
                if recent_errors[-1]["error_count"] > recent_errors[-2]["error_count"]:
                    recommendations.append(
                        "Error count is increasing. Investigate recent changes."
                    )

        if not recommendations:
            recommendations.append(
                "Error analysis shows good stability. Continue monitoring."
            )

        return recommendations
