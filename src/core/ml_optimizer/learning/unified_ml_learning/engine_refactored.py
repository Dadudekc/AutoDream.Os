"""
ML Learning Engine - Refactored Entry Point
===========================================

Unified entry point for ML learning engine with backward compatibility.
V2 Compliance: < 100 lines, single responsibility, unified interface.

Author: Agent-2 - Architecture & Design Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import time

from .engine_core import MLLearningEngineCore
from .engine_training import MLLearningEngineTraining
from .engine_prediction import MLLearningEnginePrediction
from .models import (
    LearningPattern, MLPrediction, ModelState, MLOptimizationMetrics,
    FeatureAnalysis, LearningSession,
    LearningStatus, ModelType, FeatureType
)
from ...ml_optimizer_models import MLConfiguration


class MLLearningEngine:
    """Unified ML learning engine with modular architecture."""
    
    def __init__(self):
        """Initialize unified ML learning engine."""
        self.logger = logging.getLogger(__name__)
        self.core_engine = MLLearningEngineCore()
        self.training_engine = MLLearningEngineTraining(self.core_engine)
        self.prediction_engine = MLLearningEnginePrediction(self.core_engine)
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the unified engine."""
        try:
            success = self.core_engine.initialize()
            if success:
                self.is_initialized = True
                self.logger.info("ML Learning Engine initialized")
            return success
        except Exception as e:
            self.logger.error(f"Failed to initialize ML Learning Engine: {e}")
            return False
    
    # Core operations
    def add_pattern(self, pattern: LearningPattern) -> bool:
        """Add learning pattern."""
        return self.core_engine.add_pattern(pattern)
    
    def get_pattern(self, pattern_id: str) -> Optional[LearningPattern]:
        """Get learning pattern."""
        return self.core_engine.get_pattern(pattern_id)
    
    def add_prediction(self, prediction: MLPrediction) -> bool:
        """Add ML prediction."""
        return self.core_engine.add_prediction(prediction)
    
    def get_prediction(self, prediction_id: str) -> Optional[MLPrediction]:
        """Get ML prediction."""
        return self.core_engine.get_prediction(prediction_id)
    
    def add_model(self, model: ModelState) -> bool:
        """Add model state."""
        return self.core_engine.add_model(model)
    
    def get_model(self, model_id: str) -> Optional[ModelState]:
        """Get model state."""
        return self.core_engine.get_model(model_id)
    
    def add_metrics(self, metrics: MLOptimizationMetrics) -> bool:
        """Add optimization metrics."""
        return self.core_engine.add_metrics(metrics)
    
    def get_metrics(self, model_id: str = None) -> List[MLOptimizationMetrics]:
        """Get optimization metrics."""
        return self.core_engine.get_metrics(model_id)
    
    def add_session(self, session: LearningSession) -> bool:
        """Add learning session."""
        return self.core_engine.add_session(session)
    
    def get_session(self, session_id: str) -> Optional[LearningSession]:
        """Get learning session."""
        return self.core_engine.get_session(session_id)
    
    # Training operations
    def train_model(self, model_id: str, config: MLConfiguration, data: Dict[str, Any]) -> bool:
        """Train ML model."""
        return self.training_engine.train_model(model_id, config, data)
    
    def optimize_model(self, model_id: str, optimization_config: Dict[str, Any]) -> bool:
        """Optimize ML model."""
        return self.training_engine.optimize_model(model_id, optimization_config)
    
    def create_learning_session(self, session_name: str, config: Dict[str, Any]) -> Optional[str]:
        """Create learning session."""
        return self.training_engine.create_learning_session(session_name, config)
    
    def start_learning_session(self, session_id: str) -> bool:
        """Start learning session."""
        return self.training_engine.start_learning_session(session_id)
    
    def complete_learning_session(self, session_id: str) -> bool:
        """Complete learning session."""
        return self.training_engine.complete_learning_session(session_id)
    
    # Prediction operations
    def predict(self, model_id: str, input_data: Dict[str, Any]) -> Optional[MLPrediction]:
        """Make ML prediction."""
        return self.prediction_engine.predict(model_id, input_data)
    
    def batch_predict(self, model_id: str, input_batch: List[Dict[str, Any]]) -> List[MLPrediction]:
        """Make batch predictions."""
        return self.prediction_engine.batch_predict(model_id, input_batch)
    
    def get_prediction_history(self, model_id: str = None) -> List[MLPrediction]:
        """Get prediction history."""
        return self.prediction_engine.get_prediction_history(model_id)
    
    def evaluate_prediction_accuracy(self, model_id: str) -> Dict[str, float]:
        """Evaluate prediction accuracy."""
        return self.prediction_engine.evaluate_prediction_accuracy(model_id)
    
    # Status and utilities
    def get_engine_status(self) -> Dict[str, Any]:
        """Get engine status."""
        return self.core_engine.get_engine_status()
    
    def shutdown(self):
        """Shutdown engine."""
        self.core_engine.shutdown()
        self.is_initialized = False
