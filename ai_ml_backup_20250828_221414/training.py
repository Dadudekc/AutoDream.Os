"""ML model training interfaces."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class MLFramework(ABC):
    """Abstract base class for ML frameworks."""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.is_initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the ML framework."""

    @abstractmethod
    def create_model(self, model_config: Dict[str, Any]) -> Any:
        """Create a model using the framework."""

    @abstractmethod
    def train_model(self, model: Any, data: Any, **kwargs) -> Dict[str, Any]:
        """Train a model."""

    @abstractmethod
    def evaluate_model(self, model: Any, test_data: Any) -> Dict[str, float]:
        """Evaluate a model."""

    @abstractmethod
    def save_model(self, model: Any, path: str) -> bool:
        """Save a model to disk."""

    @abstractmethod
    def load_model(self, path: str) -> Any:
        """Load a model from disk."""

