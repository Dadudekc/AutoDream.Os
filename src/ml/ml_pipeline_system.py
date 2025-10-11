#!/usr/bin/env python3
"""
ML Pipeline System
=================

Main ML pipeline system interface.
"""

import sys
import logging
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .ml_pipeline_models import ModelConfig, TrainingData, DeploymentConfig
from .ml_pipeline_core import MLPipelineCore

logger = logging.getLogger(__name__)


class MLPipelineSystem:
    """Main ML pipeline system interface."""
    
    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize ML pipeline system."""
        self.config = config or ModelConfig()
        self.core = MLPipelineCore(self.config)
        self.deployment_configs: Dict[str, DeploymentConfig] = {}
        
        logger.info("ML Pipeline System initialized")
    
    def deploy_model(self, model_name: str, version: Optional[str] = None) -> Dict[str, Any]:
        """Deploy a model."""
        try:
            logger.info(f"Deploying model: {model_name}")
            
            if model_name not in self.core.models:
                raise ValueError(f"Model {model_name} not found")
            
            version = version or "1.0.0"
            
            # Create deployment configuration
            deployment_config = DeploymentConfig(
                version=version,
                environment="production"
            )
            
            self.deployment_configs[f"{model_name}_{version}"] = deployment_config
            
            # Simulate deployment process
            deployment_results = {
                "status": "deployed",
                "model_name": model_name,
                "version": version,
                "deployment_type": deployment_config.deployment_type,
                "endpoint": f"/api/v1/models/{model_name}/{version}/predict",
                "health_check": f"/api/v1/models/{model_name}/{version}/health",
                "deployment_time": datetime.now().isoformat()
            }
            
            logger.info(f"Model {model_name} deployed successfully")
            return deployment_results
            
        except Exception as e:
            logger.error(f"Error deploying model {model_name}: {e}")
            return {"status": "failed", "error": str(e)}
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status."""
        try:
            status = {
                "system_status": "operational",
                "models_count": len(self.core.models),
                "training_data_count": len(self.core.training_data),
                "deployments_count": len(self.deployment_configs),
                "config": {
                    "framework": self.config.framework,
                    "model_type": self.config.model_type,
                    "input_shape": self.config.input_shape,
                    "num_classes": self.config.num_classes
                },
                "models": list(self.core.models.keys()),
                "deployments": list(self.deployment_configs.keys()),
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("System status retrieved successfully")
            return status
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"system_status": "error", "error": str(e)}
    
    def export_system_data(self, output_file: Optional[str] = None) -> str:
        """Export system data."""
        try:
            if output_file is None:
                output_file = f"ml_pipeline_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            export_data = {
                "export_timestamp": datetime.now().isoformat(),
                "system_status": self.get_system_status(),
                "config": {
                    "framework": self.config.framework,
                    "model_type": self.config.model_type,
                    "input_shape": self.config.input_shape,
                    "num_classes": self.config.num_classes,
                    "learning_rate": self.config.learning_rate,
                    "batch_size": self.config.batch_size,
                    "epochs": self.config.epochs
                },
                "models": {},
                "training_data": {},
                "deployments": {}
            }
            
            # Export model information
            for model_name, model in self.core.models.items():
                export_data["models"][model_name] = {
                    "type": type(model).__name__,
                    "trained": hasattr(model, 'is_trained') and model.is_trained
                }
            
            # Export training data information
            for data_name, data in self.core.training_data.items():
                export_data["training_data"][data_name] = {
                    "samples": len(data.features),
                    "features": data.features.shape[1] if len(data.features.shape) > 1 else 1,
                    "has_validation": data.validation_features is not None,
                    "has_test": data.test_features is not None
                }
            
            # Export deployment information
            for deployment_name, config in self.deployment_configs.items():
                export_data["deployments"][deployment_name] = {
                    "version": config.version,
                    "environment": config.environment,
                    "deployment_type": config.deployment_type
                }
            
            # Write to file
            with open(output_file, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            logger.info(f"System data exported to {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Error exporting system data: {e}")
            raise
    
    # Delegate core methods
    def create_training_data(self, **kwargs):
        """Create training data."""
        return self.core.create_training_data(**kwargs)
    
    def create_model(self, model_name: str, model_type: str = "neural_network"):
        """Create a model."""
        return self.core.create_model(model_name, model_type)
    
    def train_model(self, model_name: str, training_data: TrainingData, **kwargs):
        """Train a model."""
        return self.core.train_model(model_name, training_data, **kwargs)
    
    def evaluate_model(self, model_name: str, test_data: TrainingData):
        """Evaluate a model."""
        return self.core.evaluate_model(model_name, test_data)


def create_ml_pipeline(config: Optional[ModelConfig] = None) -> MLPipelineSystem:
    """Create a new ML pipeline system."""
    return MLPipelineSystem(config)