#!/usr/bin/env python3
"""
ML Robot Package - V2 Core ML Robot System
==========================================

Refactored ML Robot system following V2 coding standards.
Split from monolithic test_ml_robot_maker.py into focused modules.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from .robot_types import (
    ModelConfig, TrainingConfig, DatasetConfig, ModelResult
)

from .robot_core import MLRobotMaker

from .robot_execution import (
    ModelCreator, ModelTrainer, ModelEvaluator, HyperparameterOptimizer
)

from .robot_cli import MLRobotCLI, run_smoke_test

__all__ = [
    # Types and data classes
    'ModelConfig', 'TrainingConfig', 'DatasetConfig', 'ModelResult',

    # Core ML Robot Maker
    'MLRobotMaker',

    # Execution components
    'ModelCreator', 'ModelTrainer', 'ModelEvaluator', 'HyperparameterOptimizer',

    # CLI interface
    'MLRobotCLI', 'run_smoke_test'
]

__version__ = "2.0.0"
__author__ = "Agent-2 (Architecture & Design Specialist)"
