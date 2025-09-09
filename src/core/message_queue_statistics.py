"""
Message Queue Statistics - V2 Compliance Module
==============================================

Handles queue statistics calculations following SRP.

Author: Agent-1 (System Recovery Specialist)
License: MIT
"""

from typing import Any, Dict, List
from datetime import datetime as dt, timedelta


class QueueStatisticsCalculator:
    """Calculates comprehensive queue statistics."""

    def calculate_statistics(self, entries: List[Any]) -> Dict[str, Any]:
        """Calculate comprehensive queue statistics."""
        if not entries:
            return self._get_empty_statistics()

        stats = {
            "total_entries": len(entries),
            "pending_entries": 0,
            "processing_entries": 0,
            "delivered_entries": 0,
            "failed_entries": 0,
            "expired_entries": 0,
            "oldest_entry_age": None,
            "newest_entry_age": None,
            "average_age": 0.0,
            "priority_distribution": {},
            "status_distribution": {},
            "retry_distribution": {}
        }

        now = dt.now()
        total_age = 0.0

        for entry in entries:
            # Count by status
            status = getattr(entry, 'status', 'unknown')
            stats["status_distribution"][status] = stats["status_distribution"].get(status, 0) + 1

            # Count specific statuses
            if status == "PENDING":
                stats["pending_entries"] += 1
            elif status == "PROCESSING":
                stats["processing_entries"] += 1
            elif status == "DELIVERED":
                stats["delivered_entries"] += 1
            elif status == "FAILED":
                stats["failed_entries"] += 1
            elif status == "EXPIRED":
                stats["expired_entries"] += 1

            # Calculate age statistics
            if hasattr(entry, 'created_at'):
                created_at = entry.created_at
                if isinstance(created_at, str):
                    # Parse ISO string if needed
                    created_at = dt.fromisoformat(created_at.replace('Z', '+00:00'))

                if isinstance(created_at, dt):
                    age = (now - created_at).total_seconds()
                    total_age += age

                    if stats["oldest_entry_age"] is None or age > stats["oldest_entry_age"]:
                        stats["oldest_entry_age"] = age
                    if stats["newest_entry_age"] is None or age < stats["newest_entry_age"]:
                        stats["newest_entry_age"] = age

            # Priority distribution
            if hasattr(entry, 'priority_score'):
                priority_bucket = self._get_priority_bucket(entry.priority_score)
                stats["priority_distribution"][priority_bucket] = stats["priority_distribution"].get(priority_bucket, 0) + 1

            # Retry distribution
            if hasattr(entry, 'delivery_attempts'):
                retry_bucket = self._get_retry_bucket(entry.delivery_attempts)
                stats["retry_distribution"][retry_bucket] = stats["retry_distribution"].get(retry_bucket, 0) + 1

        # Calculate averages
        if entries:
            stats["average_age"] = total_age / len(entries)

        # Convert ages to human-readable format
        stats.update(self._format_age_statistics(stats))

        return stats

    def _get_empty_statistics(self) -> Dict[str, Any]:
        """Get statistics for empty queue."""
        return {
            "total_entries": 0,
            "pending_entries": 0,
            "processing_entries": 0,
            "delivered_entries": 0,
            "failed_entries": 0,
            "expired_entries": 0,
            "oldest_entry_age": None,
            "newest_entry_age": None,
            "average_age": 0.0,
            "priority_distribution": {},
            "status_distribution": {},
            "retry_distribution": {},
            "oldest_entry_age_formatted": "N/A",
            "newest_entry_age_formatted": "N/A",
            "average_age_formatted": "N/A"
        }

    def _get_priority_bucket(self, priority_score: float) -> str:
        """Get priority bucket for statistics."""
        if priority_score >= 0.8:
            return "high"
        elif priority_score >= 0.6:
            return "medium"
        elif priority_score >= 0.4:
            return "low"
        else:
            return "very_low"

    def _get_retry_bucket(self, attempts: int) -> str:
        """Get retry bucket for statistics."""
        if attempts == 0:
            return "never_retried"
        elif attempts == 1:
            return "retried_once"
        elif attempts <= 3:
            return "retried_few"
        else:
            return "retried_many"

    def _format_age_statistics(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        """Format age statistics into human-readable format."""
        formatted = {}

        for key in ["oldest_entry_age", "newest_entry_age", "average_age"]:
            age_seconds = stats[key]
            if age_seconds is not None:
                formatted[f"{key}_formatted"] = self._format_duration(age_seconds)
            else:
                formatted[f"{key}_formatted"] = "N/A"

        return formatted

    def _format_duration(self, seconds: float) -> str:
        """Format duration in seconds to human-readable string."""
        if seconds < 60:
            return ".1f"
        elif seconds < 3600:
            minutes = seconds / 60
            return ".1f"
        elif seconds < 86400:
            hours = seconds / 3600
            return ".1f"
        else:
            days = seconds / 86400
            return ".1f"


class QueueHealthMonitor:
    """Monitors queue health and provides recommendations."""

    def __init__(self, stats_calculator: QueueStatisticsCalculator):
        """Initialize health monitor."""
        self.stats_calculator = stats_calculator

    def assess_health(self, entries: List[Any]) -> Dict[str, Any]:
        """Assess overall queue health."""
        stats = self.stats_calculator.calculate_statistics(entries)

        health = {
            "overall_health": "good",
            "issues": [],
            "recommendations": [],
            "metrics": stats
        }

        # Check for health issues
        self._check_queue_size_health(health, stats)
        self._check_processing_health(health, stats)
        self._check_age_health(health, stats)
        self._check_failure_health(health, stats)

        # Determine overall health
        if health["issues"]:
            if len(health["issues"]) > 2:
                health["overall_health"] = "critical"
            else:
                health["overall_health"] = "warning"

        return health

    def _check_queue_size_health(self, health: Dict[str, Any], stats: Dict[str, Any]) -> None:
        """Check queue size health."""
        total_entries = stats["total_entries"]
        if total_entries > 1000:
            health["issues"].append(f"Queue size critically high: {total_entries} entries")
            health["recommendations"].append("Consider increasing processing capacity or reducing message volume")
        elif total_entries > 500:
            health["issues"].append(f"Queue size elevated: {total_entries} entries")
            health["recommendations"].append("Monitor processing capacity")

    def _check_processing_health(self, health: Dict[str, Any], stats: Dict[str, Any]) -> None:
        """Check processing health."""
        processing_entries = stats["processing_entries"]
        total_entries = stats["total_entries"]

        if total_entries > 0:
            processing_ratio = processing_entries / total_entries
            if processing_ratio > 0.5:
                health["issues"].append(".1%")
                health["recommendations"].append("Check for stuck processing entries")

    def _check_age_health(self, health: Dict[str, Any], stats: Dict[str, Any]) -> None:
        """Check message age health."""
        average_age = stats["average_age"]
        if average_age > 3600:  # 1 hour
            health["issues"].append(f"Messages are aging: average {stats['average_age_formatted']}")
            health["recommendations"].append("Increase processing capacity or optimize message handling")

    def _check_failure_health(self, health: Dict[str, Any], stats: Dict[str, Any]) -> None:
        """Check failure rate health."""
        failed_entries = stats["failed_entries"]
        total_entries = stats["total_entries"]

        if total_entries > 0:
            failure_rate = failed_entries / total_entries
            if failure_rate > 0.1:  # 10%
                health["issues"].append(".1%")
                health["recommendations"].append("Investigate message delivery failures")
