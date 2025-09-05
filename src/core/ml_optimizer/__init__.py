#!/usr/bin/env python3
"""
ML Optimizer Package - V2 Compliance
====================================

Modular vector database ML optimization system with V2 compliance.
Replaces the monolithic vector_database_ml_optimizer.py.

Package Structure:
- ml_optimizer_models.py: Data models and configuration
- ml_learning_engine.py: Machine learning engine for pattern recognition
- ml_optimizer_orchestrator.py: Main orchestrator and unified interface

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

# Import main classes for easy access
from .ml_optimizer_models import (
    MLConfiguration,
    MLModel,
    OptimizationMetrics,
    MLStrategy,
    LearningPhase,
    OptimizationStatus,
    create_ml_model,
    create_learning_pattern,
    create_optimization_metrics,
    create_ml_configuration
)

from .ml_learning_engine import MLLearningEngine

from .ml_optimizer_orchestrator import (
    VectorDatabaseMLOptimizer,
    create_vector_database_ml_optimizer,
    get_vector_database_ml_optimizer
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular vector database ML optimization system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "VectorDatabaseMLOptimizer",
    "MLLearningEngine",
    
    # Data models
    "MLOptimizationConfig",
    "MLPrediction",
    "LearningPattern",
    "ModelState",
    "MLOptimizationMetrics",
    
    # Enums
    "MLStrategy",
    "LearningMode",
    "OptimizationType",
    
    # Factory functions
    "create_default_config",
    "create_ml_prediction",
    "create_learning_pattern",
    "create_model_state",
    "create_optimization_metrics",
    
    # Constants
    "DEFAULT_ML_STRATEGIES",
    "LEARNING_MODE_CONFIGS",
    
    # Main interface functions
    "create_vector_database_ml_optimizer",
    "get_vector_database_ml_optimizer"
]
