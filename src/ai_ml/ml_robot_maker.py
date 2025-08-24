"""Orchestrator for the modular ML Robot system.

This lightweight module coordinates task creation, blueprint generation and
experiment execution by delegating work to specialized components.
It references configuration dataclasses such as ``class MLTask`` and
``class MLExperiment`` defined in :mod:`ml_robot_config`.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

from .core import ModelManager
from .ml_frameworks import MLFrameworkManager
from .utils import config_loader, logger_setup, performance_monitor
from .ml_robot_config import MLTask, MLModelBlueprint, MLExperiment
from .ml_robot_creator import MLRobotCreator
from .ml_robot_processor import MLRobotProcessor


class MLRobotMaker:
    """High level façade exposing the ML robot functionality."""

    def __init__(self, config_path: Optional[str] = None):
        self.config = config_loader(config_path or "config/ai_ml/ai_ml.json")
        self.logger = logger_setup(
            "ml_robot_maker", self.config.get("environment", {}).get("log_level", "INFO")
        )
        self.framework_manager = MLFrameworkManager(self.config)
        self.model_manager = ModelManager(
            self.config.get("model_management", {}).get("model_registry", "models/")
        )
        self.creator = MLRobotCreator(self.config, self.framework_manager)
        self.processor = MLRobotProcessor(self.framework_manager, self.model_manager)
        self.performance_monitor = performance_monitor

    # Task and blueprint operations -------------------------------------------------
    def create_task(
        self,
        task_type: str,
        description: str,
        dataset_info: Dict[str, Any],
        model_requirements: Dict[str, Any],
        **kwargs: Any,
    ) -> MLTask:
        return self.creator.create_task(
            task_type, description, dataset_info, model_requirements, **kwargs
        )

    def generate_model_blueprint(self, task: MLTask) -> MLModelBlueprint:
        return self.creator.generate_model_blueprint(task)

    # Experiment operations --------------------------------------------------------
    def execute_experiment(self, task: MLTask, blueprint: MLModelBlueprint) -> MLExperiment:
        return self.processor.execute_experiment(task, blueprint)

    def auto_ml_pipeline(
        self,
        task_description: str,
        dataset_info: Dict[str, Any],
        model_requirements: Dict[str, Any],
    ) -> MLExperiment:
        task_type = self.creator.infer_task_type(task_description)
        task = self.create_task(task_type, task_description, dataset_info, model_requirements)
        blueprint = self.generate_model_blueprint(task)
        return self.execute_experiment(task, blueprint)

    # Reporting --------------------------------------------------------------------
    def get_experiment_summary(self) -> Dict[str, Any]:
        return self.processor.get_experiment_summary(
            self.creator.tasks, self.creator.blueprints
        )

    def cleanup_experiments(self, older_than_days: int = 30) -> int:
        return self.processor.cleanup_experiments(older_than_days)


# Factory function for compatibility ----------------------------------------------
def get_ml_robot_maker(config_path: Optional[str] = None) -> MLRobotMaker:
    return MLRobotMaker(config_path)


__all__ = [
    "MLRobotMaker",
    "MLTask",
    "MLModelBlueprint",
    "MLExperiment",
    "get_ml_robot_maker",
]
