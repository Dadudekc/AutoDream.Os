#!/usr/bin/env python3
"""
ML Training Infrastructure Tool
==============================

Infrastructure automation for ML training workloads and environments.
Designed for collaboration with Agent-2 (Architecture & Design) for ML systems.

Features:
- Training environment provisioning
- GPU/CPU resource management and scaling
- Training job orchestration and scheduling
- Training data pipeline infrastructure
- Training monitoring and alerting

Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

import argparse
import json
import logging
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

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
    specifications: Dict[str, Any] = None


@dataclass
class TrainingEnvironment:
    """Training environment configuration."""
    env_id: str
    name: str
    framework: FrameworkType
    version: str
    base_image: str
    requirements: List[str]
    environment_vars: Dict[str, str] = None
    resources: List[TrainingResource] = None


@dataclass
class TrainingJob:
    """Training job configuration."""
    job_id: str
    name: str
    environment: TrainingEnvironment
    training_script: str
    data_path: str
    output_path: str
    hyperparameters: Dict[str, Any]
    resources: List[TrainingResource]
    priority: int = 1
    timeout: int = 3600
    created_at: str = ""


@dataclass
class TrainingJobStatus:
    """Training job status tracking."""
    job_id: str
    status: TrainingStatus
    environment_id: str
    resources_allocated: List[TrainingResource]
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    progress: float = 0.0
    metrics: Dict[str, float] = None
    logs: List[str] = None


class MLTrainingInfrastructureTool:
    """ML Training Infrastructure Tool."""
    
    def __init__(self):
        self.training_dir = Path("ml_training")
        self.training_dir.mkdir(exist_ok=True)
        self.environments_dir = self.training_dir / "environments"
        self.jobs_dir = self.training_dir / "jobs"
        self.environments_dir.mkdir(exist_ok=True)
        self.jobs_dir.mkdir(exist_ok=True)
        
        self.active_jobs: Dict[str, TrainingJobStatus] = {}
        self.job_queue: List[TrainingJob] = []
        self.resource_pool: Dict[str, int] = {
            "cpu_cores": 16,
            "gpu_units": 4,
            "memory_gb": 64,
            "storage_gb": 1000
        }
        
    def create_training_environment(self, env: TrainingEnvironment) -> bool:
        """Create a training environment."""
        try:
            logger.info(f"Creating training environment: {env.name}")
            
            # Simulate environment creation
            self._simulate_environment_creation(env)
            
            # Save environment configuration
            env_file = self.environments_dir / f"{env.env_id}.json"
            env_dict = asdict(env)
            env_dict['framework'] = env.framework.value
            if env.resources:
                env_dict['resources'] = [
                    {
                        'resource_type': r.resource_type.value,
                        'quantity': r.quantity,
                        'specifications': r.specifications or {}
                    }
                    for r in env.resources
                ]
            
            with open(env_file, 'w') as f:
                json.dump(env_dict, f, indent=2)
            
            logger.info(f"Training environment created: {env.env_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create training environment {env.env_id}: {e}")
            return False
    
    def submit_training_job(self, job: TrainingJob) -> bool:
        """Submit a training job for execution."""
        try:
            job.job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            job.created_at = datetime.now().isoformat()
            
            logger.info(f"Submitting training job: {job.name}")
            
            # Add to queue
            self.job_queue.append(job)
            self.job_queue.sort(key=lambda x: x.priority, reverse=True)
            
            # Create job status
            status = TrainingJobStatus(
                job_id=job.job_id,
                status=TrainingStatus.QUEUED,
                environment_id=job.environment.env_id,
                resources_allocated=[],
                metrics={},
                logs=[]
            )
            
            self.active_jobs[job.job_id] = status
            
            # Save job configuration
            job_file = self.jobs_dir / f"{job.job_id}.json"
            job_dict = asdict(job)
            job_dict['environment']['framework'] = job.environment.framework.value
            if job.resources:
                job_dict['resources'] = [
                    {
                        'resource_type': r.resource_type.value,
                        'quantity': r.quantity,
                        'specifications': r.specifications or {}
                    }
                    for r in job.resources
                ]
            
            with open(job_file, 'w') as f:
                json.dump(job_dict, f, indent=2)
            
            # Try to start job if resources available
            self._process_job_queue()
            
            logger.info(f"Training job submitted: {job.job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to submit training job: {e}")
            return False
    
    def start_training_job(self, job_id: str) -> bool:
        """Start a training job."""
        try:
            if job_id not in self.active_jobs:
                logger.error(f"Job {job_id} not found")
                return False
            
            status = self.active_jobs[job_id]
            if status.status != TrainingStatus.QUEUED:
                logger.error(f"Job {job_id} is not queued")
                return False
            
            # Check resource availability
            job = self._get_job_by_id(job_id)
            if not job:
                return False
            
            if not self._allocate_resources(job):
                logger.info(f"Insufficient resources for job {job_id}, keeping in queue")
                return False
            
            logger.info(f"Starting training job: {job_id}")
            
            # Update status
            status.status = TrainingStatus.PROVISIONING
            status.start_time = datetime.now().isoformat()
            
            # Simulate provisioning
            self._simulate_provisioning(job)
            
            # Start training
            status.status = TrainingStatus.RUNNING
            self._simulate_training_progress(status)
            
            logger.info(f"Training job started: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start training job {job_id}: {e}")
            return False
    
    def monitor_training_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Monitor a training job."""
        try:
            if job_id not in self.active_jobs:
                return None
            
            status = self.active_jobs[job_id]
            
            # Simulate training progress
            if status.status == TrainingStatus.RUNNING:
                self._simulate_training_progress(status)
            
            monitoring_data = {
                "job_id": job_id,
                "status": status.status.value,
                "progress": status.progress,
                "environment_id": status.environment_id,
                "resources_allocated": [
                    {
                        "type": r.resource_type.value,
                        "quantity": r.quantity
                    }
                    for r in status.resources_allocated
                ],
                "start_time": status.start_time,
                "end_time": status.end_time,
                "metrics": status.metrics,
                "recent_logs": status.logs[-5:] if status.logs else [],
                "timestamp": datetime.now().isoformat()
            }
            
            return monitoring_data
            
        except Exception as e:
            logger.error(f"Failed to monitor training job {job_id}: {e}")
            return None
    
    def cancel_training_job(self, job_id: str) -> bool:
        """Cancel a training job."""
        try:
            if job_id not in self.active_jobs:
                logger.error(f"Job {job_id} not found")
                return False
            
            status = self.active_jobs[job_id]
            
            if status.status in [TrainingStatus.COMPLETED, TrainingStatus.FAILED, TrainingStatus.CANCELLED]:
                logger.info(f"Job {job_id} is already finished")
                return True
            
            logger.info(f"Cancelling training job: {job_id}")
            
            # Release resources
            self._release_resources(status.resources_allocated)
            
            # Update status
            status.status = TrainingStatus.CANCELLED
            status.end_time = datetime.now().isoformat()
            
            # Remove from queue if present
            self.job_queue = [job for job in self.job_queue if job.job_id != job_id]
            
            logger.info(f"Training job cancelled: {job_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel training job {job_id}: {e}")
            return False
    
    def get_resource_status(self) -> Dict[str, Any]:
        """Get current resource status."""
        allocated_resources = {
            "cpu_cores": 0,
            "gpu_units": 0,
            "memory_gb": 0,
            "storage_gb": 0
        }
        
        # Calculate allocated resources
        for status in self.active_jobs.values():
            if status.status in [TrainingStatus.RUNNING, TrainingStatus.PROVISIONING]:
                for resource in status.resources_allocated:
                    if resource.resource_type == ResourceType.CPU:
                        allocated_resources["cpu_cores"] += resource.quantity
                    elif resource.resource_type == ResourceType.GPU:
                        allocated_resources["gpu_units"] += resource.quantity
                    elif resource.resource_type == ResourceType.MEMORY:
                        allocated_resources["memory_gb"] += resource.quantity
                    elif resource.resource_type == ResourceType.STORAGE:
                        allocated_resources["storage_gb"] += resource.quantity
        
        available_resources = {
            resource_type: self.resource_pool[resource_type] - allocated_resources[resource_type]
            for resource_type in self.resource_pool
        }
        
        return {
            "total_resources": self.resource_pool,
            "allocated_resources": allocated_resources,
            "available_resources": available_resources,
            "utilization_percentage": {
                resource_type: (allocated_resources[resource_type] / self.resource_pool[resource_type]) * 100
                for resource_type in self.resource_pool
            },
            "timestamp": datetime.now().isoformat()
        }
    
    def get_training_summary(self) -> Dict[str, Any]:
        """Get training infrastructure summary."""
        return {
            "total_jobs": len(self.active_jobs),
            "queued_jobs": len([job for job in self.job_queue if job.job_id in self.active_jobs and self.active_jobs[job.job_id].status == TrainingStatus.QUEUED]),
            "running_jobs": len([status for status in self.active_jobs.values() if status.status == TrainingStatus.RUNNING]),
            "completed_jobs": len([status for status in self.active_jobs.values() if status.status == TrainingStatus.COMPLETED]),
            "failed_jobs": len([status for status in self.active_jobs.values() if status.status == TrainingStatus.FAILED]),
            "resource_status": self.get_resource_status(),
            "active_environments": len(list(self.environments_dir.glob("*.json"))),
            "last_updated": datetime.now().isoformat()
        }
    
    # Helper methods
    def _simulate_environment_creation(self, env: TrainingEnvironment) -> None:
        """Simulate training environment creation."""
        logger.info(f"Creating environment {env.name} with {env.framework.value}")
        logger.info(f"Base image: {env.base_image}")
        logger.info(f"Requirements: {len(env.requirements)} packages")
        if env.resources:
            for resource in env.resources:
                logger.info(f"Resource: {resource.resource_type.value} x{resource.quantity}")
        logger.info("Environment created successfully")
    
    def _simulate_provisioning(self, job: TrainingJob) -> None:
        """Simulate job provisioning."""
        logger.info(f"Provisioning resources for job {job.job_id}")
        for resource in job.resources:
            logger.info(f"Allocating {resource.resource_type.value} x{resource.quantity}")
        logger.info("Provisioning completed")
    
    def _simulate_training_progress(self, status: TrainingJobStatus) -> None:
        """Simulate training progress."""
        if status.progress < 100.0:
            status.progress = min(status.progress + 10.0, 100.0)
            
            # Simulate metrics
            status.metrics = {
                "loss": max(1.0 - (status.progress / 100.0), 0.1),
                "accuracy": min(status.progress / 100.0, 0.95),
                "learning_rate": 0.001 * (1.0 - status.progress / 100.0),
                "epoch": int(status.progress / 10.0)
            }
            
            # Simulate logs
            log_entry = f"Epoch {int(status.progress / 10.0)}: Loss={status.metrics['loss']:.4f}, Accuracy={status.metrics['accuracy']:.4f}"
            if not status.logs:
                status.logs = []
            status.logs.append(log_entry)
            
            if status.progress >= 100.0:
                status.status = TrainingStatus.COMPLETED
                status.end_time = datetime.now().isoformat()
                self._release_resources(status.resources_allocated)
                logger.info(f"Training job {status.job_id} completed")
    
    def _allocate_resources(self, job: TrainingJob) -> bool:
        """Allocate resources for a training job."""
        # Simplified resource allocation logic
        for resource in job.resources:
            if resource.resource_type == ResourceType.GPU and self.resource_pool["gpu_units"] < resource.quantity:
                return False
            if resource.resource_type == ResourceType.CPU and self.resource_pool["cpu_cores"] < resource.quantity:
                return False
        
        # Allocate resources
        status = self.active_jobs[job.job_id]
        status.resources_allocated = job.resources.copy()
        
        for resource in job.resources:
            if resource.resource_type == ResourceType.GPU:
                self.resource_pool["gpu_units"] -= resource.quantity
            elif resource.resource_type == ResourceType.CPU:
                self.resource_pool["cpu_cores"] -= resource.quantity
        
        return True
    
    def _release_resources(self, resources: List[TrainingResource]) -> None:
        """Release allocated resources."""
        for resource in resources:
            if resource.resource_type == ResourceType.GPU:
                self.resource_pool["gpu_units"] += resource.quantity
            elif resource.resource_type == ResourceType.CPU:
                self.resource_pool["cpu_cores"] += resource.quantity
    
    def _process_job_queue(self) -> None:
        """Process the job queue."""
        for job in self.job_queue[:]:  # Copy to avoid modification during iteration
            if job.job_id in self.active_jobs:
                status = self.active_jobs[job.job_id]
                if status.status == TrainingStatus.QUEUED:
                    if self.start_training_job(job.job_id):
                        break  # Only start one job at a time
    
    def _get_job_by_id(self, job_id: str) -> Optional[TrainingJob]:
        """Get job by ID."""
        job_file = self.jobs_dir / f"{job_id}.json"
        if job_file.exists():
            with open(job_file, 'r') as f:
                job_data = json.load(f)
                # Convert back to objects
                job_data['environment']['framework'] = FrameworkType(job_data['environment']['framework'])
                if job_data.get('resources'):
                    job_data['resources'] = [
                        TrainingResource(
                            resource_type=ResourceType(r['resource_type']),
                            quantity=r['quantity'],
                            specifications=r.get('specifications', {})
                        )
                        for r in job_data['resources']
                    ]
                return TrainingJob(**job_data)
        return None


