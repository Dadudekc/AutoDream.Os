"""
AI/ML Framework Module
Modularized from src/ai_ml/core.py

Contains the abstract base class for ML frameworks:
- MLFramework: Abstract base class for ML frameworks
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class MLFramework(ABC):
    """Abstract base class for ML frameworks"""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.is_initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the ML framework.

        Returns:
            bool: True if initialization succeeded.
        """
        raise NotImplementedError("initialize must be implemented by subclasses")

    @abstractmethod
    def create_model(self, model_config: Dict[str, Any]) -> Any:
        """Create a model using the framework.

        Args:
            model_config (Dict[str, Any]): Model configuration parameters.

        Returns:
            Any: The created model instance.
        """
        raise NotImplementedError("create_model must be implemented by subclasses")

    @abstractmethod
    def train_model(self, model: Any, data: Any, **kwargs) -> Dict[str, Any]:
        """Train a model.

        Args:
            model (Any): Model instance to train.
            data (Any): Training data.
            **kwargs: Additional training parameters.

        Returns:
            Dict[str, Any]: Training metrics or results.
        """
        raise NotImplementedError("train_model must be implemented by subclasses")

    @abstractmethod
    def evaluate_model(self, model: Any, test_data: Any) -> Dict[str, float]:
        """Evaluate a model.

        Args:
            model (Any): Model instance to evaluate.
            test_data (Any): Evaluation dataset.

        Returns:
            Dict[str, float]: Evaluation metrics.
        """
        raise NotImplementedError("evaluate_model must be implemented by subclasses")

    @abstractmethod
    def save_model(self, model: Any, path: str) -> bool:
        """Save a model to disk.

        Args:
            model (Any): Model instance.
            path (str): Destination path.

        Returns:
            bool: True if the model was saved successfully.
        """
        raise NotImplementedError("save_model must be implemented by subclasses")

    @abstractmethod
    def load_model(self, path: str) -> Any:
        """Load a model from disk.

        Args:
            path (str): Path to the saved model.

        Returns:
            Any: The loaded model instance.
        """
        raise NotImplementedError("load_model must be implemented by subclasses")
