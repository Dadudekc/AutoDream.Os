#!/usr/bin/env python3
"""
Pattern Analysis Models Refactored - V2 Compliance Module
=========================================================

Refactored models.py for V2 compliance.
Maintains backward compatibility while using modular architecture.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

# V2 COMPLIANCE REFACTOR - Import from modular components
from .models_core import (
    PatternType,
    RecommendationType,
    ImpactLevel,
    MissionPattern,
    PatternCorrelation,
    MissionContext,
    StrategicRecommendation,
    create_pattern_id,
    create_correlation_id,
    create_context_id,
    create_recommendation_id
)

from .models_extended import (
    PatternAnalysisResult,
    PerformanceMetrics,
    ResourceUtilization,
    TimingPattern,
    CoordinationPattern,
    create_analysis_id,
    create_metrics_id,
    create_utilization_id,
    create_timing_id,
    create_coordination_id
)

# Re-export for backward compatibility
__all__ = [
    # Core models
    'PatternType',
    'RecommendationType',
    'ImpactLevel',
    'MissionPattern',
    'PatternCorrelation',
    'MissionContext',
    'StrategicRecommendation',
    
    # Extended models
    'PatternAnalysisResult',
    'PerformanceMetrics',
    'ResourceUtilization',
    'TimingPattern',
    'CoordinationPattern',
    
    # ID generators
    'create_pattern_id',
    'create_correlation_id',
    'create_context_id',
    'create_recommendation_id',
    'create_analysis_id',
    'create_metrics_id',
    'create_utilization_id',
    'create_timing_id',
    'create_coordination_id'
]
