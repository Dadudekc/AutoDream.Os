"""
ML Robot Maker Module
Agent-2: AI & ML Framework Integration
TDD Integration Project - Agent_Cellphone_V2_Repository

Intelligent system for automatically creating, training, and managing ML models
"""

import os
import json
import logging
import warnings
from typing import Dict, List, Optional, Any, Union, Tuple, Callable
from pathlib import Path
from datetime import datetime, timedelta
import asyncio
import numpy as np
from dataclasses import dataclass, field

# Import required modules
from .core import MLFramework, ModelManager, WorkflowAutomation
from .ml_frameworks import MLFrameworkManager
from .integrations import OpenAIIntegration, AnthropicIntegration
from .utils import config_loader, logger_setup, performance_monitor

logger = logging.getLogger(__name__)

@dataclass
class MLTask:
    """Represents an ML task to be executed"""
    task_id: str
    task_type: str  # 'classification', 'regression', 'clustering', 'custom'
    description: str
    dataset_info: Dict[str, Any]
    model_requirements: Dict[str, Any]
    framework_preference: Optional[str] = None
    hyperparameter_tuning: bool = True
    cross_validation: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "pending"
    priority: int = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "description": self.description,
            "dataset_info": self.dataset_info,
            "model_requirements": self.model_requirements,
            "framework_preference": self.framework_preference,
            "hyperparameter_tuning": self.hyperparameter_tuning,
            "cross_validation": self.cross_validation,
            "created_at": self.created_at.isoformat(),
            "status": self.status,
            "priority": self.priority
        }

@dataclass
class MLModelBlueprint:
    """Blueprint for creating ML models"""
    name: str
    framework: str
    architecture: Dict[str, Any]
    hyperparameters: Dict[str, Any]
    training_config: Dict[str, Any]
    evaluation_metrics: List[str]
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "name": self.name,
            "framework": self.framework,
            "architecture": self.architecture,
            "hyperparameters": self.hyperparameters,
            "training_config": self.training_config,
            "evaluation_metrics": self.evaluation_metrics,
            "created_at": self.created_at.isoformat()
        }

@dataclass
class MLExperiment:
    """Represents an ML experiment"""
    experiment_id: str
    task: MLTask
    blueprint: MLModelBlueprint
    model: Any
    training_results: Dict[str, Any]
    evaluation_results: Dict[str, Any]
    model_path: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "experiment_id": self.experiment_id,
            "task": self.task.to_dict(),
            "blueprint": self.blueprint.to_dict(),
            "training_results": self.training_results,
            "evaluation_results": self.evaluation_results,
            "model_path": self.model_path,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }

