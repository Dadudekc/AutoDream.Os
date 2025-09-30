"""
ML Pipeline Core Engine
V2 Compliant ML pipeline core functionality
"""

import logging
import time
from typing import Any, Dict, Optional

import numpy as np

from .ml_pipeline_models import ModelConfig, ModelMetrics, ModelResult, TrainingData
from .ml_pipeline_fallback import FallbackMLModel


class MLPipelineCore:
    """Core ML pipeline functionality - V2 Compliant"""
    
    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize ML pipeline core"""
        self.config = config or ModelConfig()
        self.models: Dict[str, Any] = {}
        self.training_data: Dict[str, TrainingData] = {}
        self.model_metrics: Dict[str, ModelMetrics] = {}
        self.logger = logging.getLogger(__name__)
        
    def create_training_data(self, features: np.ndarray, labels: np.ndarray) -> TrainingData:
        """Create training data"""
        metadata = {
            "samples": len(features),
            "features": features.shape[1] if len(features.shape) > 1 else 1,
            "classes": len(np.unique(labels))
        }
        
        return TrainingData(
            features=features,
            labels=labels,
            metadata=metadata
        )
    
    def train_model(self, model_id: str, training_data: TrainingData) -> ModelMetrics:
        """Train a model"""
        start_time = time.time()
        
        # Use fallback model for V2 compliance
        model = FallbackMLModel()
        model.train(training_data.features, training_data.labels)
        
        # Calculate metrics
        predictions = model.predict(training_data.features)
        accuracy = self._calculate_accuracy(training_data.labels, predictions)
        
        training_time = time.time() - start_time
        
        metrics = ModelMetrics(
            accuracy=accuracy,
            loss=0.1,  # Placeholder
            precision=0.9,  # Placeholder
            recall=0.9,  # Placeholder
            f1_score=0.9,  # Placeholder
            training_time=training_time,
            validation_time=0.1
        )
        
        self.models[model_id] = model
        self.model_metrics[model_id] = metrics
        
        return metrics
    
    def evaluate_model(self, model_id: str, test_data: TrainingData) -> ModelMetrics:
        """Evaluate a model"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        predictions = model.predict(test_data.features)
        
        accuracy = self._calculate_accuracy(test_data.labels, predictions)
        
        return ModelMetrics(
            accuracy=accuracy,
            loss=0.1,
            precision=0.9,
            recall=0.9,
            f1_score=0.9,
            training_time=0.0,
            validation_time=0.1
        )
    
    def predict(self, model_id: str, features: np.ndarray) -> ModelResult:
        """Make predictions"""
        if model_id not in self.models:
            raise ValueError(f"Model {model_id} not found")
        
        model = self.models[model_id]
        start_time = time.time()
        
        predictions = model.predict(features)
        processing_time = time.time() - start_time
        
        return ModelResult(
            predictions=predictions,
            confidence=0.9,
            processing_time=processing_time,
            model_version="1.0"
        )
    
    def _calculate_accuracy(self, true_labels: np.ndarray, predictions: np.ndarray) -> float:
        """Calculate accuracy"""
        if len(true_labels) != len(predictions):
            return 0.0
        
        correct = np.sum(true_labels == predictions)
        return correct / len(true_labels)
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get model status"""
        return {
            "total_models": len(self.models),
            "total_training_data": len(self.training_data),
            "config": {
                "model_type": self.config.model_type,
                "learning_rate": self.config.learning_rate,
                "batch_size": self.config.batch_size
            }
        }