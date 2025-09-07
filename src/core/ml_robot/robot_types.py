#!/usr/bin/env python3
"""
ML Robot Types - Data Classes and Type Definitions
=================================================

Contains all data classes and type definitions for the ML Robot system.
Extracted from monolithic test_ml_robot_maker.py for V2 standards compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, Optional, Any, List


@dataclass
class ModelConfig:
    """Configuration for ML model creation"""

    model_type: str  # "classification", "regression", "clustering", "nlp"
    algorithm: str  # "random_forest", "neural_network", "svm", etc.
    hyperparameters: Dict[str, Any]
    input_features: int
    output_classes: Optional[int] = None
    architecture: Optional[str] = None
    pretrained: bool = False

    def __post_init__(self):
        if self.output_classes is None and self.model_type in [
            "classification",
            "clustering",
        ]:
            self.output_classes = 2


@dataclass
class TrainingConfig:
    """Configuration for model training"""

    epochs: int = 100
    batch_size: int = 32
    learning_rate: float = 0.001
    validation_split: float = 0.2
    early_stopping: bool = True
    patience: int = 10
    optimizer: str = "adam"
    loss_function: str = "auto"
    metrics: List[str] = None

    def __post_init__(self):
        if self.metrics is None:
            if self.loss_function == "auto":
                self.loss_function = "binary_crossentropy"
            self.metrics = ["accuracy"]


@dataclass
class DatasetConfig:
    """Configuration for dataset handling"""

    data_path: str
    data_type: str  # "csv", "json", "image", "text"
    target_column: str
    feature_columns: List[str] = None
    test_size: float = 0.2
    random_state: int = 42
    preprocessing: List[str] = None

    def __post_init__(self):
        if self.preprocessing is None:
            self.preprocessing = ["normalization", "encoding"]


@dataclass
class ModelResult:
    """Result of model creation and training"""

    model_id: str
    model_path: str
    config: ModelConfig
    training_history: Dict[str, List[float]]
    performance_metrics: Dict[str, float]
    training_time: float
    model_size: float
    accuracy: Optional[float] = None
    loss: Optional[float] = None

    def __post_init__(self):
        if self.accuracy is None:
            self.accuracy = self.performance_metrics.get("accuracy", 0.0)
        if self.loss is None:
            self.loss = self.performance_metrics.get("loss", float("inf"))


def run_smoke_test():
    """Run smoke test for robot types module"""
    print("🧪 Testing ML Robot Types Module...")
    
    try:
        # Test ModelConfig
        model_config = ModelConfig(
            model_type="classification",
            algorithm="neural_network",
            hyperparameters={"layers": 2, "neurons": 64},
            input_features=10,
            output_classes=3
        )
        assert model_config.model_type == "classification"
        assert model_config.output_classes == 3
        print("✅ ModelConfig smoke test passed")

        # Test TrainingConfig
        training_config = TrainingConfig(
            epochs=200,
            batch_size=64,
            learning_rate=0.0001
        )
        assert training_config.epochs == 200
        assert training_config.metrics == ["accuracy"]
        print("✅ TrainingConfig smoke test passed")

        # Test DatasetConfig
        dataset_config = DatasetConfig(
            data_path="data/test.csv",
            data_type="csv",
            target_column="target"
        )
        assert dataset_config.data_path == "data/test.csv"
        assert dataset_config.preprocessing == ["normalization", "encoding"]
        print("✅ DatasetConfig smoke test passed")

        # Test ModelResult
        result = ModelResult(
            model_id="test_123",
            model_path="models/test.pkl",
            config=model_config,
            training_history={"loss": [1.0, 0.5]},
            performance_metrics={"accuracy": 0.85},
            training_time=15.0,
            model_size=25.0
        )
        assert result.model_id == "test_123"
        assert result.accuracy == 0.85
        print("✅ ModelResult smoke test passed")

        print("🎉 All robot types smoke tests passed!")
        return True

    except Exception as e:
        print(f"❌ Robot types smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
