"""
Unified ML Pipeline Utils - V2 Compliant
=========================================

Utility functions for model validation and configuration export.
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import time
from typing import Any

from .unified_ml_pipeline_core import UnifiedMLPipeline
from .unified_ml_pipeline_models import ModelType


class ModelValidator:
    """Model configuration validator."""

    @staticmethod
    def validate_model_config(pipeline: UnifiedMLPipeline) -> list[str]:
        """Validate model configuration and return issues."""
        issues = []

        if not pipeline.current_model:
            issues.append("No model configuration loaded")
            return issues

        model = pipeline.current_model

        # Check for required fields
        if not model.features:
            issues.append("No features defined for model")

        if not model.target:
            issues.append("No target variable defined")

        if model.accuracy < 0.0 or model.accuracy > 1.0:
            issues.append("Invalid accuracy value (must be 0.0-1.0)")

        if model.training_time < 0:
            issues.append("Invalid training time (must be >= 0)")

        return issues


class ModelInfoManager:
    """Model information and metrics manager."""

    @staticmethod
    def get_model_info(pipeline: UnifiedMLPipeline) -> dict[str, Any] | None:
        """Get current model information."""
        if not pipeline.current_model:
            return None

        return {
            "model_name": pipeline.current_model.name,
            "model_type": pipeline.current_model.model_type.value,
            "version": pipeline.current_model.version,
            "accuracy": pipeline.current_model.accuracy,
            "training_time": pipeline.current_model.training_time,
            "features": len(pipeline.current_model.features),
            "parameters": pipeline.current_model.parameters,
            "status": pipeline.pipeline_status.value,
        }

    @staticmethod
    def get_pipeline_metrics(pipeline: UnifiedMLPipeline) -> dict[str, float]:
        """Get pipeline performance metrics."""
        return {
            "accuracy": pipeline.metrics.accuracy,
            "training_time": pipeline.metrics.training_time,
            "inference_time": pipeline.metrics.inference_time,
            "memory_usage": pipeline.metrics.memory_usage,
        }

    @staticmethod
    def reset_pipeline(pipeline: UnifiedMLPipeline):
        """Reset ML pipeline to initial state."""
        from .unified_ml_pipeline_models import PipelineMetrics, PipelineStatus

        pipeline.current_model = None
        pipeline.pipeline_status = PipelineStatus.IDLE
        pipeline.metrics = PipelineMetrics()


class ModelExporter:
    """Model configuration exporter."""

    @staticmethod
    def export_model_config(pipeline: UnifiedMLPipeline, filepath: str) -> bool:
        """Export model configuration to JSON file."""
        try:
            if not pipeline.current_model:
                return False

            config_data = {
                "model_config": {
                    "name": pipeline.current_model.name,
                    "type": pipeline.current_model.model_type.value,
                    "version": pipeline.current_model.version,
                    "parameters": pipeline.current_model.parameters,
                    "features": pipeline.current_model.features,
                    "target": pipeline.current_model.target,
                    "created_at": pipeline.current_model.created_at,
                    "accuracy": pipeline.current_model.accuracy,
                    "training_time": pipeline.current_model.training_time,
                },
                "pipeline_metrics": pipeline.get_pipeline_metrics(),
                "export_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            }

            with open(filepath, "w") as f:
                json.dump(config_data, f, indent=2)
            return True

        except Exception:
            return False


def create_sample_model() -> dict[str, Any]:
    """Create sample model configuration for testing."""
    return {
        "model_type": ModelType.REGRESSION,
        "name": "dream_os_predictor",
        "parameters": {"learning_rate": 0.01, "epochs": 100},
        "features": ["feature1", "feature2", "feature3"],
        "target": "prediction",
    }


def create_sample_training_data() -> dict[str, Any]:
    """Create sample training data for testing."""
    return {
        "features": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
        "targets": [1.5, 2.5, 3.5],
        "feature_names": ["feature1", "feature2", "feature3"],
    }


def run_pipeline_demo():
    """Run a demonstration of the ML pipeline."""
    from .unified_ml_pipeline_core import create_unified_ml_pipeline

    pipeline = create_unified_ml_pipeline()
    validator = ModelValidator()
    exporter = ModelExporter()
    info_manager = ModelInfoManager()

    # Create model configuration
    model_config = create_sample_model()
    model = pipeline.create_model(model_config)

    print(f"✅ Created model: {model.name} v{model.version}")
    print(f"📊 Model type: {model.model_type.value}")
    print(f"🎯 Features: {len(model.features)}")

    # Prepare training data
    training_data_config = create_sample_training_data()
    training_data = pipeline.prepare_training_data(training_data_config)

    print(f"📈 Training data prepared: {len(training_data.features)} samples")

    # Train model
    if pipeline.train_model(training_data):
        print("✅ Model training completed successfully")
        print(f"📊 Accuracy: {pipeline.current_model.accuracy:.3f}")
        print(f"⏱️ Training time: {pipeline.current_model.training_time:.2f}s")
    else:
        print("❌ Model training failed")

    # Make prediction
    prediction = pipeline.make_prediction([1.0, 2.0, 3.0])
    if prediction is not None:
        print(f"🔮 Prediction: {prediction:.3f}")
    else:
        print("❌ Prediction failed")

    # Save model
    if pipeline.save_model():
        print("💾 Model saved successfully")
    else:
        print("❌ Model save failed")

    # Validate model
    issues = validator.validate_model_config(pipeline)
    if not issues:
        print("✅ Model validation passed")
    else:
        print(f"⚠️ Validation issues: {issues}")

    # Export model config
    if exporter.export_model_config(pipeline, "model_config.json"):
        print("📤 Model configuration exported")
    else:
        print("❌ Model export failed")

    # Get model info
    info = info_manager.get_model_info(pipeline)
    if info:
        print(f"📋 Model info: {info['model_name']} v{info['version']}")
    else:
        print("❌ Failed to get model info")
