#!/usr/bin/env python3
"""
Learning Modules Package - Agent Cellphone V2
===========================================

Modularized learning components extracted from unified_learning_engine.py.
Follows V2 standards: clean architecture, SRP, maintainable code.

**Author:** Captain Agent-3 (MODULAR-007 Contract)
**Created:** Current Sprint
**Status:** ACTIVE - MODULARIZATION COMPLETE
"""

from .learning_algorithms import LearningAlgorithmsModule
from .data_processing import DataProcessingModule, DataProcessingResult
from .model_management import ModelManagementModule, ModelType, ModelStatus
from .interfaces import UnifiedLearningInterface, LearningModuleInterface

__all__ = [
    # Core modules
    "LearningAlgorithmsModule",
    "DataProcessingModule", 
    "DataProcessingResult",
    "ModelManagementModule",
    "ModelType",
    "ModelStatus",
    
    # Interfaces
    "UnifiedLearningInterface",
    "LearningModuleInterface",
]

__version__ = "1.0.0"
__author__ = "Captain Agent-3"
__status__ = "ACTIVE - MODULARIZATION COMPLETE"
