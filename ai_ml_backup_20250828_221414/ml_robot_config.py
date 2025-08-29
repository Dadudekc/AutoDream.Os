"""Configuration models for the modular ML Robot system.

This module provides lightweight dataclasses used across the
ML robot creator, processor and orchestrator components.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class MLTask:
    """Represents an ML task to be executed."""

    task_id: str
    task_type: str
    description: str
    dataset_info: Dict[str, Any]
    model_requirements: Dict[str, Any]
    framework_preference: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    priority: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "description": self.description,
            "dataset_info": self.dataset_info,
            "model_requirements": self.model_requirements,
            "framework_preference": self.framework_preference,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "priority": self.priority,
        }


@dataclass
class MLModelBlueprint:
    """Blueprint describing how to build and train a model."""

    name: str
    framework: str
    architecture: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    training_config: Dict[str, Any]
    evaluation_metrics: List[str]
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "framework": self.framework,
            "architecture": self.architecture,
            "hyperparameters": self.hyperparameters,
            "training_config": self.training_config,
            "evaluation_metrics": self.evaluation_metrics,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class MLExperiment:
    """Record of an experiment executed by the ML robot."""

    experiment_id: str
    task: MLTask
    blueprint: MLModelBlueprint
    model: Any
    training_results: Dict[str, Any]
    evaluation_results: Dict[str, Any]
    model_path: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "task": self.task.to_dict(),
            "blueprint": self.blueprint.to_dict(),
            "training_results": self.training_results,
            "evaluation_results": self.evaluation_results,
            "model_path": self.model_path,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat()
            if self.completed_at
            else None,
        }


__all__ = ["MLTask", "MLModelBlueprint", "MLExperiment"]
