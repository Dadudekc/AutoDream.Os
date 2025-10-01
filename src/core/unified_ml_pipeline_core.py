"""
Unified ML Pipeline Core - V2 Compliant
========================================

Core ML pipeline functionality with training and inference capabilities.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import hashlib
import os
import pickle
import time
from pathlib import Path
from typing import Any

from .unified_ml_pipeline_models import (
    ModelConfig,
    ModelType,
    PipelineMetrics,
    PipelineStatus,
    TrainingData,
)


class UnifiedMLPipeline:
    """
    Unified ML Pipeline Core - V2 Compliant Implementation.

    Provides consolidated machine learning pipeline functionality with
    V2 compliance and quality-focused design.
    """

    def __init__(self, model_storage_path: str = "./models"):
        """Initialize unified ML pipeline."""
        self.model_storage_path = Path(model_storage_path)
        self.current_model: ModelConfig | None = None
        self.pipeline_status = PipelineStatus.IDLE
        self.metrics = PipelineMetrics()
        self._ensure_storage_path()

    def _ensure_storage_path(self):
        """Ensure model storage path exists."""
        self.model_storage_path.mkdir(parents=True, exist_ok=True)

    def create_model(self, config: dict[str, Any]) -> ModelConfig:
        """Create a new ML model configuration."""
        self.pipeline_status = PipelineStatus.IDLE

        model = ModelConfig(
            model_type=config["model_type"],
            name=config["name"],
            version=f"1.0.0-{int(time.time())}",
            parameters=config["parameters"],
            features=config["features"],
            target=config["target"],
            created_at=time.strftime("%Y-%m-%d %H:%M:%S"),
        )

        self.current_model = model
        return model

    def prepare_training_data(self, data: dict[str, Any]) -> TrainingData:
        """Prepare training data for ML model."""
        if not self.current_model:
            raise ValueError("No model configuration available")

        features = data.get("features", [])
        targets = data.get("targets", [])
        feature_names = data.get("feature_names", [])

        if len(features) != len(targets):
            raise ValueError("Features and targets must have same length")

        return TrainingData(features=features, targets=targets, feature_names=feature_names)

    def train_model(self, training_data: TrainingData) -> bool:
        """Train the ML model with provided data."""
        if not self.current_model:
            return False

        try:
            self.pipeline_status = PipelineStatus.TRAINING
            start_time = time.time()

            # Simple training simulation (replace with actual ML training)
            model_hash = hashlib.md5(
                f"{self.current_model.name}-{self.current_model.version}".encode()
            ).hexdigest()

            # Simulate training process
            time.sleep(1)  # Simulate training time
            accuracy = 0.85 + (hash(model_hash) % 1000) / 10000  # 0.85-0.95 range

            self.current_model.accuracy = accuracy
            self.current_model.training_time = time.time() - start_time
            self.metrics.accuracy = accuracy
            self.metrics.training_time = self.current_model.training_time

            self.pipeline_status = PipelineStatus.COMPLETED
            return True

        except Exception:
            self.pipeline_status = PipelineStatus.ERROR
            return False

    def make_prediction(self, input_data: list[float]) -> float | None:
        """Make prediction using trained model."""
        if not self.current_model or self.pipeline_status != PipelineStatus.COMPLETED:
            return None

        try:
            # Simple prediction simulation (replace with actual ML inference)
            if self.current_model.model_type == ModelType.REGRESSION:
                # Simple linear regression simulation
                prediction = sum(x * (i + 1) * 0.1 for i, x in enumerate(input_data))
            elif self.current_model.model_type == ModelType.CLASSIFICATION:
                # Simple classification simulation
                prediction = 1.0 if sum(input_data) > len(input_data) * 0.5 else 0.0
            else:
                prediction = 0.5

            self.metrics.inference_time = 0.001  # Simulate fast inference
            return prediction

        except Exception:
            return None

    def save_model(self, filepath: str | None = None) -> bool:
        """Save trained model to file."""
        if not self.current_model or self.pipeline_status != PipelineStatus.COMPLETED:
            return False

        try:
            if filepath is None:
                filepath = str(
                    self.model_storage_path
                    / f"{self.current_model.name}_v{self.current_model.version}.pkl"
                )

            model_data = {
                "config": self.current_model.__dict__,
                "metrics": self.metrics.__dict__,
                "saved_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            with open(filepath, "wb") as f:
                pickle.dump(model_data, f)

            return True

        except Exception:
            return False

    def load_model(self, filepath: str) -> bool:
        """Load trained model from file."""
        try:
            if not os.path.exists(filepath):
                return False

            with open(filepath, "rb") as f:
                model_data = pickle.load(f)

            config_data = model_data.get("config", {})
            self.current_model = ModelConfig(**config_data)
            self.metrics = PipelineMetrics(**model_data.get("metrics", {}))
            self.pipeline_status = PipelineStatus.COMPLETED

            return True

        except Exception:
            return False


def create_unified_ml_pipeline() -> UnifiedMLPipeline:
    """Create unified ML pipeline instance."""
    return UnifiedMLPipeline()
