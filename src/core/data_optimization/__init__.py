#!/usr/bin/env python3
"""
Data Optimization Package - V2 Compliance Module
===============================================

Modular data processing optimization system for V2 compliance.
Replaces monolithic data_processing_optimizer_orchestrator.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .data_optimization_models import (
    ProcessingStrategy,
    OptimizationLevel,
    ProcessingMetrics,
    OptimizationConfig,
)
from .data_optimization_engine import DataOptimizationEngine
from .data_optimization_orchestrator import (
    DataProcessingOptimizer,
    get_data_processing_optimizer,
    optimize_data_processing,
    get_optimization_metrics,
    clear_optimization_cache,
    reset_optimization_metrics,
)

__all__ = [
    'ProcessingStrategy',
    'OptimizationLevel',
    'ProcessingMetrics',
    'OptimizationConfig',
    'DataOptimizationEngine',
    'DataProcessingOptimizer',
    'get_data_processing_optimizer',
    'optimize_data_processing',
    'get_optimization_metrics',
    'clear_optimization_cache',
    'reset_optimization_metrics',
]
