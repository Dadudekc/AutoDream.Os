#!/usr/bin/env python3
"""Extended AI Manager - Agent Cellphone V2
=======================================

Consolidated AIManager inheriting from BaseManager.
Follows V2 standards: OOP, SRP, clean production-grade code.
"""

from typing import Any, Dict, List, Optional
import logging

from src.core.base_manager import BaseManager
from src.extended.ai_ml.config import load_ai_config
from src.extended.ai_ml.constants import DEFAULT_AI_MANAGER_CONFIG
from src.extended.ai_ml.lifecycle import AgentLifecycle
from src.core.metrics import MetricsCollector

logger = logging.getLogger(__name__)


class ExtendedAIManager(BaseManager):
    """Extended AI Manager - inherits from BaseManager for unified functionality."""

    def __init__(self, config_path: str = DEFAULT_AI_MANAGER_CONFIG) -> None:
        super().__init__(
            manager_name="ExtendedAIManager",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True,
        )
        self.metrics = MetricsCollector()
        self.lifecycle = AgentLifecycle(self.metrics, self.emit_event)
        self.api_keys: Dict[str, str] = {}
        self._load_ai_config()
        logger.info("ExtendedAIManager initialized successfully")

    def _load_ai_config(self) -> None:
        """Load AI-specific configuration."""
        if self.config:
            cfg = load_ai_config(self.config.get("ai_ml", {}))
            self.api_keys = cfg.api_keys
            self.emit_event(
                "ai_config_loaded",
                {
                    "models_count": len(self.lifecycle.models),
                    "workflows_count": len(self.lifecycle.workflows),
                    "api_keys_count": len(self.api_keys),
                },
            )

    # Agent lifecycle wrappers
    def register_model(self, model: Any) -> bool:
        """Register an AI model."""
        return self.lifecycle.register_model(model)

    def get_model(self, model_name: str) -> Optional[Any]:
        """Get a registered model by name."""
        return self.lifecycle.get_model(model_name)

    def list_models(self) -> List[str]:
        """List all registered model names."""
        return self.lifecycle.list_models()

    def create_workflow(self, name: str, description: str) -> Dict[str, Any]:
        """Create a new ML workflow."""
        return self.lifecycle.create_workflow(name, description)

    def get_workflow(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a workflow by name."""
        return self.lifecycle.get_workflow(name)

    def list_workflows(self) -> List[str]:
        """List all active workflow names."""
        return self.lifecycle.list_workflows()

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow."""
        return self.lifecycle.execute_workflow(workflow_name)

    def add_workflow_step(
        self, workflow_name: str, step_name: str, step_type: str = "task"
    ) -> bool:
        """Add a step to a workflow."""
        return self.lifecycle.add_workflow_step(workflow_name, step_name, step_type)

    def get_api_key(self, service: str) -> Optional[str]:
        """Get API key for a specific service."""
        api_key = self.api_keys.get(service)
        if api_key:
            self.emit_event("api_key_retrieved", {"service": service})
        return api_key
