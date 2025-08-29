from typing import Optional

from src.core.managers.unified_ai_ml_manager import UnifiedAIMLManager

from .interfaces.api_key import APIKeyManagerInterface


class APIKeyOrchestrator(APIKeyManagerInterface):
    """Orchestration layer for API key management."""

    def __init__(self, manager: Optional[UnifiedAIMLManager] = None) -> None:
        self.manager = manager or UnifiedAIMLManager()

    def generate_api_key(
        self, service: str, description: str = "", expires_in_days: int = 365
    ) -> str:
        return self.manager.generate_api_key(service, description, expires_in_days)

    def validate_api_key(self, api_key: str, service: str) -> bool:
        return self.manager.validate_api_key(api_key, service)

    def revoke_api_key(self, key_id: str) -> bool:
        return self.manager.revoke_api_key(key_id)
