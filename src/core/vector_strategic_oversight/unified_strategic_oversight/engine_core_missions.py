"""
Strategic Oversight Engine Core Missions - KISS Simplified
=========================================================

Mission management functionality for strategic oversight operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined mission operations.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Optional
from .models import StrategicMission
from .enums import MissionStatus


class StrategicOversightEngineCoreMissions:
    """Mission management for strategic oversight engine."""

    def __init__(self, missions: Dict[str, StrategicMission], logger: logging.Logger):
        """Initialize mission management."""
        self.missions = missions
        self.logger = logger

    def add_mission(self, mission: StrategicMission) -> bool:
        """Add a strategic mission - simplified."""
        try:
            self.missions[mission.mission_id] = mission
            self.logger.info(f"Added strategic mission: {mission.mission_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add strategic mission: {e}")
            return False

    def get_mission(self, mission_id: str) -> Optional[StrategicMission]:
        """Get a strategic mission by ID - simplified."""
        try:
            return self.missions.get(mission_id)
        except Exception as e:
            self.logger.error(f"Failed to get strategic mission: {e}")
            return None

    def get_missions(
        self, status: MissionStatus = None, limit: int = 10
    ) -> List[StrategicMission]:
        """Get strategic missions - simplified."""
        try:
            missions = list(self.missions.values())

            if status:
                missions = [m for m in missions if m.status == status]

            # Sort by creation date (newest first)
            missions.sort(key=lambda x: x.created_at, reverse=True)

            return missions[:limit]
        except Exception as e:
            self.logger.error(f"Failed to get strategic missions: {e}")
            return []
