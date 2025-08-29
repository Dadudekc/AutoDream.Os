"""
AI/ML Manager Module
Modularized from src/ai_ml/core.py

Contains the central AI management and coordination:
- AIManager: Central AI management and coordination class
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from src.utils.stability_improvements import stability_manager, safe_import
from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority
from .models import AIModel, MLWorkflow
from .api_key_manager import APIKeyManager


class AIManager(BaseManager):
    """Central AI management and coordination

    Now inherits from BaseManager for unified functionality
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        api_key_manager: Optional[APIKeyManager] = None,
    ):
        """Initialize AI manager with BaseManager"""
        super().__init__(
            manager_id="ai_manager",
            name="AI Manager",
            description="Central AI management and coordination",
        )

        self.config_path = (
            Path(config_path) if config_path else Path("config/ai_ml/ai_ml.json")
        )
        self.models: Dict[str, AIModel] = {}
        self.active_workflows: Dict[str, MLWorkflow] = {}
        self.config = self._load_config()
        self.api_keys = api_key_manager or APIKeyManager()

        # AI management tracking
        self.model_registrations: List[Dict[str, Any]] = []
        self.workflow_executions: List[Dict[str, Any]] = []
        self.api_key_requests: List[Dict[str, Any]] = []

        self._setup_logging()
        self.logger.info("AI Manager initialized")

    def _setup_logging(self):
        """Setup logging for AI manager"""
        self.logger = logging.getLogger(__name__)

    def _load_config(self) -> Dict[str, Any]:
        """Load AI/ML configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================

    def _on_start(self) -> bool:
        """Initialize AI management system"""
        try:
            self.logger.info("Starting AI Manager...")

            # Clear tracking data
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()

            # Validate configuration
            if not self.config:
                self.logger.warning("No configuration loaded")

            self.logger.info("AI Manager started successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start AI Manager: {e}")
            return False

    def _on_stop(self):
        """Cleanup AI management system"""
        try:
            self.logger.info("Stopping AI Manager...")

            # Save tracking data
            self._save_ai_management_data()

            # Clear data
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()

            self.logger.info("AI Manager stopped successfully")

        except Exception as e:
            self.logger.error(f"Failed to stop AI Manager: {e}")

    def _on_heartbeat(self):
        """AI manager heartbeat"""
        try:
            # Check AI management health
            self._check_ai_management_health()

            # Update metrics
            self.record_operation("heartbeat", True, 0.0)

        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        """Initialize AI management resources"""
        try:
            # Initialize data structures
            self.model_registrations = []
            self.workflow_executions = []
            self.api_key_requests = []

            # Ensure config directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup AI management resources"""
        try:
            # Clear data
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    # ============================================================================
    # AI Management Methods
    # ============================================================================

    def register_model(self, model: AIModel) -> bool:
        """Register a new AI model"""
        try:
            if model.model_id in self.models:
                self.logger.warning(f"Model {model.model_id} already registered")
                return False

            self.models[model.model_id] = model
            self.model_registrations.append({
                "model_id": model.model_id,
                "name": model.name,
                "provider": model.provider,
                "timestamp": datetime.now().isoformat()
            })

            self.logger.info(f"Registered model: {model.name} ({model.model_id})")
            self.record_operation("register_model", True, 0.0)
            return True

        except Exception as e:
            self.logger.error(f"Failed to register model: {e}")
            self.record_operation("register_model", False, 0.0)
            return False

    def create_workflow(self, name: str, description: str = "") -> Optional[MLWorkflow]:
        """Create a new ML workflow"""
        try:
            if name in self.active_workflows:
                self.logger.warning(f"Workflow {name} already exists")
                return None

            workflow = MLWorkflow(name=name, description=description)
            self.active_workflows[name] = workflow

            self.logger.info(f"Created workflow: {name}")
            self.record_operation("create_workflow", True, 0.0)
            return workflow

        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            self.record_operation("create_workflow", False, 0.0)
            return None

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow"""
        try:
            if workflow_name not in self.active_workflows:
                self.logger.error(f"Workflow {workflow_name} not found")
                return False

            workflow = self.active_workflows[workflow_name]
            workflow.status = "running"

            # Record execution
            self.workflow_executions.append({
                "workflow_name": workflow_name,
                "started_at": datetime.now().isoformat(),
                "status": "started"
            })

            self.logger.info(f"Executing workflow: {workflow_name}")
            self.record_operation("execute_workflow", True, 0.0)
            return True

        except Exception as e:
            self.logger.error(f"Failed to execute workflow: {e}")
            self.record_operation("execute_workflow", False, 0.0)
            return False

    def _check_ai_management_health(self):
        """Check AI management system health"""
        try:
            # Check model registrations
            if len(self.model_registrations) > 1000:
                self.logger.info(
                    f"Large model registration history: {len(self.model_registrations)} records"
                )

            # Check workflow executions
            if len(self.workflow_executions) > 500:
                self.logger.info(
                    f"Large workflow execution history: {len(self.workflow_executions)} records"
                )

        except Exception as e:
            self.logger.error(f"Failed to check AI management health: {e}")

    def get_ai_management_stats(self) -> Dict[str, Any]:
        """Get AI management statistics"""
        try:
            stats = {
                "total_models": len(self.models),
                "total_workflows": len(self.active_workflows),
                "model_registrations_count": len(self.model_registrations),
                "workflow_executions_count": len(self.workflow_executions),
                "api_key_requests_count": len(self.api_key_requests),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds,
            }

            # Record operation
            self.record_operation("get_ai_management_stats", True, 0.0)

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get AI management stats: {e}")
            self.record_operation("get_ai_management_stats", False, 0.0)
            return {"error": str(e)}

    def _save_ai_management_data(self):
        """Save AI management data to persistent storage"""
        try:
            # This would implement actual data persistence
            # For now, just log the action
            self.logger.info("AI management data saved")
        except Exception as e:
            self.logger.error(f"Failed to save AI management data: {e}")
