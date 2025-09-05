#!/usr/bin/env python3
"""
ML Optimizer Orchestrator - V2 Compliance
=========================================

Main orchestrator for ML optimization operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from .ml_optimizer_models import (
    MLConfiguration, MLModel, OptimizationMetrics, MLOptimizationConfig,
    MLPrediction, LearningPattern, ModelState, MLOptimizationMetrics,
    MLStrategy, LearningPhase, OptimizationStatus
)
from .ml_learning_engine import MLLearningEngine


class VectorDatabaseMLOptimizer:
    """Main orchestrator for vector database ML optimization."""
    
    def __init__(self, config: Optional[MLConfiguration] = None):
        """Initialize ML optimizer orchestrator."""
        self.config = config or MLConfiguration(config_id="default")
        self.learning_engine = MLLearningEngine()
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
        self.models: Dict[str, MLModel] = {}
        self.predictions: Dict[str, MLPrediction] = {}
        self.learning_patterns: Dict[str, LearningPattern] = {}
    
    def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            if not self.learning_engine.initialize():
                raise Exception("Failed to initialize learning engine")
            
            self.is_initialized = True
            self.logger.info("Vector Database ML Optimizer initialized")
            return True
        except Exception as e:
            self.logger.error(f"Failed to initialize Vector Database ML Optimizer: {e}")
            return False
    
    def add_model(self, model: MLModel) -> bool:
        """Add an ML model."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator not initialized")
            
            self.models[model.model_id] = model
            self.logger.debug(f"Added model: {model.name}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding model: {e}")
            return False
    
    def get_model(self, model_id: str) -> Optional[MLModel]:
        """Get an ML model."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.models.get(model_id)
    
    def get_models_by_strategy(self, strategy: MLStrategy) -> List[MLModel]:
        """Get models by strategy."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [
            model for model in self.models.values()
            if model.strategy == strategy
        ]
    
    def predict(self, model_id: str, input_data: Dict[str, Any]) -> Optional[MLPrediction]:
        """Make a prediction using a model."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator not initialized")
            
            model = self.get_model(model_id)
            if not model:
                self.logger.warning(f"Model {model_id} not found")
                return None
            
            # Use learning engine for prediction
            prediction = self.learning_engine.predict(model_id, input_data)
            if prediction:
                self.predictions[prediction.prediction_id] = prediction
            
            return prediction
        except Exception as e:
            self.logger.error(f"Error making prediction: {e}")
            return None
    
    def add_learning_pattern(self, pattern: LearningPattern) -> bool:
        """Add a learning pattern."""
        try:
            if not self.is_initialized:
                raise RuntimeError("Orchestrator not initialized")
            
            self.learning_patterns[pattern.pattern_id] = pattern
            self.logger.debug(f"Added learning pattern: {pattern.pattern_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding learning pattern: {e}")
            return False
    
    def get_learning_pattern(self, pattern_id: str) -> Optional[LearningPattern]:
        """Get a learning pattern."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.learning_patterns.get(pattern_id)
    
    def get_learning_patterns_by_type(self, pattern_type: str) -> List[LearningPattern]:
        """Get learning patterns by type."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return [
            pattern for pattern in self.learning_patterns.values()
            if pattern.pattern_type == pattern_type
        ]
    
    def get_optimizer_status(self) -> Dict[str, Any]:
        """Get optimizer status."""
        if not self.is_initialized:
            return {'status': 'not_initialized'}
        
        return {
            'status': 'initialized',
            'models_count': len(self.models),
            'predictions_count': len(self.predictions),
            'learning_patterns_count': len(self.learning_patterns),
            'learning_engine_initialized': self.learning_engine.is_initialized
        }
    
    def shutdown(self):
        """Shutdown orchestrator."""
        if not self.is_initialized:
            return
        
        self.logger.info("Shutting down Vector Database ML Optimizer")
        self.learning_engine.shutdown()
        self.is_initialized = False


# Factory functions
def create_vector_database_ml_optimizer(config: Optional[MLConfiguration] = None) -> VectorDatabaseMLOptimizer:
    """Create a vector database ML optimizer."""
    return VectorDatabaseMLOptimizer(config)


def get_vector_database_ml_optimizer(config: Optional[MLConfiguration] = None) -> VectorDatabaseMLOptimizer:
    """Get or create a vector database ML optimizer."""
    return create_vector_database_ml_optimizer(config)
