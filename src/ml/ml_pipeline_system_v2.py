#!/usr/bin/env python3
"""
ML Pipeline System - V2 Compliant
=================================

Refactored ML pipeline system for V2 compliance.
V2 Compliance: ≤400 lines, single responsibility, KISS principle.

Features:
- Modular design with core functionality extracted
- TensorFlow/PyTorch integration
- Model training and deployment
- Data preprocessing pipelines
- Model versioning and management
- Performance monitoring
- Automated retraining

Usage:
    from src.ml.ml_pipeline_system_v2 import MLPipelineSystem
    
    ml_system = MLPipelineSystem()
    model = ml_system.train_model(training_data)
"""

import logging
from typing import Dict, Any, List, Optional
import numpy as np

# ML Framework imports
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️ TensorFlow not available - using fallback ML system")

try:
    import torch
    import torch.nn as nn
    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False
    print("⚠️ PyTorch not available - using fallback ML system")

from .ml_pipeline_core import (
    MLPipelineCore,
    ModelConfig,
    TrainingData,
    FallbackMLModel
)

logger = logging.getLogger(__name__)


class TensorFlowModel:
    """TensorFlow model wrapper."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        self.is_trained = False
        self.training_history = []
    
    def _create_model(self):
        """Create TensorFlow model."""
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow not available")
        
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(self.config.hidden_sizes[0], activation='relu', 
                                input_shape=(self.config.input_size,)),
            tf.keras.layers.Dropout(self.config.dropout_rate),
            tf.keras.layers.Dense(self.config.hidden_sizes[1], activation='relu'),
            tf.keras.layers.Dropout(self.config.dropout_rate),
            tf.keras.layers.Dense(self.config.output_size, activation='linear')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=self.config.learning_rate),
            loss='mse',
            metrics=['mae']
        )
        
        return model
    
    def train(self, features: np.ndarray, labels: np.ndarray):
        """Train TensorFlow model."""
        logger.info("🔄 Training TensorFlow model...")
        
        self.model = self._create_model()
        
        # Train the model
        history = self.model.fit(
            features, labels,
            epochs=self.config.epochs,
            batch_size=self.config.batch_size,
            validation_split=0.2,
            verbose=0
        )
        
        self.is_trained = True
        self.training_history = history.history
        
        logger.info("✅ TensorFlow model training completed")
        
        return {
            "final_loss": float(history.history['loss'][-1]),
            "epochs_trained": self.config.epochs,
            "training_time": 0.0,  # TensorFlow doesn't provide this directly
            "model_type": "tensorflow_neural_network"
        }
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Make predictions."""
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")
        
        return self.model.predict(features, verbose=0)


