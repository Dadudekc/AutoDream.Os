"""Base functionality for ModelManager."""

from pathlib import Path
from typing import Dict, List, Optional, Any

from ...core.base_manager import BaseManager
from ..api_key_manager import APIKeyManager


class ModelManagerBase(BaseManager):
    """Initialization and lifecycle management for models."""

    def __init__(
        self,
        storage_path: str = "models",
        api_key_manager: Optional[APIKeyManager] = None,
    ):
        super().__init__(
            manager_id="model_manager",
            name="Model Manager",
            description="Manages AI/ML models and their lifecycle",
        )
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.models: Dict[str, Dict[str, Any]] = {}
        self.api_keys = api_key_manager or APIKeyManager()

        self.model_operations: List[Dict[str, Any]] = []
        self.storage_operations: List[Dict[str, Any]] = []
        self.api_key_operations: List[Dict[str, Any]] = []

        self._load_model_registry()
        self.logger.info("Model Manager initialized")

    # lifecycle hooks -------------------------------------------------
    def _on_start(self) -> bool:
        """Initialize model management system."""
        try:
            self.logger.info("Starting Model Manager...")
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self.logger.info("Model Manager started successfully")
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to start Model Manager: {e}")
            return False

    def _on_stop(self) -> None:
        """Cleanup model management system."""
        try:
            self.logger.info("Stopping Model Manager...")
            self._save_model_management_data()
            self._save_model_registry()
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()
            self.logger.info("Model Manager stopped successfully")
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to stop Model Manager: {e}")

    def _on_heartbeat(self) -> None:
        """Model manager heartbeat."""
        try:
            self._check_model_management_health()
            self.record_operation("heartbeat", True, 0.0)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        """Initialize model management resources."""
        try:
            self.model_operations = []
            self.storage_operations = []
            self.api_key_operations = []
            self.storage_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self) -> None:
        """Cleanup model management resources."""
        try:
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors."""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            self._load_model_registry()
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()
            self.logger.info("Recovery successful")
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Recovery failed: {e}")
            return False
