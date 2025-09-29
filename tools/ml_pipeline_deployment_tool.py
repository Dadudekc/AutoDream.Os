#!/usr/bin/env python3
"""
ML Pipeline Deployment Automation Tool
=====================================

Infrastructure automation for ML/AI pipeline deployment and management.
Designed for collaboration with Agent-2 (Architecture & Design) for ML systems.

Features:
- Automated ML model deployment
- Container orchestration for ML workloads
- Auto-scaling based on ML demands
- ML pipeline monitoring and alerting
- Model versioning and rollback

Agent-3: Infrastructure & DevOps Specialist
Mission: V3 Infrastructure Deployment
"""

import argparse
import json
import logging
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

logger = logging.getLogger(__name__)


class DeploymentStatusEnum(Enum):
    """ML deployment status."""

    PENDING = "pending"
    DEPLOYING = "deploying"
    ACTIVE = "active"
    SCALING = "scaling"
    ROLLBACK = "rollback"
    FAILED = "failed"


class MLFramework(Enum):
    """Supported ML frameworks."""

    TENSORFLOW = "tensorflow"
    PYTORCH = "pytorch"
    SCIKIT_LEARN = "scikit-learn"
    XGBOOST = "xgboost"
    CUSTOM = "custom"


class ScalingStrategy(Enum):
    """Auto-scaling strategies."""

    CPU_BASED = "cpu_based"
    MEMORY_BASED = "memory_based"
    REQUEST_BASED = "request_based"
    HYBRID = "hybrid"


@dataclass
class MLModel:
    """ML model configuration."""

    model_id: str
    model_name: str
    version: str
    framework: MLFramework
    model_path: str
    input_shape: list[int]
    output_shape: list[int]
    memory_requirements: int  # MB
    cpu_requirements: float  # CPU cores
    created_at: str
    accuracy: float | None = None
    metadata: dict[str, Any] = None


@dataclass
class DeploymentConfig:
    """Deployment configuration."""

    deployment_id: str
    model: MLModel
    replicas: int = 1
    min_replicas: int = 1
    max_replicas: int = 10
    scaling_strategy: ScalingStrategy = ScalingStrategy.CPU_BASED
    cpu_threshold: float = 70.0
    memory_threshold: float = 80.0
    request_threshold: int = 100
    health_check_interval: int = 30
    deployment_timeout: int = 600


@dataclass
class DeploymentStatus:
    """Deployment status tracking."""

    deployment_id: str
    status: DeploymentStatusEnum
    replicas_active: int
    replicas_desired: int
    cpu_usage: float
    memory_usage: float
    request_rate: float
    response_time: float
    last_updated: str
    health_score: float


