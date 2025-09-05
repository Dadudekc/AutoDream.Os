"""
Pattern Analysis Models - Backward Compatibility Wrapper
========================================================

Backward compatibility wrapper for pattern analysis models.
V2 Compliance: < 30 lines, single responsibility, compatibility layer.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Import everything from the refactored modules
from .models_refactored import *

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