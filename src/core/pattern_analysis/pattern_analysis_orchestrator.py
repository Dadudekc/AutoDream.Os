#!/usr/bin/env python3
"""
Pattern Analysis Orchestrator - V2 Compliance Module
====================================================

Main coordination logic for pattern analysis operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from typing import List, Dict, Any, Optional

from .pattern_analysis_models import (
    MissionPattern,
    PatternCorrelation,
    MissionContext,
    StrategicRecommendation,
    PatternAnalysisResult,
    PatternMetrics,
    PatternAnalysisConfig,
)
from .pattern_analysis_engine import PatternAnalysisEngine


class PatternAnalysisSystem:
    """Main orchestrator for pattern analysis operations."""

    def __init__(self, config: PatternAnalysisConfig = None):
        """Initialize pattern analysis system."""
        self.config = config or PatternAnalysisConfig()
        self.engine = PatternAnalysisEngine(self.config)

    def analyze_mission_patterns(
        self, mission_context: MissionContext
    ) -> PatternAnalysisResult:
        """Analyze mission patterns for strategic decision making."""
        return self.engine.analyze_mission_patterns(mission_context)

    def add_pattern(self, pattern: MissionPattern) -> bool:
        """Add a new mission pattern."""
        return self.engine.add_pattern(pattern)

    def get_pattern(self, pattern_id: str) -> Optional[MissionPattern]:
        """Get pattern by ID."""
        return self.engine.get_pattern(pattern_id)

    def get_metrics(self) -> PatternMetrics:
        """Get pattern analysis metrics."""
        return self.engine.get_metrics()

    def clear_old_patterns(self, days: int = 30) -> int:
        """Clear patterns older than specified days."""
        return self.engine.clear_old_patterns(days)

    # ================================
    # CONVENIENCE METHODS
    # ================================

    def analyze_success_patterns(
        self, mission_context: MissionContext
    ) -> PatternAnalysisResult:
        """Analyze success patterns specifically."""
        # Filter to only success patterns
        original_patterns = self.engine.mission_patterns.copy()
        success_patterns = {
            pid: pattern
            for pid, pattern in original_patterns.items()
            if pattern.success_rate > 0.7
        }

        # Temporarily replace patterns
        self.engine.mission_patterns = success_patterns
        result = self.analyze_mission_patterns(mission_context)

        # Restore original patterns
        self.engine.mission_patterns = original_patterns

        return result

    def analyze_risk_patterns(
        self, mission_context: MissionContext
    ) -> PatternAnalysisResult:
        """Analyze risk patterns specifically."""
        # Filter to patterns with high risk factors
        original_patterns = self.engine.mission_patterns.copy()
        risk_patterns = {
            pid: pattern
            for pid, pattern in original_patterns.items()
            if len(pattern.risk_factors) > 2
        }

        # Temporarily replace patterns
        self.engine.mission_patterns = risk_patterns
        result = self.analyze_mission_patterns(mission_context)

        # Restore original patterns
        self.engine.mission_patterns = original_patterns

        return result

    def get_pattern_summary(self) -> Dict[str, Any]:
        """Get summary of all patterns."""
        patterns = list(self.engine.mission_patterns.values())

        if not patterns:
            return {"message": "No patterns available"}

        pattern_types = {}
        for pattern in patterns:
            pattern_type = pattern.pattern_type
            if pattern_type not in pattern_types:
                pattern_types[pattern_type] = 0
            pattern_types[pattern_type] += 1

        return {
            "total_patterns": len(patterns),
            "pattern_types": pattern_types,
            "average_success_rate": (
                sum(p.success_rate for p in patterns) / len(patterns)
            ),
            "high_success_patterns": len([p for p in patterns if p.success_rate > 0.8]),
            "recent_patterns": len([p for p in patterns if p.usage_count > 0]),
        }

    def generate_strategic_insights(
        self, mission_context: MissionContext
    ) -> List[StrategicRecommendation]:
        """Generate strategic insights and recommendations."""
        analysis_result = self.analyze_mission_patterns(mission_context)
        return analysis_result.recommendations


# ================================
# GLOBAL INSTANCE
# ================================

_global_pattern_system = None


def get_pattern_analysis_system() -> PatternAnalysisSystem:
    """Get global pattern analysis system instance."""
    global _global_pattern_system

    if _global_pattern_system is None:
        _global_pattern_system = PatternAnalysisSystem()

    return _global_pattern_system


# ================================
# CONVENIENCE FUNCTIONS
# ================================


def analyze_mission_patterns(mission_context: MissionContext) -> PatternAnalysisResult:
    """Convenience function to analyze mission patterns."""
    system = get_pattern_analysis_system()
    return system.analyze_mission_patterns(mission_context)


def add_mission_pattern(pattern: MissionPattern) -> bool:
    """Convenience function to add mission pattern."""
    system = get_pattern_analysis_system()
    return system.add_pattern(pattern)


def get_pattern_analysis_metrics() -> PatternMetrics:
    """Convenience function to get pattern analysis metrics."""
    system = get_pattern_analysis_system()
    return system.get_metrics()
