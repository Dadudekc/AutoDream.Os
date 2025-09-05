"""
ML Learning Models
=================

Data models for ML learning engine operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from enum import Enum
import uuid


class LearningStatus(Enum):
    """Learning status."""
    IDLE = "idle"
    TRAINING = "training"
    PREDICTING = "predicting"
    EVALUATING = "evaluating"
    ERROR = "error"


class ModelType(Enum):
    """Model type."""
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    REINFORCEMENT = "reinforcement"


class FeatureType(Enum):
    """Feature type."""
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEXT = "text"
    IMAGE = "image"
    TIME_SERIES = "time_series"


@dataclass
class LearningPattern:
    """Learning pattern data."""
    pattern_id: str
    name: str
    description: str
    pattern_type: str
    features: List[str]
    target: str
    data_points: int
    accuracy: float
    created_at: datetime
    updated_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class MLPrediction:
    """ML prediction data."""
    prediction_id: str
    model_id: str
    input_data: Dict[str, Any]
    prediction: Any
    confidence: float
    prediction_type: str
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class ModelState:
    """Model state data."""
    model_id: str
    name: str
    model_type: ModelType
    status: LearningStatus
    accuracy: float
    loss: float
    epochs_trained: int
    last_trained: datetime
    parameters: Dict[str, Any]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.last_trained is None:
            self.last_trained = datetime.now()


@dataclass
class MLOptimizationMetrics:
    """ML optimization metrics."""
    metrics_id: str
    model_id: str
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    loss: float
    training_time: float
    prediction_time: float
    memory_usage: float
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class MLOptimizationConfig:
    """ML optimization configuration."""
    config_id: str
    name: str
    description: str
    learning_rate: float
    batch_size: int
    epochs: int
    validation_split: float
    early_stopping: bool
    model_type: ModelType
    features: List[str]
    target: str
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class FeatureAnalysis:
    """Feature analysis data."""
    analysis_id: str
    feature_name: str
    feature_type: FeatureType
    importance: float
    correlation: float
    missing_values: int
    unique_values: int
    statistics: Dict[str, Any]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class LearningSession:
    """Learning session data."""
    session_id: str
    model_id: str
    config_id: str
    status: LearningStatus
    start_time: datetime
    end_time: Optional[datetime]
    metrics: Optional[MLOptimizationMetrics]
    created_at: datetime
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


# KISS Simplified - Factory methods removed, use direct constructors
def validate_learning_pattern(pattern: LearningPattern) -> Dict[str, Any]:
    """Validate learning pattern - KISS simplified."""
    validation = {'is_valid': True, 'warnings': [], 'errors': []}
    
    if not pattern.name:
        validation['errors'].append("Pattern name is required")
        validation['is_valid'] = False
    
    if not pattern.features:
        validation['errors'].append("Features are required")
        validation['is_valid'] = False
    
    if pattern.accuracy < 0 or pattern.accuracy > 1:
        validation['warnings'].append("Accuracy should be between 0 and 1")
    
    return validation

def validate_model_state(state: ModelState) -> Dict[str, Any]:
    """Validate model state - KISS simplified."""
    validation = {'is_valid': True, 'warnings': [], 'errors': []}
    
    if not state.name:
        validation['errors'].append("Model name is required")
        validation['is_valid'] = False
    
    if state.accuracy < 0 or state.accuracy > 1:
        validation['warnings'].append("Accuracy should be between 0 and 1")
    
    return validation
