#!/usr/bin/env python3
"""
ML Pipeline Core - V2 Compliant
===============================

Core ML pipeline functionality for V2 compliance.
V2 Compliance: ≤400 lines, single responsibility, KISS principle.
"""

import json
import logging
import pickle
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

# ML Framework imports
try:
    import tensorflow as tf

    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

try:
    import torch
    import torch.nn as nn

    PYTORCH_AVAILABLE = True
except ImportError:
    PYTORCH_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    """Configuration for ML models."""

    model_type: str = "neural_network"
    input_size: int = 100
    hidden_size: int = 64
    output_size: int = 10
    learning_rate: float = 0.001
    epochs: int = 100
    batch_size: int = 32
    validation_split: float = 0.2


@dataclass
class TrainingData:
    """Training data structure."""

    features: np.ndarray
    labels: np.ndarray
    metadata: dict[str, Any]


class FallbackMLModel:
    """Fallback ML model when TensorFlow/PyTorch are not available."""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.weights = np.random.randn(config.input_size, config.output_size) * 0.1
        self.bias = np.zeros(config.output_size)
        self.is_trained = False
        self.training_history = []
        self.input_size = None

    def train(self, data: TrainingData) -> dict[str, Any]:
        """Train the fallback model."""
        logger.info("🤖 Training fallback ML model...")

        # Initialize weights based on actual feature dimensions
        if self.input_size is None or self.input_size != data.features.shape[1]:
            self.input_size = data.features.shape[1]
            self.weights = np.random.randn(self.input_size, self.config.output_size) * 0.1
            logger.info(f"  Initialized weights for input size: {self.input_size}")

        # Simple gradient descent training
        for epoch in range(self.config.epochs):
            # Forward pass
            predictions = np.dot(data.features, self.weights) + self.bias

            # Simple loss calculation (MSE)
            loss = np.mean((predictions - data.labels) ** 2)

            # Backward pass (simple gradient descent)
            gradient_w = np.dot(data.features.T, (predictions - data.labels)) / len(data.features)
            gradient_b = np.mean(predictions - data.labels, axis=0)

            # Update weights
            self.weights -= self.config.learning_rate * gradient_w
            self.bias -= self.config.learning_rate * gradient_b

            # Store training history
            self.training_history.append(
                {"epoch": epoch + 1, "loss": float(loss), "timestamp": datetime.now().isoformat()}
            )

            if epoch % 10 == 0:
                logger.info(f"  Epoch {epoch + 1}/{self.config.epochs}, Loss: {loss:.4f}")

        self.is_trained = True
        logger.info("✅ Fallback ML model training completed")

        return {
            "final_loss": float(loss),
            "epochs_trained": self.config.epochs,
            "training_history": self.training_history,
        }

    def predict(self, features: np.ndarray) -> np.ndarray:
        """Make predictions using the trained model."""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")

        predictions = np.dot(features, self.weights) + self.bias
        return predictions

    def save(self, filepath: str):
        """Save the model to disk."""
        model_data = {
            "weights": self.weights,
            "bias": self.bias,
            "config": self.config,
            "is_trained": self.is_trained,
            "training_history": self.training_history,
            "input_size": self.input_size,
        }

        with open(filepath, "wb") as f:
            pickle.dump(model_data, f)

        logger.info(f"📂 Model saved to {filepath}")

    def load(self, filepath: str):
        """Load the model from disk."""
        with open(filepath, "rb") as f:
            model_data = pickle.load(f)

        self.weights = model_data["weights"]
        self.bias = model_data["bias"]
        self.config = model_data["config"]
        self.is_trained = model_data["is_trained"]
        self.training_history = model_data["training_history"]
        self.input_size = model_data["input_size"]

        logger.info(f"📂 Model loaded from {filepath}")


