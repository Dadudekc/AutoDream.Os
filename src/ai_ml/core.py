"""
Core AI/ML Components
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Core classes and functionality for AI/ML integration
"""

import os
import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

from .api_key_manager import APIKeyManager

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class AIModel:
    """AI model configuration and metadata"""

    name: str
    provider: str
    model_id: str
    version: str
    capabilities: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "provider": self.provider,
            "model_id": self.model_id,
            "version": self.version,
            "capabilities": self.capabilities,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class MLWorkflow:
    """Machine learning workflow definition"""

    name: str
    description: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)

    def add_step(
        self, step_name: str, step_type: str, parameters: Dict[str, Any]
    ) -> None:
        """Add a step to the workflow"""
        step = {
            "name": step_name,
            "type": step_type,
            "parameters": parameters,
            "status": "pending",
            "created_at": datetime.now().isoformat(),
        }
        self.steps.append(step)

    def update_step_status(self, step_name: str, status: str) -> bool:
        """Update the status of a workflow step"""
        for step in self.steps:
            if step["name"] == step_name:
                step["status"] = status
                return True
        return False


class AIManager:
    """Central AI management and coordination"""

    def __init__(
        self,
        config_path: Optional[str] = None,
        api_key_manager: Optional[APIKeyManager] = None,
    ):
        self.config_path = (
            Path(config_path) if config_path else Path("config/ai_ml/ai_ml.json")
        )
        self.models: Dict[str, AIModel] = {}
        self.active_workflows: Dict[str, MLWorkflow] = {}
        self.config = self._load_config()
        self.api_keys = api_key_manager or APIKeyManager()
        self._setup_logging()

    def _load_config(self) -> Dict[str, Any]:
        """Load AI/ML configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {}

    def _setup_logging(self) -> None:
        """Setup logging configuration"""
        log_level = self.config.get("ai_ml", {}).get("logging", {}).get("level", "INFO")
        logging.basicConfig(level=getattr(logging, log_level.upper()))

    def register_model(self, model: AIModel) -> bool:
        """Register an AI model"""
        try:
            self.models[model.name] = model
            logger.info(f"Registered model: {model.name}")
            return True
        except Exception as e:
            logger.error(f"Error registering model {model.name}: {e}")
            return False

    def get_model(self, model_name: str) -> Optional[AIModel]:
        """Get a registered model by name"""
        return self.models.get(model_name)

    def list_models(self) -> List[str]:
        """List all registered model names"""
        return list(self.models.keys())

    def create_workflow(self, name: str, description: str) -> MLWorkflow:
        """Create a new ML workflow"""
        workflow = MLWorkflow(name=name, description=description)
        self.active_workflows[name] = workflow
        logger.info(f"Created workflow: {name}")
        return workflow

    def get_workflow(self, name: str) -> Optional[MLWorkflow]:
        """Get a workflow by name"""
        return self.active_workflows.get(name)

    def list_workflows(self) -> List[str]:
        """List all active workflow names"""
        return list(self.active_workflows.keys())

    def get_api_key(self, service: str) -> Optional[str]:
        """Proxy API key retrieval to the API key manager"""
        return self.api_keys.get_key(service)

    def execute_workflow(self, workflow_name: str) -> bool:
        """Execute a workflow"""
        workflow = self.get_workflow(workflow_name)
        if not workflow:
            logger.error(f"Workflow not found: {workflow_name}")
            return False

        try:
            logger.info(f"Executing workflow: {workflow_name}")
            workflow.status = "running"

            # Execute each step
            for step in workflow.steps:
                if step["status"] == "pending":
                    step["status"] = "running"
                    # Here you would implement actual step execution
                    step["status"] = "completed"

            workflow.status = "completed"
            logger.info(f"Workflow completed: {workflow_name}")
            return True

        except Exception as e:
            workflow.status = "failed"
            logger.error(f"Workflow execution failed: {workflow_name} - {e}")
            return False


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


class ModelManager:
    """Manages AI/ML models and their lifecycle"""

    def __init__(
        self,
        storage_path: str = "models",
        api_key_manager: Optional[APIKeyManager] = None,
    ):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.models: Dict[str, Dict[str, Any]] = {}
        self.api_keys = api_key_manager or APIKeyManager()
        self._load_model_registry()

    def _load_model_registry(self) -> None:
        """Load the model registry from disk"""
        registry_path = self.storage_path / "model_registry.json"
        if registry_path.exists():
            try:
                with open(registry_path, "r") as f:
                    self.models = json.load(f)
            except Exception as e:
                logger.error(f"Error loading model registry: {e}")

    def _save_model_registry(self) -> None:
        """Save the model registry to disk"""
        registry_path = self.storage_path / "model_registry.json"
        try:
            with open(registry_path, "w") as f:
                json.dump(self.models, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving model registry: {e}")

    def register_model(self, model_id: str, model_info: Dict[str, Any]) -> bool:
        """Register a new model"""
        try:
            self.models[model_id] = {
                **model_info,
                "registered_at": datetime.now().isoformat(),
                "status": "registered",
            }
            self._save_model_registry()
            logger.info(f"Registered model: {model_id}")
            return True
        except Exception as e:
            logger.error(f"Error registering model {model_id}: {e}")
            return False

    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a registered model"""
        return self.models.get(model_id)

    def update_model_status(self, model_id: str, status: str) -> bool:
        """Update the status of a model"""
        if model_id in self.models:
            self.models[model_id]["status"] = status
            self.models[model_id]["updated_at"] = datetime.now().isoformat()
            self._save_model_registry()
            return True
        return False

    def list_models(self, status_filter: Optional[str] = None) -> List[str]:
        """List models, optionally filtered by status"""
        if status_filter:
            return [
                mid
                for mid, info in self.models.items()
                if info.get("status") == status_filter
            ]
        return list(self.models.keys())

    def delete_model(self, model_id: str) -> bool:
        """Delete a model registration"""
        if model_id in self.models:
            del self.models[model_id]
            self._save_model_registry()
            logger.info(f"Deleted model registration: {model_id}")
            return True
        return False

    def get_api_key(self, service: str) -> Optional[str]:
        """Proxy API key retrieval to the API key manager"""
        return self.api_keys.get_key(service)


