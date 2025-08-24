#!/usr/bin/env python3
"""
ML Robot CLI - Command Line Interface and Smoke Tests
====================================================

Provides CLI interface for the ML Robot system and comprehensive smoke tests.
Extracted from monolithic test_ml_robot_maker.py for V2 standards compliance.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import argparse
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path

try:
    from .robot_types import ModelConfig, TrainingConfig, DatasetConfig, ModelResult
    from .robot_core import MLRobotMaker
    from .robot_execution import ModelCreator, ModelTrainer, ModelEvaluator, HyperparameterOptimizer
except ImportError:
    from robot_types import ModelConfig, TrainingConfig, DatasetConfig, ModelResult
    from robot_core import MLRobotMaker
    from robot_execution import ModelCreator, ModelTrainer, ModelEvaluator, HyperparameterOptimizer


class MLRobotCLI:
    """Command Line Interface for ML Robot system"""

    def __init__(self):
        self.maker = MLRobotMaker()
        self.creator = ModelCreator()
        self.trainer = ModelTrainer()
        self.evaluator = ModelEvaluator()
        self.optimizer = HyperparameterOptimizer()

    def create_model(self, model_type: str, algorithm: str, input_features: int, 
                    output_classes: int = None, architecture: str = None):
        """Create a model via CLI"""
        print(f"🤖 Creating {algorithm} model for {model_type}...")
        
        try:
            model_config = ModelConfig(
                model_type=model_type,
                algorithm=algorithm,
                hyperparameters={},
                input_features=input_features,
                output_classes=output_classes,
                architecture=architecture
            )
            
            training_config = TrainingConfig()
            
            result = self.maker.create_model(model_config, training_config)
            
            print(f"✅ Model created successfully!")
            print(f"   Model ID: {result.model_id}")
            print(f"   Model Path: {result.model_path}")
            print(f"   Accuracy: {result.accuracy:.3f}")
            print(f"   Loss: {result.loss:.3f}")
            print(f"   Training Time: {result.training_time:.2f}s")
            print(f"   Model Size: {result.model_size:.1f} MB")
            
            return result
            
        except Exception as e:
            print(f"❌ Model creation failed: {e}")
            return None

    def auto_create_model(self, data_path: str, data_type: str, target_column: str):
        """Auto-create best model for dataset via CLI"""
        print(f"🔍 Auto-creating best model for dataset: {data_path}")
        
        try:
            dataset_config = DatasetConfig(
                data_path=data_path,
                data_type=data_type,
                target_column=target_column
            )
            
            result = self.maker.auto_create_model(dataset_config)
            
            print(f"✅ Auto model creation successful!")
            print(f"   Model Type: {result.config.model_type}")
            print(f"   Algorithm: {result.config.algorithm}")
            print(f"   Accuracy: {result.accuracy:.3f}")
            print(f"   Loss: {result.loss:.3f}")
            
            return result
            
        except Exception as e:
            print(f"❌ Auto model creation failed: {e}")
            return None

    def optimize_hyperparameters(self, model_type: str, algorithm: str, 
                               input_features: int, output_classes: int,
                               optimization_method: str = "grid_search", max_trials: int = 50):
        """Optimize hyperparameters via CLI"""
        print(f"⚡ Optimizing hyperparameters for {algorithm}...")
        
        try:
            model_config = ModelConfig(
                model_type=model_type,
                algorithm=algorithm,
                hyperparameters={},
                input_features=input_features,
                output_classes=output_classes
            )
            
            dataset_config = DatasetConfig(
                data_path="mock_data.csv",
                data_type="csv",
                target_column="target"
            )
            
            result = self.optimizer.optimize_hyperparameters(
                model_config, dataset_config, optimization_method, max_trials
            )
            
            print(f"✅ Hyperparameter optimization successful!")
            print(f"   Method: {result['optimization_method']}")
            print(f"   Trials: {result['trials_performed']}")
            print(f"   Best Score: {result['best_score']:.3f}")
            print(f"   Best Parameters: {result['best_parameters']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Hyperparameter optimization failed: {e}")
            return None

    def list_supported_models(self):
        """List supported models and algorithms"""
        print("📋 Supported Models and Algorithms:")
        print("=" * 50)
        
        for model_type, algorithms in self.maker.supported_models.items():
            print(f"\n🔹 {model_type.upper()}:")
            for algorithm in algorithms:
                print(f"   - {algorithm}")
        
        print(f"\n🔹 FRAMEWORKS:")
        for framework, algorithms in self.maker.supported_frameworks.items():
            print(f"   - {framework}: {', '.join(algorithms[:3])}...")

    def run_demo(self):
        """Run a complete demo of the ML Robot system"""
        print("🎬 Running ML Robot System Demo...")
        print("=" * 50)
        
        # Demo 1: Create classification model
        print("\n1️⃣ Creating Classification Model...")
        result1 = self.create_model("classification", "neural_network", 10, 2, "simple")
        
        # Demo 2: Auto-create model
        print("\n2️⃣ Auto-Creating Model...")
        result2 = self.auto_create_model("data/demo.csv", "csv", "target")
        
        # Demo 3: Hyperparameter optimization
        print("\n3️⃣ Hyperparameter Optimization...")
        result3 = self.optimize_hyperparameters("classification", "random_forest", 10, 2, "grid_search", 10)
        
        # Demo 4: List supported models
        print("\n4️⃣ Supported Models...")
        self.list_supported_models()
        
        print("\n🎉 Demo completed successfully!")

    def run_smoke_tests(self):
        """Run comprehensive smoke tests"""
        print("🧪 Running ML Robot System Smoke Tests...")
        print("=" * 50)
        
        tests_passed = 0
        total_tests = 4
        
        # Test 1: Types module
        try:
            from robot_types import run_smoke_test
            if run_smoke_test():
                tests_passed += 1
                print("✅ Types module smoke test passed")
            else:
                print("❌ Types module smoke test failed")
        except Exception as e:
            print(f"❌ Types module smoke test failed: {e}")
        
        # Test 2: Core module
        try:
            from robot_core import run_smoke_test
            if run_smoke_test():
                tests_passed += 1
                print("✅ Core module smoke test passed")
            else:
                print("❌ Core module smoke test failed")
        except Exception as e:
            print(f"❌ Core module smoke test failed: {e}")
        
        # Test 3: Execution module
        try:
            from robot_execution import run_smoke_test
            if run_smoke_test():
                tests_passed += 1
                print("✅ Execution module smoke test passed")
            else:
                print("❌ Execution module smoke test failed")
        except Exception as e:
            print(f"❌ Execution module smoke test failed: {e}")
        
        # Test 4: CLI functionality
        try:
            self.list_supported_models()
            tests_passed += 1
            print("✅ CLI functionality smoke test passed")
        except Exception as e:
            print(f"❌ CLI functionality smoke test failed: {e}")
        
        print(f"\n📊 Smoke Test Results: {tests_passed}/{total_tests} tests passed")
        
        if tests_passed == total_tests:
            print("🎉 All smoke tests passed!")
            return True
        else:
            print("❌ Some smoke tests failed!")
            return False


def run_smoke_test():
    """Run smoke test for robot CLI module"""
    print("🧪 Testing ML Robot CLI Module...")
    
    try:
        # Test CLI initialization
        cli = MLRobotCLI()
        assert cli.maker is not None
        assert cli.creator is not None
        assert cli.trainer is not None
        assert cli.evaluator is not None
        assert cli.optimizer is not None
        print("✅ CLI initialization smoke test passed")

        # Test supported models listing
        cli.list_supported_models()
        print("✅ Supported models listing smoke test passed")

        print("🎉 All robot CLI smoke tests passed!")
        return True

    except Exception as e:
        print(f"❌ Robot CLI smoke test failed: {e}")
        return False


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="ML Robot CLI - Automated ML Model Creation")
    
    parser.add_argument("--create", action="store_true", help="Create a model")
    parser.add_argument("--auto", action="store_true", help="Auto-create best model")
    parser.add_argument("--optimize", action="store_true", help="Optimize hyperparameters")
    parser.add_argument("--list", action="store_true", help="List supported models")
    parser.add_argument("--demo", action="store_true", help="Run complete demo")
    parser.add_argument("--smoke", action="store_true", help="Run smoke tests")
    
    # Model creation parameters
    parser.add_argument("--model-type", default="classification", help="Model type")
    parser.add_argument("--algorithm", default="neural_network", help="Algorithm")
    parser.add_argument("--input-features", type=int, default=10, help="Input features")
    parser.add_argument("--output-classes", type=int, default=2, help="Output classes")
    parser.add_argument("--architecture", help="Model architecture")
    
    # Dataset parameters
    parser.add_argument("--data-path", help="Dataset path")
    parser.add_argument("--data-type", default="csv", help="Dataset type")
    parser.add_argument("--target-column", help="Target column")
    
    # Optimization parameters
    parser.add_argument("--optimization-method", default="grid_search", help="Optimization method")
    parser.add_argument("--max-trials", type=int, default=50, help="Maximum trials")
    
    args = parser.parse_args()
    
    cli = MLRobotCLI()
    
    if args.smoke:
        cli.run_smoke_tests()
    elif args.demo:
        cli.run_demo()
    elif args.create:
        cli.create_model(
            args.model_type, args.algorithm, args.input_features,
            args.output_classes, args.architecture
        )
    elif args.auto:
        if not args.data_path or not args.target_column:
            print("❌ --data-path and --target-column required for auto creation")
            sys.exit(1)
        cli.auto_create_model(args.data_path, args.data_type, args.target_column)
    elif args.optimize:
        cli.optimize_hyperparameters(
            args.model_type, args.algorithm, args.input_features,
            args.output_classes, args.optimization_method, args.max_trials
        )
    elif args.list:
        cli.list_supported_models()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
