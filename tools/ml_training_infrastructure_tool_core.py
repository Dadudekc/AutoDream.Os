#!/usr/bin/env python3
"""
ML Training Infrastructure Tool - Core
======================================

Core classes and data structures for ML training infrastructure.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class TrainingStatus(Enum):
    """Training job status."""

    QUEUED = "queued"
    PROVISIONING = "provisioning"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ResourceType(Enum):
    """Resource types for training."""

    CPU = "cpu"
    GPU = "gpu"
    MEMORY = "memory"
    STORAGE = "storage"


class FrameworkType(Enum):
    """ML framework types."""

    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
    SCIKIT_LEARN = "scikit-learn"
    XGBOOST = "xgboost"
    CUSTOM = "custom"


@dataclass
class TrainingResource:
    """Training resource configuration."""

    resource_type: ResourceType
    quantity: int
    specifications: dict[str, Any] = None

    def __post_init__(self):
        if self.specifications is None:
            self.specifications = {}


@dataclass
class TrainingEnvironment:
    """Training environment configuration."""

    env_id: str
    name: str
    framework: FrameworkType
    version: str
    base_image: str
    requirements: list[str]
    environment_vars: dict[str, str] = None
    resources: list[TrainingResource] = None

    def __post_init__(self):
        if self.environment_vars is None:
            self.environment_vars = {}
        if self.resources is None:
            self.resources = []


@dataclass
class TrainingJob:
    """Training job configuration."""

    job_id: str
    name: str
    environment: TrainingEnvironment
    training_script: str
    data_path: str
    output_path: str
    hyperparameters: dict[str, Any]
    resources: list[TrainingResource]
    priority: int = 1
    timeout: int = 3600
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


@dataclass
class TrainingJobStatus:
    """Training job status tracking."""

    job_id: str
    status: TrainingStatus
    environment_id: str
    resources_allocated: list[TrainingResource]
    start_time: str | None = None
    end_time: str | None = None
    progress: float = 0.0
    metrics: dict[str, float] = None
    logs: list[str] = None

    def __post_init__(self):
        if self.metrics is None:
            self.metrics = {}
        if self.logs is None:
            self.logs = []


@dataclass
class TrainingInfrastructureConfig:
    """Training infrastructure configuration."""

    max_concurrent_jobs: int = 10
    resource_pool_size: int = 100
    default_timeout: int = 3600
    monitoring_interval: int = 30
    log_retention_days: int = 30
    auto_scaling_enabled: bool = True
    gpu_memory_threshold: float = 0.8
    cpu_utilization_threshold: float = 0.7


class TrainingInfrastructureCore:
    """Core infrastructure management for ML training."""

    def __init__(self, config: TrainingInfrastructureConfig = None):
        """Initialize the training infrastructure core."""
        self.config = config or TrainingInfrastructureConfig()
        self.environments: dict[str, TrainingEnvironment] = {}
        self.jobs: dict[str, TrainingJob] = {}
        self.job_statuses: dict[str, TrainingJobStatus] = {}
        self.resource_pool: list[TrainingResource] = []
        self.job_queue: list[str] = []

        # Initialize resource pool
        self._initialize_resource_pool()

        logger.info(f"ML Training Infrastructure Core initialized with config: {self.config}")

    def _initialize_resource_pool(self) -> None:
        """Initialize the resource pool with available resources."""
        # Add CPU resources
        for i in range(20):
            self.resource_pool.append(
                TrainingResource(
                    resource_type=ResourceType.CPU,
                    quantity=1,
                    specifications={"cores": 4, "frequency": "2.4GHz"},
                )
            )

        # Add GPU resources
        for i in range(4):
            self.resource_pool.append(
                TrainingResource(
                    resource_type=ResourceType.GPU,
                    quantity=1,
                    specifications={"memory": "8GB", "compute_capability": "7.5"},
                )
            )

        # Add memory resources
        for i in range(10):
            self.resource_pool.append(
                TrainingResource(
                    resource_type=ResourceType.MEMORY,
                    quantity=1,
                    specifications={"size": "16GB", "type": "DDR4"},
                )
            )

        # Add storage resources
        for i in range(5):
            self.resource_pool.append(
                TrainingResource(
                    resource_type=ResourceType.STORAGE,
                    quantity=1,
                    specifications={"size": "1TB", "type": "SSD"},
                )
            )

        logger.info(f"Resource pool initialized with {len(self.resource_pool)} resources")

    def get_available_resources(self) -> dict[str, int]:
        """Get count of available resources by type."""
        available = {}
        for resource_type in ResourceType:
            available[resource_type.value] = sum(
                1 for resource in self.resource_pool if resource.resource_type == resource_type
            )
        return available

    def get_resource_utilization(self) -> dict[str, float]:
        """Get current resource utilization."""
        total_resources = len(self.resource_pool)
        allocated_resources = sum(
            len(status.resources_allocated)
            for status in self.job_statuses.values()
            if status.status in [TrainingStatus.RUNNING, TrainingStatus.PROVISIONING]
        )

        utilization = allocated_resources / total_resources if total_resources > 0 else 0.0

        return {
            "total_resources": total_resources,
            "allocated_resources": allocated_resources,
            "utilization_percentage": utilization * 100,
            "available_resources": total_resources - allocated_resources,
        }

    def get_job_statistics(self) -> dict[str, Any]:
        """Get comprehensive job statistics."""
        total_jobs = len(self.jobs)
        status_counts = {}

        for status in TrainingStatus:
            status_counts[status.value] = sum(
                1 for job_status in self.job_statuses.values() if job_status.status == status
            )

        return {
            "total_jobs": total_jobs,
            "status_counts": status_counts,
            "queue_length": len(self.job_queue),
            "resource_utilization": self.get_resource_utilization(),
            "available_resources": self.get_available_resources(),
        }
