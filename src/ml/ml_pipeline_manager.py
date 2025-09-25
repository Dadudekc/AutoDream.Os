#!/usr/bin/env python3
"""
ML Pipeline Manager - V2-Compliant Module
=========================================

ML pipeline orchestration and management functionality.
File size: ≤200 lines, Classes: ≤5, Functions: ≤10
"""

import sys
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Union

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from .ml_pipeline_core_refactored import MLPipelineCore
from .ml_pipeline_models import ModelConfig, TrainingData
from .ml_pipeline_utils import DataProcessor, ModelValidator

logger = logging.getLogger(__name__)


class MLPipelineManager:
    """ML pipeline orchestration and management."""

    def __init__(self, config: Optional[ModelConfig] = None):
        """Initialize ML pipeline manager."""
        self.config = config or ModelConfig()
        self.core = MLPipelineCore(self.config)
        self.data_processor = DataProcessor()
        self.model_validator = ModelValidator()
        self.pipeline_status = "initialized"
        
        logger.info("ML Pipeline Manager initialized")

    def run_complete_pipeline(self, 
                            data_config: Dict[str, Any],
                            model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Run complete ML pipeline from data creation to evaluation."""
        try:
            logger.info("Starting complete ML pipeline...")
            
            # Create training data
            training_data = self._create_training_data(data_config)
            if not training_data:
                return {"status": "failed", "error": "Failed to create training data"}
            
            # Create and train model
            model_name = model_config.get("name", "default_model")
            model_type = model_config.get("type", "neural_network")
            
            model = self.core.create_model(model_name, model_type)
            if not model:
                return {"status": "failed", "error": "Failed to create model"}
            
            # Train model
            training_results = self.core.train_model(
                model_name, training_data,
                epochs=model_config.get("epochs"),
                batch_size=model_config.get("batch_size")
            )
            
            if training_results.get("status") != "completed":
                return {"status": "failed", "error": "Model training failed"}
            
            # Evaluate model
            evaluation_results = self.core.evaluate_model(model_name, training_data)
            if evaluation_results.get("status") != "completed":
                return {"status": "failed", "error": "Model evaluation failed"}
            
            # Validate results
            validation_results = self.model_validator.validate_results(
                training_results, evaluation_results
            )
            
            self.pipeline_status = "completed"
            return {
                "status": "completed", "model_name": model_name,
                "training_results": training_results,
                "evaluation_results": evaluation_results,
                "validation_results": validation_results
            }
            
        except Exception as e:
            logger.error(f"Error in complete pipeline: {e}")
            self.pipeline_status = "failed"
            return {"status": "failed", "error": str(e)}

    def _create_training_data(self, data_config: Dict[str, Any]) -> Optional[TrainingData]:
        """Create training data based on configuration."""
        try:
            return self.core.create_training_data(
                num_samples=data_config.get("num_samples", 1000),
                num_features=data_config.get("num_features", 10),
                num_classes=data_config.get("num_classes", 3),
                data_type=data_config.get("data_type", "classification")
            )
        except Exception as e:
            logger.error(f"Error creating training data: {e}")
            return None

    def batch_train_models(self, 
                          models_config: List[Dict[str, Any]],
                          shared_data_config: Dict[str, Any]) -> Dict[str, Any]:
        """Train multiple models with shared data configuration."""
        try:
            logger.info(f"Starting batch training for {len(models_config)} models...")
            
            # Create shared training data
            training_data = self._create_training_data(shared_data_config)
            if not training_data:
                return {"status": "failed", "error": "Failed to create shared training data"}
            
            results = {}
            for model_config in models_config:
                model_name = model_config.get("name", f"model_{len(results)}")
                try:
                    model = self.core.create_model(model_name, model_config.get("type", "neural_network"))
                    training_results = self.core.train_model(model_name, training_data,
                                                           epochs=model_config.get("epochs"),
                                                           batch_size=model_config.get("batch_size"))
                    evaluation_results = self.core.evaluate_model(model_name, training_data)
                    results[model_name] = {
                        "training": training_results, "evaluation": evaluation_results,
                        "status": "completed" if training_results.get("status") == "completed" else "failed"
                    }
                except Exception as e:
                    logger.error(f"Error training model {model_name}: {e}")
                    results[model_name] = {"status": "failed", "error": str(e)}
            
            successful_models = sum(1 for r in results.values() if r.get("status") == "completed")
            return {
                "status": "completed", "total_models": len(models_config),
                "successful_models": successful_models, "results": results
            }
        except Exception as e:
            logger.error(f"Error in batch training: {e}")
            return {"status": "failed", "error": str(e)}

    def compare_models(self, model_names: List[str]) -> Dict[str, Any]:
        """Compare performance of multiple models."""
        try:
            logger.info(f"Comparing models: {model_names}")
            comparison_results = {}
            for model_name in model_names:
                if model_name not in self.core.models:
                    comparison_results[model_name] = {"error": "Model not found"}
                    continue
                model_info = self.core.get_model_info(model_name)
                metrics = self.core.model_metrics.get(model_name)
                comparison_results[model_name] = {
                    "info": model_info,
                    "metrics": metrics.to_dict() if metrics else None
                }
            return {"status": "completed", "comparison_results": comparison_results}
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return {"status": "failed", "error": str(e)}

    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status."""
        return {
            "pipeline_status": self.pipeline_status,
            "core_status": self.core.get_status(),
            "models_count": len(self.core.models),
            "config": self.config.__dict__ if hasattr(self.config, '__dict__') else str(self.config)
        }

    def reset_pipeline(self) -> bool:
        """Reset pipeline to initial state."""
        try:
            logger.info("Resetting pipeline...")
            self.core = MLPipelineCore(self.config)
            self.pipeline_status = "initialized"
            logger.info("Pipeline reset successfully")
            return True
        except Exception as e:
            logger.error(f"Error resetting pipeline: {e}")
            return False

    def export_results(self, output_path: str) -> bool:
        """Export pipeline results to file."""
        try:
            logger.info(f"Exporting results to: {output_path}")
            results = {
                "pipeline_status": self.get_pipeline_status(),
                "models": {name: self.core.get_model_info(name) for name in self.core.list_models()},
                "metrics": {name: metrics.to_dict() for name, metrics in self.core.model_metrics.items()}
            }
            with open(output_path, 'w') as f:
                f.write(str(results))
            logger.info("Results exported successfully")
            return True
        except Exception as e:
            logger.error(f"Error exporting results: {e}")
            return False