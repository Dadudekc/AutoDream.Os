from typing import Optional

from src.core.managers.unified_ai_ml_manager import UnifiedAIMLManager

from .agent_orchestrator import AgentOrchestrator
from .api_key_orchestrator import APIKeyOrchestrator
from .model_orchestrator import ModelOrchestrator
from .workflow_orchestrator import WorkflowOrchestrator


class AIMLOrchestrator:
    """Simplified entry point exposing AI/ML subsystem orchestrators."""

    def __init__(self, manager: Optional[UnifiedAIMLManager] = None) -> None:
        self.manager = manager or UnifiedAIMLManager()
        self.models = ModelOrchestrator(self.manager)
        self.agents = AgentOrchestrator(self.manager)
        self.workflows = WorkflowOrchestrator(self.manager)
        self.api_keys = APIKeyOrchestrator(self.manager)


__all__ = ["AIMLOrchestrator"]
