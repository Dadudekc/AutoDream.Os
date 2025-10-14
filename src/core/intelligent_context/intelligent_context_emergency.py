#!/usr/bin/env python3
"""
Intelligent Context Emergency - V2 Compliance Module
===================================================

Emergency operations for intelligent context retrieval.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time

from .core_models import MissionContext
from .emergency_models import EmergencyContext, InterventionProtocol


class IntelligentContextEmergency:
    """Emergency operations for intelligent context retrieval."""

    def __init__(self, engine):
        """Initialize context emergency."""
        self.engine = engine

    def get_emergency_context(self, mission: MissionContext) -> EmergencyContext:
        """Get emergency context for mission."""
        start_time = time.time()

        try:
            emergency_context = EmergencyContext(
                emergency_id=f"emergency_{mission.mission_id}",
                mission_id=mission.mission_id,
                emergency_type="mission_critical",
                severity_level="high",
                affected_agents=list(mission.agent_assignments.keys()),
                intervention_protocols=self._get_intervention_protocols(mission),
                estimated_resolution_time=30.0,
            )

            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("emergency", True, execution_time)

            return emergency_context

        except Exception:
            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("emergency", False, execution_time)
            return EmergencyContext(
                emergency_id=f"emergency_{mission.mission_id}",
                mission_id=mission.mission_id,
                emergency_type="unknown",
                severity_level="unknown",
            )

    def get_intervention_protocols(self, mission: MissionContext) -> list[InterventionProtocol]:
        """Get intervention protocols for mission."""
        return self._get_intervention_protocols(mission)

    def _get_intervention_protocols(self, mission: MissionContext) -> list[str]:
        """Get intervention protocols for mission."""
        protocols = [
            "Emergency agent reassignment",
            "Mission priority escalation",
            "Resource reallocation",
            "Communication protocol activation",
        ]
        return protocols

    def create_emergency_protocol(
        self, mission: MissionContext, protocol_name: str
    ) -> InterventionProtocol:
        """Create emergency intervention protocol."""
        return InterventionProtocol(
            protocol_id=f"protocol_{mission.mission_id}_{protocol_name}",
            protocol_name=protocol_name,
            trigger_conditions=["Mission critical failure", "Agent unavailability"],
            intervention_steps=[
                "Assess emergency situation",
                "Activate backup agents",
                "Implement emergency procedures",
                "Monitor resolution progress",
            ],
            success_criteria=["Mission completion", "Agent availability restored"],
            estimated_duration=30.0,
            required_agents=list(mission.agent_assignments.keys()),
        )

    def assess_emergency_severity(self, mission: MissionContext) -> str:
        """Assess emergency severity level."""
        risk_factors = len(mission.risk_factors)
        agent_count = len(mission.agent_assignments)

        if risk_factors > 5 or agent_count < 2:
            return "critical"
        elif risk_factors > 3 or agent_count < 3:
            return "high"
        elif risk_factors > 1 or agent_count < 4:
            return "medium"
        else:
            return "low"

    def get_emergency_agents(self, mission: MissionContext) -> list[str]:
        """Get agents available for emergency intervention."""
        emergency_agents = []
        for agent_id, capability in self.engine.agent_capabilities.items():
            if capability.availability_status == "available":
                emergency_agents.append(agent_id)
        return emergency_agents

    def calculate_emergency_response_time(self, mission: MissionContext) -> float:
        """Calculate estimated emergency response time."""
        base_time = 15.0  # Base response time in minutes

        # Adjust based on risk factors
        risk_adjustment = len(mission.risk_factors) * 2.0
        base_time += risk_adjustment

        # Adjust based on agent availability
        available_agents = len(self.get_emergency_agents(mission))
        if available_agents < 2:
            base_time += 10.0
        elif available_agents < 4:
            base_time += 5.0

        return base_time
