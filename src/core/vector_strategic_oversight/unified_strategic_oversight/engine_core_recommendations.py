"""
Strategic Oversight Engine Core Recommendations - KISS Simplified
================================================================

Recommendation management functionality for strategic oversight operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined recommendation operations.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Optional
from .models import StrategicRecommendation
from .enums import PriorityLevel


class StrategicOversightEngineCoreRecommendations:
    """Recommendation management for strategic oversight engine."""

    def __init__(
        self,
        recommendations: Dict[str, StrategicRecommendation],
        logger: logging.Logger,
    ):
        """Initialize recommendation management."""
        self.recommendations = recommendations
        self.logger = logger

    def add_recommendation(self, recommendation: StrategicRecommendation) -> bool:
        """Add a strategic recommendation - simplified."""
        try:
            self.recommendations[recommendation.recommendation_id] = recommendation
            self.logger.info(
                f"Added strategic recommendation: {recommendation.recommendation_id}"
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to add strategic recommendation: {e}")
            return False

    def get_recommendation(
        self, recommendation_id: str
    ) -> Optional[StrategicRecommendation]:
        """Get a strategic recommendation by ID - simplified."""
        try:
            return self.recommendations.get(recommendation_id)
        except Exception as e:
            self.logger.error(f"Failed to get strategic recommendation: {e}")
            return None

    def get_recommendations(
        self, priority: PriorityLevel = None, limit: int = 10
    ) -> List[StrategicRecommendation]:
        """Get strategic recommendations - simplified."""
        try:
            recommendations = list(self.recommendations.values())

            if priority:
                recommendations = [r for r in recommendations if r.priority == priority]

            # Sort by priority and creation date
            recommendations.sort(
                key=lambda x: (x.priority.value, x.created_at), reverse=True
            )

            return recommendations[:limit]
        except Exception as e:
            self.logger.error(f"Failed to get strategic recommendations: {e}")
            return []
