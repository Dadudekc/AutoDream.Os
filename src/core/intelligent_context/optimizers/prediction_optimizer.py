"""
Prediction Optimizer - V2 Compliant Module
==========================================

Optimizes success predictions and recommendations.
Extracted from intelligent_context_optimization.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any, Dict, List
from datetime import datetime

from ..intelligent_context_models import (
    MissionContext,
    AgentCapability,
    SearchResult,
    AgentRecommendation,
    RiskAssessment,
    SuccessPrediction,
    MissionPhase,
    AgentStatus,
    RiskLevel,
)


class PredictionOptimizer:
    """Optimizes success predictions and recommendations.

    Handles success prediction generation, factor analysis, and recommendation creation.
    """

    def __init__(self, engine):
        """Initialize prediction optimizer."""
        self.engine = engine

    def generate_success_predictions(
        self, mission: MissionContext
    ) -> SuccessPrediction:
        """Generate success predictions for mission."""
        start_time = time.time()

        try:
            historical_patterns = self._find_similar_missions(mission)
            success_probability = self._calculate_success_probability(
                mission, historical_patterns
            )
            key_factors = self._identify_key_success_factors(mission)
            potential_bottlenecks = self._identify_bottlenecks(mission)

            prediction = SuccessPrediction(
                prediction_id=f"prediction_{mission.mission_id}",
                success_probability=success_probability,
                confidence_level=0.8,
                key_factors=key_factors,
                potential_bottlenecks=potential_bottlenecks,
                recommended_actions=self._generate_recommended_actions(mission),
            )

            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("prediction", True, execution_time)

            return prediction

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("prediction", False, execution_time)
            return SuccessPrediction(
                prediction_id=f"prediction_{mission.mission_id}",
                success_probability=0.5,
                confidence_level=0.0,
                key_factors=[],
                potential_bottlenecks=[],
                recommended_actions=[],
            )

    def _find_similar_missions(self, mission: MissionContext) -> List[SearchResult]:
        """Find similar missions for pattern analysis."""
        # This would typically search historical mission data
        # For now, return empty list as placeholder
        return []

    def _calculate_success_probability(
        self, mission: MissionContext, historical_patterns: List[SearchResult]
    ) -> float:
        """Calculate success probability."""
        base_probability = 0.7

        # Adjust based on risk factors
        risk_adjustment = len(mission.risk_factors) * -0.1
        base_probability += risk_adjustment

        # Adjust based on agent assignments
        agent_adjustment = len(mission.agent_assignments) * 0.05
        base_probability += agent_adjustment

        # Adjust based on historical patterns
        if historical_patterns:
            base_probability += 0.1

        return max(0.0, min(1.0, base_probability))

    def _identify_key_success_factors(self, mission: MissionContext) -> List[str]:
        """Identify key success factors."""
        factors = []

        if len(mission.agent_assignments) >= 3:
            factors.append("Adequate agent coverage")

        if len(mission.success_criteria) > 0:
            factors.append("Clear success criteria")

        if mission.current_phase != MissionPhase.EMERGENCY.value:
            factors.append("Stable mission phase")

        return factors

    def _identify_bottlenecks(self, mission: MissionContext) -> List[str]:
        """Identify potential bottlenecks."""
        bottlenecks = []

        if len(mission.critical_path) > 5:
            bottlenecks.append("Complex critical path")

        if len(mission.agent_assignments) < 2:
            bottlenecks.append("Limited agent availability")

        if len(mission.risk_factors) > 3:
            bottlenecks.append("High risk concentration")

        return bottlenecks

    def _generate_recommended_actions(self, mission: MissionContext) -> List[str]:
        """Generate recommended actions."""
        actions = []

        if len(mission.agent_assignments) < 3:
            actions.append("Assign additional agents")

        if len(mission.risk_factors) > 2:
            actions.append("Implement risk mitigation strategies")

        actions.append("Monitor progress regularly")
        actions.append("Maintain communication channels")

        return actions

    def get_prediction_confidence(self, mission: MissionContext) -> float:
        """Get prediction confidence level."""
        confidence = 0.5  # Base confidence

        # Increase confidence based on mission clarity
        if len(mission.success_criteria) > 0:
            confidence += 0.2

        # Increase confidence based on agent assignments
        if len(mission.agent_assignments) >= 2:
            confidence += 0.2

        # Decrease confidence based on risk factors
        if len(mission.risk_factors) > 2:
            confidence -= 0.1

        return max(0.0, min(1.0, confidence))

    def get_prediction_summary(self, mission: MissionContext) -> Dict[str, Any]:
        """Get prediction summary for mission."""
        prediction = self.generate_success_predictions(mission)
        confidence = self.get_prediction_confidence(mission)

        return {
            "success_probability": prediction.success_probability,
            "confidence_level": confidence,
            "key_factors_count": len(prediction.key_factors),
            "bottlenecks_count": len(prediction.potential_bottlenecks),
            "recommended_actions_count": len(prediction.recommended_actions),
        }

    def get_prediction_trends(self) -> Dict[str, Any]:
        """Get prediction trends across missions."""
        # This would typically analyze historical prediction data
        # For now, return placeholder data
        return {
            "average_success_rate": 0.75,
            "prediction_accuracy": 0.82,
            "common_success_factors": ["clear_criteria", "adequate_resources"],
            "common_bottlenecks": ["resource_constraints", "timeline_pressure"],
        }

    def get_optimizer_status(self) -> Dict[str, Any]:
        """Get optimizer status."""
        return {
            "prediction_count": 0,  # Would track actual count
            "trends": self.get_prediction_trends(),
        }
