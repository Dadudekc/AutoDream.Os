"""
OSRS Swarm Activity Planner - V2 Compliant
===========================================

Plans strategic activities for swarm coordination.
Extracted from swarm_coordinator.py for V2 compliance.

Author: Agent-3 - Infrastructure & DevOps Specialist (extracted)
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class SwarmActivity:
    """Coordinated swarm activity."""

    activity_id: str
    activity_type: str
    description: str
    participating_agents: list[str]
    start_time: datetime
    end_time: datetime | None
    status: str
    requirements: dict[str, Any]


class SwarmActivityPlanner:
    """Plans strategic activities for swarm."""

    def __init__(self, agents_ref, logger):
        """Initialize planner."""
        self.agents = agents_ref
        self.logger = logger

    def plan_strategic_activities(self) -> list[SwarmActivity]:
        """Plan strategic activities based on current swarm state."""
        planned_activities = []

        if self.should_plan_resource_gathering():
            activity = SwarmActivity(
                activity_id=f"resource_gather_{int(time.time())}",
                activity_type="resource_gathering",
                description="Coordinated resource gathering",
                participating_agents=self._get_resource_agents(),
                start_time=datetime.now(),
                end_time=None,
                status="planned",
                requirements={"min_agents": 2},
            )
            planned_activities.append(activity)

        if self.should_plan_combat_activity():
            activity = SwarmActivity(
                activity_id=f"combat_{int(time.time())}",
                activity_type="combat",
                description="Group combat activity",
                participating_agents=self._get_combat_agents(),
                start_time=datetime.now(),
                end_time=None,
                status="planned",
                requirements={"min_combat_level": 60},
            )
            planned_activities.append(activity)

        return planned_activities

    def should_plan_resource_gathering(self) -> bool:
        """Check if resource gathering should be planned."""
        resource_agents = self._get_resource_agents()
        return len(resource_agents) >= 2

    def should_plan_combat_activity(self) -> bool:
        """Check if combat activity should be planned."""
        combat_agents = self._get_combat_agents()
        return len(combat_agents) >= 3

    def _get_resource_agents(self) -> list[str]:
        """Get agents with resource gathering role."""
        return [
            aid
            for aid, agent in self.agents.items()
            if hasattr(agent, "role") and agent.role.value == "resource_manager"
        ]

    def _get_combat_agents(self) -> list[str]:
        """Get agents with combat role."""
        return [
            aid
            for aid, agent in self.agents.items()
            if hasattr(agent, "role") and agent.role.value == "combat_specialist"
        ]
