"""
Core AI/ML Components
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Core classes and functionality for AI/ML integration
"""

import json
import logging

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pathlib import Path
from datetime import datetime

from .api_key_manager import APIKeyManager
from ..core.base_manager import BaseManager, ManagerStatus, ManagerPriority
from .models import AIModel
from .workflows import MLWorkflow
from .engine import AIEngine


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
        self.engine = AIEngine(config_path=self.config_path)
        self.models: Dict[str, AIModel] = {}
        self.active_workflows: Dict[str, MLWorkflow] = {}
        self.config = self.engine.config
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

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")

            # Reload configuration
            self.config = self.engine.load_config()

            # Reset tracking
            self.model_registrations.clear()
            self.workflow_executions.clear()
            self.api_key_requests.clear()

            self.logger.info("Recovery successful")
            return True

        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    # ============================================================================
    # AI Management Methods
    # ============================================================================

    def register_model(self, model: AIModel) -> bool:
        """Register an AI model"""
        try:
            start_time = datetime.now()

            self.models[model.name] = model

            # Record registration
            registration_record = {
                "timestamp": datetime.now().isoformat(),
                "model_name": model.name,
                "provider": model.provider,
                "model_id": model.model_id,
                "version": model.version,
            }
            self.model_registrations.append(registration_record)

            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("register_model", True, operation_time)

            self.logger.info(f"Registered model: {model.name}")
            return True

        except Exception as e:
            self.logger.error(f"Error registering model {model.name}: {e}")
            self.record_operation("register_model", False, 0.0)
            return False

    def get_model(self, model_name: str) -> Optional[AIModel]:
        """Get a registered model by name"""
        try:
            model = self.models.get(model_name)

            # Record operation
            self.record_operation("get_model", True, 0.0)

            return model

        except Exception as e:
            self.logger.error(f"Error getting model {model_name}: {e}")
            self.record_operation("get_model", False, 0.0)
            return None

    def list_models(self) -> List[str]:
        """List all registered model names"""
        try:
            model_names = list(self.models.keys())

            # Record operation
            self.record_operation("list_models", True, 0.0)

            return model_names

        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
            self.record_operation("list_models", False, 0.0)
            return []

    def create_workflow(self, name: str, description: str) -> MLWorkflow:
        """Create a new ML workflow"""
        try:
            start_time = datetime.now()

            workflow = MLWorkflow(name=name, description=description)
            self.active_workflows[name] = workflow

            # Record workflow creation
            workflow_record = {
                "timestamp": datetime.now().isoformat(),
                "workflow_name": name,
                "description": description,
                "steps_count": 0,
            }
            self.workflow_executions.append(workflow_record)

            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("create_workflow", True, operation_time)

            self.logger.info(f"Created workflow: {name}")
            return workflow

        except Exception as e:
            self.logger.error(f"Error creating workflow {name}: {e}")
            self.record_operation("create_workflow", False, 0.0)
            raise

    def get_workflow(self, name: str) -> Optional[MLWorkflow]:
        """Get a workflow by name"""
        try:
            workflow = self.active_workflows.get(name)

            # Record operation
            self.record_operation("get_workflow", True, 0.0)

            return workflow

        except Exception as e:
            self.logger.error(f"Error getting workflow {name}: {e}")
            self.record_operation("get_workflow", False, 0.0)
            return None

    def list_workflows(self) -> List[str]:
        """List all active workflow names"""
        try:
            workflow_names = list(self.active_workflows.keys())

            # Record operation
            self.record_operation("list_workflows", True, 0.0)

            return workflow_names

        except Exception as e:
            self.logger.error(f"Error listing workflows: {e}")
            self.record_operation("list_workflows", False, 0.0)
            return []

    def get_api_key(self, service: str) -> Optional[str]:
        """Proxy API key retrieval to the API key manager"""
        try:
            start_time = datetime.now()

            api_key = self.api_keys.get_key(service)

            # Record API key request
            request_record = {
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "success": api_key is not None,
            }
            self.api_key_requests.append(request_record)

            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("get_api_key", api_key is not None, operation_time)

            return api_key

        except Exception as e:
            self.logger.error(f"Error getting API key for {service}: {e}")
            self.record_operation("get_api_key", False, 0.0)
            return None

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow"""
        try:
            start_time = datetime.now()

            workflow = self.get_workflow(workflow_name)
            if not workflow:
                self.logger.error(f"Workflow not found: {workflow_name}")
                self.record_operation("execute_workflow", False, 0.0)
                return False

            result = self.engine.execute_workflow(workflow)

            if result:
                for record in self.workflow_executions:
                    if record.get("workflow_name") == workflow_name:
                        record["status"] = "completed"
                        record["completed_at"] = datetime.now().isoformat()
                        break
                self.logger.info(f"Workflow completed: {workflow_name}")
            else:
                self.logger.error(f"Workflow execution failed: {workflow_name}")

            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("execute_workflow", result, operation_time)

            return result

        except Exception as e:
            self.logger.error(f"Workflow execution failed: {workflow_name} - {e}")
            self.record_operation("execute_workflow", False, 0.0)
            return False

    # ============================================================================
    # Private Helper Methods
    # ============================================================================

    def _save_ai_management_data(self):
        """Save AI management data to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/ai_ml_core")
            persistence_dir.mkdir(parents=True, exist_ok=True)

            # Prepare data for persistence
            ai_data = {
                "models": {k: v.__dict__ for k, v in self.models.items()},
                "active_workflows": self.active_workflows,
                "model_registrations": self.model_registrations,
                "workflow_executions": self.workflow_executions,
                "api_key_requests": self.api_key_requests,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0",
            }

            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_ml_core_data_{timestamp}.json"
            filepath = persistence_dir / filename

            with open(filepath, "w") as f:
                json.dump(ai_data, f, indent=2, default=str)

            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "ai_ml_core_data_*.json", 5)

            self.logger.info(f"AI management data saved to {filepath}")

        except Exception as e:
            self.logger.error(f"Failed to save AI management data: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")

    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int):
        """Clean up old backup files, keeping only the specified number"""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                # Sort by modification time (oldest first)
                files.sort(key=lambda x: x.stat().st_mtime)
                # Remove oldest files
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup old backups: {e}")

    def _check_ai_management_health(self):
        """Check AI management health status"""
        try:
            # Check for excessive API key requests
            if len(self.api_key_requests) > 100:
                self.logger.warning(
                    f"High number of API key requests: {len(self.api_key_requests)}"
                )

            # Check workflow execution history
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


