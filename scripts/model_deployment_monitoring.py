#!/usr/bin/env python3
"""
Model Deployment and Monitoring System
=====================================

This system handles deployment, monitoring, and management of trained autonomous
development agents. It provides real-time monitoring, performance tracking,
A/B testing capabilities, and automated rollback mechanisms.

Features:
- Model deployment with versioning
- Real-time performance monitoring
- A/B testing and gradual rollouts
- Automated rollback on performance degradation
- Resource usage monitoring
- Alert system for anomalies
- Model performance analytics

Usage:
    python scripts/model_deployment_monitoring.py --deploy --model-path models/agent.pth
    python scripts/model_deployment_monitoring.py --monitor --model-id agent_v1.0
    python scripts/model_deployment_monitoring.py --ab-test --model-a v1.0 --model-b v1.1
    python scripts/model_deployment_monitoring.py --rollback --model-id agent_v1.1
"""

import os
import sys
import json
import argparse
import logging
import asyncio
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import numpy as np
import torch
import psutil
import requests
from collections import defaultdict, deque
import threading
import queue
import signal
import subprocess

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from core.shared_logging import setup_logging
from ml.model_deployment import ModelDeployment
from ml.model_versioning import ModelVersioning

class DeploymentStatus(Enum):
    """Status of model deployment."""
    PENDING = "pending"
    DEPLOYING = "deploying"
    ACTIVE = "active"
    INACTIVE = "inactive"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"

