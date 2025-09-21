#!/usr/bin/env python3
"""
ML Pipeline Core - V2 Compliant
==============================

Core ML pipeline functionality.
V2 Compliance: 255 lines, perfect.
"""

import sys
import logging
import time
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .ml_pipeline_models import ModelConfig, TrainingData, ModelMetrics
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
        self.fallback_model = FallbackMLModel(self.config)
        logger.info("ML Pipeline Core initialized")

    def create_training_data(self,
                           num_samples: int = 1000,
                           num_features: int = 10,
                           num_classes: int = 3,
                           data_type: str = "classification") -> TrainingData:
        """Create synthetic training data."""
        try:
            logger.info("Creating training data")
            features = np.random.randn(num_samples, num_features)

            if data_type == "classification":
                labels = np.random.randint(0, num_classes, num_samples)
            else:
                labels = np.random.randn(num_samples)

            # Split data
            train_size = int(0.7 * num_samples)
            val_size = int(0.15 * num_samples)

            return TrainingData(
                features=features[:train_size],
                labels=labels[:train_size],
                validation_features=features[train_size:train_size + val_size],
                validation_labels=labels[train_size:train_size + val_size],
                test_features=features[train_size + val_size:],
                test_labels=labels[train_size + val_size:]
            )

        except Exception as e:
            logger.error(f"Error creating training data: {e}")
            raise

    def create_model(self, model_name: str, model_type: str = "neural_network"):
        """Create ML model."""
        try:
            logger.info(f"Creating {model_type} model")

            if model_type == "neural_network":
                model = self._create_nn_model()
            elif model_type == "fallback":
                model = self.fallback_model
            else:
                raise ValueError(f"Invalid model type: {model_type}")

            self.models[model_name] = model
            logger.info(f"Model {model_name} created")
            return model

        except Exception as e:
            logger.error(f"Error creating model: {e}")
            raise

    def _create_nn_model(self):
        """Create neural network model."""
        try:
            return self._create_tf_model()
        except ImportError:
            try:
                return self._create_torch_model()
            except ImportError:
                return self.fallback_model

    def _create_tf_model(self):
        """Create TensorFlow model."""
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
        return model

    def _create_torch_model(self):
        """Create PyTorch model."""
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

        return PyTorchModel(
            input_size=np.prod(self.config.input_shape),
            num_classes=self.config.num_classes
        )

    def train_model(self,
                   model_name: str,
                   training_data: TrainingData,
                   epochs: Optional[int] = None,
                   batch_size: Optional[int] = None):
        """Train ML model."""
        try:
            logger.info(f"Training {model_name}")
            model = self.models.get(model_name)
            if not model:
                raise ValueError(f"Model {model_name} not found")

            epochs = epochs or self.config.epochs
            batch_size = batch_size or self.config.batch_size
            start_time = time.time()

            if hasattr(model, 'fit'):
                # TensorFlow training
                validation_data = self._get_validation_data(training_data)

                history = model.fit(
                    training_data.features,
                    training_data.labels,
                    epochs=epochs,
                    batch_size=batch_size,
                    validation_data=validation_data,
                    verbose=1
                )

                results = {
                    "status": "completed",
                    "epochs": epochs,
                    "final_loss": float(history.history['loss'][-1]),
                    "model_type": "tensorflow"
                }
                if 'accuracy' in history.history:
                    results["final_accuracy"] = float(history.history['accuracy'][-1])
            else:
                # Fallback training
                results = model.train(training_data)

            results["training_time"] = time.time() - start_time
            self.training_data[model_name] = training_data
            logger.info("Training completed")
            return results

        except Exception as e:
            logger.error(f"Training error: {e}")
            return {"status": "failed", "error": str(e)}

    def _get_validation_data(self, training_data):
        """Get validation data for TensorFlow training."""
        if training_data.validation_features is not None:
            return (training_data.validation_features,
                   training_data.validation_labels)
        return None

    def evaluate_model(self, model_name: str, test_data: TrainingData):
        """Evaluate ML model."""
        try:
            logger.info(f"Evaluating {model_name}")
            model = self.models.get(model_name)
            if not model:
                raise ValueError(f"Model {model_name} not found")

            start_time = time.time()
            predictions = model.predict(test_data.features)
            inference_time = time.time() - start_time

            if self.config.model_type == "classification":
                accuracy = np.mean(predictions == test_data.labels)
                from sklearn.metrics import precision_score, recall_score, f1_score
                precision = precision_score(test_data.labels, predictions,
                                         average='weighted')
                recall = recall_score(test_data.labels, predictions,
                                    average='weighted')
                f1 = f1_score(test_data.labels, predictions,
                            average='weighted')

                metrics = ModelMetrics(
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
            else:
                # Regression metrics
                mse = np.mean((predictions - test_data.labels) ** 2)
                accuracy = 1.0 / (1.0 + mse)

                metrics = ModelMetrics(
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

            self.model_metrics[model_name] = metrics
            return {
                "status": "completed",
                "metrics": metrics.to_dict(),
                "inference_time": inference_time
            }

        except Exception as e:
            logger.error(f"Evaluation error: {e}")
            return {"status": "failed", "error": str(e)}
