"""
Emergency Logger - V2 Compliant Module
=====================================

Logs emergency events and maintains history.
Extracted from orchestrator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from datetime import datetime
from typing import Any


class EmergencyLogger:
    """Logs emergency events and maintains history.

    Handles emergency event logging, history management, and system health monitoring.
    """

    def __init__(self):
        """Initialize emergency logger."""
        self.emergency_history: dict[str, list[dict[str, Any]]] = {}
        self.system_events = []
        self.health_metrics = {}

    def log_emergency_event(self, emergency_id: str, event_type: str, data: dict[str, Any]) -> None:
        """Log emergency event."""
        if emergency_id not in self.emergency_history:
            self.emergency_history[emergency_id] = []

        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data,
        }

        self.emergency_history[emergency_id].append(event)
        self.system_events.append(event)

    def get_emergency_history(self, emergency_id: str) -> list[dict[str, Any]]:
        """Get history for specific emergency."""
        return self.emergency_history.get(emergency_id, [])

    def get_all_emergency_history(self) -> dict[str, list[dict[str, Any]]]:
        """Get all emergency history."""
        return self.emergency_history.copy()

    def get_system_events(self, limit: int | None = None) -> list[dict[str, Any]]:
        """Get system events."""
        events = self.system_events.copy()
        if limit:
            events = events[-limit:]
        return events

    def get_health_recommendations(
        self, health_score: int, active_emergencies: int, metrics: dict[str, Any]
    ) -> list[str]:
        """Get health recommendations."""
        recommendations = []

        if active_emergencies > 5:
            recommendations.append("High number of active emergencies. Review system stability.")

        if metrics.get("escalation_rate", 0) > 0.3:
            recommendations.append("High escalation rate. Improve intervention protocols.")

        if metrics.get("average_response_time", 0) > 300:
            recommendations.append("Slow response time. Optimize intervention processes.")

        if health_score < 70:
            recommendations.append("System health is below optimal. Review emergency procedures.")

        if not recommendations:
            recommendations.append("System health is good. Continue monitoring.")

        return recommendations

    def calculate_system_health(
        self, active_emergencies: int, metrics: dict[str, Any]
    ) -> dict[str, Any]:
        """Calculate system health status."""
        health_score = 100

        # Deduct points for active emergencies
        health_score -= min(active_emergencies * 10, 50)

        # Deduct points for high escalation rate
        if metrics.get("escalation_rate", 0) > 0.3:  # 30%
            health_score -= 20

        # Deduct points for slow response time
        if metrics.get("average_response_time", 0) > 300:  # 5 minutes
            health_score -= 15

        health_status = (
            "excellent"
            if health_score >= 90
            else ("good" if health_score >= 70 else "fair" if health_score >= 50 else "poor")
        )

        return {
            "health_score": health_score,
            "health_status": health_status,
            "active_emergencies": active_emergencies,
            "metrics": metrics,
            "recommendations": self.get_health_recommendations(
                health_score, active_emergencies, metrics
            ),
        }

    def get_emergency_statistics(self) -> dict[str, Any]:
        """Get emergency statistics."""
        total_emergencies = len(self.emergency_history)
        total_events = sum(len(events) for events in self.emergency_history.values())

        # Count events by type
        event_types = {}
        for events in self.emergency_history.values():
            for event in events:
                event_type = event.get("event_type", "unknown")
                event_types[event_type] = event_types.get(event_type, 0) + 1

        return {
            "total_emergencies": total_emergencies,
            "total_events": total_events,
            "event_types": event_types,
            "average_events_per_emergency": total_events / max(total_emergencies, 1),
        }

    def export_emergency_data(self, emergency_id: str | None = None) -> dict[str, Any]:
        """Export emergency data."""
        if emergency_id:
            return {
                "emergency_id": emergency_id,
                "history": self.get_emergency_history(emergency_id),
                "exported_at": datetime.now().isoformat(),
            }
        else:
            return {
                "all_emergencies": self.get_all_emergency_history(),
                "system_events": self.get_system_events(),
                "statistics": self.get_emergency_statistics(),
                "exported_at": datetime.now().isoformat(),
            }

    def clear_emergency_history(self, emergency_id: str | None = None):
        """Clear emergency history."""
        if emergency_id:
            if emergency_id in self.emergency_history:
                del self.emergency_history[emergency_id]
        else:
            self.emergency_history.clear()
            self.system_events.clear()

    def get_logger_status(self) -> dict[str, Any]:
        """Get logger status."""
        return {
            "emergency_count": len(self.emergency_history),
            "total_events": len(self.system_events),
            "statistics": self.get_emergency_statistics(),
        }
