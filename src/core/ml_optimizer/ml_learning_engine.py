#!/usr/bin/env python3
"""
ML Learning Engine - V2 Compliant Redirect
==========================================

V2 COMPLIANT: Modular architecture with clean separation of concerns.
Original monolithic implementation refactored into focused modules.

@version 2.0.0 - V2 COMPLIANCE MODULAR REFACTOR
@license MIT
"""

# Import the new modular orchestrator
from .learning import (
    MLLearningEngineOrchestrator,
    create_ml_learning_engine_orchestrator,
    PatternLearningEngine,
    PredictionEngine,
    ModelManagementEngine,
    FeatureAnalysisEngine
)

# Re-export for backward compatibility
MLLearningEngine = MLLearningEngineOrchestrator

# Export all public interfaces
__all__ = [
    'MLLearningEngine',
    'MLLearningEngineOrchestrator',
    'create_ml_learning_engine_orchestrator',
    'PatternLearningEngine',
    'PredictionEngine',
    'ModelManagementEngine',
    'FeatureAnalysisEngine'
]
