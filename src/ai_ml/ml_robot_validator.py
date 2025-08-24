"""Validation helpers for the modular ML Robot system."""
from __future__ import annotations

from typing import Any, Dict, List


def _default_values() -> Dict[str, Any]:
    return {
        "framework": "scikit_learn",
        "architecture": {"type": "auto", "parameters": {}},
        "hyperparameters": {"learning_rate": 0.001, "batch_size": 32, "epochs": 10},
        "training_config": {"optimizer": "adam", "loss_function": "auto", "validation_split": 0.2},
        "evaluation_metrics": ["accuracy"],
    }


def get_default_value(key: str) -> Any:
    """Return a default value for a blueprint configuration key."""
    return _default_values().get(key, {})


def validate_blueprint_config(config: Dict[str, Any], supported_frameworks: List[str]) -> Dict[str, Any]:
    """Ensure blueprint config contains required keys and valid framework."""
    required = [
        "framework",
        "architecture",
        "hyperparameters",
        "training_config",
        "evaluation_metrics",
    ]
    for key in required:
        config.setdefault(key, get_default_value(key))
    if config["framework"] not in supported_frameworks:
        config["framework"] = get_default_value("framework")
    return config


__all__ = ["validate_blueprint_config", "get_default_value"]
