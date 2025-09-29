#!/usr/bin/env python3
"""
ML Pipeline Utils - V2-Compliant Module
=======================================

Utility functions and helper classes for ML pipeline.
File size: ≤150 lines, Classes: ≤5, Functions: ≤10
"""

import logging
import sys
from pathlib import Path
from typing import Any

import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


class DataProcessor:
    """Data processing utilities."""

    def __init__(self):
        """Initialize data processor."""
        self.processed_data_count = 0
        logger.info("DataProcessor initialized")

    def normalize_data(self, data: np.ndarray, method: str = "standard") -> np.ndarray:
        """Normalize data using specified method."""
        try:
            if method == "standard":
                return (data - np.mean(data, axis=0)) / np.std(data, axis=0)
            elif method == "minmax":
                return (data - np.min(data, axis=0)) / (np.max(data, axis=0) - np.min(data, axis=0))
            else:
                raise ValueError(f"Unsupported normalization method: {method}")
        except Exception as e:
            logger.error(f"Error normalizing data: {e}")
            return data

    def split_data(
        self, data: np.ndarray, labels: np.ndarray, test_size: float = 0.2, val_size: float = 0.1
    ) -> dict[str, Any]:
        """Split data into train/validation/test sets."""
        try:
            n_samples = len(data)
            test_samples = int(n_samples * test_size)
            val_samples = int(n_samples * val_size)
            indices = np.random.permutation(n_samples)

            return {
                "train_data": data[indices[test_samples + val_samples :]],
                "train_labels": labels[indices[test_samples + val_samples :]],
                "val_data": data[indices[test_samples : test_samples + val_samples]],
                "val_labels": labels[indices[test_samples : test_samples + val_samples]],
                "test_data": data[indices[:test_samples]],
                "test_labels": labels[indices[:test_samples]],
            }
        except Exception as e:
            logger.error(f"Error splitting data: {e}")
            return {}


class ModelValidator:
    """Model validation utilities."""

    def __init__(self):
        """Initialize model validator."""
        self.validation_count = 0
        logger.info("ModelValidator initialized")

    def validate_results(
        self, training_results: dict[str, Any], evaluation_results: dict[str, Any]
    ) -> dict[str, Any]:
        """Validate training and evaluation results."""
        try:
            training_valid = self._validate_training_results(training_results)
            evaluation_valid = self._validate_evaluation_results(evaluation_results)
            self.validation_count += 1

            return {
                "training_valid": training_valid,
                "evaluation_valid": evaluation_valid,
                "overall_valid": training_valid and evaluation_valid,
            }
        except Exception as e:
            logger.error(f"Error validating results: {e}")
            return {"overall_valid": False, "error": str(e)}

    def _validate_training_results(self, results: dict[str, Any]) -> bool:
        """Validate training results."""
        try:
            return (
                results.get("status") == "completed"
                and "epochs" in results
                and "training_time" in results
                and results.get("training_time", 0) >= 0
            )
        except Exception as e:
            logger.error(f"Error validating training results: {e}")
            return False

    def _validate_evaluation_results(self, results: dict[str, Any]) -> bool:
        """Validate evaluation results."""
        try:
            metrics = results.get("metrics", {})
            accuracy = metrics.get("accuracy", 0)
            return results.get("status") == "completed" and metrics and 0 <= accuracy <= 1
        except Exception as e:
            logger.error(f"Error validating evaluation results: {e}")
            return False


def calculate_model_complexity(model: Any) -> dict[str, int]:
    """Calculate model complexity metrics."""
    try:
        metrics = {"layers": 0, "parameters": 0, "trainable_parameters": 0}
        if hasattr(model, "layers"):
            metrics["layers"] = len(model.layers)
        if hasattr(model, "count_params"):
            metrics["parameters"] = model.count_params()
            metrics["trainable_parameters"] = model.count_params()
        return metrics
    except Exception as e:
        logger.error(f"Error calculating model complexity: {e}")
        return {"layers": 0, "parameters": 0, "trainable_parameters": 0}


def format_metrics(metrics: dict[str, Any]) -> str:
    """Format metrics for display."""
    try:
        formatted = []
        for key, value in metrics.items():
            if isinstance(value, float):
                formatted.append(f"{key}: {value:.4f}")
            else:
                formatted.append(f"{key}: {value}")
        return "\n".join(formatted)
    except Exception as e:
        logger.error(f"Error formatting metrics: {e}")
        return str(metrics)


def validate_config(config: dict[str, Any]) -> bool:
    """Validate configuration parameters."""
    try:
        required_fields = ["model_type", "num_classes"]
        for field in required_fields:
            if field not in config:
                logger.error(f"Missing required field: {field}")
                return False
        return config.get("num_classes", 0) > 0 and config.get("epochs", 0) > 0
    except Exception as e:
        logger.error(f"Error validating config: {e}")
        return False


def get_system_info() -> dict[str, Any]:
    """Get system information for ML pipeline."""
    try:
        import platform

        import psutil

        return {
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
        }
    except ImportError:
        return {
            "platform": "unknown",
            "python_version": "unknown",
            "cpu_count": "unknown",
            "memory_total": "unknown",
            "memory_available": "unknown",
        }
    except Exception as e:
        logger.error(f"Error getting system info: {e}")
        return {"error": str(e)}
