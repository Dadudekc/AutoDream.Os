import asyncio
import logging
from datetime import datetime
from typing import Any

from src.ml.pytorch_infrastructure import PyTorchInfrastructure
from src.ml.tensorflow_infrastructure import TensorFlowInfrastructure


class ModelDeployment:
    """
    Manages ML model deployment, serving, and lifecycle management.
    Provides REST API endpoints for model inference and management.
    """

    def __init__(self, model_path: str = "/app/models", port: int = 8080):
        """
        Initializes the ModelDeployment system.

        Args:
            model_path: Path to store and load models.
            port: Port for the deployment server.
        """
        if not model_path:
            raise ValueError("Model path cannot be empty.")
        if not 1 <= port <= 65535:
            raise ValueError("Port must be between 1 and 65535.")

        self.model_path = model_path
        self.port = port
        self.logger = logging.getLogger(__name__)

        # Initialize ML frameworks
        self.tf_infrastructure = TensorFlowInfrastructure(model_path)
        self.pytorch_infrastructure = PyTorchInfrastructure(model_path)

        # Model registry
        self.deployed_models: dict[str, dict[str, Any]] = {}
        self.model_versions: dict[str, list[str]] = {}

    def deploy_model(
        self,
        model_name: str,
        framework: str,
        version: str = "1.0",
        model_config: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Deploys a model for serving.

        Args:
            model_name: Name of the model to deploy.
            framework: ML framework ('tensorflow' or 'pytorch').
            version: Version of the model.
            model_config: Optional configuration for the model.

        Returns:
            Deployment information dictionary.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        if framework not in ["tensorflow", "pytorch"]:
            raise ValueError("Framework must be 'tensorflow' or 'pytorch'.")
        if not version:
            raise ValueError("Version cannot be empty.")

        deployment_id = f"{model_name}_{framework}_{version}"

        # Load model based on framework
        if framework == "tensorflow":
            model = self.tf_infrastructure.load_model(model_name, version)
        else:  # pytorch
            model = self.pytorch_infrastructure.load_model(model_name, version)

        # Register deployment
        deployment_info = {
            "deployment_id": deployment_id,
            "model_name": model_name,
            "framework": framework,
            "version": version,
            "deployed_at": datetime.utcnow().isoformat(),
            "status": "active",
            "endpoint": f"/predict/{deployment_id}",
            "config": model_config or {},
        }

        self.deployed_models[deployment_id] = deployment_info

        # Track versions
        if model_name not in self.model_versions:
            self.model_versions[model_name] = []
        if version not in self.model_versions[model_name]:
            self.model_versions[model_name].append(version)

        self.logger.info(f"Model deployed: {deployment_id}")
        return deployment_info

    def predict(self, deployment_id: str, input_data: Any) -> dict[str, Any]:
        """
        Makes predictions using a deployed model.

        Args:
            deployment_id: ID of the deployed model.
            input_data: Input data for prediction.

        Returns:
            Prediction results dictionary.
        """
        if not deployment_id:
            raise ValueError("Deployment ID cannot be empty.")
        if deployment_id not in self.deployed_models:
            raise ValueError(f"Model deployment '{deployment_id}' not found.")

        deployment = self.deployed_models[deployment_id]
        if deployment["status"] != "active":
            raise ValueError(f"Model deployment '{deployment_id}' is not active.")

        start_time = datetime.utcnow()

        try:
            # Make prediction based on framework
            if deployment["framework"] == "tensorflow":
                predictions = self.tf_infrastructure.predict(deployment["model_name"], input_data)
            else:  # pytorch
                predictions = self.pytorch_infrastructure.predict(
                    deployment["model_name"], input_data
                )

            end_time = datetime.utcnow()
            duration = (end_time - start_time).total_seconds()

            result = {
                "deployment_id": deployment_id,
                "predictions": predictions.tolist()
                if hasattr(predictions, "tolist")
                else predictions,
                "timestamp": end_time.isoformat(),
                "duration_seconds": duration,
                "status": "success",
            }

            self.logger.info(f"Prediction completed for {deployment_id} in {duration:.3f}s")
            return result

        except Exception as e:
            self.logger.error(f"Prediction failed for {deployment_id}: {e}")
            return {
                "deployment_id": deployment_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error",
            }

    def get_deployment_status(self, deployment_id: str) -> dict[str, Any]:
        """
        Gets the status of a model deployment.

        Args:
            deployment_id: ID of the deployed model.

        Returns:
            Deployment status dictionary.
        """
        if not deployment_id:
            raise ValueError("Deployment ID cannot be empty.")
        if deployment_id not in self.deployed_models:
            raise ValueError(f"Model deployment '{deployment_id}' not found.")

        return self.deployed_models[deployment_id]

    def list_deployments(self) -> list[dict[str, Any]]:
        """
        Lists all deployed models.

        Returns:
            List of deployment information dictionaries.
        """
        return list(self.deployed_models.values())

    def undeploy_model(self, deployment_id: str) -> bool:
        """
        Undeploys a model.

        Args:
            deployment_id: ID of the deployed model to undeploy.

        Returns:
            True if successfully undeployed, False otherwise.
        """
        if not deployment_id:
            raise ValueError("Deployment ID cannot be empty.")
        if deployment_id not in self.deployed_models:
            return False

        self.deployed_models[deployment_id]["status"] = "inactive"
        self.logger.info(f"Model undeployed: {deployment_id}")
        return True

    def get_model_versions(self, model_name: str) -> list[str]:
        """
        Gets all versions of a model.

        Args:
            model_name: Name of the model.

        Returns:
            List of version strings.
        """
        if not model_name:
            raise ValueError("Model name cannot be empty.")
        return self.model_versions.get(model_name, [])

    def health_check(self) -> dict[str, Any]:
        """
        Performs a health check on the deployment system.

        Returns:
            Health status dictionary.
        """
        active_deployments = sum(
            1 for dep in self.deployed_models.values() if dep["status"] == "active"
        )

        return {
            "status": "healthy",
            "active_deployments": active_deployments,
            "total_deployments": len(self.deployed_models),
            "timestamp": datetime.utcnow().isoformat(),
            "model_path": self.model_path,
            "port": self.port,
        }

    async def start_server(self) -> None:
        """
        Starts the model deployment server.
        """
        import aiohttp_cors
        from aiohttp import web

        app = web.Application()
        cors = aiohttp_cors.setup(
            app,
            defaults={
                "*": aiohttp_cors.ResourceOptions(
                    allow_credentials=True, expose_headers="*", allow_headers="*", allow_methods="*"
                )
            },
        )

        # Health check endpoint
        async def health_handler(request):
            return web.json_response(self.health_check())

        # List deployments endpoint
        async def list_deployments_handler(request):
            return web.json_response(self.list_deployments())

        # Predict endpoint
        async def predict_handler(request):
            try:
                data = await request.json()
                deployment_id = data.get("deployment_id")
                input_data = data.get("input_data")

                if not deployment_id or input_data is None:
                    return web.json_response(
                        {"error": "deployment_id and input_data are required"}, status=400
                    )

                result = self.predict(deployment_id, input_data)
                return web.json_response(result)

            except Exception as e:
                return web.json_response({"error": str(e)}, status=500)

        # Add routes
        app.router.add_get("/health", health_handler)
        app.router.add_get("/deployments", list_deployments_handler)
        app.router.add_post("/predict", predict_handler)

        # Add CORS to all routes
        for route in list(app.router.routes()):
            cors.add(route)

        self.logger.info(f"Starting model deployment server on port {self.port}")
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()

        # Keep server running
        try:
            await asyncio.Future()
        except KeyboardInterrupt:
            self.logger.info("Shutting down model deployment server")
        finally:
            await runner.cleanup()