class MLFramework(ABC):
    """Abstract base class for ML frameworks"""

    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        self.is_initialized = False

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the ML framework"""
        pass

    @abstractmethod
    def create_model(self, model_config: Dict[str, Any]) -> Any:
        """Create a model using the framework"""
        pass

    @abstractmethod
    def train_model(self, model: Any, data: Any, **kwargs) -> Dict[str, Any]:
        """Train a model"""
        pass

    @abstractmethod
    def evaluate_model(self, model: Any, test_data: Any) -> Dict[str, float]:
        """Evaluate a model"""
        pass

    @abstractmethod
    def save_model(self, model: Any, path: str) -> bool:
        """Save a model to disk"""
        pass

    @abstractmethod
    def load_model(self, path: str) -> Any:
        """Load a model from disk"""
        pass


class ModelManager(BaseManager):
    """Manages AI/ML models and their lifecycle

    Now inherits from BaseManager for unified functionality
    """

    def __init__(
        self,
        storage_path: str = "models",
        api_key_manager: Optional[APIKeyManager] = None,
    ):
        """Initialize model manager with BaseManager"""
        super().__init__(
            manager_id="model_manager",
            name="Model Manager",
            description="Manages AI/ML models and their lifecycle",
        )

        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.models: Dict[str, Dict[str, Any]] = {}
        self.api_keys = api_key_manager or APIKeyManager()

        # Model management tracking
        self.model_operations: List[Dict[str, Any]] = []
        self.storage_operations: List[Dict[str, Any]] = []
        self.api_key_operations: List[Dict[str, Any]] = []

        self._load_model_registry()
        self.logger.info("Model Manager initialized")

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================

    def _on_start(self) -> bool:
        """Initialize model management system"""
        try:
            self.logger.info("Starting Model Manager...")

            # Clear tracking data
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()

            # Ensure storage directory exists
            self.storage_path.mkdir(parents=True, exist_ok=True)

            self.logger.info("Model Manager started successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to start Model Manager: {e}")
            return False

    def _on_stop(self):
        """Cleanup model management system"""
        try:
            self.logger.info("Stopping Model Manager...")

            # Save tracking data
            self._save_model_management_data()

            # Save model registry
            self._save_model_registry()

            # Clear data
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()

            self.logger.info("Model Manager stopped successfully")

        except Exception as e:
            self.logger.error(f"Failed to stop Model Manager: {e}")

    def _on_heartbeat(self):
        """Model manager heartbeat"""
        try:
            # Check model management health
            self._check_model_management_health()

            # Update metrics
            self.record_operation("heartbeat", True, 0.0)

        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        """Initialize model management resources"""
        try:
            # Initialize data structures
            self.model_operations = []
            self.storage_operations = []
            self.api_key_operations = []

            # Ensure storage directory exists
            self.storage_path.mkdir(parents=True, exist_ok=True)

            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup model management resources"""
        try:
            # Clear data
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()

        except Exception as e:
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        """Attempt recovery from errors"""
        try:
            self.logger.info(f"Attempting recovery for {context}")

            # Reload model registry
            self._load_model_registry()

            # Reset tracking
            self.model_operations.clear()
            self.storage_operations.clear()
            self.api_key_operations.clear()

            self.logger.info("Recovery successful")
            return True

        except Exception as e:
            self.logger.error(f"Recovery failed: {e}")
            return False

    # ============================================================================
    # Model Management Methods
    # ============================================================================

    def _load_model_registry(self) -> None:
        """Load the model registry from disk"""
        try:
            registry_path = self.storage_path / "model_registry.json"
            if registry_path.exists():
                with open(registry_path, "r") as f:
                    self.models = json.load(f)

                # Record operation
                self.record_operation("load_model_registry", True, 0.0)

        except Exception as e:
            self.logger.error(f"Error loading model registry: {e}")
            self.record_operation("load_model_registry", False, 0.0)

    def _save_model_registry(self) -> None:
        """Save the model registry to disk"""
        try:
            registry_path = self.storage_path / "model_registry.json"
            with open(registry_path, "w") as f:
                json.dump(self.models, f, indent=2)

            # Record operation
            self.record_operation("save_model_registry", True, 0.0)

        except Exception as e:
            self.logger.error(f"Error saving model registry: {e}")
            self.record_operation("save_model_registry", False, 0.0)

    def register_model(self, model_id: str, model_info: Dict[str, Any]) -> bool:
        """Register a new model"""
        try:
            start_time = datetime.now()

            self.models[model_id] = {
                **model_info,
                "registered_at": datetime.now().isoformat(),
                "status": "registered",
            }
            self._save_model_registry()

            # Record model operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "register",
                "model_id": model_id,
                "model_info": model_info,
            }
            self.model_operations.append(operation_record)

            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("register_model", True, operation_time)

            self.logger.info(f"Registered model: {model_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error registering model {model_id}: {e}")
            self.record_operation("register_model", False, 0.0)
            return False

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a registered model"""
        try:
            model_info = self.models.get(model_id)

            # Record operation
            self.record_operation("get_model_info", True, 0.0)

            return model_info

        except Exception as e:
            self.logger.error(f"Error getting model info for {model_id}: {e}")
            self.record_operation("get_model_info", False, 0.0)
            return None

    def update_model_status(self, model_id: str, status: str) -> bool:
        """Update the status of a model"""
        try:
            start_time = datetime.now()

            if model_id in self.models:
                self.models[model_id]["status"] = status
                self.models[model_id]["updated_at"] = datetime.now().isoformat()
                self._save_model_registry()

                # Record model operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "update_status",
                    "model_id": model_id,
                    "new_status": status,
                }
                self.model_operations.append(operation_record)

                # Record operation
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("update_model_status", True, operation_time)

                return True

            self.record_operation("update_model_status", False, 0.0)
            return False

        except Exception as e:
            self.logger.error(f"Error updating model status for {model_id}: {e}")
            self.record_operation("update_model_status", False, 0.0)
            return False

    def list_models(self, status_filter: Optional[str] = None) -> List[str]:
        """List models, optionally filtered by status"""
        try:
            if status_filter:
                model_ids = [
                    mid
                    for mid, info in self.models.items()
                    if info.get("status") == status_filter
                ]
            else:
                model_ids = list(self.models.keys())

            # Record operation
            self.record_operation("list_models", True, 0.0)

            return model_ids

        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
            self.record_operation("list_models", False, 0.0)
            return []

    def delete_model(self, model_id: str) -> bool:
        """Delete a model registration"""
        try:
            start_time = datetime.now()

            if model_id in self.models:
                del self.models[model_id]
                self._save_model_registry()

                # Record model operation
                operation_record = {
                    "timestamp": datetime.now().isoformat(),
                    "operation": "delete",
                    "model_id": model_id,
                }
                self.model_operations.append(operation_record)

                # Record operation
                operation_time = (datetime.now() - start_time).total_seconds()
                self.record_operation("delete_model", True, operation_time)

                self.logger.info(f"Deleted model registration: {model_id}")
                return True

            self.record_operation("delete_model", False, 0.0)
            return False

        except Exception as e:
            self.logger.error(f"Error deleting model {model_id}: {e}")
            self.record_operation("delete_model", False, 0.0)
            return False

    def get_api_key(self, service: str) -> Optional[str]:
        """Proxy API key retrieval to the API key manager"""
        try:
            start_time = datetime.now()

            api_key = self.api_keys.get_key(service)

            # Record API key operation
            operation_record = {
                "timestamp": datetime.now().isoformat(),
                "operation": "get_api_key",
                "service": service,
                "success": api_key is not None,
            }
            self.api_key_operations.append(operation_record)

            # Record operation
            operation_time = (datetime.now() - start_time).total_seconds()
            self.record_operation("get_api_key", api_key is not None, operation_time)

            return api_key

        except Exception as e:
            self.logger.error(f"Error getting API key for {service}: {e}")
            self.record_operation("get_api_key", False, 0.0)
            return None

    # ============================================================================
    # Private Helper Methods
    # ============================================================================

    def _save_model_management_data(self):
        """Save model management data to persistent storage"""
        try:
            # Create persistence directory if it doesn't exist
            persistence_dir = Path("data/persistent/ai_ml_models")
            persistence_dir.mkdir(parents=True, exist_ok=True)

            # Prepare data for persistence
            model_data = {
                "models": {k: v.__dict__ for k, v in self.models.items()},
                "model_operations": self.model_operations,
                "storage_operations": self.storage_operations,
                "api_key_operations": self.api_key_operations,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0",
            }

            # Save to JSON file with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_ml_models_data_{timestamp}.json"
            filepath = persistence_dir / filename

            with open(filepath, "w") as f:
                json.dump(model_data, f, indent=2, default=str)

            # Keep only the latest 5 backup files
            self._cleanup_old_backups(persistence_dir, "ai_ml_models_data_*.json", 5)

            self.logger.info(f"Model management data saved to {filepath}")

        except Exception as e:
            self.logger.error(f"Failed to save model management data: {e}")
            # Fallback to basic logging if persistence fails
            self.logger.warning("Persistence failed, data only logged in memory")

    def _check_model_management_health(self):
        """Check model management health status"""
        try:
            # Check for excessive model operations
            if len(self.model_operations) > 1000:
                self.logger.warning(
                    f"High number of model operations: {len(self.model_operations)}"
                )

            # Check storage operations
            if len(self.storage_operations) > 500:
                self.logger.info(
                    f"Large storage operations history: {len(self.storage_operations)} records"
                )

        except Exception as e:
            self.logger.error(f"Failed to check model management health: {e}")

    def get_model_management_stats(self) -> Dict[str, Any]:
        """Get model management statistics"""
        try:
            stats = {
                "total_models": len(self.models),
                "model_operations_count": len(self.model_operations),
                "storage_operations_count": len(self.storage_operations),
                "api_key_operations_count": len(self.api_key_operations),
                "manager_status": self.status.value,
                "manager_uptime": self.metrics.uptime_seconds,
            }

            # Record operation
            self.record_operation("get_model_management_stats", True, 0.0)

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get model management stats: {e}")
            self.record_operation("get_model_management_stats", False, 0.0)
            return {"error": str(e)}
