"""
ML Optimizer Models - KISS Simplified
=====================================

Simplified data models for ML optimization.
KISS PRINCIPLE: Keep It Simple, Stupid - removed overengineering.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-1 - Integration & Core Systems Specialist
License: MIT
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class MLStrategy(Enum):
    """Simple ML optimization strategies."""
    GRADIENT_DESCENT = "gradient_descent"
    ADAPTIVE_LEARNING = "adaptive_learning"
    BATCH_OPTIMIZATION = "batch_optimization"


class LearningPhase(Enum):
    """Simple learning phases."""
    TRAINING = "training"
    VALIDATION = "validation"
    TESTING = "testing"
    PRODUCTION = "production"


class OptimizationStatus(Enum):
    """Simple optimization status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class MLModel:
    """Simple ML model representation."""
    model_id: str
    name: str
    strategy: MLStrategy
    status: OptimizationStatus
    accuracy: float = 0.0
    created_at: datetime = None
    updated_at: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class LearningPattern:
    """Simple learning pattern model."""
    pattern_id: str
    pattern_type: str
    confidence: float
    frequency: int = 0
    last_seen: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.last_seen is None:
            self.last_seen = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class OptimizationMetrics:
    """Simple optimization metrics."""
    total_models: int = 0
    active_models: int = 0
    average_accuracy: float = 0.0
    optimization_time: float = 0.0
    last_optimization: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.last_optimization is None:
            self.last_optimization = datetime.now()
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        if self.total_models == 0:
            return 0.0
        return self.active_models / self.total_models


@dataclass
class MLConfiguration:
    """Simple ML configuration."""
    config_id: str
    learning_rate: float = 0.01
    batch_size: int = 32
    epochs: int = 100
    validation_split: float = 0.2
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class MLOptimizationConfig:
    """ML optimization configuration."""
    config_id: str
    model_type: str = "default"
    learning_rate: float = 0.01
    batch_size: int = 32
    epochs: int = 100
    strategy: MLStrategy = MLStrategy.GRADIENT_DESCENT
    optimization_type: str = "gradient_descent"
    validation_split: float = 0.2
    early_stopping: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class MLPrediction:
    """ML prediction result."""
    prediction_id: str
    model_id: str
    input_data: Dict[str, Any]
    prediction_value: Any
    confidence: float
    prediction_type: str = "default"
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class LearningPattern:
    """Learning pattern data."""
    pattern_id: str
    pattern_type: str
    pattern_data: Dict[str, Any]
    confidence: float
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ModelState:
    """Model state data."""
    state_id: str
    model_id: str
    session_id: str
    state_data: Dict[str, Any]
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class MLOptimizationMetrics:
    """ML optimization metrics."""
    metrics_id: str
    model_id: str
    session_id: str
    accuracy: float
    loss: float
    metrics_data: Dict[str, Any]
    created_at: datetime = None
    
    def __post_init__(self):
        """Initialize default values."""
        if self.created_at is None:
            self.created_at = datetime.now()


# Factory functions for backward compatibility
def create_ml_model(model_id: str, name: str, strategy: MLStrategy = MLStrategy.GRADIENT_DESCENT) -> MLModel:
    """Create an ML model."""
    return MLModel(
        model_id=model_id,
        name=name,
        strategy=strategy,
        status=OptimizationStatus.PENDING
    )


def create_ml_prediction(prediction_id: str, model_id: str, input_data: Dict[str, Any], 
                        prediction_value: Any, confidence: float) -> MLPrediction:
    """Create an ML prediction."""
    return MLPrediction(
        prediction_id=prediction_id,
        model_id=model_id,
        input_data=input_data,
        prediction_value=prediction_value,
        confidence=confidence
    )


def create_learning_pattern(pattern_id: str, pattern_type: str, confidence: float) -> LearningPattern:
    """Create a learning pattern."""
    return LearningPattern(
        pattern_id=pattern_id,
        pattern_type=pattern_type,
        confidence=confidence
    )


def create_model_state(state_id: str, model_id: str, session_id: str, state_data: Dict[str, Any]) -> ModelState:
    """Create a model state."""
    return ModelState(
        state_id=state_id,
        model_id=model_id,
        session_id=session_id,
        state_data=state_data
    )


def create_optimization_metrics() -> OptimizationMetrics:
    """Create optimization metrics."""
    return OptimizationMetrics()


def create_ml_configuration(config_id: str) -> MLConfiguration:
    """Create ML configuration."""
    return MLConfiguration(config_id=config_id)
