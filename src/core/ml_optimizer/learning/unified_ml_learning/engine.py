"""
ML Learning Engine - Backward Compatibility Wrapper
==================================================

Backward compatibility wrapper for ML learning engine.
V2 Compliance: < 30 lines, single responsibility, compatibility layer.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

# Import everything from the refactored engine
from .engine_refactored import *

# Re-export everything for backward compatibility
__all__ = [
    'MLLearningEngine',
    'LearningPattern', 'MLPrediction', 'ModelState', 'MLOptimizationMetrics',
    'FeatureAnalysis', 'LearningSession',
    'LearningStatus', 'ModelType', 'FeatureType'
]