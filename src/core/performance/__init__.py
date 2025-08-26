#!/usr/bin/env python3
"""
Performance Package - Unified Performance Management System

This package provides modular performance management functionality
extracted from the massive unified_performance_system.py file to
achieve V2 compliance standards.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""

from .performance_core import (
    PerformanceLevel,
    ValidationSeverity,
    BenchmarkType,
    MetricType,
    PerformanceMetric,
    ValidationRule,
    ValidationThreshold,
    PerformanceBenchmark,
    PerformanceResult,
    UnifiedPerformanceSystem
)

from .performance_validator import PerformanceValidator
from .performance_reporter import PerformanceReporter
from .performance_config import PerformanceConfig, PerformanceConfigManager

# Factory functions for easy component creation
def create_performance_system() -> UnifiedPerformanceSystem:
    """Create a new performance system instance."""
    return UnifiedPerformanceSystem()

def create_performance_validator() -> PerformanceValidator:
    """Create a new performance validator instance."""
    return PerformanceValidator()

def create_performance_reporter() -> PerformanceReporter:
    """Create a new performance reporter instance."""
    return PerformanceReporter()

def create_performance_config_manager() -> PerformanceConfigManager:
    """Create a new performance configuration manager instance."""
    return PerformanceConfigManager()

# Export all components
__all__ = [
    # Core classes
    'PerformanceLevel',
    'ValidationSeverity',
    'BenchmarkType',
    'MetricType',
    'PerformanceMetric',
    'ValidationRule',
    'ValidationThreshold',
    'PerformanceBenchmark',
    'PerformanceResult',
    'UnifiedPerformanceSystem',
    
    # Management classes
    'PerformanceValidator',
    'PerformanceReporter',
    'PerformanceConfig',
    'PerformanceConfigManager',
    
    # Factory functions
    'create_performance_system',
    'create_performance_validator',
    'create_performance_reporter',
    'create_performance_config_manager'
]