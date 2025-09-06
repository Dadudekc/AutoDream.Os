"""
Recommendation Engine Base - V2 Compliant Module
===============================================

Base functionality for optimization recommendation generation.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
import logging

from ..vector_integration_models import (
    OptimizationRecommendation,
    PerformanceMetrics,
    TrendAnalysis,
    create_optimization_recommendation,
)


class RecommendationEngineBase:
    """Base engine for optimization recommendation generation."""

    def __init__(self, config):
        """Initialize recommendation engine."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.recommendation_cache: List[OptimizationRecommendation] = []

    def get_latest_recommendations(self) -> List[OptimizationRecommendation]:
        """Get latest recommendations from cache."""
        return self.recommendation_cache.copy()

    def get_recommendations_by_priority(
        self, priority: str
    ) -> List[OptimizationRecommendation]:
        """Get recommendations filtered by priority."""
        return [rec for rec in self.recommendation_cache if rec.priority == priority]

    def get_recommendations_by_category(
        self, category: str
    ) -> List[OptimizationRecommendation]:
        """Get recommendations filtered by category."""
        return [rec for rec in self.recommendation_cache if rec.category == category]

    def clear_recommendation_cache(self):
        """Clear all recommendations from cache."""
        self.recommendation_cache.clear()
        self.logger.info("Cleared recommendation cache")

    def add_recommendation(self, recommendation: OptimizationRecommendation):
        """Add recommendation to cache."""
        self.recommendation_cache.append(recommendation)
        self.logger.debug(f"Added recommendation: {recommendation.title}")

    def get_recommendation_count(self) -> int:
        """Get total number of recommendations in cache."""
        return len(self.recommendation_cache)

    def get_recommendation_summary(self) -> Dict[str, Any]:
        """Get summary of recommendations."""
        if not self.recommendation_cache:
            return {"total": 0, "by_priority": {}, "by_category": {}}

        by_priority = {}
        by_category = {}

        for rec in self.recommendation_cache:
            # Count by priority
            priority = rec.priority
            by_priority[priority] = by_priority.get(priority, 0) + 1

            # Count by category
            category = rec.category
            by_category[category] = by_category.get(category, 0) + 1

        return {
            "total": len(self.recommendation_cache),
            "by_priority": by_priority,
            "by_category": by_category,
        }
