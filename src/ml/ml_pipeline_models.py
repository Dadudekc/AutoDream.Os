"""
ML Pipeline Core Models
V2 Compliant data models for ML pipeline
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import numpy as np


@dataclass
class ModelConfig:
    """Model configuration"""
    model_type: str = "default"
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2
    random_seed: int = 42


@dataclass
class TrainingData:
    """Training data structure"""
    features: np.ndarray
    labels: np.ndarray
    metadata: Dict[str, Any]


@dataclass
class ModelMetrics:
    """Model performance metrics"""
    accuracy: float
    loss: float
    precision: float
    recall: float
    f1_score: float
    training_time: float
    validation_time: float


@dataclass
class ModelResult:
    """Model prediction result"""
    predictions: np.ndarray
    confidence: float
    processing_time: float
    model_version: str