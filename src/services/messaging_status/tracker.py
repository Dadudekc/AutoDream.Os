"""
Messaging Status Tracker
========================

Main status tracking engine for messaging system.
V2 Compliance: < 300 lines, single responsibility, status tracking.

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
    StatusTrackerModels,
)
from .analytics import StatusAnalytics
from .reports import StatusReporter


class MessagingStatusTracker:
    """Main status tracking engine for messaging system."""

    def __init__(self, logger=None):
        """Initialize status tracker."""
        self.logger = logger or __import__("logging").getLogger(__name__)
        self.analytics = StatusAnalytics()
        self.reporter = StatusReporter(self.analytics)

        # Status tracking
        self.message_status = {}
        self.agent_status = {}
        self.performance_metrics = {}

    def track_message_sent(
        self, message_id: str, agent_id: str, details: Dict[str, Any] = None
    ) -> None:
        """Track a message sent event."""
        entry = StatusTrackerModels.create_status_entry(
            StatusType.MESSAGE_SENT, message_id, agent_id, details or {}, True
        )

        self.analytics.add_status_entry(entry)
        self.message_status[message_id] = entry

        self.logger.info(f"Message {message_id} sent to {agent_id}")

    def track_message_delivered(
        self, message_id: str, agent_id: str, details: Dict[str, Any] = None
    ) -> None:
        """Track a message delivered event."""
        entry = StatusTrackerModels.create_status_entry(
            StatusType.MESSAGE_DELIVERED, message_id, agent_id, details or {}, True
        )

        self.analytics.add_status_entry(entry)

        # Update message status
        if message_id in self.message_status:
            self.message_status[message_id] = entry

        self.logger.info(f"Message {message_id} delivered to {agent_id}")

    def track_message_failed(
        self, message_id: str, agent_id: str, error: str, details: Dict[str, Any] = None
    ) -> None:
        """Track a message failed event."""
        error_details = details or {}
        error_details["error_type"] = "delivery_failed"
        error_details["error_message"] = error

        entry = StatusTrackerModels.create_status_entry(
            StatusType.MESSAGE_FAILED, message_id, agent_id, error_details, False
        )

        self.analytics.add_status_entry(entry)

        # Update message status
        if message_id in self.message_status:
            self.message_status[message_id] = entry

        self.logger.error(f"Message {message_id} failed to {agent_id}: {error}")

    def track_system_error(self, error: str, details: Dict[str, Any] = None) -> None:
        """Track a system error event."""
        error_details = details or {}
        error_details["error_type"] = "system_error"
        error_details["error_message"] = error

        entry = StatusTrackerModels.create_status_entry(
            StatusType.SYSTEM_ERROR, "system", "system", error_details, False
        )

        self.analytics.add_status_entry(entry)
        self.logger.error(f"System error: {error}")

    def track_performance_metric(
        self, metric_name: str, value: float, details: Dict[str, Any] = None
    ) -> None:
        """Track a performance metric."""
        metric_details = details or {}
        metric_details["metric_name"] = metric_name
        metric_details["metric_value"] = value

        entry = StatusTrackerModels.create_status_entry(
            StatusType.PERFORMANCE_METRIC, "performance", "system", metric_details, True
        )

        self.analytics.add_status_entry(entry)
        self.performance_metrics[metric_name] = value

    def get_status_summary(
        self, time_window: Optional[timedelta] = None
    ) -> StatusSummary:
        """Get status summary for time window."""
        performance_metrics = self.analytics.get_performance_metrics(time_window)

        return StatusTrackerModels.create_status_summary(
            total_messages=performance_metrics.total_requests,
            successful_messages=performance_metrics.total_requests
            - performance_metrics.error_count,
            failed_messages=performance_metrics.error_count,
            average_response_time=performance_metrics.average_response_time,
        )

    def get_agent_status(
        self, agent_id: str, time_window: Optional[timedelta] = None
    ) -> Optional[AgentStatus]:
        """Get status for specific agent."""
        agent_stats = self.analytics.get_agent_statistics(time_window)
        agent_data = agent_stats.get(agent_id)

        if not agent_data:
            return None

        return StatusTrackerModels.create_agent_status(
            agent_id=agent_id,
            total_messages=agent_data["total_messages"],
            successful_messages=agent_data["successful_messages"],
            failed_messages=agent_data["failed_messages"],
            last_activity=agent_data["last_activity"],
            is_online=agent_data["last_activity"] > datetime.now() - timedelta(hours=1),
        )

    def get_performance_metrics(
        self, time_window: Optional[timedelta] = None
    ) -> PerformanceMetrics:
        """Get performance metrics for time window."""
        return self.analytics.get_performance_metrics(time_window)

    def generate_report(
        self, report_type: str = "status", time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Generate report of specified type."""
        if report_type == "status":
            return self.reporter.generate_status_report(time_window)
        elif report_type == "performance":
            return self.reporter.generate_performance_report(time_window)
        elif report_type == "error":
            return self.reporter.generate_error_report(time_window)
        elif report_type == "daily":
            return self.reporter.generate_daily_summary()
        elif report_type == "weekly":
            return self.reporter.generate_weekly_summary()
        else:
            return {"error": f"Unknown report type: {report_type}"}

    def get_agent_report(
        self, agent_id: str, time_window: Optional[timedelta] = None
    ) -> Dict[str, Any]:
        """Get report for specific agent."""
        return self.reporter.generate_agent_report(agent_id, time_window)

    def clear_old_data(self, days_to_keep: int = 30) -> int:
        """Clear old data older than specified days."""
        cutoff_time = datetime.now() - timedelta(days=days_to_keep)

        # Count entries to be removed
        old_entries = [
            entry
            for entry in self.analytics.status_entries
            if entry.timestamp < cutoff_time
        ]
        count = len(old_entries)

        # Remove old entries
        self.analytics.status_entries = [
            entry
            for entry in self.analytics.status_entries
            if entry.timestamp >= cutoff_time
        ]

        # Clear performance cache
        self.analytics.performance_cache.clear()

        self.logger.info(f"Cleared {count} old status entries")
        return count
