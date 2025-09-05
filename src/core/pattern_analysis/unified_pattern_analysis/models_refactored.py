"""
Pattern Analysis Models - Refactored Entry Point
================================================

Unified entry point for pattern analysis models with backward compatibility.
V2 Compliance: < 50 lines, single responsibility, unified interface.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Core models and enums
from .models_core import (
    PatternType, RecommendationType, ImpactLevel, AnalysisStatus,
    MissionPattern, PatternCorrelation, MissionContext
)

# Extended models
from .models_extended import (
    StrategicRecommendation, PatternAnalysisResult, PerformanceMetrics,
    ResourceUtilization, TimingPattern, CoordinationPattern
)

# Factory methods and configuration
from .models_factory import (
    PatternAnalysisConfig, PatternAnalysisModels
)

# Re-export everything for backward compatibility
__all__ = [
    # Enums
    'PatternType', 'RecommendationType', 'ImpactLevel', 'AnalysisStatus',
    
    # Core Models
    'MissionPattern', 'PatternCorrelation', 'MissionContext',
    
    # Extended Models
    'StrategicRecommendation', 'PatternAnalysisResult', 'PerformanceMetrics',
    'ResourceUtilization', 'TimingPattern', 'CoordinationPattern',
    
    # Configuration and Factory
    'PatternAnalysisConfig', 'PatternAnalysisModels'
]