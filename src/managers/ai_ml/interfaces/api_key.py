from abc import ABC, abstractmethod


class APIKeyManagerInterface(ABC):
    """Interface for API key lifecycle operations."""

    @abstractmethod
    def generate_api_key(
        self, service: str, description: str = "", expires_in_days: int = 365
    ) -> str:
        """Generate a new API key for a service."""

    @abstractmethod
    def validate_api_key(self, api_key: str, service: str) -> bool:
        """Validate that an API key is active for a service."""

    @abstractmethod
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke an API key by identifier."""
