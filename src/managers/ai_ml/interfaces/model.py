from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.models import AIModel


class ModelManagerInterface(ABC):
    """Interface for AI/ML model management operations."""

    @abstractmethod
    def register_model(self, model: AIModel) -> bool:
        """Register an AI model."""

    @abstractmethod
    def get_model(self, model_id: str) -> Optional[AIModel]:
        """Retrieve an AI model by ID."""

    @abstractmethod
    def list_models(
        self, provider: Optional[str] = None, model_type: Optional[str] = None
    ) -> List[AIModel]:
        """List available models with optional filtering."""
