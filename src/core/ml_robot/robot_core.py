#!/usr/bin/env python3
"""
ML Robot Core - Core ML Robot Maker Logic
========================================

Contains the core MLRobotMaker class and main logic.
Extracted from monolithic test_ml_robot_maker.py for V2 standards compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import logging
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock

try:
    from .robot_types import ModelConfig, TrainingConfig, DatasetConfig, ModelResult
except ImportError:
    from robot_types import ModelConfig, TrainingConfig, DatasetConfig, ModelResult

# Configure logging
logger = logging.getLogger(__name__)


class MLRobotMaker:
    """Automated ML model creation and training tool"""

    def __init__(self):
        self.supported_models = {
            "classification": ["random_forest", "svm", "neural_network", "xgboost", "lightgbm"],
            "regression": ["linear_regression", "ridge", "lasso", "neural_network", "random_forest"],
            "clustering": ["kmeans", "dbscan", "hierarchical", "gaussian_mixture"],
            "nlp": ["transformer", "lstm", "cnn", "bert", "gpt"],
        }

        self.supported_frameworks = {
            "scikit-learn": ["random_forest", "svm", "kmeans", "linear_regression"],
            "tensorflow": ["neural_network", "lstm", "cnn", "transformer"],
            "pytorch": ["neural_network", "lstm", "cnn", "transformer"],
            "xgboost": ["xgboost"],
            "lightgbm": ["lightgbm"],
        }

        self.auto_hyperparameter_ranges = {
            "random_forest": {"n_estimators": [50, 100, 200], "max_depth": [3, 5, 10, None]},
            "neural_network": {"layers": [1, 2, 3], "neurons": [32, 64, 128, 256]},
            "svm": {"C": [0.1, 1.0, 10.0], "kernel": ["rbf", "linear", "poly"]},
        }

    def create_model(self, model_config: ModelConfig, training_config: TrainingConfig) -> ModelResult:
        """Create and train an ML model automatically"""
        logger.info(f"Creating {model_config.algorithm} model for {model_config.model_type}")

        try:
            self._validate_model_config(model_config)
            self._validate_training_config(training_config)

            if not model_config.hyperparameters:
                model_config.hyperparameters = self._auto_tune_hyperparameters(
                    model_config.algorithm, model_config.model_type
                )

            model = self._create_model_architecture(model_config)
            training_result = self._train_model(model, training_config)
            performance_metrics = self._evaluate_model(model, training_result)
            model_path = self._save_model(model, model_config)

            return ModelResult(
                model_id=f"{model_config.algorithm}_{model_config.model_type}_{hash(str(model_config))}",
                model_path=model_path,
                config=model_config,
                training_history=training_result.get("history", {}),
                performance_metrics=performance_metrics,
                training_time=training_result.get("training_time", 0.0),
                model_size=self._calculate_model_size(model),
                accuracy=performance_metrics.get("accuracy", 0.0),
                loss=performance_metrics.get("loss", float("inf")),
            )

        except Exception as e:
            logger.error(f"Model creation failed: {e}")
            raise

    def auto_create_model(self, dataset_config: DatasetConfig, target_metric: str = "accuracy") -> ModelResult:
        """Automatically create the best model for a dataset"""
        logger.info(f"Auto-creating best model for dataset: {dataset_config.data_path}")

        try:
            dataset_analysis = self._analyze_dataset(dataset_config)
            model_type = self._determine_model_type(dataset_analysis)
            algorithm = self._select_best_algorithm(model_type, dataset_analysis)

            model_config = ModelConfig(
                model_type=model_type,
                algorithm=algorithm,
                hyperparameters={},
                input_features=dataset_analysis["feature_count"],
                output_classes=dataset_analysis.get("output_classes"),
            )

            training_config = self._create_optimal_training_config(dataset_analysis)
            return self.create_model(model_config, training_config)

        except Exception as e:
            logger.error(f"Auto model creation failed: {e}")
            raise

    def _validate_model_config(self, config: ModelConfig) -> None:
        """Validate model configuration"""
        if config.model_type not in self.supported_models:
            raise ValueError(f"Unsupported model type: {config.model_type}")

        if config.algorithm not in self.supported_models[config.model_type]:
            raise ValueError(f"Unsupported algorithm {config.algorithm} for model type {config.model_type}")

        if config.input_features <= 0:
            raise ValueError("Input features must be positive")

        if config.model_type in ["classification", "clustering"] and config.output_classes <= 1:
            raise ValueError(f"Output classes must be > 1 for {config.model_type}")

    def _validate_training_config(self, config: TrainingConfig) -> None:
        """Validate training configuration"""
        if config.epochs <= 0:
            raise ValueError("Epochs must be positive")

        if config.batch_size <= 0:
            raise ValueError("Batch size must be positive")

        if config.learning_rate <= 0:
            raise ValueError("Learning rate must be positive")

        if not 0 < config.validation_split < 1:
            raise ValueError("Validation split must be between 0 and 1")

    def _auto_tune_hyperparameters(self, algorithm: str, model_type: str) -> Dict[str, Any]:
        """Auto-tune hyperparameters for an algorithm"""
        if algorithm in self.auto_hyperparameter_ranges:
            params = {}
            for param, values in self.auto_hyperparameter_ranges[algorithm].items():
                if values:
                    if None in values:
                        params[param] = next(v for v in values if v is not None)
                    else:
                        params[param] = values[len(values) // 2]
            return params
        else:
            return {}

    def _analyze_dataset(self, config: DatasetConfig) -> Dict[str, Any]:
        """Analyze dataset characteristics"""
        return {
            "feature_count": 10,
            "sample_count": 1000,
            "output_classes": 2 if config.data_type in ["csv", "json"] else None,
            "data_type": config.data_type,
            "missing_values": 0.05,
            "categorical_features": 3,
            "numerical_features": 7,
        }

    def _determine_model_type(self, analysis: Dict[str, Any]) -> str:
        """Determine best model type for dataset"""
        if analysis.get("output_classes"):
            return "classification"
        else:
            return "regression"

    def _select_best_algorithm(self, model_type: str, analysis: Dict[str, Any]) -> str:
        """Select best algorithm for model type"""
        if model_type == "classification":
            return "random_forest" if analysis["feature_count"] < 50 else "neural_network"
        elif model_type == "regression":
            return "linear_regression" if analysis["feature_count"] < 20 else "random_forest"
        else:
            return "kmeans"

    def _create_optimal_training_config(self, analysis: Dict[str, Any]) -> TrainingConfig:
        """Create optimal training configuration"""
        if analysis["sample_count"] < 1000:
            epochs, batch_size = 50, 16
        elif analysis["sample_count"] < 10000:
            epochs, batch_size = 100, 32
        else:
            epochs, batch_size = 200, 64

        return TrainingConfig(
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=0.001,
            validation_split=0.2,
            early_stopping=True,
            patience=10,
        )

    def _create_model_architecture(self, config: ModelConfig) -> Any:
        """Create model architecture based on configuration"""
        if config.algorithm == "neural_network":
            return self._create_neural_network(config)
        elif config.algorithm == "random_forest":
            return self._create_random_forest(config)
        elif config.algorithm == "svm":
            return self._create_svm(config)
        else:
            return self._create_generic_model(config)

    def _create_neural_network(self, config: ModelConfig) -> Mock:
        """Create neural network model"""
        model = Mock()
        model.layers = [config.input_features, 64, 32, config.output_classes or 1]
        model.optimizer = "adam"
        model.loss = "binary_crossentropy"
        model.metrics = ["accuracy"]
        return model

    def _create_random_forest(self, config: ModelConfig) -> Mock:
        """Create random forest model"""
        model = Mock()
        model.n_estimators = config.hyperparameters.get("n_estimators", 100)
        model.max_depth = config.hyperparameters.get("max_depth", 10)
        model.min_samples_split = config.hyperparameters.get("min_samples_split", 2)
        model.random_state = 42
        return model

    def _create_svm(self, config: ModelConfig) -> Mock:
        """Create SVM model"""
        model = Mock()
        model.C = config.hyperparameters.get("C", 1.0)
        model.kernel = config.hyperparameters.get("kernel", "rbf")
        model.gamma = config.hyperparameters.get("gamma", "scale")
        model.random_state = 42
        return model

    def _create_generic_model(self, config: ModelConfig) -> Mock:
        """Create generic model"""
        model = Mock()
        model.algorithm = config.algorithm
        model.model_type = config.model_type
        model.hyperparameters = config.hyperparameters
        return model

    def _train_model(self, model: Any, config: TrainingConfig) -> Dict[str, Any]:
        """Train the model"""
        training_time = 10.0
        history = {
            "loss": [1.0, 0.8, 0.6, 0.4, 0.2],
            "accuracy": [0.5, 0.6, 0.7, 0.8, 0.9],
            "val_loss": [1.1, 0.9, 0.7, 0.5, 0.3],
            "val_accuracy": [0.4, 0.5, 0.6, 0.7, 0.8],
        }

        return {
            "history": history,
            "training_time": training_time,
            "epochs_completed": config.epochs,
        }

    def _evaluate_model(self, model: Any, training_result: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate model performance"""
        history = training_result.get("history", {})
        final_loss = history.get("loss", [1.0])[-1] if history.get("loss") else 1.0
        final_accuracy = history.get("accuracy", [0.5])[-1] if history.get("accuracy") else 0.5
        final_val_loss = history.get("val_loss", [1.0])[-1] if history.get("val_loss") else 1.0
        final_val_accuracy = history.get("val_accuracy", [0.5])[-1] if history.get("val_accuracy") else 0.5

        return {
            "loss": final_loss,
            "accuracy": final_accuracy,
            "val_loss": final_val_loss,
            "val_accuracy": final_val_accuracy,
            "overfitting_score": final_loss - final_val_loss,
        }

    def _save_model(self, model: Any, config: ModelConfig) -> str:
        """Save the trained model"""
        model_dir = Path("models")
        model_dir.mkdir(exist_ok=True)
        model_filename = f"{config.algorithm}_{config.model_type}_{hash(str(config))}.pkl"
        model_path = model_dir / model_filename

        with open(model_path, "w") as f:
            f.write("Mock model content")

        return str(model_path)

    def _calculate_model_size(self, model: Any) -> float:
        """Calculate model size in MB"""
        return 15.5


def run_smoke_test():
    """Run smoke test for robot core module"""
    print("🧪 Testing ML Robot Core Module...")
    
    try:
        maker = MLRobotMaker()
        assert "classification" in maker.supported_models
        assert "regression" in maker.supported_models
        print("✅ MLRobotMaker initialization smoke test passed")

        from robot_types import ModelConfig, TrainingConfig
        
        model_config = ModelConfig(
            model_type="classification",
            algorithm="neural_network",
            hyperparameters={"layers": 2, "neurons": 64},
            input_features=10,
            output_classes=2
        )
        
        training_config = TrainingConfig(epochs=50, batch_size=32)
        
        result = maker.create_model(model_config, training_config)
        assert result.model_id is not None
        assert result.model_path is not None
        print("✅ Model creation smoke test passed")

        print("🎉 All robot core smoke tests passed!")
        return True

    except Exception as e:
        print(f"❌ Robot core smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
