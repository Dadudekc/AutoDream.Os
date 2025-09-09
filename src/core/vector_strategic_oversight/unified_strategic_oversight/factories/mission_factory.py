"""
Strategic Oversight Mission Factory - V2 Compliance Module
=========================================================

Factory methods for creating strategic missions.

V2 Compliance: < 300 lines, single responsibility, mission factory.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import uuid
from datetime import datetime

from ..data_models import StrategicMission
from ..enums import PriorityLevel


class MissionFactory:
    """Factory class for creating strategic missions."""

    @staticmethod
    def create_strategic_mission(
        title: str,
        description: str,
        priority: PriorityLevel,
        assigned_agents: list[str],
        objectives: list[str],
        success_criteria: list[str],
        deadline: datetime | None = None,
        dependencies: list[str] = None,
    ) -> StrategicMission:
        """Create strategic mission."""
        return StrategicMission(
            mission_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=priority,
            assigned_agents=assigned_agents,
            objectives=objectives,
            success_criteria=success_criteria,
            deadline=deadline,
            dependencies=dependencies or [],
            created_at=datetime.now(),
            status="PENDING",
        )

    @staticmethod
    def create_quick_mission(
        title: str, description: str, assigned_agent: str, objective: str
    ) -> StrategicMission:
        """Create quick mission with minimal parameters."""
        return StrategicMission(
            mission_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=PriorityLevel.MEDIUM,
            assigned_agents=[assigned_agent],
            objectives=[objective],
            success_criteria=["Complete objective"],
            created_at=datetime.now(),
            status="PENDING",
        )

    @staticmethod
    def create_emergency_mission(
        title: str, description: str, assigned_agents: list[str], objectives: list[str]
    ) -> StrategicMission:
        """Create emergency mission with high priority."""
        return StrategicMission(
            mission_id=str(uuid.uuid4()),
            title=title,
            description=description,
            priority=PriorityLevel.HIGH,
            assigned_agents=assigned_agents,
            objectives=objectives,
            success_criteria=["Resolve emergency"],
            created_at=datetime.now(),
            status="ACTIVE",
        )
