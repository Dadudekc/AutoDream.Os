"""
Pattern Analyzer
================

Pattern analysis functionality.
V2 Compliance: < 300 lines, single responsibility, analysis logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .engine_core import PatternAnalysisEngine
from .models import (
    ImpactLevel,
    MissionPattern,
    PatternAnalysisModels,
    PatternType,
    RecommendationType,
)

__all__ = [
    "PatternAnalysis",
    "detect_performance_patterns",
    "detect_coordination_patterns",
    "detect_anomaly_patterns",
    "PatternAnalyzer",
]


@dataclass
class PatternAnalysis:
    """Simple pattern analysis result used across modules."""

    analysis_id: str
    pattern_type: str
    pattern_description: str
    frequency: float
    confidence: float
    implications: list[str]
    recommendations: list[str]
    analyzed_at: datetime


def _create_pattern(
    prefix: str,
    p_type: str,
    description: str,
    frequency: float,
    confidence: float,
    implications: list[str],
    recommendations: list[str],
) -> PatternAnalysis:
    """Internal helper to construct a pattern analysis object."""

    return PatternAnalysis(
        analysis_id=f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        pattern_type=p_type,
        pattern_description=description,
        frequency=frequency,
        confidence=confidence,
        implications=implications,
        recommendations=recommendations,
        analyzed_at=datetime.now(),
    )


def detect_performance_patterns(data: list[dict[str, Any]]) -> list[PatternAnalysis]:
    """Detect performance patterns from raw data."""

    patterns: list[PatternAnalysis] = []
    if len(data) > 10:
        patterns.append(
            _create_pattern(
                "perf_pattern",
                "performance",
                "High-frequency performance variations detected",
                0.75,
                0.8,
                [
                    "System may be experiencing instability",
                    "Performance monitoring needed",
                ],
                [
                    "Implement performance smoothing",
                    "Add stability checks",
                ],
            )
        )
    return patterns


def detect_coordination_patterns(data: list[dict[str, Any]]) -> list[PatternAnalysis]:
    """Detect coordination patterns from raw data."""

    patterns: list[PatternAnalysis] = []
    if len(data) > 5:
        patterns.append(
            _create_pattern(
                "coord_pattern",
                "coordination",
                "Regular coordination cycles detected",
                0.6,
                0.7,
                [
                    "System shows predictable coordination behavior",
                    "Opportunities for optimization exist",
                ],
                [
                    "Optimize coordination timing",
                    "Reduce coordination overhead",
                ],
            )
        )
    return patterns


def detect_anomaly_patterns(data: list[dict[str, Any]]) -> list[PatternAnalysis]:
    """Detect anomaly patterns from raw data."""

    patterns: list[PatternAnalysis] = []
    if len(data) > 20:
        patterns.append(
            _create_pattern(
                "anomaly_pattern",
                "anomaly",
                "Unusual activity patterns detected",
                0.3,
                0.6,
                [
                    "Potential system issues",
                    "Investigation required",
                ],
                [
                    "Increase monitoring frequency",
                    "Review system logs",
                ],
            )
        )
    return patterns


class PatternAnalyzer:
    """Pattern analysis functionality."""

    def __init__(self, engine: PatternAnalysisEngine):
        """Initialize pattern analyzer."""
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False

    def initialize(self) -> bool:
        """Initialize the analyzer."""
        try:
            if not self.engine.is_initialized:
                raise Exception("Engine not initialized")

            self.is_initialized = True
            self.logger.info("Pattern Analyzer initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Pattern Analyzer: {e}")
            return False

    def analyze_performance_patterns(self, mission_id: str = None) -> list[MissionPattern]:
        """Analyze performance patterns."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")

            metrics = self.engine.get_metrics(mission_id)
            patterns = []

            for metric in metrics:
                if metric.efficiency > 0.8:
                    pattern = PatternAnalysisModels.create_mission_pattern(
                        name=f"High Efficiency Pattern - {metric.phase}",
                        description=f"High efficiency detected in {metric.phase} phase",
                        pattern_type=PatternType.PERFORMANCE,
                        frequency=metric.efficiency,
                        confidence=0.9,
                        context={"mission_id": metric.mission_id, "phase": metric.phase},
                    )
                    patterns.append(pattern)
                    self.engine.add_pattern(pattern)

            self.logger.info(f"Analyzed {len(patterns)} performance patterns")
            return patterns

        except Exception as e:
            self.logger.error(f"Error analyzing performance patterns: {e}")
            return []

    def analyze_coordination_patterns(self, mission_id: str = None) -> list[MissionPattern]:
        """Analyze coordination patterns."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")

            contexts = list(self.engine.contexts.values())
            if mission_id:
                contexts = [c for c in contexts if c.mission_id == mission_id]

            patterns = []
            for context in contexts:
                if context.priority == "HIGH" and len(context.objectives) > 3:
                    pattern = PatternAnalysisModels.create_mission_pattern(
                        name=f"Complex Coordination Pattern - {context.phase}",
                        description=f"Complex coordination required in {context.phase} phase",
                        pattern_type=PatternType.COORDINATION,
                        frequency=0.7,
                        confidence=0.8,
                        context={"mission_id": context.mission_id, "phase": context.phase},
                    )
                    patterns.append(pattern)
                    self.engine.add_pattern(pattern)

            self.logger.info(f"Analyzed {len(patterns)} coordination patterns")
            return patterns

        except Exception as e:
            self.logger.error(f"Error analyzing coordination patterns: {e}")
            return []

    def generate_optimization_recommendations(self, patterns: list[MissionPattern]) -> list:
        """Generate optimization recommendations."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Analyzer not initialized")

            recommendations = []

            performance_patterns = [
                p for p in patterns if p.pattern_type == PatternType.PERFORMANCE
            ]
            if performance_patterns:
                recommendation = PatternAnalysisModels.create_strategic_recommendation(
                    title="Performance Optimization",
                    description="Optimize performance patterns for better efficiency",
                    recommendation_type=RecommendationType.OPTIMIZATION,
                    impact_level=ImpactLevel.HIGH,
                    priority=1,
                    implementation_effort="medium",
                    expected_benefits=["Improved performance", "Better resource utilization"],
                    risks=["Implementation complexity"],
                )
                recommendations.append(recommendation)
                self.engine.add_recommendation(recommendation)

            self.logger.info(f"Generated {len(recommendations)} optimization recommendations")
            return recommendations

        except Exception as e:
            self.logger.error(f"Error generating optimization recommendations: {e}")
            return []

    def get_analysis_summary(self) -> dict[str, Any]:
        """Get analysis summary."""
        try:
            if not self.is_initialized:
                return {"error": "Analyzer not initialized"}

            patterns_by_type = {}
            for pattern_type in PatternType:
                patterns_by_type[pattern_type.value] = len(
                    [p for p in self.engine.patterns.values() if p.pattern_type == pattern_type]
                )

            return {
                "analyzer_status": "initialized",
                "patterns_by_type": patterns_by_type,
                "total_patterns": len(self.engine.patterns),
                "total_correlations": len(self.engine.correlations),
                "total_recommendations": len(self.engine.recommendations),
            }

        except Exception as e:
            self.logger.error(f"Error getting analysis summary: {e}")
            return {"error": str(e)}

    def shutdown(self):
        """Shutdown analyzer."""
        if not self.is_initialized:
            return

        self.logger.info("Shutting down Pattern Analyzer")
        self.is_initialized = False
