"""
Messaging Status Analytics
=========================

Analytics engine for messaging status data.
V2 Compliance: < 300 lines, single responsibility, analytics processing.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict
from .models import StatusEntry, StatusType, PerformanceMetrics


class StatusAnalytics:
    """Analytics engine for messaging status data."""

    def __init__(self):
        """Initialize analytics engine."""
        self.status_entries: List[StatusEntry] = []
        self.performance_cache: Dict[str, Any] = {}

    def add_status_entry(self, entry: StatusEntry) -> None:
        """Add a status entry for analysis."""
        self.status_entries.append(entry)

        # Clear performance cache when new data is added
        self.performance_cache.clear()

    def get_success_rate(self, time_window: Optional[timedelta] = None) -> float:
        """Calculate overall success rate."""
        entries = self._filter_by_time_window(time_window)

        if not entries:
            return 0.0

        successful = sum(1 for entry in entries if entry.success)
        return (successful / len(entries)) * 100

    def get_agent_success_rate(
        self, agent_id: str, time_window: Optional[timedelta] = None
    ) -> float:
        """Calculate success rate for specific agent."""
        entries = self._filter_by_agent_and_time(agent_id, time_window)

        if not entries:
            return 0.0

        successful = sum(1 for entry in entries if entry.success)
        return (successful / len(entries)) * 100

    def get_performance_metrics(
        self, time_window: Optional[timedelta] = None
    ) -> PerformanceMetrics:
        """Calculate performance metrics."""
        cache_key = f"metrics_{time_window}"

        if cache_key in self.performance_cache:
            return self.performance_cache[cache_key]

        entries = self._filter_by_time_window(time_window)

        if not entries:
            metrics = PerformanceMetrics(0.0, 0.0, 0.0, 0, 0, 0.0)
        else:
            response_times = [
                entry.details.get("response_time", 0.0)
                for entry in entries
                if "response_time" in entry.details
            ]

            total_requests = len(entries)
            error_count = sum(1 for entry in entries if not entry.success)

            metrics = PerformanceMetrics(
                average_response_time=(
                    sum(response_times) / len(response_times) if response_times else 0.0
                ),
                max_response_time=max(response_times) if response_times else 0.0,
                min_response_time=min(response_times) if response_times else 0.0,
                total_requests=total_requests,
                error_count=error_count,
                error_rate=(
                    (error_count / total_requests * 100) if total_requests > 0 else 0.0
                ),
            )

        self.performance_cache[cache_key] = metrics
        return metrics

    def get_agent_statistics(
        self, time_window: Optional[timedelta] = None
    ) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all agents."""
        entries = self._filter_by_time_window(time_window)

        agent_stats = defaultdict(
            lambda: {
                "total_messages": 0,
                "successful_messages": 0,
                "failed_messages": 0,
                "success_rate": 0.0,
                "last_activity": None,
            }
        )

        for entry in entries:
            agent_id = entry.agent_id
            agent_stats[agent_id]["total_messages"] += 1

            if entry.success:
                agent_stats[agent_id]["successful_messages"] += 1
            else:
                agent_stats[agent_id]["failed_messages"] += 1

            # Update last activity
            if (
                agent_stats[agent_id]["last_activity"] is None
                or entry.timestamp > agent_stats[agent_id]["last_activity"]
            ):
                agent_stats[agent_id]["last_activity"] = entry.timestamp

        # Calculate success rates
        for agent_id, stats in agent_stats.items():
            if stats["total_messages"] > 0:
                stats["success_rate"] = (
                    stats["successful_messages"] / stats["total_messages"]
                ) * 100

        return dict(agent_stats)

    def get_error_analysis(
        self, time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Analyze error patterns."""
        entries = self._filter_by_time_window(time_window)
        error_entries = [entry for entry in entries if not entry.success]

        if not error_entries:
            return {
                "total_errors": 0,
                "error_rate": 0.0,
                "common_errors": [],
                "error_trends": [],
            }

        # Count error types
        error_types = defaultdict(int)
        for entry in error_entries:
            error_type = entry.details.get("error_type", "unknown")
            error_types[error_type] += 1

        # Get common errors
        common_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)[
            :5
        ]

        return {
            "total_errors": len(error_entries),
            "error_rate": (len(error_entries) / len(entries)) * 100,
            "common_errors": common_errors,
            "error_trends": self._calculate_error_trends(error_entries),
        }

    def _filter_by_time_window(
        self, time_window: Optional[timedelta]
    ) -> List[StatusEntry]:
        """Filter entries by time window."""
        if time_window is None:
            return self.status_entries

        cutoff_time = datetime.now() - time_window
        return [
            entry for entry in self.status_entries if entry.timestamp >= cutoff_time
        ]

    def _filter_by_agent_and_time(
        self, agent_id: str, time_window: Optional[timedelta]
    ) -> List[StatusEntry]:
        """Filter entries by agent and time window."""
        entries = self._filter_by_time_window(time_window)
        return [entry for entry in entries if entry.agent_id == agent_id]

    def _calculate_error_trends(
        self, error_entries: List[StatusEntry]
    ) -> List[Dict[str, Any]]:
        """Calculate error trends over time."""
        # Group errors by hour
        hourly_errors = defaultdict(int)
        for entry in error_entries:
            hour_key = entry.timestamp.replace(minute=0, second=0, microsecond=0)
            hourly_errors[hour_key] += 1

        # Convert to trend data
        trends = []
        for hour, count in sorted(hourly_errors.items()):
            trends.append({"timestamp": hour.isoformat(), "error_count": count})

        return trends
