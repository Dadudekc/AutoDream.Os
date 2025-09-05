#!/usr/bin/env python3
"""
Pattern Analysis Package - V2 Compliance Module
==============================================

Modular pattern analysis system for V2 compliance.
Replaces monolithic pattern_analysis_system.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .pattern_analysis_models import (
    MissionPattern,
    PatternCorrelation,
    MissionContext,
    StrategicRecommendation,
    PatternAnalysisResult,
)
from .pattern_analysis_engine import PatternAnalysisEngine
from .pattern_analysis_orchestrator import (
    PatternAnalysisSystem,
    get_pattern_analysis_system,
    analyze_mission_patterns,
    add_mission_pattern,
    get_pattern_analysis_metrics,
)

__all__ = [
    'MissionPattern',
    'PatternCorrelation',
    'MissionContext',
    'StrategicRecommendation',
    'PatternAnalysisResult',
    'PatternAnalysisEngine',
    'PatternAnalysisSystem',
    'get_pattern_analysis_system',
    'analyze_mission_patterns',
    'add_mission_pattern',
    'get_pattern_analysis_metrics',
]
