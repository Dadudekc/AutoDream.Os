#!/usr/bin/env python3
"""
OSRS Swarm Strategic Activity Planner
Extracted from swarm_coordinator.py for V2 compliance.

Author: Agent-1 - Testing & Quality Assurance Specialist
Date: 2025-10-14
"""

from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .swarm_coordinator import OSRS_Swarm_Coordinator, SwarmActivity

from ..agents.osrs_agent_core import AgentRole, AgentStatus


class OSRSStrategicPlanner:
    """Handles strategic activity planning for OSRS swarm."""

    @staticmethod
    def plan_strategic_activities(coordinator: "OSRS_Swarm_Coordinator") -> list["SwarmActivity"]:
        """Plan strategic activities for the swarm."""
        from .swarm_coordinator import SwarmActivity
        
        activities = []

        try:
            # Plan resource gathering activity
            if OSRSStrategicPlanner.should_plan_resource_gathering(coordinator):
                activity = SwarmActivity(
                    activity_id=f"resource_gathering_{int(datetime.now().timestamp())}",
                    activity_type="resource_gathering",
                    description="Coordinated resource gathering across multiple locations",
                    participating_agents=["Agent-2", "Agent-6"],
                    start_time=datetime.now(),
                    end_time=None,
                    status="planned",
                    requirements={
                        "locations": ["Mining Guild", "Woodcutting Guild"],
                        "resources": ["Coal", "Iron ore", "Logs"],
                        "duration_minutes": 60,
                    },
                )
                activities.append(activity)

            # Plan combat activity
            if OSRSStrategicPlanner.should_plan_combat_activity(coordinator):
                activity = SwarmActivity(
                    activity_id=f"combat_training_{int(datetime.now().timestamp())}",
                    activity_type="combat_training",
                    description="Coordinated combat training and PvP preparation",
                    participating_agents=["Agent-1", "Agent-4"],
                    start_time=datetime.now(),
                    end_time=None,
                    status="planned",
                    requirements={
                        "training_area": "Wilderness",
                        "combat_level": 50,
                        "equipment": ["Rune armor", "Rune weapons"],
                    },
                )
                activities.append(activity)

        except Exception as e:
            coordinator.logger.error(f"Error planning strategic activities: {e}")

        return activities

    @staticmethod
    def should_plan_resource_gathering(coordinator: "OSRS_Swarm_Coordinator") -> bool:
        """Determine if resource gathering should be planned."""
        low_resource_agents = 0
        for agent in coordinator.agents.values():
            if agent.game_state and len(agent.game_state.inventory_items) < 10:
                low_resource_agents += 1

        return low_resource_agents >= 2

    @staticmethod
    def should_plan_combat_activity(coordinator: "OSRS_Swarm_Coordinator") -> bool:
        """Determine if combat activity should be planned."""
        combat_agents = [
            agent
            for agent in coordinator.agents.values()
            if agent.role == AgentRole.COMBAT_SPECIALIST and agent.status == AgentStatus.ACTIVE
        ]

        return len(combat_agents) >= 1

