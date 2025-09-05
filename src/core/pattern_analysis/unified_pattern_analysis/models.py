#!/usr/bin/env python3
"""
Pattern Analysis Models - V2 Compliance Module
==============================================

V2 compliance redirect to modular pattern analysis models.
Original monolithic implementation refactored into focused modules.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactoring)
Created: 2025-09-05
Purpose: V2 compliant modular pattern analysis models
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .models_refactored import *

# Backward compatibility maintained
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