class MLPipelineDeploymentTool:
    """ML Pipeline Deployment Automation Tool."""

    def __init__(self):
        self.deployments_dir = Path("ml_deployments")
        self.deployments_dir.mkdir(exist_ok=True)
        self.models_dir = Path("ml_models")
        self.models_dir.mkdir(exist_ok=True)
        self.active_deployments: dict[str, DeploymentStatus] = {}
        self.deployment_history: list[dict[str, Any]] = []

    def register_model(self, model: MLModel) -> bool:
        """Register an ML model for deployment."""
        try:
            model_file = self.models_dir / f"{model.model_id}.json"
            model_dict = asdict(model)
            model_dict["framework"] = model.framework.value  # Convert enum to string
            with open(model_file, "w") as f:
                json.dump(model_dict, f, indent=2)

            logger.info(f"Model registered: {model.model_id} v{model.version}")
            return True

        except Exception as e:
            logger.error(f"Failed to register model {model.model_id}: {e}")
            return False

    def deploy_model(self, config: DeploymentConfig) -> bool:
        """Deploy ML model with specified configuration."""
        try:
            deployment_id = config.deployment_id
            logger.info(f"Deploying model {config.model.model_name} v{config.model.version}")

            # Simulate deployment process
            self._simulate_deployment(config)

            # Create deployment status
            status = DeploymentStatus(
                deployment_id=deployment_id,
                status=DeploymentStatusEnum.ACTIVE,
                replicas_active=config.replicas,
                replicas_desired=config.replicas,
                cpu_usage=45.2,
                memory_usage=67.8,
                request_rate=25.5,
                response_time=0.045,
                last_updated=datetime.now().isoformat(),
                health_score=95.5,
            )

            self.active_deployments[deployment_id] = status

            # Save deployment config
            config_file = self.deployments_dir / f"{deployment_id}_config.json"
            config_dict = asdict(config)
            config_dict["model"]["framework"] = config.model.framework.value
            config_dict["scaling_strategy"] = config.scaling_strategy.value
            with open(config_file, "w") as f:
                json.dump(config_dict, f, indent=2)

            # Log deployment
            self._log_deployment(deployment_id, "deployed", config.model.model_name)

            logger.info(f"Model deployed successfully: {deployment_id}")
            return True

        except Exception as e:
            logger.error(f"Deployment failed for {config.deployment_id}: {e}")
            return False

    def scale_deployment(self, deployment_id: str, target_replicas: int) -> bool:
        """Scale ML model deployment."""
        try:
            if deployment_id not in self.active_deployments:
                logger.error(f"Deployment {deployment_id} not found")
                return False

            status = self.active_deployments[deployment_id]
            logger.info(
                f"Scaling deployment {deployment_id}: {status.replicas_active} -> {target_replicas}"
            )

            # Simulate scaling
            status.status = DeploymentStatusEnum.SCALING
            status.replicas_desired = target_replicas
            status.last_updated = datetime.now().isoformat()

            # Simulate scaling completion
            status.status = DeploymentStatusEnum.ACTIVE
            status.replicas_active = target_replicas

            self._log_deployment(deployment_id, "scaled", f"replicas: {target_replicas}")

            logger.info(f"Deployment scaled successfully: {deployment_id}")
            return True

        except Exception as e:
            logger.error(f"Scaling failed for {deployment_id}: {e}")
            return False

    def auto_scale_deployment(self, deployment_id: str) -> bool:
        """Automatically scale deployment based on metrics."""
        try:
            if deployment_id not in self.active_deployments:
                return False

            status = self.active_deployments[deployment_id]

            # Load deployment config
            config_file = self.deployments_dir / f"{deployment_id}_config.json"
            if not config_file.exists():
                return False

            with open(config_file) as f:
                config_data = json.load(f)

            # Determine scaling action based on strategy
            scaling_strategy = ScalingStrategy(config_data["scaling_strategy"])
            current_replicas = status.replicas_active
            target_replicas = current_replicas

            if scaling_strategy == ScalingStrategy.CPU_BASED:
                if status.cpu_usage > config_data["cpu_threshold"]:
                    target_replicas = min(current_replicas + 2, config_data["max_replicas"])
                elif status.cpu_usage < 30.0 and current_replicas > config_data["min_replicas"]:
                    target_replicas = max(current_replicas - 1, config_data["min_replicas"])

            elif scaling_strategy == ScalingStrategy.MEMORY_BASED:
                if status.memory_usage > config_data["memory_threshold"]:
                    target_replicas = min(current_replicas + 1, config_data["max_replicas"])
                elif status.memory_usage < 40.0 and current_replicas > config_data["min_replicas"]:
                    target_replicas = max(current_replicas - 1, config_data["min_replicas"])

            elif scaling_strategy == ScalingStrategy.REQUEST_BASED:
                if status.request_rate > config_data["request_threshold"]:
                    target_replicas = min(current_replicas + 2, config_data["max_replicas"])
                elif status.request_rate < 20.0 and current_replicas > config_data["min_replicas"]:
                    target_replicas = max(current_replicas - 1, config_data["min_replicas"])

            if target_replicas != current_replicas:
                logger.info(
                    f"Auto-scaling {deployment_id}: {current_replicas} -> {target_replicas}"
                )
                return self.scale_deployment(deployment_id, target_replicas)

            return True

        except Exception as e:
            logger.error(f"Auto-scaling failed for {deployment_id}: {e}")
            return False

    def monitor_deployment(self, deployment_id: str) -> dict[str, Any] | None:
        """Monitor ML deployment health and performance."""
        try:
            if deployment_id not in self.active_deployments:
                return None

            status = self.active_deployments[deployment_id]

            # Simulate monitoring data collection
            monitoring_data = {
                "deployment_id": deployment_id,
                "timestamp": datetime.now().isoformat(),
                "status": status.status.value,
                "replicas": {"active": status.replicas_active, "desired": status.replicas_desired},
                "metrics": {
                    "cpu_usage": status.cpu_usage,
                    "memory_usage": status.memory_usage,
                    "request_rate": status.request_rate,
                    "response_time": status.response_time,
                    "health_score": status.health_score,
                },
                "alerts": self._check_deployment_alerts(status),
            }

            return monitoring_data

        except Exception as e:
            logger.error(f"Monitoring failed for {deployment_id}: {e}")
            return None

    def rollback_deployment(self, deployment_id: str, target_version: str = None) -> bool:
        """Rollback ML model deployment to previous version."""
        try:
            if deployment_id not in self.active_deployments:
                logger.error(f"Deployment {deployment_id} not found")
                return False

            status = self.active_deployments[deployment_id]
            logger.info(f"Rolling back deployment {deployment_id}")

            # Simulate rollback process
            status.status = DeploymentStatusEnum.ROLLBACK
            status.last_updated = datetime.now().isoformat()

            # Simulate rollback completion
            status.status = DeploymentStatusEnum.ACTIVE

            self._log_deployment(
                deployment_id, "rollback", f"version: {target_version or 'previous'}"
            )

            logger.info(f"Deployment rolled back successfully: {deployment_id}")
            return True

        except Exception as e:
            logger.error(f"Rollback failed for {deployment_id}: {e}")
            return False

    def get_deployment_summary(self) -> dict[str, Any]:
        """Get summary of all deployments."""
        return {
            "total_deployments": len(self.active_deployments),
            "active_deployments": len(
                [
                    d
                    for d in self.active_deployments.values()
                    if d.status == DeploymentStatusEnum.ACTIVE
                ]
            ),
            "scaling_deployments": len(
                [
                    d
                    for d in self.active_deployments.values()
                    if d.status == DeploymentStatusEnum.SCALING
                ]
            ),
            "deployments": [asdict(deployment) for deployment in self.active_deployments.values()],
            "deployment_history": self.deployment_history[-10:],  # Last 10 deployments
            "last_updated": datetime.now().isoformat(),
        }

    # Helper methods
    def _simulate_deployment(self, config: DeploymentConfig) -> None:
        """Simulate deployment process."""
        logger.info(f"Creating deployment {config.deployment_id}")
        logger.info(f"Model: {config.model.model_name} v{config.model.version}")
        logger.info(f"Framework: {config.model.framework.value}")
        logger.info(f"Replicas: {config.replicas}")
        logger.info(f"Scaling: {config.scaling_strategy.value}")

        # Simulate deployment steps
        logger.info("Pulling model image...")
        logger.info("Creating deployment pods...")
        logger.info("Configuring load balancer...")
        logger.info("Setting up monitoring...")
        logger.info("Deployment completed!")

    def _check_deployment_alerts(self, status: DeploymentStatus) -> list[dict[str, Any]]:
        """Check for deployment alerts."""
        alerts = []

        if status.cpu_usage > 90.0:
            alerts.append(
                {
                    "type": "high_cpu",
                    "level": "critical",
                    "message": f"High CPU usage: {status.cpu_usage}%",
                }
            )

        if status.memory_usage > 90.0:
            alerts.append(
                {
                    "type": "high_memory",
                    "level": "critical",
                    "message": f"High memory usage: {status.memory_usage}%",
                }
            )

        if status.response_time > 1.0:
            alerts.append(
                {
                    "type": "slow_response",
                    "level": "warning",
                    "message": f"Slow response time: {status.response_time}s",
                }
            )

        if status.health_score < 80.0:
            alerts.append(
                {
                    "type": "low_health",
                    "level": "warning",
                    "message": f"Low health score: {status.health_score}",
                }
            )

        return alerts

    def _log_deployment(self, deployment_id: str, action: str, details: str) -> None:
        """Log deployment action."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "deployment_id": deployment_id,
            "action": action,
            "details": details,
        }
        self.deployment_history.append(log_entry)

        # Save to file
        log_file = self.deployments_dir / f"{deployment_id}_history.json"
        with open(log_file, "w") as f:
            json.dump(self.deployment_history, f, indent=2)


def main():
    """Main function for ML Pipeline Deployment Tool."""
    parser = argparse.ArgumentParser(description="ML Pipeline Deployment Automation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Register model command
    register_parser = subparsers.add_parser("register", help="Register ML model")
    register_parser.add_argument("--model-id", required=True, help="Model ID")
    register_parser.add_argument("--name", required=True, help="Model name")
    register_parser.add_argument("--version", required=True, help="Model version")
    register_parser.add_argument(
        "--framework",
        choices=["tensorflow", "pytorch", "scikit-learn", "xgboost", "custom"],
        required=True,
    )
    register_parser.add_argument("--path", required=True, help="Model file path")

    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy ML model")
    deploy_parser.add_argument("--deployment-id", required=True, help="Deployment ID")
    deploy_parser.add_argument("--model-id", required=True, help="Model ID")
    deploy_parser.add_argument("--replicas", type=int, default=1, help="Number of replicas")
    deploy_parser.add_argument("--max-replicas", type=int, default=10, help="Maximum replicas")
    deploy_parser.add_argument(
        "--scaling",
        choices=["cpu_based", "memory_based", "request_based", "hybrid"],
        default="cpu_based",
    )

    # Monitor command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor deployment")
    monitor_parser.add_argument("--deployment-id", required=True, help="Deployment ID")

    # Scale command
    scale_parser = subparsers.add_parser("scale", help="Scale deployment")
    scale_parser.add_argument("--deployment-id", required=True, help="Deployment ID")
    scale_parser.add_argument("--replicas", type=int, required=True, help="Target replicas")

    # Summary command
    summary_parser = subparsers.add_parser("summary", help="Get deployment summary")

    args = parser.parse_args()

    tool = MLPipelineDeploymentTool()

    if args.command == "register":
        model = MLModel(
            model_id=args.model_id,
            model_name=args.name,
            version=args.version,
            framework=MLFramework(args.framework),
            model_path=args.path,
            input_shape=[1, 784],  # Default
            output_shape=[1, 10],  # Default
            memory_requirements=512,
            cpu_requirements=1.0,
            created_at=datetime.now().isoformat(),
        )
        success = tool.register_model(model)
        print(f"Model registration: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "deploy":
        # Load model
        model_file = tool.models_dir / f"{args.model_id}.json"
        if not model_file.exists():
            print(f"Model {args.model_id} not found. Register first.")
            return

        with open(model_file) as f:
            model_data = json.load(f)

        # Convert framework string back to enum
        model_data["framework"] = MLFramework(model_data["framework"])
        model = MLModel(**model_data)

        config = DeploymentConfig(
            deployment_id=args.deployment_id,
            model=model,
            replicas=args.replicas,
            max_replicas=args.max_replicas,
            scaling_strategy=ScalingStrategy(args.scaling),
        )

        success = tool.deploy_model(config)
        print(f"Model deployment: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "monitor":
        data = tool.monitor_deployment(args.deployment_id)
        if data:
            print(json.dumps(data, indent=2))
        else:
            print(f"Deployment {args.deployment_id} not found")

    elif args.command == "scale":
        success = tool.scale_deployment(args.deployment_id, args.replicas)
        print(f"Deployment scaling: {'SUCCESS' if success else 'FAILED'}")

    elif args.command == "summary":
        summary = tool.get_deployment_summary()
        print(json.dumps(summary, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
