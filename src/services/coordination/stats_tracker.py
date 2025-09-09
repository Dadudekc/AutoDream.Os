"""
Stats Tracker - V2 Compliant Module
==================================

Handles coordination statistics tracking and reporting.
Extracted from messaging_coordination_handler.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from datetime import datetime
from typing import Any


class StatsTracker:
    """Handles coordination statistics tracking and reporting.

    Manages statistics collection, calculation, and reporting for coordination
    operations.
    """

    def __init__(self):
        """Initialize stats tracker."""
        self.coordination_stats = {
            "total_coordinations": 0,
            "successful_coordinations": 0,
            "failed_coordinations": 0,
            "average_coordination_time": 0.0,
        }
        self.detailed_stats = {
            "strategy_stats": {},
            "priority_stats": {},
            "type_stats": {},
            "sender_stats": {},
        }
        self.performance_history = []

    def update_coordination_stats(
        self,
        success: bool,
        coordination_time: float,
        strategy: str = None,
        priority: str = None,
        message_type: str = None,
        sender_type: str = None,
    ):
        """Update coordination statistics."""
        self.coordination_stats["total_coordinations"] += 1

        if success:
            self.coordination_stats["successful_coordinations"] += 1
        else:
            self.coordination_stats["failed_coordinations"] += 1

        # Update average coordination time
        total = self.coordination_stats["total_coordinations"]
        current_avg = self.coordination_stats["average_coordination_time"]
        self.coordination_stats["average_coordination_time"] = (
            current_avg * (total - 1) + coordination_time
        ) / total

        # Update detailed stats
        self._update_detailed_stats(
            success, coordination_time, strategy, priority, message_type, sender_type
        )

        # Record performance history
        self.performance_history.append(
            {
                "timestamp": datetime.now().isoformat(),
                "success": success,
                "coordination_time": coordination_time,
                "strategy": strategy,
                "priority": priority,
                "message_type": message_type,
                "sender_type": sender_type,
            }
        )

        # Keep only last 1000 records
        if len(self.performance_history) > 1000:
            self.performance_history = self.performance_history[-1000:]

    def _update_detailed_stats(
        self,
        success: bool,
        coordination_time: float,
        strategy: str = None,
        priority: str = None,
        message_type: str = None,
        sender_type: str = None,
    ):
        """Update detailed statistics."""
        # Update strategy stats
        if strategy:
            if strategy not in self.detailed_stats["strategy_stats"]:
                self.detailed_stats["strategy_stats"][strategy] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "avg_time": 0.0,
                }
            self._update_category_stats("strategy_stats", strategy, success, coordination_time)

        # Update priority stats
        if priority:
            if priority not in self.detailed_stats["priority_stats"]:
                self.detailed_stats["priority_stats"][priority] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "avg_time": 0.0,
                }
            self._update_category_stats("priority_stats", priority, success, coordination_time)

        # Update type stats
        if message_type:
            if message_type not in self.detailed_stats["type_stats"]:
                self.detailed_stats["type_stats"][message_type] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "avg_time": 0.0,
                }
            self._update_category_stats("type_stats", message_type, success, coordination_time)

        # Update sender stats
        if sender_type:
            if sender_type not in self.detailed_stats["sender_stats"]:
                self.detailed_stats["sender_stats"][sender_type] = {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "avg_time": 0.0,
                }
            self._update_category_stats("sender_stats", sender_type, success, coordination_time)

    def _update_category_stats(
        self, category: str, key: str, success: bool, coordination_time: float
    ):
        """Update category statistics."""
        stats = self.detailed_stats[category][key]
        stats["total"] += 1

        if success:
            stats["successful"] += 1
        else:
            stats["failed"] += 1

        # Update average time
        total = stats["total"]
        current_avg = stats["avg_time"]
        stats["avg_time"] = (current_avg * (total - 1) + coordination_time) / total

    def get_coordination_stats(self) -> dict[str, Any]:
        """Get coordination statistics."""
        stats = self.coordination_stats.copy()

        # Calculate success rate
        if stats["total_coordinations"] > 0:
            stats["success_rate"] = stats["successful_coordinations"] / stats["total_coordinations"]
        else:
            stats["success_rate"] = 0.0

        return stats

    def get_detailed_stats(self) -> dict[str, Any]:
        """Get detailed statistics."""
        detailed = {}

        for category, stats in self.detailed_stats.items():
            detailed[category] = {}
            for key, stat in stats.items():
                detailed[category][key] = stat.copy()
                if stat["total"] > 0:
                    detailed[category][key]["success_rate"] = stat["successful"] / stat["total"]
                else:
                    detailed[category][key]["success_rate"] = 0.0

        return detailed

    def get_performance_summary(self, hours: int = 24) -> dict[str, Any]:
        """Get performance summary for specified hours."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)

        recent_history = [
            record
            for record in self.performance_history
            if datetime.fromisoformat(record["timestamp"]).timestamp() >= cutoff_time
        ]

        if not recent_history:
            return {"message": "No data available for the specified time period"}

        total_coordinations = len(recent_history)
        successful = sum(1 for record in recent_history if record["success"])
        failed = total_coordinations - successful

        avg_time = (
            sum(record["coordination_time"] for record in recent_history) / total_coordinations
        )

        return {
            "time_period_hours": hours,
            "total_coordinations": total_coordinations,
            "successful": successful,
            "failed": failed,
            "success_rate": (successful / total_coordinations if total_coordinations > 0 else 0),
            "average_coordination_time": avg_time,
        }

    def reset_stats(self):
        """Reset coordination statistics."""
        self.coordination_stats = {
            "total_coordinations": 0,
            "successful_coordinations": 0,
            "failed_coordinations": 0,
            "average_coordination_time": 0.0,
        }
        self.detailed_stats = {
            "strategy_stats": {},
            "priority_stats": {},
            "type_stats": {},
            "sender_stats": {},
        }
        self.performance_history = []

    def get_tracker_status(self) -> dict[str, Any]:
        """Get stats tracker status."""
        return {
            "coordination_stats": self.get_coordination_stats(),
            "detailed_stats_categories": list(self.detailed_stats.keys()),
            "performance_history_count": len(self.performance_history),
        }