class MLPipelineCore:
    """Core ML pipeline functionality."""

    def __init__(self, config: ModelConfig):
        """Initialize ML pipeline core."""
        self.config = config
        self.models: dict[str, Any] = {}
        self.training_data: dict[str, TrainingData] = {}
        self.model_versions: dict[str, list[str]] = {}

        # Create ML directories
        self.ml_dir = Path("src/ml")
        self.models_dir = self.ml_dir / "models"
        self.data_dir = self.ml_dir / "data"
        self.logs_dir = self.ml_dir / "logs"

        for dir_path in [self.ml_dir, self.models_dir, self.data_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Check ML framework availability
        self.tensorflow_available = TENSORFLOW_AVAILABLE
        self.pytorch_available = PYTORCH_AVAILABLE

        logger.info("🤖 ML Pipeline Core initialized")

    def create_training_data(
        self, data_type: str = "synthetic", num_samples: int = 1000, num_features: int = 100
    ) -> TrainingData:
        """Create training data for ML models."""
        logger.info(f"📊 Creating {data_type} training data...")

        if data_type == "synthetic":
            # Generate synthetic data
            features = np.random.randn(num_samples, num_features)
            # Create simple linear relationship with noise
            true_weights = np.random.randn(num_features, self.config.output_size)
            labels = (
                np.dot(features, true_weights)
                + np.random.randn(num_samples, self.config.output_size) * 0.1
            )
        else:
            # Default to random data
            features = np.random.randn(num_samples, num_features)
            labels = np.random.randn(num_samples, self.config.output_size)

        metadata = {
            "data_type": data_type,
            "num_samples": num_samples,
            "num_features": num_features,
            "created_at": datetime.now().isoformat(),
            "feature_mean": float(np.mean(features)),
            "feature_std": float(np.std(features)),
            "label_mean": float(np.mean(labels)),
            "label_std": float(np.std(labels)),
        }

        training_data = TrainingData(features, labels, metadata)
        self.training_data[data_type] = training_data

        logger.info(
            f"✅ Created {data_type} training data: {num_samples} samples, {num_features} features"
        )
        return training_data

    def create_model(self, model_name: str, model_type: str = "neural_network") -> Any:
        """Create a new ML model."""
        logger.info(f"🏗️ Creating {model_type} model: {model_name}")

        if self.tensorflow_available and model_type == "tensorflow":
            model = self._create_tensorflow_model()
        elif self.pytorch_available and model_type == "pytorch":
            model = self._create_pytorch_model()
        else:
            # Use fallback model
            model = FallbackMLModel(self.config)

        self.models[model_name] = model
        logger.info(f"✅ Created model: {model_name}")
        return model

    def train_model(self, model_name: str, data_name: str, epochs: int = None) -> dict[str, Any]:
        """Train a model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        if data_name not in self.training_data:
            raise ValueError(f"Training data {data_name} not found")

        model = self.models[model_name]
        data = self.training_data[data_name]

        logger.info(f"🔄 Training model: {model_name}")

        # Train the model
        training_results = model.train(data)

        # Update model versions
        if model_name not in self.model_versions:
            self.model_versions[model_name] = []

        version = f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.model_versions[model_name].append(version)

        # Save the trained model
        model_path = self.models_dir / f"{model_name}_{version}.pkl"
        model.save(str(model_path))

        logger.info(f"✅ Model training completed: {model_name}")
        return training_results

    def evaluate_model(self, model_name: str, test_data: TrainingData) -> dict[str, Any]:
        """Evaluate a model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        model = self.models[model_name]

        logger.info(f"📊 Evaluating model: {model_name}")

        # Make predictions
        predictions = model.predict(test_data.features)

        # Calculate metrics
        mse = np.mean((predictions - test_data.labels) ** 2)
        mae = np.mean(np.abs(predictions - test_data.labels))
        rmse = np.sqrt(mse)

        evaluation_results = {
            "mse": float(mse),
            "mae": float(mae),
            "rmse": float(rmse),
            "evaluated_at": datetime.now().isoformat(),
        }

        logger.info(f"✅ Model evaluation completed: {model_name}")
        return evaluation_results

    def deploy_model(self, model_name: str) -> dict[str, Any]:
        """Deploy a model."""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not found")

        logger.info(f"🚀 Deploying model: {model_name}")

        # Simulate deployment
        endpoint = f"http://localhost:8000/api/models/{model_name}/predict"

        deployment_results = {
            "model_name": model_name,
            "endpoint": endpoint,
            "status": "deployed",
            "deployed_at": datetime.now().isoformat(),
        }

        logger.info(f"✅ Model deployment completed: {model_name}")
        return deployment_results

    def get_system_status(self) -> dict[str, Any]:
        """Get system status."""
        return {
            "total_models": len(self.models),
            "total_datasets": len(self.training_data),
            "model_versions": self.model_versions,
            "tensorflow_available": self.tensorflow_available,
            "pytorch_available": self.pytorch_available,
            "status": "operational",
        }

    def export_system_data(self) -> str:
        """Export system data."""
        export_file = (
            self.logs_dir / f"ml_system_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )

        export_data = {
            "system_status": self.get_system_status(),
            "exported_at": datetime.now().isoformat(),
        }

        with open(export_file, "w") as f:
            json.dump(export_data, f, indent=2)

        logger.info(f"📤 System data exported to: {export_file}")
        return str(export_file)

    def _create_tensorflow_model(self):
        """Create TensorFlow model - placeholder."""
        return FallbackMLModel(self.config)

    def _create_pytorch_model(self):
        """Create PyTorch model - placeholder."""
        return FallbackMLModel(self.config)
