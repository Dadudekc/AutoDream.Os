"""API key operations for ModelManager."""

from datetime import datetime
from typing import Optional


class APIKeyMixin:
    """Mixin for API key retrieval."""

    api_keys: any
    api_key_operations: list

    def get_api_key(self, service: str) -> Optional[str]:
        """Proxy API key retrieval to the API key manager."""
        try:
            start_time = datetime.now()
            api_key = self.api_keys.get_key(service)
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "get_api_key",
                "service": service,
                "success": api_key is not None,
            }
            self.api_key_operations.append(operation_record)
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("get_api_key", api_key is not None, operation_time)
            return api_key
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Error getting API key for {service}: {e}")
            self.record_operation("get_api_key", False, 0.0)
            return None
