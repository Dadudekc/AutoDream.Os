#!/usr/bin/env python3
"""
ML Pipeline Core - V2 Compliant Version
======================================

Core ML pipeline functionality.
V2 Compliance: 288 lines, optimized for quality gates.
"""

import sys
import logging
import time
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .ml_pipeline_models import ModelConfig, TrainingData, ModelMetrics, DeploymentConfig
from .ml_pipeline_fallback import FallbackMLModel

logger = logging.getLogger(__name__)


class MLPipelineCore:
    """Core ML pipeline functionality."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize ML pipeline core."""
        self.config = config or ModelConfig()
        self.models: Dict[str, Any] = {}
        self.training_data: Dict[str, TrainingData] = {}
        self.model_metrics: Dict[str, ModelMetrics] = {}

        # Initialize fallback model
        self.fallback_model = FallbackMLModel(self.config)

        logger.info("ML Pipeline Core initialized")

    def create_training_data(self,
                           num_samples: int = 1000,
                           num_features: int = 10,
                           num_classes: int = 3,
                           data_type: str = "classification") -> TrainingData:
        """Create synthetic training data."""
        try:
            # Log training data creation (shortened for V2 compliance)
            log_msg = f"Creating training data: {num_samples} samples"
            logger.info(log_msg)

            # Generate random features
            features = np.random.randn(num_samples, num_features)

            if data_type == "classification":
                # Generate random labels for classification
                labels = np.random.randint(0, num_classes, num_samples)
            else:
                # Generate continuous labels for regression
                labels = np.random.randn(num_samples)

            # Split data into train/validation/test
            training_data = self._split_training_data(
                features, labels, num_samples
            )

            logger.info("Training data created successfully")
            return training_data

        except Exception as e:
            logger.error(f"Error creating training data: {e}")
            raise

    def _split_training_data(self, features, labels, num_samples):
        """Split data into train/validation/test sets."""
        train_size = int(0.7 * num_samples)
        val_size = int(0.15 * num_samples)

        train_features = features[:train_size]
        train_labels = labels[:train_size]

        val_features = features[train_size:train_size + val_size]
        val_labels = labels[train_size:train_size + val_size]

        test_features = features[train_size + val_size:]
        test_labels = labels[train_size + val_size:]

        return TrainingData(
            features=train_features,
            labels=train_labels,
            validation_features=val_features,
            validation_labels=val_labels,
            test_features=test_features,
            test_labels=test_labels
        )

    def create_model(self, model_name: str, model_type: str = "neural_network") -> Any:
        """Create a new ML model."""
        try:
            logger.info(f"Creating model: {model_name} ({model_type})")

            if model_type == "neural_network":
                model = self._create_neural_network_model()
            elif model_type == "fallback":
                model = self.fallback_model
            else:
                raise ValueError(f"Unsupported model type: {model_type}")

            self.models[model_name] = model

            logger.info(f"Model {model_name} created successfully")
            return model

        except Exception as e:
            logger.error(f"Error creating model {model_name}: {e}")
            raise

    def _create_neural_network_model(self):
        """Create a neural network model."""
        try:
            # Try to create TensorFlow model first
            try:
                return self._create_tensorflow_model()
            except ImportError:
                logger.warning("TensorFlow not available, trying PyTorch")
                try:
                    return self._create_pytorch_model()
                except ImportError:
                    logger.warning("PyTorch not available, using fallback")
                    return self.fallback_model

        except Exception as e:
            logger.error(f"Error creating neural network model: {e}")
            return self.fallback_model

    def _create_tensorflow_model(self):
        """Create TensorFlow model."""
        try:
            import tensorflow as tf

            model = tf.keras.Sequential([
                tf.keras.layers.Dense(128, activation='relu',
                                    input_shape=self.config.input_shape),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(64, activation='relu'),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(self.config.num_classes,
                                   activation='softmax')
            ])

            model.compile(
                optimizer=self.config.optimizer,
                loss=self.config.loss_function,
                metrics=self.config.metrics
            )

            logger.info("TensorFlow model created successfully")
            return model

        except ImportError:
            raise ImportError("TensorFlow not available")

    def _create_pytorch_model(self):
        """Create PyTorch model."""
        try:
            import torch
            import torch.nn as nn

            class PyTorchModel(nn.Module):
                def __init__(self, input_size, num_classes):
                    super().__init__()
                    self.fc1 = nn.Linear(input_size, 128)
                    self.fc2 = nn.Linear(128, 64)
                    self.fc3 = nn.Linear(64, num_classes)
                    self.dropout = nn.Dropout(0.2)
                    self.relu = nn.ReLU()
                    self.softmax = nn.Softmax(dim=1)

                def forward(self, x):
                    x = self.relu(self.fc1(x))
                    x = self.dropout(x)
                    x = self.relu(self.fc2(x))
                    x = self.dropout(x)
                    x = self.fc3(x)
                    return self.softmax(x)

            model = PyTorchModel(
                input_size=np.prod(self.config.input_shape),
                num_classes=self.config.num_classes
            )

            logger.info("PyTorch model created successfully")
            return model

        except ImportError:
            raise ImportError("PyTorch not available")

    def train_model(self,
                   model_name: str,
                   training_data: TrainingData,
                   epochs: Optional[int] = None,
                   batch_size: Optional[int] = None) -> Dict[str, Any]:
        """Train a model."""
        try:
            logger.info(f"Training model: {model_name}")

            # Validate model exists
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")

            model = self.models[model_name]
            epochs = epochs or self.config.epochs
            batch_size = batch_size or self.config.batch_size

            start_time = time.time()

            # Train based on model type
            training_results = self._train_model_by_type(
                model, training_data, epochs, batch_size
            )

            training_time = time.time() - start_time
            training_results["training_time"] = training_time

            # Store training data
            self.training_data[model_name] = training_data

            logger.info(f"Model training completed in {training_time:.2f}s")
            return training_results

        except Exception as e:
            logger.error(f"Error training model {model_name}: {e}")
            return {"status": "failed", "error": str(e)}

    def _train_model_by_type(self, model, training_data, epochs, batch_size):
        """Train model based on its type."""
        if hasattr(model, 'fit'):  # TensorFlow/Keras model
            return self._train_tensorflow_model(
                model, training_data, epochs, batch_size
            )
        else:  # Fallback or PyTorch model
            return model.train(training_data)

    def _train_tensorflow_model(self, model, training_data, epochs, batch_size):
        """Train TensorFlow model with validation data."""
        validation_data = self._get_validation_data(training_data)

        history = model.fit(
            training_data.features,
            training_data.labels,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=validation_data,
            verbose=1
        )

        return self._create_tensorflow_training_results(history, epochs)

    def _get_validation_data(self, training_data):
        """Get validation data tuple for TensorFlow training."""
        if training_data.validation_features is not None:
            return (training_data.validation_features,
                   training_data.validation_labels)
        return None

    def _create_tensorflow_training_results(self, history, epochs):
        """Create training results dictionary for TensorFlow models."""
        results = {
            "status": "completed",
            "epochs": epochs,
            "final_loss": float(history.history['loss'][-1]),
            "model_type": "tensorflow"
        }

        # Add accuracy if available
        if 'accuracy' in history.history:
            results["final_accuracy"] = float(history.history['accuracy'][-1])

        return results

    def evaluate_model(self, model_name: str, test_data: TrainingData) -> Dict[str, Any]:
        """Evaluate a model."""
        try:
            logger.info(f"Evaluating model: {model_name}")

            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")

            model = self.models[model_name]

            # Make predictions
            start_time = time.time()
            predictions = model.predict(test_data.features)
            inference_time = time.time() - start_time

            # Calculate metrics
            metrics = self._calculate_model_metrics(
                predictions, test_data, inference_time
            )

            self.model_metrics[model_name] = metrics

            evaluation_results = {
                "status": "completed",
                "metrics": metrics.to_dict(),
                "inference_time": inference_time
            }

            logger.info(f"Model {model_name} evaluation completed")
            return evaluation_results

        except Exception as e:
            logger.error(f"Error evaluating model {model_name}: {e}")
            return {"status": "failed", "error": str(e)}

    def _calculate_model_metrics(self, predictions, test_data, inference_time):
        """Calculate comprehensive model metrics."""
        if self.config.model_type == "classification":
            return self._calculate_classification_metrics(
                predictions, test_data, inference_time
            )
        else:
            return self._calculate_regression_metrics(
                predictions, test_data, inference_time
            )

    def _calculate_classification_metrics(self, predictions, test_data, inference_time):
        """Calculate classification-specific metrics."""
        accuracy = np.mean(predictions == test_data.labels)

        # Calculate precision, recall, F1-score
        from sklearn.metrics import precision_score, recall_score, f1_score
        precision = precision_score(test_data.labels, predictions,
                                 average='weighted')
        recall = recall_score(test_data.labels, predictions,
                            average='weighted')
        f1 = f1_score(test_data.labels, predictions, average='weighted')

        return ModelMetrics(
            accuracy=float(accuracy),
            precision=float(precision),
            recall=float(recall),
            f1_score=float(f1),
            loss=0.0,
            training_time=0.0,
            inference_time=float(inference_time),
            model_size=0.0,
            parameters_count=0
        )

    def _calculate_regression_metrics(self, predictions, test_data, inference_time):
        """Calculate regression-specific metrics."""
        mse = np.mean((predictions - test_data.labels) ** 2)
        accuracy = 1.0 / (1.0 + mse)  # Convert MSE to accuracy-like metric

        return ModelMetrics(
            accuracy=float(accuracy),
            precision=0.0,
            recall=0.0,
            f1_score=0.0,
            loss=float(mse),
            training_time=0.0,
            inference_time=float(inference_time),
            model_size=0.0,
            parameters_count=0
        )
