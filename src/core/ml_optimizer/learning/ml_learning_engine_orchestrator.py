#!/usr/bin/env python3
"""
ML Learning Engine Orchestrator
===============================

Main orchestrator for ML learning engine system.
Coordinates pattern learning, prediction generation, model management, and feature analysis.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..ml_optimizer_models import (
    MLOptimizationConfig, LearningPattern, MLPrediction, ModelState,
    MLOptimizationMetrics, create_default_config
)
from .pattern_learning_engine import PatternLearningEngine, create_pattern_learning_engine
from .prediction_engine import PredictionEngine, create_prediction_engine
from .model_management_engine import ModelManagementEngine, create_model_management_engine
from .feature_analysis_engine import FeatureAnalysisEngine, create_feature_analysis_engine


class MLLearningEngineOrchestrator:
    """Main orchestrator for ML learning engine system"""
    
    def __init__(self, config: Optional[MLOptimizationConfig] = None):
        """Initialize ML learning engine orchestrator"""
        self.logger = logging.getLogger(__name__)
        self.config = config or create_default_config()
        
        # Validate configuration
        try:
            self.config.validate()
        except Exception as e:
            self.logger.error(f"Invalid ML configuration: {e}")
            raise
        
        # Initialize engines
        self.pattern_engine = create_pattern_learning_engine(self.config)
        self.prediction_engine = create_prediction_engine(self.config, self.pattern_engine)
        self.model_engine = create_model_management_engine(self.config, self.pattern_engine)
        self.feature_engine = create_feature_analysis_engine()
        
        # Performance tracking
        self.metrics = MLOptimizationMetrics()
        
        self.logger.info("ML Learning Engine Orchestrator initialized")
    
    def learn_pattern(self, pattern_type: str, features: Dict[str, Any], 
                     target_value: Any, pattern_id: Optional[str] = None) -> bool:
        """Learn a new pattern or update existing one"""
        try:
            # Extract features if raw data provided
            if not isinstance(features, dict):
                features = self.feature_engine.extract_features(features)
            
            success = self.pattern_engine.learn_pattern(
                pattern_type, features, target_value, pattern_id
            )
            
            if success:
                self.metrics.increment_patterns_learned()
            
            return success
        except Exception as e:
            self.logger.error(f"Error learning pattern: {e}")
            return False
    
    def generate_prediction(self, prediction_type: str, input_features: Dict[str, Any],
                          cache_key: Optional[str] = None) -> MLPrediction:
        """Generate prediction based on learned patterns"""
        try:
            # Extract features if raw data provided
            if not isinstance(input_features, dict):
                input_features = self.feature_engine.extract_features(input_features)
            
            prediction = self.prediction_engine.generate_prediction(
                prediction_type, input_features, cache_key
            )
            
            self.metrics.increment_predictions_generated()
            return prediction
        except Exception as e:
            self.logger.error(f"Error generating prediction: {e}")
            # Return error prediction
            from ..ml_optimizer_models import create_ml_prediction
            return create_ml_prediction(
                prediction_type=prediction_type,
                predicted_value=None,
                confidence=0.0,
                input_features=input_features,
                metadata={'error': str(e), 'status': 'error'}
            )
    
    def create_model(self, model_id: str, model_type: str, 
                    initial_params: Optional[Dict[str, Any]] = None) -> ModelState:
        """Create a new model"""
        try:
            model_state = self.model_engine.create_model_state(
                model_id, model_type, initial_params
            )
            self.metrics.increment_models_created()
            return model_state
        except Exception as e:
            self.logger.error(f"Error creating model: {e}")
            raise
    
    def start_training(self, model_id: str) -> bool:
        """Start training for a specific model"""
        try:
            success = self.model_engine.start_training(model_id)
            if success:
                self.metrics.increment_training_sessions()
            return success
        except Exception as e:
            self.logger.error(f"Error starting training: {e}")
            return False
    
    def complete_training(self, model_id: str, training_metrics: Optional[Dict[str, Any]] = None) -> bool:
        """Complete training for a specific model"""
        try:
            success = self.model_engine.complete_training(model_id, training_metrics)
            if success:
                self.metrics.increment_training_completions()
            return success
        except Exception as e:
            self.logger.error(f"Error completing training: {e}")
            return False
    
    def validate_prediction(self, prediction: MLPrediction, actual_value: Any) -> Dict[str, Any]:
        """Validate prediction against actual value"""
        try:
            validation_result = self.prediction_engine.validate_prediction(prediction, actual_value)
            
            # Update pattern accuracy if validation successful
            if 'accuracy' in validation_result:
                accuracy = validation_result['accuracy']
                # Find and update related patterns
                similar_patterns = self.pattern_engine.find_similar_patterns(
                    prediction.prediction_type, prediction.input_features
                )
                for pattern in similar_patterns[:3]:  # Update top 3 similar patterns
                    self.pattern_engine.update_pattern_accuracy(pattern.pattern_id, accuracy)
            
            return validation_result
        except Exception as e:
            self.logger.error(f"Error validating prediction: {e}")
            return {'error': str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            pattern_stats = self.pattern_engine.get_pattern_statistics()
            prediction_stats = self.prediction_engine.get_prediction_statistics()
            model_stats = self.model_engine.get_model_statistics()
            training_status = self.model_engine.get_training_status()
            
            return {
                'patterns': pattern_stats,
                'predictions': prediction_stats,
                'models': model_stats,
                'training': training_status,
                'metrics': self.metrics.to_dict(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {'error': str(e)}
    
    def save_models(self, save_path: Optional[str] = None) -> bool:
        """Save all models and patterns to disk"""
        try:
            success = self.model_engine.save_models(save_path)
            if success:
                self.metrics.increment_model_saves()
            return success
        except Exception as e:
            self.logger.error(f"Error saving models: {e}")
            return False
    
    def load_models(self, load_path: Optional[str] = None) -> bool:
        """Load all models and patterns from disk"""
        try:
            success = self.model_engine.load_models(load_path)
            if success:
                self.metrics.increment_model_loads()
            return success
        except Exception as e:
            self.logger.error(f"Error loading models: {e}")
            return False
    
    def clear_caches(self):
        """Clear all caches"""
        self.pattern_engine.clear_patterns()
        self.prediction_engine.clear_cache()
        self.feature_engine.clear_cache()
        self.logger.info("All caches cleared")
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get learning summary and statistics"""
        try:
            pattern_stats = self.pattern_engine.get_pattern_statistics()
            prediction_stats = self.prediction_engine.get_prediction_statistics()
            model_stats = self.model_engine.get_model_statistics()
            
            return {
                'learning_summary': {
                    'total_patterns': pattern_stats.get('total_patterns', 0),
                    'total_predictions': prediction_stats.get('total_predictions', 0),
                    'total_models': model_stats.get('total_models', 0),
                    'is_training': model_stats.get('is_training', False)
                },
                'pattern_breakdown': pattern_stats.get('pattern_types', {}),
                'prediction_breakdown': prediction_stats.get('prediction_types', {}),
                'model_breakdown': model_stats.get('model_types', {}),
                'performance_metrics': self.metrics.to_dict(),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Error getting learning summary: {e}")
            return {'error': str(e)}


# Factory function for dependency injection
def create_ml_learning_engine_orchestrator(config: Optional[MLOptimizationConfig] = None) -> MLLearningEngineOrchestrator:
    """Factory function to create ML learning engine orchestrator with optional configuration"""
    return MLLearningEngineOrchestrator(config)


# Export for DI
__all__ = ['MLLearningEngineOrchestrator', 'create_ml_learning_engine_orchestrator']
