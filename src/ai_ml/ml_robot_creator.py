"""Task and blueprint generation for the modular ML Robot system."""
from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from ml_robot_config import MLTask, MLModelBlueprint

# Handle missing dependencies gracefully
try:
    from ml_robot_validator import validate_blueprint_config
except ImportError:
    from unittest.mock import Mock
    validate_blueprint_config = Mock(return_value={})

try:
    from ml_frameworks import MLFrameworkManager
except ImportError:
    from unittest.mock import Mock
    MLFrameworkManager = Mock

try:
    from integrations import OpenAIIntegration, AnthropicIntegration
except ImportError:
    from unittest.mock import Mock
    OpenAIIntegration = Mock
    AnthropicIntegration = Mock

logger = logging.getLogger(__name__)


class MLRobotCreator:
    """Handles task creation and blueprint generation."""

    def __init__(self, config: Dict[str, Any], framework_manager: MLFrameworkManager):
        self.config = config
        self.framework_manager = framework_manager
        self.tasks: Dict[str, MLTask] = {}
        self.blueprints: Dict[str, MLModelBlueprint] = {}
        self.openai = None
        self.anthropic = None
        self._setup_integrations()

    def _setup_integrations(self) -> None:
        ai_cfg = self.config.get("ai_services", {})
        if ai_cfg.get("openai", {}).get("enabled"):
            self.openai = OpenAIIntegration()
            logger.info("OpenAI integration enabled")
        if ai_cfg.get("anthropic", {}).get("enabled"):
            self.anthropic = AnthropicIntegration()
            logger.info("Anthropic integration enabled")

    def create_task(
        self,
        task_type: str,
        description: str,
        dataset_info: Dict[str, Any],
        model_requirements: Dict[str, Any],
        **kwargs: Any,
    ) -> MLTask:
        task_id = f"task_{len(self.tasks) + 1}_{datetime.now():%Y%m%d_%H%M%S}"
        task = MLTask(
            task_id=task_id,
            task_type=task_type,
            description=description,
            dataset_info=dataset_info,
            model_requirements=model_requirements,
            framework_preference=kwargs.get("framework_preference"),
            priority=kwargs.get("priority", 1),
        )
        self.tasks[task_id] = task
        return task

    def generate_model_blueprint(self, task: MLTask) -> MLModelBlueprint:
        config = self._ai_generate_blueprint(task)
        config = validate_blueprint_config(
            config, self.framework_manager.list_frameworks()
        )
        blueprint = MLModelBlueprint(
            name=f"blueprint_{task.task_id}_{datetime.now():%Y%m%d_%H%M%S}",
            framework=config["framework"],
            architecture=config["architecture"],
            hyperparameters=config["hyperparameters"],
            training_config=config["training_config"],
            evaluation_metrics=config["evaluation_metrics"],
        )
        self.blueprints[blueprint.name] = blueprint
        return blueprint

    def _ai_generate_blueprint(self, task: MLTask) -> Dict[str, Any]:
        prompt = self._create_prompt(task)
        response = None
        if self.openai:
            response = self.openai.generate_code(prompt)
        elif self.anthropic:
            response = self.anthropic.generate_code(prompt)
        if response:
            try:
                import re

                match = re.search(r"\{.*\}", response, re.DOTALL)
                if match:
                    return json.loads(match.group())
            except Exception:  # pragma: no cover - fall back to rules
                logger.warning("AI response parsing failed, using defaults")
        return self._rule_based_blueprint_generation(task)

    def _create_prompt(self, task: MLTask) -> str:
        return (
            "Generate a JSON blueprint for the following ML task:\n" +
            json.dumps(task.to_dict(), indent=2)
        )

    def _rule_based_blueprint_generation(self, task: MLTask) -> Dict[str, Any]:
        if task.task_type == "classification":
            arch = {"type": "random_forest", "parameters": {"n_estimators": 50}}
        elif task.task_type == "regression":
            arch = {"type": "linear", "parameters": {}}
        else:
            arch = {"type": "kmeans", "parameters": {"n_clusters": 3}}
        return {
            "framework": "scikit_learn",
            "architecture": arch,
            "hyperparameters": {"learning_rate": 0.001, "batch_size": 32, "epochs": 10},
            "training_config": {"optimizer": "adam", "loss_function": "auto", "validation_split": 0.2},
            "evaluation_metrics": ["accuracy"],
        }

    def infer_task_type(self, description: str) -> str:
        d = description.lower()
        if any(w in d for w in ["classify", "label"]):
            return "classification"
        if any(w in d for w in ["regress", "predict", "forecast"]):
            return "regression"
        if any(w in d for w in ["cluster", "segment"]):
            return "clustering"
        return "classification"


__all__ = ["MLRobotCreator"]
