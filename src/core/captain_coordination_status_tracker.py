#!/usr/bin/env python3
"""
Captain Coordination Status Tracker - V2 Compliance Module
=========================================================

Handles captain coordination status tracking and reporting.
Extracted from monolithic agent-1-captain-coordination-breakthrough-activation-coordinator.py for V2 compliance.

Responsibilities:
- Status tracking and updates
- Efficiency score calculation
- Status reporting and aggregation
- Performance monitoring

V2 Compliance: < 300 lines, single responsibility, dependency injection ready.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

import statistics


@dataclass
class CaptainCoordinationBreakthroughStatus:
    """Captain coordination breakthrough status structure"""

    agent_id: str
    agent_name: str
    domain: str
    coordination_status: str
    breakthrough_patterns: int
    consolidation_patterns: int
    parallel_deployment: int
    total_efficiency_score: float
    breakthrough_efficiency: float
    last_coordination_attempt: Optional[str] = None
    coordination_history: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self):
        if self.coordination_history is None:
            self.coordination_history = []

    def update_efficiency_score(self, new_score: float):
        """Update efficiency score with timestamp."""
        self.total_efficiency_score = new_score
        self.last_coordination_attempt = datetime.now().isoformat()

        # Add to history
        if self.coordination_history is None:
            self.coordination_history = []

        self.coordination_history.append(
            {
                "timestamp": self.last_coordination_attempt,
                "efficiency_score": new_score,
                "breakthrough_patterns": self.breakthrough_patterns,
                "consolidation_patterns": self.consolidation_patterns,
                "parallel_deployment": self.parallel_deployment,
            }
        )

        # Keep only last 10 entries
        if len(self.coordination_history) > 10:
            self.coordination_history = self.coordination_history[-10:]

    def calculate_breakthrough_efficiency(self) -> float:
        """Calculate breakthrough efficiency score."""
        if self.breakthrough_patterns == 0:
            return 0.0

        # Efficiency based on patterns and coordination status
        base_efficiency = min(self.breakthrough_patterns * 10, 100)

        if self.coordination_status == "completed":
            base_efficiency *= 1.2
        elif self.coordination_status == "active":
            base_efficiency *= 1.1
        elif self.coordination_status == "failed":
            base_efficiency *= 0.8

        return min(base_efficiency, 100.0)

    def get_status_summary(self) -> Dict[str, Any]:
        """Get status summary for reporting."""
        return {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "domain": self.domain,
            "status": self.coordination_status,
            "efficiency_score": self.total_efficiency_score,
            "breakthrough_efficiency": self.breakthrough_efficiency,
            "patterns_total": (
                self.breakthrough_patterns
                + self.consolidation_patterns
                + self.parallel_deployment
            ),
            "last_attempt": self.last_coordination_attempt,
            "history_entries": (
                len(self.coordination_history) if self.coordination_history else 0
            ),
        }


class CaptainCoordinationStatusTracker:
    """
    Tracks captain coordination breakthrough status.

    V2 Compliance: Single responsibility for status tracking.
    """

    def __init__(self):
        """Initialize status tracker."""
        self.captain_coordination_breakthrough_status: Dict[
            str, CaptainCoordinationBreakthroughStatus
        ] = {}
        self.status_history: List[Dict[str, Any]] = []

    def register_agent_status(self, status: CaptainCoordinationBreakthroughStatus):
        """
        Register agent coordination status.

        Args:
            status: Agent status to register
        """
        self.captain_coordination_breakthrough_status[status.agent_id] = status

    def update_agent_status(self, agent_id: str, **updates):
        """
        Update agent coordination status.

        Args:
            agent_id: Agent identifier
            **updates: Status updates to apply
        """
        status = self.captain_coordination_breakthrough_status.get(agent_id)
        if not get_unified_validator().validate_required(status):
            return

        # Update coordination status
        if "coordination_status" in updates:
            status.coordination_status = updates["coordination_status"]

        # Update pattern counts
        if "breakthrough_patterns" in updates:
            status.breakthrough_patterns = updates["breakthrough_patterns"]
        if "consolidation_patterns" in updates:
            status.consolidation_patterns = updates["consolidation_patterns"]
        if "parallel_deployment" in updates:
            status.parallel_deployment = updates["parallel_deployment"]

        # Update efficiency score
        if "efficiency_score" in updates:
            status.update_efficiency_score(updates["efficiency_score"])

        # Recalculate breakthrough efficiency
        status.breakthrough_efficiency = status.calculate_breakthrough_efficiency()

    def get_agent_status(
        self, agent_id: str
    ) -> Optional[CaptainCoordinationBreakthroughStatus]:
        """
        Get agent coordination status.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent status if found, None otherwise
        """
        return self.captain_coordination_breakthrough_status.get(agent_id)

    def get_all_agent_statuses(self) -> List[CaptainCoordinationBreakthroughStatus]:
        """
        Get all agent coordination statuses.

        Returns:
            List of all agent statuses
        """
        return list(self.captain_coordination_breakthrough_status.values())

    def get_agents_by_status(
        self, coordination_status: str
    ) -> List[CaptainCoordinationBreakthroughStatus]:
        """
        Get agents by coordination status.

        Args:
            coordination_status: Status to filter by

        Returns:
            List of agents with specified status
        """
        return [
            status
            for status in self.get_all_agent_statuses()
            if status.coordination_status == coordination_status
        ]

    def calculate_overall_efficiency_score(self) -> float:
        """
        Calculate overall coordination efficiency score.

        Returns:
            Overall efficiency score
        """
        all_statuses = self.get_all_agent_statuses()
        if not get_unified_validator().validate_required(all_statuses):
            return 0.0

        efficiency_scores = [status.total_efficiency_score for status in all_statuses]
        return statistics.mean(efficiency_scores) if efficiency_scores else 0.0

    def calculate_breakthrough_efficiency_score(self) -> float:
        """
        Calculate overall breakthrough efficiency score.

        Returns:
            Overall breakthrough efficiency score
        """
        all_statuses = self.get_all_agent_statuses()
        if not get_unified_validator().validate_required(all_statuses):
            return 0.0

        breakthrough_scores = [
            status.breakthrough_efficiency for status in all_statuses
        ]
        return statistics.mean(breakthrough_scores) if breakthrough_scores else 0.0

    def get_coordination_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive coordination statistics.

        Returns:
            Dict containing coordination statistics
        """
        all_statuses = self.get_all_agent_statuses()
        total_agents = len(all_statuses)

        if total_agents == 0:
            return {"total_agents": 0, "status_breakdown": {}, "domain_breakdown": {}}

        # Status breakdown
        status_breakdown = {}
        domain_breakdown = {}
        total_patterns = 0
        total_efficiency = 0

        for status in all_statuses:
            # Status count
            coord_status = status.coordination_status
            status_breakdown[coord_status] = status_breakdown.get(coord_status, 0) + 1

            # Domain count
            domain = status.domain
            domain_breakdown[domain] = domain_breakdown.get(domain, 0) + 1

            # Aggregate metrics
            total_patterns += (
                status.breakthrough_patterns
                + status.consolidation_patterns
                + status.parallel_deployment
            )
            total_efficiency += status.total_efficiency_score

        return {
            "total_agents": total_agents,
            "status_breakdown": status_breakdown,
            "domain_breakdown": domain_breakdown,
            "average_patterns_per_agent": total_patterns / total_agents,
            "overall_efficiency_score": total_efficiency / total_agents,
            "overall_breakthrough_efficiency": (
                self.calculate_breakthrough_efficiency_score()
            ),
            "timestamp": datetime.now().isoformat(),
        }

    def get_efficiency_trends(self) -> Dict[str, Any]:
        """
        Get efficiency trends over time.

        Returns:
            Dict containing efficiency trend analysis
        """
        trends = {
            "data_points": len(self.status_history),
            "efficiency_trend": "stable",
            "recent_efficiency": 0.0,
            "trend_direction": "stable",
        }

        if len(self.status_history) < 3:
            return trends

        # Analyze recent efficiency scores
        recent_scores = [
            entry["efficiency_score"] for entry in self.status_history[-5:]
        ]
        trends["recent_efficiency"] = (
            statistics.mean(recent_scores) if recent_scores else 0.0
        )

        # Calculate trend
        if len(recent_scores) >= 3:
            first_half = statistics.mean(recent_scores[: len(recent_scores) // 2])
            second_half = statistics.mean(recent_scores[len(recent_scores) // 2 :])

            if second_half > first_half + 5:
                trends["efficiency_trend"] = "improving"
                trends["trend_direction"] = "up"
            elif first_half > second_half + 5:
                trends["efficiency_trend"] = "declining"
                trends["trend_direction"] = "down"
            else:
                trends["efficiency_trend"] = "stable"
                trends["trend_direction"] = "stable"

        return trends

    def export_status_report(self) -> Dict[str, Any]:
        """
        Export comprehensive status report.

        Returns:
            Dict containing complete status report
        """
        return {
            "agent_statuses": [
                status.get_status_summary() for status in self.get_all_agent_statuses()
            ],
            "coordination_statistics": self.get_coordination_statistics(),
            "efficiency_trends": self.get_efficiency_trends(),
            "export_timestamp": datetime.now().isoformat(),
            "total_agents": len(self.captain_coordination_breakthrough_status),
            "active_coordination": len(self.get_agents_by_status("active")),
            "completed_coordination": len(self.get_agents_by_status("completed")),
        }


# Factory function for dependency injection
def create_status_tracker() -> CaptainCoordinationStatusTracker:
    """
    Factory function to create CaptainCoordinationStatusTracker.
    """
    return CaptainCoordinationStatusTracker()


# Export service interface
__all__ = [
    "CaptainCoordinationBreakthroughStatus",
    "CaptainCoordinationStatusTracker",
    "create_status_tracker",
]
