import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from datetime import datetime
from src.ml.tensorflow_infrastructure import TensorFlowInfrastructure
from src.ml.pytorch_infrastructure import PyTorchInfrastructure
from src.ml.model_deployment import ModelDeployment
from src.ml.training_pipeline import TrainingPipeline
from src.ml.model_versioning import ModelVersioning
from src.ml.ml_monitoring import MLMonitoring
from src.ml.validation_framework import MLValidationFramework

class MLPipelineManager:
    """
    Main manager for the ML pipeline system.
    Integrates all ML components: training, deployment, versioning, monitoring, and validation.
    """

    def __init__(self, base_path: str = "/app"):
        """
        Initializes the MLPipelineManager.

        Args:
            base_path: Base path for all ML components.
        """
        if not base_path:
            raise ValueError("Base path cannot be empty.")

        self.base_path = base_path
        self.logger = logging.getLogger(__name__)
        
        # Component paths
        self.model_path = os.path.join(base_path, "models")
        self.data_path = os.path.join(base_path, "data")
        self.metrics_path = os.path.join(base_path, "metrics")
        self.test_path = os.path.join(base_path, "tests")
        self.results_path = os.path.join(base_path, "test_results")
        self.registry_path = os.path.join(base_path, "registry")

        # Initialize components
        self.tf_infrastructure = TensorFlowInfrastructure(self.model_path, self.data_path)
        self.pytorch_infrastructure = PyTorchInfrastructure(self.model_path, self.data_path)
        self.model_deployment = ModelDeployment(self.model_path)
        self.training_pipeline = TrainingPipeline(self.data_path, self.model_path)
        self.model_versioning = ModelVersioning(self.model_path, self.registry_path)
        self.ml_monitoring = MLMonitoring(self.metrics_path)
        self.validation_framework = MLValidationFramework(self.test_path, self.results_path)

        # Pipeline status
        self.pipeline_status = "initialized"
        self.startup_time = datetime.utcnow()

        self.logger.info("ML Pipeline Manager initialized successfully")

    async def start_pipeline(self) -> None:
        """Starts the ML pipeline system."""
        try:
            self.logger.info("Starting ML Pipeline system...")
            
            # Start model deployment server
            deployment_task = asyncio.create_task(self.model_deployment.start_server())
            
            # Start training pipeline processor
            training_task = asyncio.create_task(self.training_pipeline.process_job_queue())
            
            # Start metrics cleanup task
            cleanup_task = asyncio.create_task(self._periodic_cleanup())
            
            self.pipeline_status = "running"
            self.logger.info("ML Pipeline system started successfully")
            
            # Wait for tasks
            await asyncio.gather(deployment_task, training_task, cleanup_task)
            
        except Exception as e:
            self.pipeline_status = "error"
            self.logger.error(f"Failed to start ML Pipeline: {e}")
            raise

    async def _periodic_cleanup(self) -> None:
        """Performs periodic cleanup tasks."""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                await self.ml_monitoring.cleanup_old_metrics()
                self.logger.info("Periodic cleanup completed")
            except Exception as e:
                self.logger.error(f"Cleanup task failed: {e}")

    def create_and_train_model(self, model_name: str, framework: str, 
                             dataset_path: str, config: Dict[str, Any]) -> str:
        """
        Creates and trains a new model.

        Args:
            model_name: Name of the model.
            framework: ML framework ('tensorflow' or 'pytorch').
            dataset_path: Path to the training dataset.
            config: Training configuration.

        Returns:
            Job ID for the training job.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if framework not in ['tensorflow', 'pytorch']:
            raise ValueError("Framework must be 'tensorflow' or 'pytorch'.")

        # Create training job
        job_id = self.training_pipeline.create_training_job(
            model_name, framework, dataset_path, config
        )

        self.logger.info(f"Created training job: {job_id}")
        return job_id

    def deploy_model(self, model_name: str, framework: str, version: str = "1.0") -> Dict[str, Any]:
        """
        Deploys a trained model.

        Args:
            model_name: Name of the model.
            framework: ML framework.
            version: Model version.

        Returns:
            Deployment information.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if framework not in ['tensorflow', 'pytorch']:
            raise ValueError("Framework must be 'tensorflow' or 'pytorch'.")

        # Deploy model
        deployment_info = self.model_deployment.deploy_model(
            model_name, framework, version
        )

        self.logger.info(f"Deployed model: {model_name} v{version}")
        return deployment_info

    def make_prediction(self, deployment_id: str, input_data: Any) -> Dict[str, Any]:
        """
        Makes a prediction using a deployed model.

        Args:
            deployment_id: ID of the deployed model.
            input_data: Input data for prediction.

        Returns:
            Prediction results.
        """
        if not deployment_id:
            raise ValueError("Deployment ID cannot be empty.")

        start_time = datetime.utcnow()
        
        # Make prediction
        result = self.model_deployment.predict(deployment_id, input_data)
        
        end_time = datetime.utcnow()
        prediction_time = (end_time - start_time).total_seconds()

        # Record metrics
        if result.get("status") == "success":
            deployment = self.model_deployment.get_deployment_status(deployment_id)
            self.ml_monitoring.record_prediction_metrics(
                deployment["model_name"],
                deployment["version"],
                prediction_time,
                result.get("confidence", 0.0),
                len(str(input_data)),
                len(str(result.get("predictions", [])))
            )

        return result

    def register_model_version(self, model_name: str, version: str, framework: str,
                             file_path: str, created_by: str, **kwargs) -> Any:
        """
        Registers a new model version.

        Args:
            model_name: Name of the model.
            version: Version string.
            framework: ML framework.
            file_path: Path to model file.
            created_by: Creator identifier.
            **kwargs: Additional registration parameters.

        Returns:
            ModelVersion object.
        """
        return self.model_versioning.register_model_version(
            model_name, version, framework, file_path, created_by, **kwargs
        )

    def promote_model_version(self, model_name: str, version: str, target_status: str) -> bool:
        """
        Promotes a model version.

        Args:
            model_name: Name of the model.
            version: Version string.
            target_status: Target status for promotion.

        Returns:
            True if successfully promoted.
        """
        from src.ml.model_versioning import VersionStatus
        status_enum = VersionStatus(target_status)
        return self.model_versioning.promote_version(model_name, version, status_enum)

    async def run_model_validation(self, model_name: str, version: str, 
                                 suite_name: str = "default") -> List[Any]:
        """
        Runs validation tests for a model.

        Args:
            model_name: Name of the model.
            version: Model version.
            suite_name: Name of the test suite.

        Returns:
            List of validation results.
        """
        return await self.validation_framework.run_test_suite(
            suite_name, model_name, version
        )

    def create_alert_rule(self, name: str, metric_name: str, threshold: float,
                         condition: str, severity: str, description: str) -> str:
        """
        Creates an alert rule.

        Args:
            name: Name of the alert rule.
            metric_name: Name of the metric to monitor.
            threshold: Threshold value.
            condition: Alert condition.
            severity: Alert severity.
            description: Alert description.

        Returns:
            Alert rule ID.
        """
        from src.ml.ml_monitoring import AlertSeverity
        severity_enum = AlertSeverity(severity)
        return self.ml_monitoring.create_alert_rule(
            name, metric_name, threshold, condition, severity_enum, description
        )

    def get_pipeline_status(self) -> Dict[str, Any]:
        """
        Gets the overall pipeline status.

        Returns:
            Pipeline status dictionary.
        """
        return {
            "pipeline_status": self.pipeline_status,
            "startup_time": self.startup_time.isoformat(),
            "uptime_seconds": (datetime.utcnow() - self.startup_time).total_seconds(),
            "components": {
                "tensorflow_infrastructure": "active",
                "pytorch_infrastructure": "active",
                "model_deployment": "active",
                "training_pipeline": "active",
                "model_versioning": "active",
                "ml_monitoring": "active",
                "validation_framework": "active"
            },
            "training_pipeline": self.training_pipeline.get_pipeline_status(),
            "monitoring": self.ml_monitoring.get_monitoring_dashboard_data(),
            "validation": self.validation_framework.get_test_summary(),
            "versioning": self.model_versioning.get_registry_summary()
        }

    def get_model_catalog(self) -> Dict[str, Any]:
        """
        Gets the model catalog with all registered models and versions.

        Returns:
            Model catalog dictionary.
        """
        catalog = {}
        
        for model_name in self.model_versioning.versions.keys():
            versions = self.model_versioning.get_model_versions(model_name)
            latest_version = self.model_versioning.get_latest_version(model_name)
            
            catalog[model_name] = {
                "total_versions": len(versions),
                "latest_version": latest_version.version if latest_version else None,
                "latest_status": latest_version.status.value if latest_version else None,
                "versions": [
                    {
                        "version": v.version,
                        "status": v.status.value,
                        "framework": v.framework,
                        "created_at": v.created_at.isoformat(),
                        "created_by": v.created_by
                    }
                    for v in versions
                ]
            }

        return catalog

    def health_check(self) -> Dict[str, Any]:
        """
        Performs a comprehensive health check of the ML pipeline.

        Returns:
            Health check results.
        """
        health_status = {
            "overall_status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "components": {}
        }

        # Check each component
        try:
            health_status["components"]["model_deployment"] = self.model_deployment.health_check()
        except Exception as e:
            health_status["components"]["model_deployment"] = {"status": "unhealthy", "error": str(e)}
            health_status["overall_status"] = "degraded"

        try:
            health_status["components"]["training_pipeline"] = self.training_pipeline.get_pipeline_status()
        except Exception as e:
            health_status["components"]["training_pipeline"] = {"status": "unhealthy", "error": str(e)}
            health_status["overall_status"] = "degraded"

        try:
            health_status["components"]["model_versioning"] = self.model_versioning.get_registry_summary()
        except Exception as e:
            health_status["components"]["model_versioning"] = {"status": "unhealthy", "error": str(e)}
            health_status["overall_status"] = "degraded"

        try:
            health_status["components"]["ml_monitoring"] = self.ml_monitoring.get_monitoring_dashboard_data()
        except Exception as e:
            health_status["components"]["ml_monitoring"] = {"status": "unhealthy", "error": str(e)}
            health_status["overall_status"] = "degraded"

        try:
            health_status["components"]["validation_framework"] = self.validation_framework.get_test_summary()
        except Exception as e:
            health_status["components"]["validation_framework"] = {"status": "unhealthy", "error": str(e)}
            health_status["overall_status"] = "degraded"

        return health_status
