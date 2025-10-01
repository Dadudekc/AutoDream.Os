"""
Unified ML Pipeline Models - V2 Compliant
==========================================

Data models and configurations for the unified ML pipeline.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class PipelineStatus(Enum):
    """ML Pipeline status enumeration."""

    IDLE = "idle"
    TRAINING = "training"
    INFERENCE = "inference"
    ERROR = "error"
    COMPLETED = "completed"


class ModelType(Enum):
    """ML Model type enumeration."""

    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    RECOMMENDATION = "recommendation"


@dataclass
class ModelConfig:
    """ML Model configuration data structure."""

    model_type: ModelType
    name: str
    version: str
    parameters: dict[str, Any]
    features: list[str]
    target: str
    created_at: str
    accuracy: float = 0.0
    training_time: float = 0.0


@dataclass
class TrainingData:
    """Training data structure."""

    features: list[list[float]]
    targets: list[float]
    feature_names: list[str]
    validation_split: float = 0.2
    test_split: float = 0.1

    def __post_init__(self):
        """Validate training data."""
        if len(self.features) != len(self.targets):
            raise ValueError("Features and targets must have same length")


@dataclass
class PipelineMetrics:
    """ML Pipeline metrics data structure."""

    accuracy: float = 0.0
    precision: float = 0.0
    recall: float = 0.0
    f1_score: float = 0.0
    training_time: float = 0.0
    inference_time: float = 0.0
    memory_usage: float = 0.0