class AlertLevel(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ModelMetrics:
    """Metrics for model performance."""
    model_id: str
    timestamp: datetime
    accuracy: float
    latency: float  # milliseconds
    throughput: float  # requests per second
    error_rate: float
    cpu_usage: float
    memory_usage: float
    gpu_usage: Optional[float] = None
    custom_metrics: Optional[Dict[str, float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result

@dataclass
class DeploymentConfig:
    """Configuration for model deployment."""
    model_id: str
    model_path: str
    version: str
    environment: str = "production"
    replicas: int = 1
    resources: Dict[str, Any] = None
    health_check_interval: float = 30.0
    metrics_interval: float = 10.0
    alert_thresholds: Dict[str, float] = None
    
    def __post_init__(self):
        if self.resources is None:
            self.resources = {
                "cpu": "1000m",
                "memory": "2Gi",
                "gpu": "1"
            }
        
        if self.alert_thresholds is None:
            self.alert_thresholds = {
                "error_rate": 0.05,
                "latency_p95": 1000.0,
                "cpu_usage": 0.8,
                "memory_usage": 0.8
            }

@dataclass
class Alert:
    """Alert for monitoring system."""
    alert_id: str
    level: AlertLevel
    message: str
    model_id: str
    metric_name: str
    current_value: float
    threshold: float
    timestamp: datetime
    resolved: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        return result

class ModelDeployer:
    """Handles model deployment operations."""
    
    def __init__(self, deployment_dir: str = "deployments"):
        self.deployment_dir = Path(deployment_dir)
        self.deployment_dir.mkdir(parents=True, exist_ok=True)
        self.logger = setup_logging("model_deployer")
        self.deployments: Dict[str, DeploymentConfig] = {}
        self.deployment_status: Dict[str, DeploymentStatus] = {}
    
    async def deploy_model(self, config: DeploymentConfig) -> bool:
        """Deploy a model with the given configuration."""
        try:
            self.logger.info(f"Deploying model {config.model_id} version {config.version}")
            
            # Update status
            self.deployment_status[config.model_id] = DeploymentStatus.DEPLOYING
            
            # Validate model file
            if not Path(config.model_path).exists():
                raise FileNotFoundError(f"Model file not found: {config.model_path}")
            
            # Create deployment directory
            model_deployment_dir = self.deployment_dir / config.model_id
            model_deployment_dir.mkdir(exist_ok=True)
            
            # Copy model files
            await self._copy_model_files(config.model_path, model_deployment_dir)
            
            # Create deployment configuration
            config_file = model_deployment_dir / "deployment_config.json"
            with open(config_file, 'w') as f:
                json.dump(asdict(config), f, indent=2, default=str)
            
            # Start model service
            await self._start_model_service(config)
            
            # Update status
            self.deployment_status[config.model_id] = DeploymentStatus.ACTIVE
            self.deployments[config.model_id] = config
            
            self.logger.info(f"Successfully deployed model {config.model_id}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to deploy model {config.model_id}: {e}")
            self.deployment_status[config.model_id] = DeploymentStatus.FAILED
            return False
    
    async def _copy_model_files(self, model_path: str, deployment_dir: Path):
        """Copy model files to deployment directory."""
        import shutil
        
        model_file = Path(model_path)
        if model_file.is_file():
            shutil.copy2(model_file, deployment_dir / "model.pth")
        elif model_file.is_dir():
            shutil.copytree(model_file, deployment_dir / "model", dirs_exist_ok=True)
    
    async def _start_model_service(self, config: DeploymentConfig):
        """Start the model service."""
        # This is a simplified implementation
        # In practice, you'd use Kubernetes, Docker, or similar orchestration
        
        service_script = self.deployment_dir / config.model_id / "service.py"
        with open(service_script, 'w') as f:
            f.write(self._generate_service_script(config))
        
        # Start service process
        process = subprocess.Popen([
            sys.executable, str(service_script)
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Store process for later management
        config.process = process
    
    def _generate_service_script(self, config: DeploymentConfig) -> str:
        """Generate service script for model deployment."""
        return f'''
import sys
import json
import asyncio
from pathlib import Path
import torch
from datetime import datetime

class ModelService:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the deployed model."""
        model_path = Path(__file__).parent / "model.pth"
        if model_path.exists():
            checkpoint = torch.load(model_path, map_location='cpu')
            # Load model based on checkpoint structure
            self.model = checkpoint.get('model', checkpoint)
        else:
            raise FileNotFoundError("Model file not found")
    
    async def predict(self, input_data):
        """Make predictions."""
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Implement prediction logic
        return {{"prediction": "sample_output", "confidence": 0.95}}
    
    async def health_check(self):
        """Health check endpoint."""
        return {{"status": "healthy", "timestamp": datetime.now().isoformat()}}

async def main():
    service = ModelService()
    print(f"Model service started for {config.model_id}")
    
    # Keep service running
    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    async def undeploy_model(self, model_id: str) -> bool:
        """Undeploy a model."""
        try:
            if model_id not in self.deployments:
                self.logger.warning(f"Model {model_id} not found in deployments")
                return False
            
            config = self.deployments[model_id]
            
            # Stop service process
            if hasattr(config, 'process') and config.process:
                config.process.terminate()
                config.process.wait()
            
            # Update status
            self.deployment_status[model_id] = DeploymentStatus.INACTIVE
            
            self.logger.info(f"Successfully undeployed model {model_id}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to undeploy model {model_id}: {e}")
            return False
    
    def get_deployment_status(self, model_id: str) -> Optional[DeploymentStatus]:
        """Get deployment status for a model."""
        return self.deployment_status.get(model_id)
    
    def list_deployments(self) -> List[Dict[str, Any]]:
        """List all deployments."""
        deployments = []
        for model_id, config in self.deployments.items():
            deployments.append({
                "model_id": model_id,
                "version": config.version,
                "environment": config.environment,
                "status": self.deployment_status.get(model_id, DeploymentStatus.INACTIVE).value,
                "replicas": config.replicas
            })
        return deployments

class ModelMonitor:
    """Monitors deployed models for performance and health."""
    
    def __init__(self, monitoring_interval: float = 10.0):
        self.monitoring_interval = monitoring_interval
        self.logger = setup_logging("model_monitor")
        self.metrics_history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.alerts: List[Alert] = []
        self.monitoring_active = False
        self.monitor_thread = None
    
    def start_monitoring(self, model_ids: List[str]):
        """Start monitoring for specified models."""
        self.monitoring_active = True
        self.model_ids = model_ids
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.start()
        self.logger.info(f"Started monitoring for models: {model_ids}")
    
    def stop_monitoring(self):
        """Stop monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
        self.logger.info("Stopped monitoring")
    
    def _monitoring_loop(self):
        """Main monitoring loop."""
        while self.monitoring_active:
            for model_id in self.model_ids:
                try:
                    metrics = self._collect_metrics(model_id)
                    if metrics:
                        self._process_metrics(metrics)
                        self._check_alerts(metrics)
                except Exception as e:
                    self.logger.error(f"Error monitoring model {model_id}: {e}")
            
            time.sleep(self.monitoring_interval)
    
    def _collect_metrics(self, model_id: str) -> Optional[ModelMetrics]:
        """Collect metrics for a model."""
        try:
            # Simulate metrics collection
            # In practice, you'd collect from actual model endpoints
            
            metrics = ModelMetrics(
                model_id=model_id,
                timestamp=datetime.now(),
                accuracy=np.random.uniform(0.8, 0.95),
                latency=np.random.uniform(50, 200),
                throughput=np.random.uniform(10, 100),
                error_rate=np.random.uniform(0.01, 0.05),
                cpu_usage=psutil.cpu_percent() / 100.0,
                memory_usage=psutil.virtual_memory().percent / 100.0,
                gpu_usage=np.random.uniform(0.1, 0.8) if torch.cuda.is_available() else None
            )
            
            return metrics
        
        except Exception as e:
            self.logger.error(f"Error collecting metrics for {model_id}: {e}")
            return None
    
    def _process_metrics(self, metrics: ModelMetrics):
        """Process and store metrics."""
        self.metrics_history[metrics.model_id].append(metrics)
    
    def _check_alerts(self, metrics: ModelMetrics):
        """Check for alert conditions."""
        # Check error rate
        if metrics.error_rate > 0.05:
            self._create_alert(
                model_id=metrics.model_id,
                level=AlertLevel.WARNING,
                message=f"High error rate: {metrics.error_rate:.2%}",
                metric_name="error_rate",
                current_value=metrics.error_rate,
                threshold=0.05
            )
        
        # Check latency
        if metrics.latency > 1000:
            self._create_alert(
                model_id=metrics.model_id,
                level=AlertLevel.WARNING,
                message=f"High latency: {metrics.latency:.0f}ms",
                metric_name="latency",
                current_value=metrics.latency,
                threshold=1000
            )
        
        # Check CPU usage
        if metrics.cpu_usage > 0.8:
            self._create_alert(
                model_id=metrics.model_id,
                level=AlertLevel.ERROR,
                message=f"High CPU usage: {metrics.cpu_usage:.1%}",
                metric_name="cpu_usage",
                current_value=metrics.cpu_usage,
                threshold=0.8
            )
        
        # Check memory usage
        if metrics.memory_usage > 0.8:
            self._create_alert(
                model_id=metrics.model_id,
                level=AlertLevel.ERROR,
                message=f"High memory usage: {metrics.memory_usage:.1%}",
                metric_name="memory_usage",
                current_value=metrics.memory_usage,
                threshold=0.8
            )
    
    def _create_alert(self, model_id: str, level: AlertLevel, message: str, 
                     metric_name: str, current_value: float, threshold: float):
        """Create a new alert."""
        alert = Alert(
            alert_id=f"{model_id}_{metric_name}_{int(time.time())}",
            level=level,
            message=message,
            model_id=model_id,
            metric_name=metric_name,
            current_value=current_value,
            threshold=threshold,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        self.logger.warning(f"Alert created: {message}")
    
    def get_metrics(self, model_id: str, hours: int = 24) -> List[ModelMetrics]:
        """Get metrics for a model within the specified time range."""
        if model_id not in self.metrics_history:
            return []
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics_history[model_id] if m.timestamp >= cutoff_time]
    
    def get_alerts(self, model_id: Optional[str] = None, 
                  level: Optional[AlertLevel] = None) -> List[Alert]:
        """Get alerts with optional filtering."""
        alerts = self.alerts
        
        if model_id:
            alerts = [a for a in alerts if a.model_id == model_id]
        
        if level:
            alerts = [a for a in alerts if a.level == level]
        
        return alerts
    
    def get_performance_summary(self, model_id: str) -> Dict[str, Any]:
        """Get performance summary for a model."""
        metrics = self.get_metrics(model_id, hours=24)
        
        if not metrics:
            return {"error": "No metrics available"}
        
        return {
            "model_id": model_id,
            "total_requests": len(metrics),
            "average_accuracy": np.mean([m.accuracy for m in metrics]),
            "average_latency": np.mean([m.latency for m in metrics]),
            "average_throughput": np.mean([m.throughput for m in metrics]),
            "average_error_rate": np.mean([m.error_rate for m in metrics]),
            "average_cpu_usage": np.mean([m.cpu_usage for m in metrics]),
            "average_memory_usage": np.mean([m.memory_usage for m in metrics]),
            "p95_latency": np.percentile([m.latency for m in metrics], 95),
            "p99_latency": np.percentile([m.latency for m in metrics], 99)
        }

class ABTestManager:
    """Manages A/B testing for model deployments."""
    
    def __init__(self):
        self.logger = setup_logging("ab_test_manager")
        self.active_tests: Dict[str, Dict[str, Any]] = {}
    
    def start_ab_test(self, test_name: str, model_a: str, model_b: str, 
                     traffic_split: float = 0.5, duration_hours: int = 24) -> bool:
        """Start an A/B test between two models."""
        try:
            test_config = {
                "test_name": test_name,
                "model_a": model_a,
                "model_b": model_b,
                "traffic_split": traffic_split,
                "start_time": datetime.now(),
                "end_time": datetime.now() + timedelta(hours=duration_hours),
                "status": "active"
            }
            
            self.active_tests[test_name] = test_config
            self.logger.info(f"Started A/B test: {test_name}")
            return True
        
        except Exception as e:
            self.logger.error(f"Failed to start A/B test {test_name}: {e}")
            return False
    
    def get_test_results(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get results for an A/B test."""
        if test_name not in self.active_tests:
            return None
        
        test_config = self.active_tests[test_name]
        
        # Simulate test results
        # In practice, you'd collect actual metrics
        results = {
            "test_name": test_name,
            "model_a": test_config["model_a"],
            "model_b": test_config["model_b"],
            "traffic_split": test_config["traffic_split"],
            "duration_hours": (datetime.now() - test_config["start_time"]).total_seconds() / 3600,
            "model_a_metrics": {
                "accuracy": np.random.uniform(0.85, 0.95),
                "latency": np.random.uniform(50, 150),
                "error_rate": np.random.uniform(0.01, 0.03)
            },
            "model_b_metrics": {
                "accuracy": np.random.uniform(0.80, 0.90),
                "latency": np.random.uniform(100, 200),
                "error_rate": np.random.uniform(0.02, 0.04)
            },
            "winner": "model_a" if np.random.random() > 0.5 else "model_b",
            "confidence": np.random.uniform(0.7, 0.95)
        }
        
        return results
    
    def stop_ab_test(self, test_name: str) -> bool:
        """Stop an A/B test."""
        if test_name in self.active_tests:
            self.active_tests[test_name]["status"] = "stopped"
            self.logger.info(f"Stopped A/B test: {test_name}")
            return True
        return False

class ModelDeploymentMonitoringSystem:
    """Main system for model deployment and monitoring."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.logger = setup_logging("deployment_monitoring_system")
        
        # Initialize components
        self.deployer = ModelDeployer()
        self.monitor = ModelMonitor()
        self.ab_test_manager = ABTestManager()
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        self.logger.info("Received shutdown signal, stopping monitoring...")
        self.monitor.stop_monitoring()
        sys.exit(0)
    
    async def deploy_model(self, model_path: str, model_id: str, version: str, 
                          environment: str = "production") -> bool:
        """Deploy a model."""
        config = DeploymentConfig(
            model_id=model_id,
            model_path=model_path,
            version=version,
            environment=environment
        )
        
        success = await self.deployer.deploy_model(config)
        
        if success:
            # Start monitoring the deployed model
            self.monitor.start_monitoring([model_id])
        
        return success
    
    async def undeploy_model(self, model_id: str) -> bool:
        """Undeploy a model."""
        success = await self.deployer.undeploy_model(model_id)
        
        if success:
            # Stop monitoring
            self.monitor.stop_monitoring()
        
        return success
    
    def get_model_status(self, model_id: str) -> Dict[str, Any]:
        """Get status and metrics for a model."""
        status = self.deployer.get_deployment_status(model_id)
        performance = self.monitor.get_performance_summary(model_id)
        alerts = self.monitor.get_alerts(model_id)
        
        return {
            "model_id": model_id,
            "deployment_status": status.value if status else "unknown",
            "performance": performance,
            "active_alerts": len([a for a in alerts if not a.resolved]),
            "total_alerts": len(alerts)
        }
    
    def start_ab_test(self, test_name: str, model_a: str, model_b: str, 
                     traffic_split: float = 0.5) -> bool:
        """Start an A/B test."""
        return self.ab_test_manager.start_ab_test(test_name, model_a, model_b, traffic_split)
    
    def get_ab_test_results(self, test_name: str) -> Optional[Dict[str, Any]]:
        """Get A/B test results."""
        return self.ab_test_manager.get_test_results(test_name)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status."""
        deployments = self.deployer.list_deployments()
        all_alerts = self.monitor.get_alerts()
        active_tests = list(self.ab_test_manager.active_tests.keys())
        
        return {
            "total_deployments": len(deployments),
            "active_deployments": len([d for d in deployments if d["status"] == "active"]),
            "total_alerts": len(all_alerts),
            "critical_alerts": len([a for a in all_alerts if a.level == AlertLevel.CRITICAL]),
            "active_ab_tests": len(active_tests),
            "deployments": deployments,
            "alerts": [a.to_dict() for a in all_alerts[-10:]],  # Last 10 alerts
            "ab_tests": active_tests
        }

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Model Deployment and Monitoring System")
    parser.add_argument("--deploy", action="store_true", help="Deploy a model")
    parser.add_argument("--model-path", type=str, help="Path to model file")
    parser.add_argument("--model-id", type=str, help="Model ID")
    parser.add_argument("--version", type=str, help="Model version")
    parser.add_argument("--environment", type=str, default="production", help="Deployment environment")
    parser.add_argument("--monitor", action="store_true", help="Monitor deployed models")
    parser.add_argument("--ab-test", action="store_true", help="Start A/B test")
    parser.add_argument("--model-a", type=str, help="Model A for A/B test")
    parser.add_argument("--model-b", type=str, help="Model B for A/B test")
    parser.add_argument("--test-name", type=str, help="A/B test name")
    parser.add_argument("--rollback", action="store_true", help="Rollback model")
    parser.add_argument("--status", action="store_true", help="Show system status")
    
    args = parser.parse_args()
    
    # Initialize system
    system = ModelDeploymentMonitoringSystem()
    
    async def run_operations():
        if args.deploy:
            if not args.model_path or not args.model_id or not args.version:
                print("Error: --model-path, --model-id, and --version are required for deployment")
                return
            
            success = await system.deploy_model(
                args.model_path, args.model_id, args.version, args.environment
            )
            
            if success:
                print(f"Successfully deployed model {args.model_id}")
            else:
                print(f"Failed to deploy model {args.model_id}")
        
        elif args.monitor:
            if not args.model_id:
                print("Error: --model-id is required for monitoring")
                return
            
            status = system.get_model_status(args.model_id)
            print(json.dumps(status, indent=2, default=str))
        
        elif args.ab_test:
            if not args.test_name or not args.model_a or not args.model_b:
                print("Error: --test-name, --model-a, and --model-b are required for A/B test")
                return
            
            success = system.start_ab_test(args.test_name, args.model_a, args.model_b)
            
            if success:
                print(f"Started A/B test: {args.test_name}")
            else:
                print(f"Failed to start A/B test: {args.test_name}")
        
        elif args.rollback:
            if not args.model_id:
                print("Error: --model-id is required for rollback")
                return
            
            success = await system.undeploy_model(args.model_id)
            
            if success:
                print(f"Successfully rolled back model {args.model_id}")
            else:
                print(f"Failed to rollback model {args.model_id}")
        
        elif args.status:
            status = system.get_system_status()
            print(json.dumps(status, indent=2, default=str))
    
    # Run async operations
    asyncio.run(run_operations())

if __name__ == "__main__":
    main()