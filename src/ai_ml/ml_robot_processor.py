"""Experiment execution and management for the modular ML Robot system."""
from __future__ import annotations

import os
from datetime import datetime, timedelta
from typing import Any, Dict

import numpy as np

from .ml_robot_config import MLTask, MLModelBlueprint, MLExperiment
from .ml_frameworks import MLFrameworkManager
from .core import ModelManager


class MLRobotProcessor:
    """Handles running experiments and aggregating results."""

    def __init__(self, framework_manager: MLFrameworkManager, model_manager: ModelManager):
        self.framework_manager = framework_manager
        self.model_manager = model_manager
        self.experiments: Dict[str, MLExperiment] = {}

    def execute_experiment(self, task: MLTask, blueprint: MLModelBlueprint) -> MLExperiment:
        experiment_id = f"exp_{task.task_id}_{datetime.now():%Y%m%d_%H%M%S}"
        framework = self.framework_manager.get_framework(blueprint.framework)
        model = framework.create_model(blueprint.architecture)
        data = self._prepare_sample_data(task)
        training_results = framework.train_model(model, data, **blueprint.hyperparameters)
        evaluation_results = framework.evaluate_model(model, data)
        model_path = f"models/{experiment_id}_{blueprint.name}.pkl"
        framework.save_model(model, model_path)
        experiment = MLExperiment(
            experiment_id=experiment_id,
            task=task,
            blueprint=blueprint,
            model=model,
            training_results=training_results,
            evaluation_results=evaluation_results,
            model_path=model_path,
            completed_at=datetime.now(),
        )
        self.experiments[experiment_id] = experiment
        self.model_manager.register_model(
            experiment_id,
            {
                "task_type": task.task_type,
                "framework": blueprint.framework,
                "architecture": blueprint.architecture,
                "performance": evaluation_results,
                "model_path": model_path,
            },
        )
        return experiment

    def get_experiment_summary(self, tasks: Dict[str, MLTask], blueprints: Dict[str, MLModelBlueprint]) -> Dict[str, Any]:
        summary = {
            "total_experiments": len(self.experiments),
            "total_tasks": len(tasks),
            "total_blueprints": len(blueprints),
            "framework_usage": {},
        }
        for exp in self.experiments.values():
            fw = exp.blueprint.framework
            summary["framework_usage"][fw] = summary["framework_usage"].get(fw, 0) + 1
        return summary

    def cleanup_experiments(self, older_than_days: int = 30) -> int:
        cutoff = datetime.now() - timedelta(days=older_than_days)
        removed = 0
        for exp_id, exp in list(self.experiments.items()):
            if exp.created_at < cutoff:
                if exp.model_path and os.path.exists(exp.model_path):
                    os.remove(exp.model_path)
                del self.experiments[exp_id]
                removed += 1
        return removed

    def _prepare_sample_data(self, task: MLTask) -> Dict[str, np.ndarray]:
        size = task.dataset_info.get("size", 100)
        x = np.random.random((size, 10))
        y = np.random.randint(0, 2, size)
        split = int(size * 0.8)
        return {
            "X_train": x[:split],
            "X_test": x[split:],
            "y_train": y[:split],
            "y_test": y[split:],
        }


__all__ = ["MLRobotProcessor"]
