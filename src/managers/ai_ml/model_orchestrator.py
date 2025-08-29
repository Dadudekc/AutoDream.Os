from typing import List, Optional

from src.core.managers.unified_ai_ml_manager import UnifiedAIMLManager
from src.core.models import AIModel

from .interfaces.model import ModelManagerInterface


class ModelOrchestrator(ModelManagerInterface):
    """Orchestration layer for AI/ML model operations."""

    def __init__(self, manager: Optional[UnifiedAIMLManager] = None) -> None:
        self.manager = manager or UnifiedAIMLManager()

    def register_model(self, model: AIModel) -> bool:
        return self.manager.register_model(model)

    def get_model(self, model_id: str) -> Optional[AIModel]:
        return self.manager.get_model(model_id)

    def list_models(
        self, provider: Optional[str] = None, model_type: Optional[str] = None
    ) -> List[AIModel]:
        return self.manager.list_models(provider=provider, model_type=model_type)
