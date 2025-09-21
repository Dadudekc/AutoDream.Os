#!/usr/bin/env python3
"""
ML Pipeline Models
=================

Data models for ML pipeline system.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Union


@dataclass
class ModelConfig:
    """Configuration for ML models."""
    framework: str = "tensorflow"
    model_type: str = "classification"
    input_shape: tuple = (224, 224, 3)
    num_classes: int = 10
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2
    optimizer: str = "adam"
    loss_function: str = "categorical_crossentropy"
    metrics: List[str] = None
    callbacks: List[str] = None
    early_stopping_patience: int = 10
    model_checkpoint: bool = True
    reduce_lr_on_plateau: bool = True
    
    def __post_init__(self):
        """Set default values after initialization."""
        if self.metrics is None:
            self.metrics = ["accuracy", "precision", "recall", "f1_score"]
        
        if self.callbacks is None:
            self.callbacks = ["early_stopping", "model_checkpoint", "reduce_lr_on_plateau"]


@dataclass
class TrainingData:
    """Training data container."""
    features: np.ndarray
    labels: np.ndarray
    validation_features: Optional[np.ndarray] = None
    validation_labels: Optional[np.ndarray] = None
    test_features: Optional[np.ndarray] = None
    test_labels: Optional[np.ndarray] = None
    
    def __post_init__(self):
        """Validate training data."""
        if self.features is None or self.labels is None:
            raise ValueError("Features and labels are required")
        
        if len(self.features) != len(self.labels):
            raise ValueError("Features and labels must have the same length")
        
        if self.validation_features is not None and self.validation_labels is not None:
            if len(self.validation_features) != len(self.validation_labels):
                raise ValueError("Validation features and labels must have the same length")
        
        if self.test_features is not None and self.test_labels is not None:
            if len(self.test_features) != len(self.test_labels):
                raise ValueError("Test features and labels must have the same length")


@dataclass
class ModelMetrics:
    """Model performance metrics."""
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    loss: float
    training_time: float
    inference_time: float
    model_size: float
    parameters_count: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "accuracy": self.accuracy,
            "precision": self.precision,
            "recall": self.recall,
            "f1_score": self.f1_score,
            "loss": self.loss,
            "training_time": self.training_time,
            "inference_time": self.inference_time,
            "model_size": self.model_size,
            "parameters_count": self.parameters_count
        }


@dataclass
class DeploymentConfig:
    """Configuration for model deployment."""
    deployment_type: str = "rest_api"
    scaling: str = "auto"
    health_checks: bool = True
    monitoring: bool = True
    version: str = "1.0.0"
    environment: str = "production"
    resources: Dict[str, Any] = None
    
    def __post_init__(self):
        """Set default values after initialization."""
        if self.resources is None:
            self.resources = {
                "cpu": "100m",
                "memory": "256Mi",
                "gpu": None
            }



