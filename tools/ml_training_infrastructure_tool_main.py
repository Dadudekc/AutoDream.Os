#!/usr/bin/env python3
"""
ML Training Infrastructure Tool - Main
======================================

Main ML training infrastructure tool with CLI interface.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from .ml_training_infrastructure_tool_core import (
    FrameworkType,
    ResourceType,
    TrainingEnvironment,
    TrainingInfrastructureConfig,
    TrainingInfrastructureCore,
    TrainingJob,
    TrainingJobStatus,
    TrainingResource,
    TrainingStatus,
)
from .ml_training_infrastructure_tool_utils import (
    FileManager,
    JobQueueManager,
    ResourceManager,
    TrainingSimulator,
)

logger = logging.getLogger(__name__)


class MLTrainingInfrastructureTool:
    """Main ML Training Infrastructure Tool."""

    def __init__(self, config: TrainingInfrastructureConfig = None):
        """Initialize the ML Training Infrastructure Tool."""
        self.config = config or TrainingInfrastructureConfig()
        self.core = TrainingInfrastructureCore(self.config)

        # Initialize components
        self.base_dir = Path("ml_training_data")
        self.file_manager = FileManager(self.base_dir)
        self.resource_manager = ResourceManager(
            {"gpu_units": 4, "cpu_cores": 20, "memory_gb": 160, "storage_gb": 1000}
        )
        self.queue_manager = JobQueueManager()
        self.simulator = TrainingSimulator()

        # Active jobs tracking
        self.active_jobs: dict[str, TrainingJobStatus] = {}

        logger.info("ML Training Infrastructure Tool initialized")

    def create_training_environment(self, env: TrainingEnvironment) -> bool:
        """Create a training environment."""
        try:
            # Simulate environment creation
            self.simulator.simulate_environment_creation(env)

            # Save environment
            success = self.file_manager.save_environment(env)
            if success:
                self.core.environments[env.env_id] = env
                logger.info(f"Environment {env.env_id} created successfully")

            return success
        except Exception as e:
            logger.error(f"Failed to create environment {env.env_id}: {e}")
            return False

    def submit_training_job(self, job: TrainingJob) -> bool:
        """Submit a training job."""
        try:
            # Generate job ID if not provided
            if not job.job_id:
                job.job_id = f"job_{int(time.time())}"

            # Create job status
            status = TrainingJobStatus(
                job_id=job.job_id,
                status=TrainingStatus.QUEUED,
                environment_id=job.environment.env_id,
                resources_allocated=[],
            )

            # Save job and status
            job_saved = self.file_manager.save_job(job)
            status_saved = self.file_manager.save_job_status(status)

            if job_saved and status_saved:
                self.core.jobs[job.job_id] = job
                self.active_jobs[job.job_id] = status
                self.queue_manager.add_job_to_queue(job.job_id)
                logger.info(f"Job {job.job_id} submitted successfully")
                return True

            return False
        except Exception as e:
            logger.error(f"Failed to submit job {job.job_id}: {e}")
            return False

    def start_training_job(self, job_id: str) -> bool:
        """Start a training job."""
        try:
            if job_id not in self.active_jobs:
                logger.error(f"Job {job_id} not found")
                return False

            status = self.active_jobs[job_id]
            if status.status != TrainingStatus.QUEUED:
                logger.warning(f"Job {job_id} is not queued")
                return False

            # Get job details
            job = self.core.jobs.get(job_id)
            if not job:
                logger.error(f"Job details for {job_id} not found")
                return False

            # Allocate resources
            if not self.resource_manager.allocate_resources(job):
                logger.warning(f"Insufficient resources for job {job_id}")
                return False

            # Update status
            status.status = TrainingStatus.PROVISIONING
            status.resources_allocated = job.resources.copy()
            status.start_time = datetime.now().isoformat()

            # Simulate provisioning
            self.simulator.simulate_provisioning(job)

            # Start training
            status.status = TrainingStatus.RUNNING
            self.file_manager.save_job_status(status)
            self.queue_manager.remove_job_from_queue(job_id)

            logger.info(f"Job {job_id} started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start job {job_id}: {e}")
            return False

    def monitor_training_job(self, job_id: str) -> dict[str, Any] | None:
        """Monitor a training job."""
        try:
            if job_id not in self.active_jobs:
                logger.error(f"Job {job_id} not found")
                return None

            status = self.active_jobs[job_id]

            # Simulate training progress if running
            if status.status == TrainingStatus.RUNNING:
                self.simulator.simulate_training_progress(status)
                if status.status == TrainingStatus.COMPLETED:
                    self.resource_manager.release_resources(status.resources_allocated)
                self.file_manager.save_job_status(status)

            # Return monitoring data
            return {
                "job_id": status.job_id,
                "status": status.status.value,
                "progress": status.progress,
                "metrics": status.metrics,
                "logs": status.logs[-5:] if status.logs else [],  # Last 5 logs
                "start_time": status.start_time,
                "end_time": status.end_time,
                "resources_allocated": len(status.resources_allocated),
            }
        except Exception as e:
            logger.error(f"Failed to monitor job {job_id}: {e}")
            return None

    def cancel_training_job(self, job_id: str) -> bool:
        """Cancel a training job."""
        try:
            if job_id not in self.active_jobs:
                logger.error(f"Job {job_id} not found")
                return False

            status = self.active_jobs[job_id]

            if status.status in [TrainingStatus.COMPLETED, TrainingStatus.CANCELLED]:
                logger.warning(f"Job {job_id} is already {status.status.value}")
                return False

            # Release resources
            if status.resources_allocated:
                self.resource_manager.release_resources(status.resources_allocated)

            # Update status
            status.status = TrainingStatus.CANCELLED
            status.end_time = datetime.now().isoformat()
            status.resources_allocated = []

            # Remove from queue if queued
            self.queue_manager.remove_job_from_queue(job_id)

            # Save status
            self.file_manager.save_job_status(status)

            logger.info(f"Job {job_id} cancelled successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to cancel job {job_id}: {e}")
            return False

    def get_resource_status(self) -> dict[str, Any]:
        """Get resource status."""
        return self.resource_manager.get_resource_status()

    def get_training_summary(self) -> dict[str, Any]:
        """Get training summary."""
        return {
            "total_jobs": len(self.core.jobs),
            "active_jobs": len(self.active_jobs),
            "queued_jobs": self.queue_manager.get_queue_length(),
            "completed_jobs": len(
                [
                    status
                    for status in self.active_jobs.values()
                    if status.status == TrainingStatus.COMPLETED
                ]
            ),
            "failed_jobs": len(
                [
                    status
                    for status in self.active_jobs.values()
                    if status.status == TrainingStatus.FAILED
                ]
            ),
            "resource_status": self.get_resource_status(),
            "active_environments": len(self.core.environments),
            "last_updated": datetime.now().isoformat(),
        }

    def process_job_queue(self) -> None:
        """Process the job queue."""
        next_job = self.queue_manager.get_next_job()
        if next_job:
            self.start_training_job(next_job)


def main():
    """Main function for ML Training Infrastructure Tool."""
    parser = argparse.ArgumentParser(description="ML Training Infrastructure Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Create environment command
    env_parser = subparsers.add_parser("create-env", help="Create training environment")
    env_parser.add_argument("--env-id", required=True, help="Environment ID")
    env_parser.add_argument("--name", required=True, help="Environment name")
    env_parser.add_argument(
        "--framework",
        choices=["tensorflow", "pytorch", "scikit-learn", "xgboost", "custom"],
        required=True,
    )
    env_parser.add_argument("--version", required=True, help="Framework version")
    env_parser.add_argument("--base-image", required=True, help="Base Docker image")

    # Submit job command
    job_parser = subparsers.add_parser("submit-job", help="Submit training job")
    job_parser.add_argument("--name", required=True, help="Job name")
    job_parser.add_argument("--env-id", required=True, help="Environment ID")
    job_parser.add_argument("--script", required=True, help="Training script path")
    job_parser.add_argument("--data-path", required=True, help="Training data path")
    job_parser.add_argument("--output-path", required=True, help="Output path")
    job_parser.add_argument("--gpu", type=int, default=1, help="GPU count")
    job_parser.add_argument("--cpu", type=int, default=2, help="CPU count")

    # Monitor job command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor training job")
    monitor_parser.add_argument("--job-id", required=True, help="Job ID")

    # Resource status command
    resources_parser = subparsers.add_parser("resources", help="Get resource status")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get training summary")

    args = parser.parse_args()

    tool = MLTrainingInfrastructureTool()

    if args.command == "create-env":
        # Check if environment already exists
        env = tool.file_manager.load_environment(args.env_id)
        if env:
            print(f"Environment {args.env_id} already exists")
            return

        env = TrainingEnvironment(
            env_id=args.env_id,
            name=args.name,
            framework=FrameworkType(args.framework),
            version=args.version,
            base_image=args.base_image,
            requirements=["numpy", "pandas", "scikit-learn"],
        )

        success = tool.create_training_environment(env)
        print(f"Environment creation: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "submit-job":
        # Load environment
        env = tool.file_manager.load_environment(args.env_id)
        if not env:
            print(f"Environment {args.env_id} not found")
            return

        # Create training job
        job = TrainingJob(
            job_id="",  # Will be generated
            name=args.name,
            environment=env,
            training_script=args.script,
            data_path=args.data_path,
            output_path=args.output_path,
            hyperparameters={"learning_rate": 0.001, "batch_size": 32},
            resources=[
                TrainingResource(ResourceType.GPU, args.gpu),
                TrainingResource(ResourceType.CPU, args.cpu),
            ],
        )

        success = tool.submit_training_job(job)
        print(f"Job submission: {'SUCCESS' if success else 'FAILED'}")
        if success:
            print(f"Job ID: {job.job_id}")

    elif args.command == "monitor":
        result = tool.monitor_training_job(args.job_id)
        if result:
            print(json.dumps(result, indent=2))
        else:
            print(f"Job {args.job_id} not found")

    elif args.command == "resources":
        status = tool.get_resource_status()
        print(json.dumps(status, indent=2))

    elif args.command == "summary":
        summary = tool.get_training_summary()
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
