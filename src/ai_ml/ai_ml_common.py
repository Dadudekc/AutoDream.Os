"""Shared utilities and protocol definitions for AI/ML managers."""

from __future__ import annotations

from typing import Any, Dict, Protocol


class DataService(Protocol):
    """Protocol for services that supply datasets."""

    def fetch(self, query: Any) -> Any:
        """Return data for the given ``query``."""


class ModelStore(Protocol):
    """Protocol defining persistence operations for models."""

    def save(self, model: Any, path: str) -> None:
        """Persist ``model`` at ``path``."""

    def load(self, path: str) -> Any:
        """Load a model from ``path``."""


class TrainingFramework(Protocol):
    """Protocol describing required behaviour of training frameworks."""

    def create_model(self, model_config: Dict[str, Any]) -> Any:
        """Create a model using ``model_config``."""

    def train_model(self, model: Any, data: Any) -> Dict[str, Any]:
        """Train ``model`` on ``data`` and return training metadata."""


class EvaluationFramework(Protocol):
    """Protocol describing required behaviour of evaluation frameworks."""

    def evaluate_model(self, model: Any, data: Any) -> Dict[str, float]:
        """Evaluate ``model`` with ``data`` and return metrics."""


DEFAULT_MODEL_DIR = "models"
"""Default directory used for storing models."""
