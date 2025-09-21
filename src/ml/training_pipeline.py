import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
import numpy as np
from dataclasses import dataclass
from enum import Enum

class PipelineStatus(Enum):
    """Status enumeration for training pipeline stages."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class TrainingJob:
    """Data class for training job information."""
    job_id: str
    model_name: str
    framework: str
    dataset_path: str
    config: Dict[str, Any]
    status: PipelineStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metrics: Optional[Dict[str, Any]] = None

class TrainingPipeline:
    """
    Manages automated ML training pipelines with job scheduling and monitoring.
    Provides workflow orchestration for model training processes.
    """

    def __init__(self, data_path: str = "/app/data", model_path: str = "/app/models"):
        """
        Initializes the TrainingPipeline.

        Args:
            data_path: Path to training datasets.
            model_path: Path to save trained models.
        """
        if not data_path:
            raise ValueError("Data path cannot be empty.")
        if not model_path:
            raise ValueError("Model path cannot be empty.")

        self.data_path = data_path
        self.model_path = model_path
        self.logger = logging.getLogger(__name__)
        
        # Job management
        self.training_jobs: Dict[str, TrainingJob] = {}
        self.job_queue: List[str] = []
        self.active_jobs: List[str] = []
        self.max_concurrent_jobs = 2

        # Ensure directories exist
        os.makedirs(data_path, exist_ok=True)
        os.makedirs(model_path, exist_ok=True)

    def create_training_job(self, model_name: str, framework: str, dataset_path: str,
                          config: Dict[str, Any]) -> str:
        """
        Creates a new training job.

        Args:
            model_name: Name of the model to train.
            framework: ML framework ('tensorflow' or 'pytorch').
            dataset_path: Path to the training dataset.
            config: Training configuration parameters.

        Returns:
            Job ID for the created training job.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if framework not in ['tensorflow', 'pytorch']:
            raise ValueError("Framework must be 'tensorflow' or 'pytorch'.")
        if not dataset_path:
            raise ValueError("Dataset path cannot be empty.")
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        job_id = f"{model_name}_{framework}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        
        job = TrainingJob(
            job_id=job_id,
            model_name=model_name,
            framework=framework,
            dataset_path=dataset_path,
            config=config,
            status=PipelineStatus.PENDING,
            created_at=datetime.utcnow()
        )

        self.training_jobs[job_id] = job
        self.job_queue.append(job_id)
        
        self.logger.info(f"Training job created: {job_id}")
        return job_id

    def get_job_status(self, job_id: str) -> Optional[TrainingJob]:
        """
        Gets the status of a training job.

        Args:
            job_id: ID of the training job.

        Returns:
            TrainingJob object or None if not found.
        """
        if not job_id:
            raise ValueError("Job ID cannot be empty.")
        return self.training_jobs.get(job_id)

    def list_jobs(self, status_filter: Optional[PipelineStatus] = None) -> List[TrainingJob]:
        """
        Lists training jobs with optional status filtering.

        Args:
            status_filter: Optional status to filter by.

        Returns:
            List of TrainingJob objects.
        """
        jobs = list(self.training_jobs.values())
        if status_filter:
            jobs = [job for job in jobs if job.status == status_filter]
        return jobs

    def cancel_job(self, job_id: str) -> bool:
        """
        Cancels a training job.

        Args:
            job_id: ID of the job to cancel.

        Returns:
            True if successfully cancelled, False otherwise.
        """
        if not job_id:
            raise ValueError("Job ID cannot be empty.")
        if job_id not in self.training_jobs:
            return False

        job = self.training_jobs[job_id]
        if job.status in [PipelineStatus.COMPLETED, PipelineStatus.FAILED, PipelineStatus.CANCELLED]:
            return False

        job.status = PipelineStatus.CANCELLED
        job.completed_at = datetime.utcnow()
        
        # Remove from active jobs and queue
        if job_id in self.active_jobs:
            self.active_jobs.remove(job_id)
        if job_id in self.job_queue:
            self.job_queue.remove(job_id)

        self.logger.info(f"Training job cancelled: {job_id}")
        return True

    async def _execute_training_job(self, job_id: str) -> None:
        """
        Executes a training job.

        Args:
            job_id: ID of the job to execute.
        """
        job = self.training_jobs[job_id]
        job.status = PipelineStatus.RUNNING
        job.started_at = datetime.utcnow()

        try:
            self.logger.info(f"Starting training job: {job_id}")
            
            # Load dataset
            dataset = self._load_dataset(job.dataset_path)
            
            # Create and train model based on framework
            if job.framework == 'tensorflow':
                model, metrics = await self._train_tensorflow_model(job, dataset)
            else:  # pytorch
                model, metrics = await self._train_pytorch_model(job, dataset)
            
            # Save trained model
            model_path = os.path.join(self.model_path, f"{job.model_name}_{job.job_id}")
            if job.framework == 'tensorflow':
                model.save(model_path)
            else:  # pytorch
                import torch
                torch.save(model.state_dict(), f"{model_path}.pth")

            # Update job status
            job.status = PipelineStatus.COMPLETED
            job.completed_at = datetime.utcnow()
            job.metrics = metrics

            self.logger.info(f"Training job completed: {job_id}")

        except Exception as e:
            job.status = PipelineStatus.FAILED
            job.completed_at = datetime.utcnow()
            job.error_message = str(e)
            self.logger.error(f"Training job failed: {job_id} - {e}")

        finally:
            # Remove from active jobs
            if job_id in self.active_jobs:
                self.active_jobs.remove(job_id)

    def _load_dataset(self, dataset_path: str) -> Dict[str, np.ndarray]:
        """
        Loads a dataset from the specified path.

        Args:
            dataset_path: Path to the dataset.

        Returns:
            Dictionary containing dataset arrays.
        """
        # This is a simplified dataset loader
        # In a real implementation, this would load actual datasets
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        # Generate sample data for demonstration
        x_train = np.random.rand(1000, 784).astype(np.float32)
        y_train = np.random.randint(0, 10, 1000)
        x_val = np.random.rand(200, 784).astype(np.float32)
        y_val = np.random.randint(0, 10, 200)

        return {
            'x_train': x_train,
            'y_train': y_train,
            'x_val': x_val,
            'y_val': y_val
        }

    async def _train_tensorflow_model(self, job: TrainingJob, dataset: Dict[str, np.ndarray]) -> tuple:
        """
        Trains a TensorFlow model.

        Args:
            job: Training job information.
            dataset: Training dataset.

        Returns:
            Tuple of (trained_model, metrics).
        """
        from src.ml.tensorflow_infrastructure import TensorFlowInfrastructure
        
        tf_infra = TensorFlowInfrastructure(self.model_path, self.data_path)
        
        # Create model
        model = tf_infra.create_sample_model(job.model_name)
        
        # Train model
        history = tf_infra.train_model(
            model,
            dataset['x_train'].reshape(-1, 28, 28, 1),
            dataset['y_train'],
            dataset['x_val'].reshape(-1, 28, 28, 1),
            dataset['y_val'],
            epochs=job.config.get('epochs', 10),
            batch_size=job.config.get('batch_size', 32)
        )

        return model, history

    async def _train_pytorch_model(self, job: TrainingJob, dataset: Dict[str, np.ndarray]) -> tuple:
        """
        Trains a PyTorch model.

        Args:
            job: Training job information.
            dataset: Training dataset.

        Returns:
            Tuple of (trained_model, metrics).
        """
        from src.ml.pytorch_infrastructure import PyTorchInfrastructure
        
        pytorch_infra = PyTorchInfrastructure(self.model_path, self.data_path)
        
        # Create model
        model = pytorch_infra.create_sample_model(job.model_name)
        
        # Train model
        history = pytorch_infra.train_model(
            model,
            dataset['x_train'],
            dataset['y_train'],
            dataset['x_val'],
            dataset['y_val'],
            epochs=job.config.get('epochs', 10),
            batch_size=job.config.get('batch_size', 32),
            learning_rate=job.config.get('learning_rate', 0.001)
        )

        return model, history

    async def process_job_queue(self) -> None:
        """
        Processes the training job queue.
        """
        while True:
            # Start new jobs if we have capacity
            while (len(self.active_jobs) < self.max_concurrent_jobs and 
                   len(self.job_queue) > 0):
                
                job_id = self.job_queue.pop(0)
                if job_id in self.training_jobs:
                    job = self.training_jobs[job_id]
                    if job.status == PipelineStatus.PENDING:
                        self.active_jobs.append(job_id)
                        asyncio.create_task(self._execute_training_job(job_id))

            # Wait before checking again
            await asyncio.sleep(5)

    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Gets the overall pipeline status.

        Returns:
            Pipeline status dictionary.
        """
        total_jobs = len(self.training_jobs)
        pending_jobs = len([j for j in self.training_jobs.values() 
                           if j.status == PipelineStatus.PENDING])
        running_jobs = len(self.active_jobs)
        completed_jobs = len([j for j in self.training_jobs.values() 
                             if j.status == PipelineStatus.COMPLETED])
        failed_jobs = len([j for j in self.training_jobs.values() 
                          if j.status == PipelineStatus.FAILED])

        return {
            "total_jobs": total_jobs,
            "pending_jobs": pending_jobs,
            "running_jobs": running_jobs,
            "completed_jobs": completed_jobs,
            "failed_jobs": failed_jobs,
            "queue_size": len(self.job_queue),
            "max_concurrent_jobs": self.max_concurrent_jobs,
            "timestamp": datetime.utcnow().isoformat()
        }



