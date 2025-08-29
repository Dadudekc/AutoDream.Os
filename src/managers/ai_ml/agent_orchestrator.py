from typing import List, Optional

from src.core.managers.unified_ai_ml_manager import UnifiedAIMLManager
from src.core.models import AIAgent

from .interfaces.agent import AgentManagerInterface


class AgentOrchestrator(AgentManagerInterface):
    """Orchestration layer for AI agent operations."""

    def __init__(self, manager: Optional[UnifiedAIMLManager] = None) -> None:
        self.manager = manager or UnifiedAIMLManager()

    def register_agent(self, agent: AIAgent) -> bool:
        return self.manager.register_agent(agent)

    def get_agent(self, agent_id: str) -> Optional[AIAgent]:
        return self.manager.get_agent(agent_id)

    def list_agents(self, agent_type: Optional[str] = None) -> List[AIAgent]:
        return self.manager.list_agents(agent_type=agent_type)