class MLRobotMaker:
    """Intelligent system for automatically creating and managing ML models"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = config_loader(config_path or "config/ai_ml/ai_ml_config.json")
        self.logger = logger_setup("ml_robot_maker", self.config.get("environment", {}).get("log_level", "INFO"))
        
        # Initialize components
        self.framework_manager = MLFrameworkManager(self.config)
        self.model_manager = ModelManager(self.config.get("model_management", {}).get("model_registry", "models/"))
        self.workflow_automation = WorkflowAutomation(None, self.model_manager)  # Will be updated
        
        # AI integrations for intelligent decision making
        self.openai_integration = None
        self.anthropic_integration = None
        self._setup_ai_integrations()
        
        # Task and experiment management
        self.tasks: Dict[str, MLTask] = {}
        self.experiments: Dict[str, MLExperiment] = {}
        self.blueprints: Dict[str, MLModelBlueprint] = {}
        
        # Performance monitoring
        self.performance_monitor = performance_monitor
        
        # Initialize frameworks
        self._initialize_frameworks()
        
        self.logger.info("ML Robot Maker initialized")
    
    def _setup_ai_integrations(self) -> None:
        """Setup AI integrations for intelligent decision making"""
        try:
            if self.config.get("ai_services", {}).get("openai", {}).get("enabled", False):
                self.openai_integration = OpenAIIntegration()
                self.logger.info("OpenAI integration enabled")
        except Exception as e:
            self.logger.warning(f"Failed to setup OpenAI integration: {e}")
        
        try:
            if self.config.get("ai_services", {}).get("anthropic", {}).get("enabled", False):
                self.anthropic_integration = AnthropicIntegration()
                self.logger.info("Anthropic integration enabled")
        except Exception as e:
            self.logger.warning(f"Failed to setup Anthropic integration: {e}")
    
    def _initialize_frameworks(self) -> None:
        """Initialize ML frameworks"""
        try:
            init_results = self.framework_manager.initialize_all_frameworks()
            self.logger.info(f"Framework initialization results: {init_results}")
        except Exception as e:
            self.logger.error(f"Failed to initialize frameworks: {e}")
    
    def create_task(self, task_type: str, description: str, dataset_info: Dict[str, Any], 
                   model_requirements: Dict[str, Any], **kwargs) -> MLTask:
        """Create a new ML task"""
        try:
            task_id = f"task_{len(self.tasks) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            task = MLTask(
                task_id=task_id,
                task_type=task_type,
                description=description,
                dataset_info=dataset_info,
                model_requirements=model_requirements,
                framework_preference=kwargs.get("framework_preference"),
                hyperparameter_tuning=kwargs.get("hyperparameter_tuning", True),
                cross_validation=kwargs.get("cross_validation", True),
                priority=kwargs.get("priority", 1)
            )
            
            self.tasks[task_id] = task
            self.logger.info(f"Created ML task: {task_id}")
            
            return task
            
        except Exception as e:
            self.logger.error(f"Error creating ML task: {e}")
            raise
    
    def generate_model_blueprint(self, task: MLTask) -> MLModelBlueprint:
        """Generate an intelligent model blueprint using AI"""
        try:
            # Use AI to generate optimal model architecture
            blueprint_config = self._ai_generate_blueprint(task)
            
            # Create blueprint
            blueprint = MLModelBlueprint(
                name=f"blueprint_{task.task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                framework=blueprint_config["framework"],
                architecture=blueprint_config["architecture"],
                hyperparameters=blueprint_config["hyperparameters"],
                training_config=blueprint_config["training_config"],
                evaluation_metrics=blueprint_config["evaluation_metrics"]
            )
            
            self.blueprints[blueprint.name] = blueprint
            self.logger.info(f"Generated model blueprint: {blueprint.name}")
            
            return blueprint
            
        except Exception as e:
            self.logger.error(f"Error generating model blueprint: {e}")
            raise
    
    def _ai_generate_blueprint(self, task: MLTask) -> Dict[str, Any]:
        """Use AI to generate optimal model blueprint"""
        try:
            # Prepare prompt for AI
            prompt = self._create_blueprint_prompt(task)
            
            # Get AI response
            if self.openai_integration:
                response = self.openai_integration.generate_code(prompt)
            elif self.anthropic_integration:
                response = self.anthropic_integration.generate_code(prompt)
            else:
                # Fallback to rule-based blueprint generation
                return self._rule_based_blueprint_generation(task)
            
            # Parse AI response
            blueprint_config = self._parse_ai_blueprint_response(response, task)
            return blueprint_config
            
        except Exception as e:
            self.logger.warning(f"AI blueprint generation failed, using rule-based: {e}")
            return self._rule_based_blueprint_generation(task)
    
    def _create_blueprint_prompt(self, task: MLTask) -> str:
        """Create prompt for AI blueprint generation"""
        prompt = f"""
        Generate an optimal ML model blueprint for the following task:
        
        Task Type: {task.task_type}
        Description: {task.description}
        Dataset Info: {json.dumps(task.dataset_info, indent=2)}
        Model Requirements: {json.dumps(task.model_requirements, indent=2)}
        
        Please provide a JSON response with the following structure:
        {{
            "framework": "framework_name",
            "architecture": {{
                "type": "model_type",
                "parameters": {{}}
            }},
            "hyperparameters": {{
                "learning_rate": 0.001,
                "batch_size": 32,
                "epochs": 100
            }},
            "training_config": {{
                "optimizer": "adam",
                "loss_function": "cross_entropy",
                "validation_split": 0.2
            }},
            "evaluation_metrics": ["accuracy", "precision", "recall", "f1"]
        }}
        
        Consider the task type, dataset characteristics, and requirements when making recommendations.
        """
        return prompt
    
    def _parse_ai_blueprint_response(self, response: str, task: MLTask) -> Dict[str, Any]:
        """Parse AI response to extract blueprint configuration"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                blueprint_config = json.loads(json_match.group())
            else:
                raise ValueError("No JSON found in AI response")
            
            # Validate and sanitize configuration
            blueprint_config = self._validate_blueprint_config(blueprint_config, task)
            return blueprint_config
            
        except Exception as e:
            self.logger.warning(f"Failed to parse AI response: {e}")
            return self._rule_based_blueprint_generation(task)
    
    def _rule_based_blueprint_generation(self, task: MLTask) -> Dict[str, Any]:
        """Generate blueprint using rule-based approach"""
        task_type = task.task_type.lower()
        
        if task_type == "classification":
            return self._generate_classification_blueprint(task)
        elif task_type == "regression":
            return self._generate_regression_blueprint(task)
        elif task_type == "clustering":
            return self._generate_clustering_blueprint(task)
        else:
            return self._generate_default_blueprint(task)
    
    def _generate_classification_blueprint(self, task: MLTask) -> Dict[str, Any]:
        """Generate blueprint for classification tasks"""
        dataset_size = task.dataset_info.get("size", 1000)
        
        if dataset_size < 1000:
            framework = "scikit_learn"
            architecture = {
                "type": "random_forest",
                "parameters": {"n_estimators": 100, "max_depth": 10}
            }
        else:
            framework = "pytorch"
            architecture = {
                "type": "mlp",
                "parameters": {"layer_sizes": [784, 128, 64, 10], "activation": "relu"}
            }
        
        return {
            "framework": framework,
            "architecture": architecture,
            "hyperparameters": {
                "learning_rate": 0.001,
                "batch_size": 32,
                "epochs": 100
            },
            "training_config": {
                "optimizer": "adam",
                "loss_function": "cross_entropy",
                "validation_split": 0.2
            },
            "evaluation_metrics": ["accuracy", "precision", "recall", "f1"]
        }
    
    def _generate_regression_blueprint(self, task: MLTask) -> Dict[str, Any]:
        """Generate blueprint for regression tasks"""
        return {
            "framework": "scikit_learn",
            "architecture": {
                "type": "random_forest",
                "parameters": {"n_estimators": 100, "max_depth": 15}
            },
            "hyperparameters": {
                "learning_rate": 0.01,
                "batch_size": 32,
                "epochs": 100
            },
            "training_config": {
                "optimizer": "adam",
                "loss_function": "mse",
                "validation_split": 0.2
            },
            "evaluation_metrics": ["mse", "mae", "r2_score"]
        }
    
    def _generate_clustering_blueprint(self, task: MLTask) -> Dict[str, Any]:
        """Generate blueprint for clustering tasks"""
        return {
            "framework": "scikit_learn",
            "architecture": {
                "type": "kmeans",
                "parameters": {"n_clusters": 5}
            },
            "hyperparameters": {
                "max_iter": 300,
                "n_init": 10
            },
            "training_config": {
                "algorithm": "kmeans",
                "random_state": 42
            },
            "evaluation_metrics": ["silhouette_score", "calinski_harabasz_score"]
        }
    
    def _generate_default_blueprint(self, task: MLTask) -> Dict[str, Any]:
        """Generate default blueprint for unknown task types"""
        return {
            "framework": "scikit_learn",
            "architecture": {
                "type": "random_forest",
                "parameters": {"n_estimators": 100}
            },
            "hyperparameters": {
                "learning_rate": 0.01,
                "batch_size": 32,
                "epochs": 100
            },
            "training_config": {
                "optimizer": "adam",
                "loss_function": "auto",
                "validation_split": 0.2
            },
            "evaluation_metrics": ["accuracy", "precision", "recall"]
        }
    
    def _validate_blueprint_config(self, config: Dict[str, Any], task: MLTask) -> Dict[str, Any]:
        """Validate and sanitize blueprint configuration"""
        required_keys = ["framework", "architecture", "hyperparameters", "training_config", "evaluation_metrics"]
        
        for key in required_keys:
            if key not in config:
                config[key] = self._get_default_value(key, task)
        
        # Ensure framework is supported
        if config["framework"] not in self.framework_manager.list_frameworks():
            config["framework"] = "scikit_learn"  # Fallback to scikit-learn
        
        return config
    
    def _get_default_value(self, key: str, task: MLTask) -> Any:
        """Get default value for missing configuration key"""
        defaults = {
            "framework": "scikit_learn",
            "architecture": {"type": "auto", "parameters": {}},
            "hyperparameters": {"learning_rate": 0.001, "batch_size": 32, "epochs": 100},
            "training_config": {"optimizer": "adam", "loss_function": "auto", "validation_split": 0.2},
            "evaluation_metrics": ["accuracy"]
        }
        return defaults.get(key, {})
    
    def execute_experiment(self, task: MLTask, blueprint: MLModelBlueprint) -> MLExperiment:
        """Execute an ML experiment based on task and blueprint"""
        try:
            experiment_id = f"exp_{task.task_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Get framework
            framework = self.framework_manager.get_framework(blueprint.framework)
            if not framework:
                raise ValueError(f"Framework {blueprint.framework} not available")
            
            # Create model
            model = framework.create_model(blueprint.architecture)
            
            # Prepare data (this would typically load and preprocess actual data)
            data = self._prepare_sample_data(task, blueprint)
            
            # Train model
            training_results = framework.train_model(model, data, **blueprint.hyperparameters)
            
            # Evaluate model
            evaluation_results = framework.evaluate_model(model, data)
            
            # Save model
            model_path = f"models/{experiment_id}_{blueprint.name}.pkl"
            framework.save_model(model, model_path)
            
            # Create experiment record
            experiment = MLExperiment(
                experiment_id=experiment_id,
                task=task,
                blueprint=blueprint,
                model=model,
                training_results=training_results,
                evaluation_results=evaluation_results,
                model_path=model_path,
                completed_at=datetime.now()
            )
            
            self.experiments[experiment_id] = experiment
            
            # Update task status
            task.status = "completed"
            
            # Register model
            self.model_manager.register_model(
                experiment_id,
                {
                    "task_type": task.task_type,
                    "framework": blueprint.framework,
                    "architecture": blueprint.architecture,
                    "performance": evaluation_results,
                    "model_path": model_path
                }
            )
            
            self.logger.info(f"Experiment completed: {experiment_id}")
            return experiment
            
        except Exception as e:
            self.logger.error(f"Error executing experiment: {e}")
            raise
    
    def _prepare_sample_data(self, task: MLTask, blueprint: MLModelBlueprint) -> Dict[str, Any]:
        """Prepare sample data for training (placeholder implementation)"""
        # This is a placeholder - in real implementation, you would load actual data
        if task.task_type == "classification":
            # Generate sample classification data
            n_samples = 1000
            n_features = 20
            n_classes = 3
            
            X = np.random.randn(n_samples, n_features)
            y = np.random.randint(0, n_classes, n_samples)
            
            # Split into train/test
            split_idx = int(0.8 * n_samples)
            return {
                "x_train": X[:split_idx],
                "y_train": y[:split_idx],
                "x_test": X[split_idx:],
                "y_test": y[split_idx:]
            }
        
        elif task.task_type == "regression":
            # Generate sample regression data
            n_samples = 1000
            n_features = 10
            
            X = np.random.randn(n_samples, n_features)
            y = np.random.randn(n_samples)
            
            # Split into train/test
            split_idx = int(0.8 * n_samples)
            return {
                "x_train": X[:split_idx],
                "y_train": y[:split_idx],
                "x_test": X[split_idx:],
                "y_test": y[split_idx:]
            }
        
        else:
            # Default sample data
            n_samples = 500
            n_features = 15
            
            X = np.random.randn(n_samples, n_features)
            y = np.random.randint(0, 2, n_samples)
            
            split_idx = int(0.8 * n_samples)
            return {
                "x_train": X[:split_idx],
                "y_train": y[:split_idx],
                "x_test": X[split_idx:],
                "y_test": y[split_idx:]
            }
    
    def auto_ml_pipeline(self, task_description: str, dataset_info: Dict[str, Any], 
                         model_requirements: Dict[str, Any]) -> MLExperiment:
        """Complete automated ML pipeline from task description to trained model"""
        try:
            # Create task
            task = self.create_task(
                task_type=self._infer_task_type(task_description),
                description=task_description,
                dataset_info=dataset_info,
                model_requirements=model_requirements
            )
            
            # Generate blueprint
            blueprint = self.generate_model_blueprint(task)
            
            # Execute experiment
            experiment = self.execute_experiment(task, blueprint)
            
            self.logger.info(f"Auto ML pipeline completed: {experiment.experiment_id}")
            return experiment
            
        except Exception as e:
            self.logger.error(f"Auto ML pipeline failed: {e}")
            raise
    
    def _infer_task_type(self, description: str) -> str:
        """Infer task type from description using AI or rules"""
        description_lower = description.lower()
        
        # Rule-based inference
        if any(word in description_lower for word in ["classify", "classification", "category", "label"]):
            return "classification"
        elif any(word in description_lower for word in ["predict", "regression", "forecast", "estimate"]):
            return "regression"
        elif any(word in description_lower for word in ["cluster", "group", "segment", "pattern"]):
            return "clustering"
        else:
            return "classification"  # Default
    
    def get_experiment_summary(self) -> Dict[str, Any]:
        """Get summary of all experiments"""
        summary = {
            "total_experiments": len(self.experiments),
            "total_tasks": len(self.tasks),
            "total_blueprints": len(self.blueprints),
            "framework_usage": {},
            "task_type_distribution": {},
            "performance_metrics": {}
        }
        
        # Framework usage
        for exp in self.experiments.values():
            framework = exp.blueprint.framework
            summary["framework_usage"][framework] = summary["framework_usage"].get(framework, 0) + 1
        
        # Task type distribution
        for task in self.tasks.values():
            task_type = task.task_type
            summary["task_type_distribution"][task_type] = summary["task_type_distribution"].get(task_type, 0) + 1
        
        # Performance metrics
        if self.experiments:
            accuracies = []
            for exp in self.experiments.values():
                if "accuracy" in exp.evaluation_results:
                    accuracies.append(exp.evaluation_results["accuracy"])
            
            if accuracies:
                summary["performance_metrics"] = {
                    "avg_accuracy": np.mean(accuracies),
                    "max_accuracy": np.max(accuracies),
                    "min_accuracy": np.min(accuracies)
                }
        
        return summary
    
    def cleanup_experiments(self, older_than_days: int = 30) -> int:
        """Clean up old experiments and models"""
        try:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            cleaned_count = 0
            
            for exp_id, experiment in list(self.experiments.items()):
                if experiment.created_at < cutoff_date:
                    # Remove model file
                    if experiment.model_path and os.path.exists(experiment.model_path):
                        os.remove(experiment.model_path)
                    
                    # Remove experiment record
                    del self.experiments[exp_id]
                    cleaned_count += 1
            
            self.logger.info(f"Cleaned up {cleaned_count} old experiments")
            return cleaned_count
            
        except Exception as e:
            self.logger.error(f"Error cleaning up experiments: {e}")
            return 0

# Factory function for easy instantiation
def get_ml_robot_maker(config_path: Optional[str] = None) -> MLRobotMaker:
    """Get an instance of ML Robot Maker"""
    return MLRobotMaker(config_path)
