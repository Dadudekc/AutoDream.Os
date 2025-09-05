#!/usr/bin/env python3
"""
ML Learning Engine Package
==========================

Modular ML learning engine system.
V2 COMPLIANT: Clean, focused, modular architecture.

@version 1.0.0 - V2 COMPLIANCE MODULAR PACKAGE
@license MIT
"""

# Import main orchestrator
from .ml_learning_engine_orchestrator import (
    MLLearningEngineOrchestrator,
    create_ml_learning_engine_orchestrator
)

# Import individual engines
from .pattern_learning_engine import (
    PatternLearningEngine,
    create_pattern_learning_engine
)

from .prediction_engine import (
    PredictionEngine,
    create_prediction_engine
)

from .model_management_engine import (
    ModelManagementEngine,
    create_model_management_engine
)

from .feature_analysis_engine import (
    FeatureAnalysisEngine,
    create_feature_analysis_engine
)

# Export all public interfaces
__all__ = [
    # Main orchestrator
    'MLLearningEngineOrchestrator',
    'create_ml_learning_engine_orchestrator',
    
    # Individual engines
    'PatternLearningEngine',
    'create_pattern_learning_engine',
    'PredictionEngine',
    'create_prediction_engine',
    'ModelManagementEngine',
    'create_model_management_engine',
    'FeatureAnalysisEngine',
    'create_feature_analysis_engine'
]