class PyTorchModel:
    """PyTorch model wrapper."""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        self.optimizer = None
        self.criterion = None
        self.is_trained = False
        self.training_history = []
    
    def _create_model(self):
        """Create PyTorch model."""
        if not PYTORCH_AVAILABLE:
            raise ImportError("PyTorch not available")
        
        class NeuralNetwork(nn.Module):
            def __init__(self, input_size, hidden_sizes, output_size, dropout_rate):
                super(NeuralNetwork, self).__init__()
                self.layers = nn.ModuleList()
                
                # Input layer
                self.layers.append(nn.Linear(input_size, hidden_sizes[0]))
                self.layers.append(nn.ReLU())
                self.layers.append(nn.Dropout(dropout_rate))
                
                # Hidden layers
                for i in range(len(hidden_sizes) - 1):
                    self.layers.append(nn.Linear(hidden_sizes[i], hidden_sizes[i+1]))
                    self.layers.append(nn.ReLU())
                    self.layers.append(nn.Dropout(dropout_rate))
                
                # Output layer
                self.layers.append(nn.Linear(hidden_sizes[-1], output_size))
            
            def forward(self, x):
                for layer in self.layers:
                    x = layer(x)
                return x
        
        return NeuralNetwork(
            self.config.input_size,
            self.config.hidden_sizes,
            self.config.output_size,
            self.config.dropout_rate
        )
    
    def train(self, features: np.ndarray, labels: np.ndarray):
        """Train PyTorch model."""
        logger.info("🔄 Training PyTorch model...")
        
        self.model = self._create_model()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.config.learning_rate)
        self.criterion = nn.MSELoss()
        
        # Convert to tensors
        X = torch.FloatTensor(features)
        y = torch.FloatTensor(labels)
        
        # Training loop
        for epoch in range(self.config.epochs):
            self.optimizer.zero_grad()
            outputs = self.model(X)
            loss = self.criterion(outputs, y)
            loss.backward()
            self.optimizer.step()
            
            self.training_history.append({
                "epoch": epoch + 1,
                "loss": float(loss.item()),
                "timestamp": str(torch.datetime.now())
            })
            
            if epoch % 10 == 0:
                logger.info(f"  Epoch {epoch + 1}/{self.config.epochs}, Loss: {loss.item():.4f}")
        
        self.is_trained = True
        logger.info("✅ PyTorch model training completed")
        
        return {
            "final_loss": float(loss.item()),
            "epochs_trained": self.config.epochs,
            "training_time": 0.0,
            "model_type": "pytorch_neural_network"
        }
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Make predictions."""
        if not self.is_trained or self.model is None:
            raise ValueError("Model must be trained before making predictions")
        
        self.model.eval()
        with torch.no_grad():
            X = torch.FloatTensor(features)
            predictions = self.model(X)
            return predictions.numpy()


class MLPipelineSystem:
    """Comprehensive ML pipeline system for V3 operations."""
    
    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize the ML pipeline system."""
        self.config = config or ModelConfig()
        
        # Initialize core functionality
        self.core = MLPipelineCore(self.config)
        
        # Check ML framework availability
        self.tensorflow_available = TENSORFLOW_AVAILABLE
        self.pytorch_available = PYTORCH_AVAILABLE
        
        logger.info("🤖 ML Pipeline System initialized")
        logger.info(f"  TensorFlow: {'✅' if self.tensorflow_available else '❌'}")
        logger.info(f"  PyTorch: {'✅' if self.pytorch_available else '❌'}")
    
    def create_model(self, model_name: str, model_type: str = "neural_network") -> Any:
        """Create a new ML model with framework support."""
        logger.info(f"🏗️ Creating {model_type} model: {model_name}")
        
        if self.tensorflow_available and model_type == "tensorflow":
            model = TensorFlowModel(self.config)
        elif self.pytorch_available and model_type == "pytorch":
            model = PyTorchModel(self.config)
        else:
            # Use fallback model
            model = FallbackMLModel(self.config)
        
        self.core.models[model_name] = model
        self.core.model_versions[model_name] = [f"v1.0-{self._get_timestamp()}"]
        
        logger.info(f"✅ Created model: {model_name}")
        return model
    
    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime('%Y%m%d-%H%M%S')
    
    # Delegate core functionality
    def create_training_data(self, data_type: str = "synthetic", 
                           num_samples: int = 1000, 
                           num_features: int = 100) -> TrainingData:
        """Create training data."""
        return self.core.create_training_data(data_type, num_samples, num_features)
    
    def train_model(self, model_name: str, data_type: str = "synthetic") -> Dict[str, Any]:
        """Train a model."""
        return self.core.train_model(model_name, data_type)
    
    def predict(self, model_name: str, features: np.ndarray) -> np.ndarray:
        """Make predictions."""
        return self.core.predict(model_name, features)
    
    def save_model(self, model_name: str, filepath: Optional[str] = None):
        """Save a model."""
        self.core.save_model(model_name, filepath)
    
    def load_model(self, model_name: str, filepath: str):
        """Load a model."""
        self.core.load_model(model_name, filepath)
    
    def get_model_info(self, model_name: str) -> Dict[str, Any]:
        """Get model information."""
        return self.core.get_model_info(model_name)
    
    def list_models(self) -> List[str]:
        """List all available models."""
        return list(self.core.models.keys())
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        return {
            "tensorflow_available": self.tensorflow_available,
            "pytorch_available": self.pytorch_available,
            "num_models": len(self.core.models),
            "num_training_datasets": len(self.core.training_data),
            "config": self.config
        }


def create_ml_pipeline(config: Optional[ModelConfig] = None) -> MLPipelineSystem:
    """Create ML pipeline system."""
    return MLPipelineSystem(config)