def main():
    """Main function for ML Training Infrastructure Tool."""
    parser = argparse.ArgumentParser(description="ML Training Infrastructure Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Create environment command
    env_parser = subparsers.add_parser("create-env", help="Create training environment")
    env_parser.add_argument("--env-id", required=True, help="Environment ID")
    env_parser.add_argument("--name", required=True, help="Environment name")
    env_parser.add_argument("--framework", choices=["tensorflow", "pytorch", "scikit-learn", "xgboost", "custom"], required=True)
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
        # Load environment file if exists
        env_file = tool.environments_dir / f"{args.env_id}.json"
        if env_file.exists():
            print(f"Environment {args.env_id} already exists")
            return
        
        env = TrainingEnvironment(
            env_id=args.env_id,
            name=args.name,
            framework=FrameworkType(args.framework),
            version=args.version,
            base_image=args.base_image,
            requirements=["numpy", "pandas", "scikit-learn"]
        )
        
        success = tool.create_training_environment(env)
        print(f"Environment creation: {'SUCCESS' if success else 'FAILED'}")
    
    elif args.command == "submit-job":
        # Load environment
        env_file = tool.environments_dir / f"{args.env_id}.json"
        if not env_file.exists():
            print(f"Environment {args.env_id} not found")
            return
        
        with open(env_file, 'r') as f:
            env_data = json.load(f)
        
        env = TrainingEnvironment(**env_data)
        env.framework = FrameworkType(env.framework)
        
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
                TrainingResource(ResourceType.CPU, args.cpu)
            ]
        )
        
        success = tool.submit_training_job(job)
        print(f"Job submission: {'SUCCESS' if success else 'FAILED'}")
    
    elif args.command == "monitor":
        data = tool.monitor_training_job(args.job_id)
        if data:
            print(json.dumps(data, indent=2))
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
    logging.basicConfig(level=logging.INFO)
    main()
