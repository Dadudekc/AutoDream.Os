#!/usr/bin/env python3
"""
ML Training Infrastructure Tool - Utils
=======================================

Utility functions for ML training infrastructure simulation and management.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from .ml_training_infrastructure_tool_core import (
    ResourceType,
    TrainingEnvironment,
    TrainingJob,
    TrainingJobStatus,
    TrainingResource,
    TrainingStatus,
)

logger = logging.getLogger(__name__)


class TrainingSimulator:
    """Simulates training environment creation and job execution."""

    @staticmethod
    def simulate_environment_creation(env: TrainingEnvironment) -> None:
        """Simulate training environment creation."""
        logger.info(f"Creating environment {env.name} with {env.framework.value}")
        logger.info(f"Base image: {env.base_image}")
        logger.info(f"Requirements: {len(env.requirements)} packages")
        if env.resources:
            for resource in env.resources:
                logger.info(f"Resource: {resource.resource_type.value} x{resource.quantity}")
        logger.info("Environment created successfully")

    @staticmethod
    def simulate_provisioning(job: TrainingJob) -> None:
        """Simulate job provisioning."""
        logger.info(f"Provisioning resources for job {job.job_id}")
        for resource in job.resources:
            logger.info(f"Allocating {resource.resource_type.value} x{resource.quantity}")
        logger.info("Provisioning completed")

    @staticmethod
    def simulate_training_progress(status: TrainingJobStatus) -> None:
        """Simulate training progress."""
        if status.progress < 100.0:
            status.progress = min(status.progress + 10.0, 100.0)

            # Simulate metrics
            status.metrics = {
                "loss": max(1.0 - (status.progress / 100.0), 0.1),
                "accuracy": min(status.progress / 100.0, 0.95),
                "learning_rate": 0.001 * (1.0 - status.progress / 100.0),
                "epoch": int(status.progress / 10.0),
            }

            # Simulate logs
            log_entry = f"Epoch {int(status.progress / 10.0)}: Loss={status.metrics['loss']:.4f}, Accuracy={status.metrics['accuracy']:.4f}"
            if not status.logs:
                status.logs = []
            status.logs.append(log_entry)

            if status.progress >= 100.0:
                status.status = TrainingStatus.COMPLETED
                status.end_time = datetime.now().isoformat()
                logger.info(f"Training job {status.job_id} completed")


class ResourceManager:
    """Manages resource allocation and deallocation."""

    def __init__(self, resource_pool: dict[str, int]):
        """Initialize resource manager with available resources."""
        self.resource_pool = resource_pool.copy()

    def allocate_resources(self, job: TrainingJob) -> bool:
        """Allocate resources for a training job."""
        # Check if resources are available
        for resource in job.resources:
            if (
                resource.resource_type == ResourceType.GPU
                and self.resource_pool.get("gpu_units", 0) < resource.quantity
            ):
                return False
            if (
                resource.resource_type == ResourceType.CPU
                and self.resource_pool.get("cpu_cores", 0) < resource.quantity
            ):
                return False

        # Allocate resources
        for resource in job.resources:
            if resource.resource_type == ResourceType.GPU:
                self.resource_pool["gpu_units"] -= resource.quantity
            elif resource.resource_type == ResourceType.CPU:
                self.resource_pool["cpu_cores"] -= resource.quantity

        return True

    def release_resources(self, resources: list[TrainingResource]) -> None:
        """Release allocated resources."""
        for resource in resources:
            if resource.resource_type == ResourceType.GPU:
                self.resource_pool["gpu_units"] += resource.quantity
            elif resource.resource_type == ResourceType.CPU:
                self.resource_pool["cpu_cores"] += resource.quantity

    def get_resource_status(self) -> dict[str, Any]:
        """Get current resource status."""
        return {
            "gpu_units": self.resource_pool.get("gpu_units", 0),
            "cpu_cores": self.resource_pool.get("cpu_cores", 0),
            "memory_gb": self.resource_pool.get("memory_gb", 0),
            "storage_gb": self.resource_pool.get("storage_gb", 0),
            "last_updated": datetime.now().isoformat(),
        }


class JobQueueManager:
    """Manages training job queue and processing."""

    def __init__(self):
        """Initialize job queue manager."""
        self.job_queue: list[str] = []

    def add_job_to_queue(self, job_id: str) -> None:
        """Add job to queue."""
        if job_id not in self.job_queue:
            self.job_queue.append(job_id)
            logger.info(f"Job {job_id} added to queue")

    def remove_job_from_queue(self, job_id: str) -> None:
        """Remove job from queue."""
        if job_id in self.job_queue:
            self.job_queue.remove(job_id)
            logger.info(f"Job {job_id} removed from queue")

    def get_queue_length(self) -> int:
        """Get current queue length."""
        return len(self.job_queue)

    def get_next_job(self) -> str | None:
        """Get next job from queue."""
        return self.job_queue[0] if self.job_queue else None


class FileManager:
    """Manages file operations for environments and jobs."""

    def __init__(self, base_dir: Path):
        """Initialize file manager with base directory."""
        self.base_dir = base_dir
        self.environments_dir = base_dir / "environments"
        self.jobs_dir = base_dir / "jobs"
        self.status_dir = base_dir / "status"

        # Create directories if they don't exist
        self.environments_dir.mkdir(parents=True, exist_ok=True)
        self.jobs_dir.mkdir(parents=True, exist_ok=True)
        self.status_dir.mkdir(parents=True, exist_ok=True)

    def save_environment(self, env: TrainingEnvironment) -> bool:
        """Save environment to file."""
        try:
            env_file = self.environments_dir / f"{env.env_id}.json"
            env_data = {
                "env_id": env.env_id,
                "name": env.name,
                "framework": env.framework.value,
                "version": env.version,
                "base_image": env.base_image,
                "requirements": env.requirements,
                "environment_vars": env.environment_vars,
                "resources": [
                    {
                        "resource_type": r.resource_type.value,
                        "quantity": r.quantity,
                        "specifications": r.specifications,
                    }
                    for r in env.resources
                ]
                if env.resources
                else [],
            }

            with open(env_file, "w") as f:
                json.dump(env_data, f, indent=2)

            logger.info(f"Environment {env.env_id} saved to {env_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save environment {env.env_id}: {e}")
            return False

    def load_environment(self, env_id: str) -> TrainingEnvironment | None:
        """Load environment from file."""
        try:
            env_file = self.environments_dir / f"{env_id}.json"
            if not env_file.exists():
                return None

            with open(env_file) as f:
                env_data = json.load(f)

            # Convert back to TrainingEnvironment
            from .ml_training_infrastructure_tool_core import FrameworkType

            resources = []
            for r_data in env_data.get("resources", []):
                resources.append(
                    TrainingResource(
                        resource_type=ResourceType(r_data["resource_type"]),
                        quantity=r_data["quantity"],
                        specifications=r_data.get("specifications", {}),
                    )
                )

            return TrainingEnvironment(
                env_id=env_data["env_id"],
                name=env_data["name"],
                framework=FrameworkType(env_data["framework"]),
                version=env_data["version"],
                base_image=env_data["base_image"],
                requirements=env_data["requirements"],
                environment_vars=env_data.get("environment_vars", {}),
                resources=resources,
            )
        except Exception as e:
            logger.error(f"Failed to load environment {env_id}: {e}")
            return None

    def save_job(self, job: TrainingJob) -> bool:
        """Save job to file."""
        try:
            job_file = self.jobs_dir / f"{job.job_id}.json"
            job_data = {
                "job_id": job.job_id,
                "name": job.name,
                "environment": {
                    "env_id": job.environment.env_id,
                    "name": job.environment.name,
                    "framework": job.environment.framework.value,
                    "version": job.environment.version,
                    "base_image": job.environment.base_image,
                    "requirements": job.environment.requirements,
                    "environment_vars": job.environment.environment_vars,
                    "resources": [
                        {
                            "resource_type": r.resource_type.value,
                            "quantity": r.quantity,
                            "specifications": r.specifications,
                        }
                        for r in job.environment.resources
                    ]
                    if job.environment.resources
                    else [],
                },
                "training_script": job.training_script,
                "data_path": job.data_path,
                "output_path": job.output_path,
                "hyperparameters": job.hyperparameters,
                "resources": [
                    {
                        "resource_type": r.resource_type.value,
                        "quantity": r.quantity,
                        "specifications": r.specifications,
                    }
                    for r in job.resources
                ],
                "priority": job.priority,
                "timeout": job.timeout,
                "created_at": job.created_at,
            }

            with open(job_file, "w") as f:
                json.dump(job_data, f, indent=2)

            logger.info(f"Job {job.job_id} saved to {job_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save job {job.job_id}: {e}")
            return False

    def load_job(self, job_id: str) -> TrainingJob | None:
        """Load job from file."""
        try:
            job_file = self.jobs_dir / f"{job_id}.json"
            if not job_file.exists():
                return None

            with open(job_file) as f:
                job_data = json.load(f)

            # Convert back to TrainingJob
            env_data = job_data["environment"]
            env_resources = []
            for r_data in env_data.get("resources", []):
                env_resources.append(
                    TrainingResource(
                        resource_type=ResourceType(r_data["resource_type"]),
                        quantity=r_data["quantity"],
                        specifications=r_data.get("specifications", {}),
                    )
                )

            job_resources = []
            for r_data in job_data.get("resources", []):
                job_resources.append(
                    TrainingResource(
                        resource_type=ResourceType(r_data["resource_type"]),
                        quantity=r_data["quantity"],
                        specifications=r_data.get("specifications", {}),
                    )
                )

            from .ml_training_infrastructure_tool_core import FrameworkType

            environment = TrainingEnvironment(
                env_id=env_data["env_id"],
                name=env_data["name"],
                framework=FrameworkType(env_data["framework"]),
                version=env_data["version"],
                base_image=env_data["base_image"],
                requirements=env_data["requirements"],
                environment_vars=env_data.get("environment_vars", {}),
                resources=env_resources,
            )

            return TrainingJob(
                job_id=job_data["job_id"],
                name=job_data["name"],
                environment=environment,
                training_script=job_data["training_script"],
                data_path=job_data["data_path"],
                output_path=job_data["output_path"],
                hyperparameters=job_data["hyperparameters"],
                resources=job_resources,
                priority=job_data.get("priority", 1),
                timeout=job_data.get("timeout", 3600),
                created_at=job_data.get("created_at", ""),
            )
        except Exception as e:
            logger.error(f"Failed to load job {job_id}: {e}")
            return None

    def save_job_status(self, status: TrainingJobStatus) -> bool:
        """Save job status to file."""
        try:
            status_file = self.status_dir / f"{status.job_id}.json"
            status_data = {
                "job_id": status.job_id,
                "status": status.status.value,
                "environment_id": status.environment_id,
                "resources_allocated": [
                    {
                        "resource_type": r.resource_type.value,
                        "quantity": r.quantity,
                        "specifications": r.specifications,
                    }
                    for r in status.resources_allocated
                ],
                "start_time": status.start_time,
                "end_time": status.end_time,
                "progress": status.progress,
                "metrics": status.metrics,
                "logs": status.logs,
            }

            with open(status_file, "w") as f:
                json.dump(status_data, f, indent=2)

            logger.info(f"Job status {status.job_id} saved to {status_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save job status {status.job_id}: {e}")
            return False

    def load_job_status(self, job_id: str) -> TrainingJobStatus | None:
        """Load job status from file."""
        try:
            status_file = self.status_dir / f"{job_id}.json"
            if not status_file.exists():
                return None

            with open(status_file) as f:
                status_data = json.load(f)

            # Convert back to TrainingJobStatus
            resources_allocated = []
            for r_data in status_data.get("resources_allocated", []):
                resources_allocated.append(
                    TrainingResource(
                        resource_type=ResourceType(r_data["resource_type"]),
                        quantity=r_data["quantity"],
                        specifications=r_data.get("specifications", {}),
                    )
                )

            return TrainingJobStatus(
                job_id=status_data["job_id"],
                status=TrainingStatus(status_data["status"]),
                environment_id=status_data["environment_id"],
                resources_allocated=resources_allocated,
                start_time=status_data.get("start_time"),
                end_time=status_data.get("end_time"),
                progress=status_data.get("progress", 0.0),
                metrics=status_data.get("metrics", {}),
                logs=status_data.get("logs", []),
            )
        except Exception as e:
            logger.error(f"Failed to load job status {job_id}: {e}")
            return None
