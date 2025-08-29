"""
AI Manager Module
Extracted from core.py for modularization

Contains:
- AIManager: Central AI management and coordination
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from datetime import datetime

from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority
from .models import AIModel, MLWorkflow
from .api_key_manager import APIKeyManager

# Configure logging
logger = logging.getLogger(__name__)


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

        self.logger.info("AI Manager initialized")

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

            self.logger.info("AI Manager resources cleaned up")

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Handle AI management recovery logic"""
        try:
            self.logger.info(f"Attempting AI Manager recovery: {context}")
            
            # Clear error state
            self.status = ManagerStatus.INITIALIZING
            
            # Reinitialize resources
            if self._on_initialize_resources():
                self.status = ManagerStatus.ONLINE
                self.logger.info("AI Manager recovery successful")
                return True
            else:
                self.status = ManagerStatus.ERROR
                self.logger.error("AI Manager recovery failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Recovery attempt failed: {e}")
            self.status = ManagerStatus.ERROR
            return False

    # ============================================================================
    # Configuration Management
    # ============================================================================

    def _load_config(self) -> Dict[str, Any]:
        """Load AI/ML configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    config = json.load(f)
                    self.logger.info(f"Loaded AI/ML config from {self.config_path}")
                    return config
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                return {}
        except Exception as e:
            self.logger.error(f"Failed to load config: {e}")
            return {}

    def _save_config(self) -> bool:
        """Save AI/ML configuration"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            return False

    # ============================================================================
    # Model Management
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
                "timestamp": datetime.now().isoformat(),
                "action": "registered"
            })

            self.logger.info(f"Registered model: {model.name} ({model.model_id})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register model: {e}")
            return False

    def get_model(self, model_id: str) -> Optional[AIModel]:
        """Get a registered model by ID"""
        return self.models.get(model_id)

    def list_models(self) -> List[AIModel]:
        """List all registered models"""
        return list(self.models.values())

    def update_model_status(self, model_id: str, status: str) -> bool:
        """Update model status"""
        try:
            if model_id in self.models:
                # Update model status logic here
                self.logger.info(f"Updated model {model_id} status to {status}")
                return True
            else:
                self.logger.warning(f"Model {model_id} not found")
                return False
        except Exception as e:
            self.logger.error(f"Failed to update model status: {e}")
            return False

    # ============================================================================
    # Workflow Management
    # ============================================================================

    def create_workflow(self, name: str, description: str = "") -> MLWorkflow:
        """Create a new ML workflow"""
        try:
            workflow = MLWorkflow(name=name, description=description)
            self.active_workflows[name] = workflow

            self.workflow_executions.append({
                "workflow_name": name,
                "timestamp": datetime.now().isoformat(),
                "action": "created"
            })

            self.logger.info(f"Created workflow: {name}")
            return workflow

        except Exception as e:
            self.logger.error(f"Failed to create workflow: {e}")
            raise

    def get_workflow(self, name: str) -> Optional[MLWorkflow]:
        """Get a workflow by name"""
        return self.active_workflows.get(name)

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow"""
        try:
            workflow = self.get_workflow(workflow_name)
            if not workflow:
                self.logger.warning(f"Workflow {workflow_name} not found")
                return False

            # Execute workflow logic here
            workflow.status = "running"
            self.logger.info(f"Executing workflow: {workflow_name}")

            self.workflow_executions.append({
                "workflow_name": workflow_name,
                "timestamp": datetime.now().isoformat(),
                "action": "executed"
            })

            return True

        except Exception as e:
            self.logger.error(f"Failed to execute workflow: {e}")
            return False

    def list_workflows(self) -> List[MLWorkflow]:
        """List all active workflows"""
        return list(self.active_workflows.values())

    # ============================================================================
    # API Key Management
    # ============================================================================

    def request_api_key(self, provider: str, purpose: str) -> Optional[str]:
        """Request an API key for a provider"""
        try:
            api_key = self.api_keys.get_key(provider)
            if api_key:
                self.api_key_requests.append({
                    "provider": provider,
                    "purpose": purpose,
                    "timestamp": datetime.now().isoformat(),
                    "status": "granted"
                })
                return api_key
            else:
                self.api_key_requests.append({
                    "provider": provider,
                    "purpose": purpose,
                    "timestamp": datetime.now().isoformat(),
                    "status": "denied"
                })
                return None
        except Exception as e:
            self.logger.error(f"Failed to request API key: {e}")
            return None

    # ============================================================================
    # Health Monitoring
    # ============================================================================

    def _check_ai_management_health(self) -> Dict[str, Any]:
        """Check AI management system health"""
        try:
            health_status = {
                "models_registered": len(self.models),
                "active_workflows": len(self.active_workflows),
                "api_keys_available": len(self.api_keys.list_providers()),
                "last_heartbeat": datetime.now().isoformat()
            }

            # Check for potential issues
            if len(self.models) == 0:
                health_status["warnings"] = ["No models registered"]
            if len(self.active_workflows) == 0:
                health_status["warnings"] = ["No active workflows"]

            return health_status

        except Exception as e:
            self.logger.error(f"Health check failed: {e}")
            return {"error": str(e)}

    def _save_ai_management_data(self) -> bool:
        """Save AI management tracking data"""
        try:
            data = {
                "model_registrations": self.model_registrations,
                "workflow_executions": self.workflow_executions,
                "api_key_requests": self.api_key_requests,
                "timestamp": datetime.now().isoformat()
            }

            data_path = self.config_path.parent / "ai_management_data.json"
            with open(data_path, "w") as f:
                json.dump(data, f, indent=2)

            return True

        except Exception as e:
            self.logger.error(f"Failed to save AI management data: {e}")
            return False

    # ============================================================================
    # Utility Methods
    # ============================================================================

    def get_statistics(self) -> Dict[str, Any]:
        """Get AI management statistics"""
        return {
            "total_models": len(self.models),
            "total_workflows": len(self.active_workflows),
            "total_api_keys": len(self.api_keys.list_providers()),
            "model_registrations": len(self.model_registrations),
            "workflow_executions": len(self.workflow_executions),
            "api_key_requests": len(self.api_key_requests)
        }
