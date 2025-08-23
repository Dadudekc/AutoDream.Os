#!/usr/bin/env python3
"""
🧪 ML Robot Modular Tests - TDD Implementation
==============================================

Test-Driven Development implementation for modular ML Robot system.
Tests the refactored V2-compliant ML Robot components following OOP and SRP principles.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

# Import our new modular components
from src.core.ml_robot import (
    ModelConfig, TrainingConfig, DatasetConfig, ModelResult,
    MLRobotMaker
)
from src.core.ml_robot.robot_execution import (
    ModelCreator, ModelTrainer, ModelEvaluator, HyperparameterOptimizer
)
from src.core.ml_robot.robot_cli import MLRobotCLI


class TestModelConfig:
    """Test ModelConfig dataclass following TDD principles"""

    @pytest.mark.unit
    def test_model_config_creation_with_all_parameters(self):
        """Test creating ModelConfig with all parameters"""
        config = ModelConfig(
            model_type="classification",
            algorithm="neural_network",
            hyperparameters={"layers": 2, "neurons": 64},
            input_features=10,
            output_classes=3,
            architecture="deep",
            pretrained=True,
        )

        assert config.model_type == "classification"
        assert config.algorithm == "neural_network"
        assert config.hyperparameters["layers"] == 2
        assert config.hyperparameters["neurons"] == 64
        assert config.input_features == 10
        assert config.output_classes == 3
        assert config.architecture == "deep"
        assert config.pretrained is True

    @pytest.mark.unit
    def test_model_config_defaults(self):
        """Test creating ModelConfig with minimal parameters"""
        config = ModelConfig(
            model_type="regression",
            algorithm="linear_regression",
            hyperparameters={},
            input_features=5,
        )

        assert config.model_type == "regression"
        assert config.algorithm == "linear_regression"
        assert config.hyperparameters == {}
        assert config.input_features == 5
        assert config.output_classes is None
        assert config.architecture is None
        assert config.pretrained is False

    @pytest.mark.unit
    def test_model_config_classification_auto_output_classes(self):
        """Test that classification models get default output_classes"""
        config = ModelConfig(
            model_type="classification",
            algorithm="random_forest",
            hyperparameters={},
            input_features=10,
        )

        assert config.output_classes == 2  # Default for binary classification


class TestTrainingConfig:
    """Test TrainingConfig dataclass following TDD principles"""

    @pytest.mark.unit
    def test_training_config_creation_with_all_parameters(self):
        """Test creating TrainingConfig with all parameters"""
        config = TrainingConfig(
            epochs=200,
            batch_size=64,
            learning_rate=0.0001,
            validation_split=0.3,
            early_stopping=False,
            patience=20,
            optimizer="sgd",
            loss_function="mse",
            metrics=["mae", "mse"],
        )

        assert config.epochs == 200
        assert config.batch_size == 64
        assert config.learning_rate == 0.0001
        assert config.validation_split == 0.3
        assert config.early_stopping is False
        assert config.patience == 20
        assert config.optimizer == "sgd"
        assert config.loss_function == "mse"
        assert "mae" in config.metrics
        assert "mse" in config.metrics

    @pytest.mark.unit
    def test_training_config_defaults(self):
        """Test creating TrainingConfig with default parameters"""
        config = TrainingConfig()

        assert config.epochs == 100
        assert config.batch_size == 32
        assert config.learning_rate == 0.001
        assert config.validation_split == 0.2
        assert config.early_stopping is True
        assert config.patience == 10
        assert config.optimizer == "adam"
        assert config.loss_function == "binary_crossentropy"
        assert config.metrics == ["accuracy"]


class TestDatasetConfig:
    """Test DatasetConfig dataclass following TDD principles"""

    @pytest.mark.unit
    def test_dataset_config_creation_with_all_parameters(self):
        """Test creating DatasetConfig with all parameters"""
        config = DatasetConfig(
            data_path="data/dataset.csv",
            data_type="csv",
            target_column="target",
            feature_columns=["feature1", "feature2"],
            test_size=0.25,
            random_state=123,
            preprocessing=["normalization", "encoding", "scaling"],
        )

        assert config.data_path == "data/dataset.csv"
        assert config.data_type == "csv"
        assert config.target_column == "target"
        assert "feature1" in config.feature_columns
        assert "feature2" in config.feature_columns
        assert config.test_size == 0.25
        assert config.random_state == 123
        assert "normalization" in config.preprocessing
        assert "encoding" in config.preprocessing
        assert "scaling" in config.preprocessing

    @pytest.mark.unit
    def test_dataset_config_defaults(self):
        """Test creating DatasetConfig with minimal parameters"""
        config = DatasetConfig(
            data_path="data/dataset.json", data_type="json", target_column="output"
        )

        assert config.data_path == "data/dataset.json"
        assert config.data_type == "json"
        assert config.target_column == "output"
        assert config.feature_columns is None
        assert config.test_size == 0.2
        assert config.random_state == 42
        assert config.preprocessing == ["normalization", "encoding"]


class TestModelResult:
    """Test ModelResult dataclass following TDD principles"""

    @pytest.fixture
    def sample_model_config(self):
        """Sample model configuration for testing"""
        return ModelConfig(
            model_type="classification",
            algorithm="neural_network",
            hyperparameters={},
            input_features=10,
            output_classes=2,
        )

    @pytest.mark.unit
    def test_model_result_creation_with_all_parameters(self, sample_model_config):
        """Test creating ModelResult with all parameters"""
        result = ModelResult(
            model_id="test_model_123",
            model_path="models/test_model.pkl",
            config=sample_model_config,
            training_history={"loss": [1.0, 0.5], "accuracy": [0.5, 0.8]},
            performance_metrics={"accuracy": 0.85, "loss": 0.3},
            training_time=15.5,
            model_size=25.0,
            accuracy=0.85,
            loss=0.3,
        )

        assert result.model_id == "test_model_123"
        assert result.model_path == "models/test_model.pkl"
        assert result.config == sample_model_config
        assert result.training_history["loss"] == [1.0, 0.5]
        assert result.performance_metrics["accuracy"] == 0.85
        assert result.training_time == 15.5
        assert result.model_size == 25.0
        assert result.accuracy == 0.85
        assert result.loss == 0.3

    @pytest.mark.unit
    def test_model_result_auto_accuracy_from_metrics(self, sample_model_config):
        """Test that accuracy is auto-populated from performance metrics"""
        result = ModelResult(
            model_id="test_model_456",
            model_path="models/test_model.pkl",
            config=sample_model_config,
            training_history={},
            performance_metrics={"accuracy": 0.75},
            training_time=10.0,
            model_size=5.0,
        )

        assert result.accuracy == 0.75  # From performance_metrics
        assert result.loss == float("inf")  # Default value


class TestMLRobotMaker:
    """Test MLRobotMaker core class following TDD principles"""

    @pytest.fixture
    def sample_model_config(self):
        """Sample model configuration for testing"""
        return ModelConfig(
            model_type="classification",
            algorithm="neural_network",
            hyperparameters={"layers": 2, "neurons": 64},
            input_features=10,
            output_classes=2,
        )

    @pytest.fixture
    def sample_training_config(self):
        """Sample training configuration for testing"""
        return TrainingConfig(epochs=50, batch_size=32, learning_rate=0.001)

    @pytest.fixture
    def sample_dataset_config(self):
        """Sample dataset configuration for testing"""
        return DatasetConfig(
            data_path="data/test.csv", data_type="csv", target_column="target"
        )

    @pytest.mark.unit
    def test_ml_robot_maker_initialization(self):
        """Test MLRobotMaker initialization following OOP principles"""
        maker = MLRobotMaker()

        assert "classification" in maker.supported_models
        assert "regression" in maker.supported_models
        assert "neural_network" in maker.supported_models["classification"]
        assert "random_forest" in maker.supported_models["classification"]
        assert "scikit-learn" in maker.supported_frameworks
        assert "tensorflow" in maker.supported_frameworks

    @pytest.mark.unit
    def test_create_model_success(self, sample_model_config, sample_training_config):
        """Test successful model creation following SRP"""
        maker = MLRobotMaker()

        result = maker.create_model(sample_model_config, sample_training_config)

        assert result.model_id is not None
        assert result.model_path is not None
        assert result.config == sample_model_config
        assert result.training_history is not None
        assert result.performance_metrics is not None
        assert result.training_time > 0
        assert result.model_size > 0
        assert result.accuracy > 0
        assert result.loss > 0

    @pytest.mark.unit
    def test_create_model_invalid_type(self, sample_training_config):
        """Test model creation with invalid model type"""
        maker = MLRobotMaker()
        invalid_config = ModelConfig(
            model_type="invalid_type",
            algorithm="neural_network",
            hyperparameters={},
            input_features=10,
        )

        with pytest.raises(ValueError, match="Unsupported model type"):
            maker.create_model(invalid_config, sample_training_config)

    @pytest.mark.unit
    def test_auto_create_model(self, sample_dataset_config):
        """Test automatic model creation following intelligent automation"""
        maker = MLRobotMaker()

        result = maker.auto_create_model(sample_dataset_config)

        assert result.model_id is not None
        assert result.model_path is not None
        assert result.config is not None
        assert result.performance_metrics is not None
        assert result.accuracy > 0


class TestModelCreator:
    """Test ModelCreator execution component following SRP"""

    @pytest.mark.unit
    def test_model_creator_initialization(self):
        """Test ModelCreator initialization"""
        creator = ModelCreator()
        
        assert "neural_network" in creator.architecture_templates
        assert "simple" in creator.architecture_templates["neural_network"]
        assert creator.architecture_templates["neural_network"]["simple"] == [64, 32]

    @pytest.mark.unit
    def test_create_neural_network_architecture(self):
        """Test neural network architecture creation"""
        creator = ModelCreator()
        config = ModelConfig(
            model_type="classification",
            algorithm="neural_network",
            hyperparameters={},
            input_features=10,
            output_classes=2,
            architecture="simple"
        )

        model = creator.create_model_architecture(config)
        
        assert hasattr(model, "layers")
        assert hasattr(model, "optimizer")
        assert model.optimizer == "adam"


class TestHyperparameterOptimizer:
    """Test HyperparameterOptimizer execution component following SRP"""

    @pytest.fixture
    def sample_model_config(self):
        """Sample model configuration for testing"""
        return ModelConfig(
            model_type="classification",
            algorithm="random_forest",
            hyperparameters={},
            input_features=10,
            output_classes=2,
        )

    @pytest.fixture
    def sample_dataset_config(self):
        """Sample dataset configuration for testing"""
        return DatasetConfig(
            data_path="data/test.csv", data_type="csv", target_column="target"
        )

    @pytest.mark.unit
    def test_hyperparameter_optimizer_initialization(self):
        """Test HyperparameterOptimizer initialization"""
        optimizer = HyperparameterOptimizer()
        
        assert "random_forest" in optimizer.auto_hyperparameter_ranges
        assert "n_estimators" in optimizer.auto_hyperparameter_ranges["random_forest"]

    @pytest.mark.unit
    def test_auto_tune_hyperparameters(self):
        """Test automatic hyperparameter tuning"""
        optimizer = HyperparameterOptimizer()

        # Test random forest
        rf_params = optimizer.auto_tune_hyperparameters("random_forest", "classification")
        assert "n_estimators" in rf_params
        assert "max_depth" in rf_params
        assert "min_samples_split" in rf_params

        # Test neural network
        nn_params = optimizer.auto_tune_hyperparameters("neural_network", "classification")
        assert "layers" in nn_params
        assert "neurons" in nn_params
        assert "dropout" in nn_params

    @pytest.mark.unit
    def test_optimize_hyperparameters_grid_search(
        self, sample_model_config, sample_dataset_config
    ):
        """Test hyperparameter optimization with grid search"""
        optimizer = HyperparameterOptimizer()

        result = optimizer.optimize_hyperparameters(
            sample_model_config, sample_dataset_config, "grid_search", 10
        )

        assert "best_parameters" in result
        assert "optimization_method" in result
        assert "trials_performed" in result
        assert "best_score" in result
        assert result["optimization_method"] == "grid_search"
        assert result["trials_performed"] == 10


class TestMLRobotCLI:
    """Test MLRobotCLI interface following interface segregation"""

    @pytest.mark.unit
    def test_cli_initialization(self):
        """Test CLI initialization with all components"""
        cli = MLRobotCLI()
        
        assert cli.maker is not None
        assert cli.creator is not None
        assert cli.trainer is not None
        assert cli.evaluator is not None
        assert cli.optimizer is not None

    @pytest.mark.unit
    def test_create_model_via_cli(self):
        """Test model creation via CLI interface"""
        cli = MLRobotCLI()
        
        result = cli.create_model(
            model_type="classification",
            algorithm="neural_network",
            input_features=10,
            output_classes=2,
            architecture="simple"
        )
        
        assert result is not None
        assert result.model_id is not None
        assert result.accuracy > 0

    @pytest.mark.unit
    def test_list_supported_models(self, capsys):
        """Test listing supported models via CLI"""
        cli = MLRobotCLI()
        
        cli.list_supported_models()
        
        captured = capsys.readouterr()
        assert "CLASSIFICATION" in captured.out
        assert "REGRESSION" in captured.out
        assert "neural_network" in captured.out


class TestIntegrationScenarios:
    """Integration tests for complete ML workflows following TDD"""

    @pytest.mark.integration
    def test_complete_ml_workflow_tdd(self):
        """Test complete ML workflow from dataset to trained model following TDD"""
        # Arrange
        maker = MLRobotMaker()
        dataset_config = DatasetConfig(
            data_path="data/classification_dataset.csv",
            data_type="csv",
            target_column="target",
            feature_columns=["feature1", "feature2", "feature3"],
        )

        # Act
        result = maker.auto_create_model(dataset_config)

        # Assert
        assert result.model_id is not None
        assert result.model_path is not None
        assert result.config is not None
        assert result.performance_metrics is not None
        
        # Verify OOP principles
        assert isinstance(result.config, ModelConfig)
        assert hasattr(result, 'accuracy')
        assert hasattr(result, 'loss')

    @pytest.mark.integration
    def test_hyperparameter_optimization_workflow_tdd(self):
        """Test hyperparameter optimization workflow following TDD"""
        # Arrange
        optimizer = HyperparameterOptimizer()
        model_config = ModelConfig(
            model_type="classification",
            algorithm="random_forest",
            hyperparameters={},
            input_features=10,
            output_classes=2,
        )
        dataset_config = DatasetConfig(
            data_path="data/test.csv", data_type="csv", target_column="target"
        )

        # Act
        optimization_result = optimizer.optimize_hyperparameters(
            model_config, dataset_config, "grid_search", 5
        )

        # Assert
        assert "best_parameters" in optimization_result
        assert "best_score" in optimization_result
        assert optimization_result["best_score"] > 0

    @pytest.mark.integration
    def test_cli_integration_workflow_tdd(self):
        """Test CLI integration workflow following TDD"""
        # Arrange
        cli = MLRobotCLI()

        # Act & Assert - Create model
        result1 = cli.create_model("classification", "neural_network", 10, 2, "simple")
        assert result1 is not None

        # Act & Assert - Auto create model
        result2 = cli.auto_create_model("data/demo.csv", "csv", "target")
        assert result2 is not None

        # Act & Assert - Optimize hyperparameters
        result3 = cli.optimize_hyperparameters("classification", "random_forest", 10, 2)
        assert result3 is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