class WorkflowAutomation:
    """Automates ML workflows and processes"""

    def __init__(self, ai_manager: AIManager, model_manager: ModelManager):
        self.ai_manager = ai_manager
        self.model_manager = model_manager
        self.automation_rules: Dict[str, Dict[str, Any]] = {}
        self.scheduled_tasks: List[Dict[str, Any]] = []

    def add_automation_rule(
        self, rule_name: str, conditions: Dict[str, Any], actions: List[Dict[str, Any]]
    ) -> bool:
        """Add an automation rule"""
        try:
            self.automation_rules[rule_name] = {
                "conditions": conditions,
                "actions": actions,
                "created_at": datetime.now().isoformat(),
                "enabled": True,
            }
            logger.info(f"Added automation rule: {rule_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding automation rule {rule_name}: {e}")
            return False

    def evaluate_conditions(
        self, conditions: Dict[str, Any], context: Dict[str, Any]
    ) -> bool:
        """Evaluate automation rule conditions"""
        try:
            for condition_key, expected_value in conditions.items():
                if condition_key not in context:
                    return False
                if context[condition_key] != expected_value:
                    return False
            return True
        except Exception as e:
            logger.error(f"Error evaluating conditions: {e}")
            return False

    def execute_actions(
        self, actions: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """Execute automation rule actions"""
        try:
            for action in actions:
                action_type = action.get("type")
                parameters = action.get("parameters", {})

                if action_type == "create_workflow":
                    self.ai_manager.create_workflow(
                        name=parameters.get("name"),
                        description=parameters.get("description", ""),
                    )
                elif action_type == "update_model_status":
                    self.model_manager.update_model_status(
                        model_id=parameters.get("model_id"),
                        status=parameters.get("status"),
                    )
                elif action_type == "execute_workflow":
                    self.ai_manager.execute_workflow(
                        workflow_name=parameters.get("workflow_name")
                    )

            return True
        except Exception as e:
            logger.error(f"Error executing actions: {e}")
            return False

    def process_automation_rules(self, context: Dict[str, Any]) -> int:
        """Process all automation rules against current context"""
        executed_count = 0

        for rule_name, rule in self.automation_rules.items():
            if not rule.get("enabled", True):
                continue

            if self.evaluate_conditions(rule["conditions"], context):
                if self.execute_actions(rule["actions"], context):
                    executed_count += 1
                    logger.info(f"Executed automation rule: {rule_name}")

        return executed_count

    def schedule_task(
        self, task_name: str, schedule: str, task_func: callable, **kwargs
    ) -> bool:
        """Schedule a task for execution"""
        try:
            scheduled_task = {
                "name": task_name,
                "schedule": schedule,
                "task_func": task_func,
                "kwargs": kwargs,
                "created_at": datetime.now().isoformat(),
                "next_run": self._calculate_next_run(schedule),
            }
            self.scheduled_tasks.append(scheduled_task)
            logger.info(f"Scheduled task: {task_name}")
            return True
        except Exception as e:
            logger.error(f"Error scheduling task {task_name}: {e}")
            return False

    def _calculate_next_run(self, schedule: str) -> datetime:
        """Calculate next run time based on schedule"""
        # Simple implementation - could be enhanced with cron-like parsing
        return datetime.now()

    def run_scheduled_tasks(self) -> int:
        """Run all scheduled tasks that are due"""
        executed_count = 0
        current_time = datetime.now()

        for task in self.scheduled_tasks[
            :
        ]:  # Copy list to avoid modification during iteration
            if current_time >= task["next_run"]:
                try:
                    task["task_func"](**task.get("kwargs", {}))
                    executed_count += 1
                    task["next_run"] = self._calculate_next_run(task["schedule"])
                    logger.info(f"Executed scheduled task: {task['name']}")
                except Exception as e:
                    logger.error(f"Error executing scheduled task {task['name']}: {e}")

        return executed_count
