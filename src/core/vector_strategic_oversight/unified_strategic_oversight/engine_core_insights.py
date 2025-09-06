"""
Strategic Oversight Engine Core Insights - KISS Simplified
=========================================================

Insight management functionality for strategic oversight operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined insight operations.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import logging
from typing import Dict, List, Optional
from .models import SwarmCoordinationInsight
from .enums import InsightType


class StrategicOversightEngineCoreInsights:
    """Insight management for strategic oversight engine."""

    def __init__(
        self, insights: Dict[str, SwarmCoordinationInsight], logger: logging.Logger
    ):
        """Initialize insight management."""
        self.insights = insights
        self.logger = logger

    def add_insight(self, insight: SwarmCoordinationInsight) -> bool:
        """Add a swarm coordination insight - simplified."""
        try:
            self.insights[insight.insight_id] = insight
            self.logger.info(f"Added swarm coordination insight: {insight.insight_id}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add swarm coordination insight: {e}")
            return False

    def get_insight(self, insight_id: str) -> Optional[SwarmCoordinationInsight]:
        """Get a swarm coordination insight by ID - simplified."""
        try:
            return self.insights.get(insight_id)
        except Exception as e:
            self.logger.error(f"Failed to get swarm coordination insight: {e}")
            return None

    def get_insights(
        self, insight_type: InsightType = None, limit: int = 10
    ) -> List[SwarmCoordinationInsight]:
        """Get swarm coordination insights - simplified."""
        try:
            insights = list(self.insights.values())

            if insight_type:
                insights = [i for i in insights if i.insight_type == insight_type]

            # Sort by creation date (newest first)
            insights.sort(key=lambda x: x.created_at, reverse=True)

            return insights[:limit]
        except Exception as e:
            self.logger.error(f"Failed to get swarm coordination insights: {e}")
            return []
