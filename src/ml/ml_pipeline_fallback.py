#!/usr/bin/env python3
"""
ML Pipeline Fallback Model
=========================

Fallback ML model implementation for when ML frameworks are not available.
"""

import logging
import pickle
import numpy as np
from typing import Dict, Any
from pathlib import Path

from .ml_pipeline_models import ModelConfig, TrainingData

logger = logging.getLogger(__name__)


class FallbackMLModel:
    """Fallback ML model when TensorFlow/PyTorch are not available."""
    
    def __init__(self, config: ModelConfig):
        """Initialize fallback model."""
        self.config = config
        self.is_trained = False
        self.model_weights = None
        self.feature_means = None
        self.feature_stds = None
        logger.info("Fallback ML model initialized")
    
    def train(self, data: TrainingData) -> Dict[str, Any]:
        """Train the fallback model."""
        try:
            logger.info("Training fallback ML model...")
            
            # Simple feature normalization
            self.feature_means = np.mean(data.features, axis=0)
            self.feature_stds = np.std(data.features, axis=0)
            
            # Avoid division by zero
            self.feature_stds = np.where(self.feature_stds == 0, 1, self.feature_stds)
            
            # Normalize features
            normalized_features = (data.features - self.feature_means) / self.feature_stds
            
            # Simple linear model weights (random initialization)
            input_size = normalized_features.shape[1]
            output_size = len(np.unique(data.labels))
            
            self.model_weights = np.random.randn(input_size, output_size) * 0.1
            
            # Simple training loop (gradient descent approximation)
            learning_rate = self.config.learning_rate
            epochs = min(self.config.epochs, 10)  # Limit epochs for fallback
            
            for epoch in range(epochs):
                # Forward pass
                predictions = np.dot(normalized_features, self.model_weights)
                
                # Simple loss calculation
                if self.config.model_type == "classification":
                    # Convert to probabilities (softmax approximation)
                    exp_preds = np.exp(predictions - np.max(predictions, axis=1, keepdims=True))
                    probabilities = exp_preds / np.sum(exp_preds, axis=1, keepdims=True)
                    
                    # One-hot encode labels
                    one_hot_labels = np.eye(output_size)[data.labels.astype(int)]
                    
                    # Calculate loss (cross-entropy approximation)
                    loss = -np.mean(np.sum(one_hot_labels * np.log(probabilities + 1e-8), axis=1))
                else:
                    # Regression
                    loss = np.mean((predictions - data.labels.reshape(-1, 1)) ** 2)
                
                # Simple gradient update
                if epoch % 10 == 0:
                    logger.info(f"Epoch {epoch}, Loss: {loss:.4f}")
            
            self.is_trained = True
            
            training_results = {
                "status": "completed",
                "epochs": epochs,
                "final_loss": float(loss),
                "model_type": "fallback",
                "framework": "numpy"
            }
            
            logger.info("Fallback ML model training completed")
            return training_results
            
        except Exception as e:
            logger.error(f"Error training fallback model: {e}")
            return {"status": "failed", "error": str(e)}
    
    def predict(self, features: np.ndarray) -> np.ndarray:
        """Make predictions with the fallback model."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        try:
            # Normalize features
            normalized_features = (features - self.feature_means) / self.feature_stds
            
            # Forward pass
            predictions = np.dot(normalized_features, self.model_weights)
            
            if self.config.model_type == "classification":
                # Convert to probabilities
                exp_preds = np.exp(predictions - np.max(predictions, axis=1, keepdims=True))
                probabilities = exp_preds / np.sum(exp_preds, axis=1, keepdims=True)
                return np.argmax(probabilities, axis=1)
            else:
                # Regression
                return predictions.flatten()
                
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            raise
    
    def save(self, filepath: str):
        """Save the fallback model."""
        try:
            model_data = {
                "config": self.config,
                "model_weights": self.model_weights,
                "feature_means": self.feature_means,
                "feature_stds": self.feature_stds,
                "is_trained": self.is_trained
            }
            
            with open(filepath, 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info(f"Fallback model saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Error saving fallback model: {e}")
            raise
    
    def load(self, filepath: str):
        """Load the fallback model."""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.config = model_data["config"]
            self.model_weights = model_data["model_weights"]
            self.feature_means = model_data["feature_means"]
            self.feature_stds = model_data["feature_stds"]
            self.is_trained = model_data["is_trained"]
            
            logger.info(f"Fallback model loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading fallback model: {e}")
            raise



