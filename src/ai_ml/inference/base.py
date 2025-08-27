"""Base functionality for AIManager."""

from pathlib import Path
from typing import Dict, List, Optional, Any

from ...core.base_manager import BaseManager
from ..engine import AIEngine
from ..api_key_manager import APIKeyManager
from ..models import AIModel
from ..workflows import MLWorkflow


class AIManagerBase(BaseManager):
    """Provides initialization and lifecycle management."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        api_key_manager: Optional[APIKeyManager] = None,
    ):
        """Initialize AI manager with BaseManager."""
        super().__init__(
            manager_id="ai_manager",
            name="AI Manager",
            description="Central AI management and coordination",
        )

        self.config_path = (
            Path(config_path) if config_path else Path("config/ai_ml/ai_ml.json")
        )
        self.engine = AIEngine(config_path=self.config_path)
        self.models: Dict[str, AIModel] = {}
        self.active_workflows: Dict[str, MLWorkflow] = {}
        self.config = self.engine.config
        self.api_keys = api_key_manager or APIKeyManager()

        # tracking structures
        self.model_registrations: List[Dict[str, Any]] = []
        self.workflow_executions: List[Dict[str, Any]] = []
        self.api_key_requests: List[Dict[str, Any]] = []

        self.logger.info("AI Manager initialized")

    # lifecycle hooks -------------------------------------------------
    def _on_start(self) -> bool:
        """Initialize AI management system."""
        try:
            self.logger.info("Starting AI Manager...")
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()

            if not self.config:
                self.logger.warning("No configuration loaded")

            self.logger.info("AI Manager started successfully")
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to start AI Manager: {e}")
            return False

    def _on_stop(self) -> None:
        """Cleanup AI management system."""
        try:
            self.logger.info("Stopping AI Manager...")
            self._save_ai_management_data()

            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()

            self.logger.info("AI Manager stopped successfully")
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to stop AI Manager: {e}")

    def _on_heartbeat(self) -> None:
        """AI manager heartbeat."""
        try:
            self._check_ai_management_health()
            self.record_operation("heartbeat", True, 0.0)
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        """Initialize AI management resources."""
        try:
            self.model_registrations = []
            self.workflow_executions = []
            self.api_key_requests = []
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self) -> None:
        """Cleanup AI management resources."""
        try:
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors."""
        try:
            self.logger.info(f"Attempting recovery for {context}")
            self.config = self.engine.load_config()
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()
            self.logger.info("Recovery successful")
            return True
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Recovery failed: {e}")
            return False
