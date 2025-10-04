#!/usr/bin/env python3
"""
Swarm Intelligence Coordination Operations - Operations Module
==============================================================

Operations and utilities for swarm intelligence coordination.

V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
Refactored By: Agent-6 (Quality Assurance Specialist)
Original: swarm_intelligence_coordination.py (410 lines) - Operations module
"""

import logging
from datetime import datetime
from typing import Any

from src.services.swarm_intelligence_coordination_core import SwarmCoordinationCore

logger = logging.getLogger(__name__)


class SwarmAnalytics:
    """Analytics for swarm coordination"""

    def __init__(self):
        """Initialize analytics"""
        self.decision_counts: dict[str, int] = {}
        self.agent_activity: dict[str, int] = {}
        self.vote_patterns: dict[str, dict[str, int]] = {}

    def manage_analytics(self, action: str, **kwargs) -> Any:
        """Consolidated analytics management"""
        if action == "record_decision":
            type_key = kwargs["decision_type"].value
            self.decision_counts[type_key] = self.decision_counts.get(type_key, 0) + 1
            self.agent_activity[kwargs["agent_id"]] = (
                self.agent_activity.get(kwargs["agent_id"], 0) + 1
            )
        elif action == "record_vote":
            agent_id = kwargs["agent_id"]
            vote = kwargs["vote"]
            if agent_id not in self.vote_patterns:
                self.vote_patterns[agent_id] = {}
            self.vote_patterns[agent_id][vote] = self.vote_patterns[agent_id].get(vote, 0) + 1
        elif action == "get_summary":
            return {
                "total_decisions": sum(self.decision_counts.values()),
                "decision_types": self.decision_counts,
                "active_agents": len(self.agent_activity),
                "agent_activity": self.agent_activity,
                "vote_patterns": self.vote_patterns,
            }
        return None


class SwarmNotificationService:
    """Notification service for swarm coordination"""

    def __init__(self):
        """Initialize notification service"""
        self.notifications: list[dict[str, Any]] = []
        self.max_notifications = 100

    def manage_notifications(self, action: str, **kwargs) -> Any:
        """Consolidated notification management"""
        if action == "send":
            notification = {
                "id": f"notif_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "message": kwargs["message"],
                "priority": kwargs.get("priority", "normal"),
                "target_agents": kwargs.get("target_agents", []),
                "timestamp": datetime.now().isoformat(),
                "read_by": [],
            }

            self.notifications.append(notification)

            if len(self.notifications) > self.max_notifications:
                self.notifications = self.notifications[-self.max_notifications :]

            logger.info(f"Notification sent: {kwargs['message']}")
            return True

        elif action == "get":
            agent_id = kwargs.get("agent_id")
            if agent_id:
                return [
                    notif
                    for notif in self.notifications
                    if agent_id not in notif["target_agents"] or agent_id in notif["target_agents"]
                ]
            return self.notifications

        elif action == "mark_read":
            notification_id = kwargs["notification_id"]
            agent_id = kwargs["agent_id"]
            for notification in self.notifications:
                if notification["id"] == notification_id:
                    if agent_id not in notification["read_by"]:
                        notification["read_by"].append(agent_id)
            return True

        return None


class SwarmCoordinationService:
    """Main service for swarm coordination"""

    def __init__(self, data_dir: str = "data/swarm"):
        """Initialize coordination service"""
        self.core = SwarmCoordinationCore(data_dir)
        self.analytics = SwarmAnalytics()
        self.notifications = SwarmNotificationService()

    def manage_decision(self, action: str, **kwargs) -> Any:
        """Manage decisions with various actions"""
        if action == "create":
            decision = self.core.create_decision(
                kwargs["decision_type"],
                kwargs["title"],
                kwargs["description"],
                kwargs["proposed_by"],
            )
            self.analytics.manage_analytics(
                "record_decision",
                decision_type=kwargs["decision_type"],
                agent_id=kwargs["proposed_by"],
            )
            self.notifications.manage_notifications(
                "send",
                message=f"New decision created: {kwargs['title']}",
                priority="normal",
                target_agents=[
                    "agent-1",
                    "agent-2",
                    "agent-3",
                    "agent-4",
                    "Agent-5",
                    "Agent-6",
                    "agent-7",
                    "agent-8",
                ],
            )
            return decision

        elif action == "vote":
            success = self.core.vote_on_decision(
                kwargs["decision_id"], kwargs["agent_id"], kwargs["vote"]
            )
            if success:
                self.analytics.manage_analytics(
                    "record_vote", agent_id=kwargs["agent_id"], vote=kwargs["vote"]
                )
                decision = self.core.get_decision(kwargs["decision_id"])
                if decision and decision.resolution:
                    self.notifications.manage_notifications(
                        "send",
                        message=f"Decision {kwargs['decision_id']} resolved as {decision.resolution}",
                        priority="high",
                    )
            return success

        elif action == "get":
            return self.core.get_decision(kwargs["decision_id"])

        elif action == "list":
            return self.core.get_active_decisions()

        return None

    def manage_agent_status(self, action: str, **kwargs) -> Any:
        """Manage agent status with various actions"""
        if action == "update":
            self.core.update_agent_status(kwargs["agent_id"], kwargs["status"], kwargs.get("task"))
            self.notifications.manage_notifications(
                "send",
                message=f"Agent {kwargs['agent_id']} status updated to {kwargs['status']}",
                priority="normal",
                target_agents=[kwargs["agent_id"]],
            )
            return True

        elif action == "get":
            return self.core.get_agent_status(kwargs["agent_id"])

        elif action == "list":
            return list(self.core.agent_statuses.values())

        return None

    def get_coordination_summary(self) -> dict[str, Any]:
        """Get coordination summary"""
        return {
            "active_decisions": len(self.core.active_decisions),
            "active_agents": len(self.core.agent_statuses),
            "analytics": self.analytics.manage_analytics("get_summary"),
            "notifications": len(self.notifications.notifications),
        }

    def cleanup_old_data(self) -> int:
        """Cleanup old data and return count removed"""
        initial_decisions = len(self.core.active_decisions)

        # Remove resolved decisions older than 7 days
        cutoff_date = datetime.now().timestamp() - (7 * 24 * 60 * 60)

        decisions_to_remove = []
        for decision_id, decision in self.core.active_decisions.items():
            if decision.resolved_at:
                resolved_timestamp = datetime.fromisoformat(decision.resolved_at).timestamp()
                if resolved_timestamp < cutoff_date:
                    decisions_to_remove.append(decision_id)

        for decision_id in decisions_to_remove:
            del self.core.active_decisions[decision_id]

        self.core._save_decisions()

        return initial_decisions - len(self.core.active_decisions)
