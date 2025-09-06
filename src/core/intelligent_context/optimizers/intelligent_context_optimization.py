"""
Intelligent Context Optimization - V2 Compliant Module
=====================================================

Main optimizer for intelligent context operations.
Coordinates all optimization components and provides unified interface.

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
from .agent_optimizer import AgentOptimizer
from .risk_optimizer import RiskOptimizer
from .prediction_optimizer import PredictionOptimizer


class IntelligentContextOptimization:
    """Main optimizer for intelligent context operations.

    Coordinates agent optimization, risk assessment, and success prediction for mission
    planning.
    """

    def __init__(self, engine):
        """Initialize context optimization."""
        self.engine = engine

        # Initialize component optimizers
        self.agent_optimizer = AgentOptimizer(engine)
        self.risk_optimizer = RiskOptimizer(engine)
        self.prediction_optimizer = PredictionOptimizer(engine)

    def optimize_agent_assignment(self, mission: MissionContext) -> Dict[str, Any]:
        """Optimize agent assignment for mission."""
        return self.agent_optimizer.optimize_agent_assignment(mission)

    def assess_mission_risks(self, mission: MissionContext) -> RiskAssessment:
        """Assess mission risks."""
        return self.risk_optimizer.assess_mission_risks(mission)

    def generate_success_predictions(
        self, mission: MissionContext
    ) -> SuccessPrediction:
        """Generate success predictions for mission."""
        return self.prediction_optimizer.generate_success_predictions(mission)

    def get_comprehensive_analysis(self, mission: MissionContext) -> Dict[str, Any]:
        """Get comprehensive analysis for mission."""
        start_time = time.time()

        try:
            # Get agent recommendations
            agent_analysis = self.optimize_agent_assignment(mission)

            # Get risk assessment
            risk_assessment = self.assess_mission_risks(mission)

            # Get success predictions
            success_prediction = self.generate_success_predictions(mission)

            # Calculate overall mission score
            mission_score = self._calculate_mission_score(
                mission, agent_analysis, risk_assessment, success_prediction
            )

            execution_time = (time.time() - start_time) * 1000

            return {
                "mission_id": mission.mission_id,
                "mission_score": mission_score,
                "agent_analysis": agent_analysis,
                "risk_assessment": risk_assessment,
                "success_prediction": success_prediction,
                "execution_time_ms": execution_time,
                "analysis_timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            return {
                "mission_id": mission.mission_id,
                "mission_score": 0.0,
                "error": str(e),
                "execution_time_ms": execution_time,
                "analysis_timestamp": datetime.now().isoformat(),
            }

    def _calculate_mission_score(
        self,
        mission: MissionContext,
        agent_analysis: Dict[str, Any],
        risk_assessment: RiskAssessment,
        success_prediction: SuccessPrediction,
    ) -> float:
        """Calculate overall mission score."""
        score = 0.0

        # Agent assignment score (40%)
        if agent_analysis.get("recommendations"):
            avg_agent_score = sum(
                rec.recommendation_score for rec in agent_analysis["recommendations"]
            ) / len(agent_analysis["recommendations"])
            score += avg_agent_score * 0.4

        # Risk assessment score (30%)
        risk_score = 1.0 - self.risk_optimizer.calculate_risk_score(mission)
        score += risk_score * 0.3

        # Success prediction score (30%)
        score += success_prediction.success_probability * 0.3

        return min(1.0, score)

    def get_optimization_status(self) -> Dict[str, Any]:
        """Get optimization status."""
        return {
            "agent_optimizer": self.agent_optimizer.get_optimizer_status(),
            "risk_optimizer": self.risk_optimizer.get_optimizer_status(),
            "prediction_optimizer": self.prediction_optimizer.get_optimizer_status(),
        }

    def get_optimization_metrics(self) -> Dict[str, Any]:
        """Get optimization metrics."""
        return {
            "total_optimizations": 0,  # Would track actual count
            "average_execution_time": 0.0,  # Would track actual time
            "success_rate": 0.0,  # Would track actual success rate
            "component_status": self.get_optimization_status(),
        }

    def shutdown(self):
        """Shutdown optimizer and cleanup resources."""
        # Cleanup any resources if needed
        pass
