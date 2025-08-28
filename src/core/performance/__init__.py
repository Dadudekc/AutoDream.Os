#!/usr/bin/env python3
"""
Performance Package - Cleaned Performance Management System

This package provides modular performance management functionality
after comprehensive cleanup and consolidation.

**CLEANUP COMPLETED**: Removed 13+ duplicate files, consolidated systems,
and optimized performance monitoring for V2 compliance standards.

Author: Agent-6 (Performance Validation Manager)
License: MIT
"""

# Core performance monitoring
from .monitoring.performance_monitor import (
    PerformanceMonitor,
    MetricType,
    MonitorMetric,
    MonitorSnapshot,
    PerformanceLevel
)

# Core performance system
from .performance_core import (
    PerformanceLevel as CorePerformanceLevel,
    ValidationSeverity,
    BenchmarkType,
    MetricType as CoreMetricType,
    PerformanceMetric,
    ValidationRule,
    ValidationThreshold,
    PerformanceBenchmark,
    PerformanceResult
)

# Essential management classes
from .performance_validator import PerformanceValidator
from .performance_reporter import PerformanceReporter
from .performance_config import PerformanceConfig, PerformanceConfigManager

# Connection management
from .connection.connection_pool_manager import ConnectionPoolManager

# Benchmarking and validation
from .benchmark_runner import BenchmarkRunner
from .performance_calculator import PerformanceCalculator
from .performance_validation_system import PerformanceValidationSystem

# Clean interface - only essential components
__all__ = [
    # Core monitoring
    'PerformanceMonitor',
    'MetricType', 
    'MonitorMetric',
    'MonitorSnapshot',
    'PerformanceLevel',
    
    # Core system
    'CorePerformanceLevel',
    'ValidationSeverity',
    'BenchmarkType',
    'CoreMetricType',
    'PerformanceMetric',
    'ValidationRule',
    'ValidationThreshold',
    'PerformanceBenchmark',
    'PerformanceResult',
    
    # Management classes
    'PerformanceValidator',
    'PerformanceReporter',
    'PerformanceConfig',
    'PerformanceConfigManager',
    
    # Connection management
    'ConnectionPoolManager',
    
    # Benchmarking
    'BenchmarkRunner',
    'PerformanceCalculator',
    'PerformanceValidationSystem'
]

# Cleanup status
CLEANUP_STATUS = {
    "status": "completed",
    "duplicate_files_removed": 13,
    "systems_consolidated": 3,
    "optimization_applied": True,
    "cleanup_date": "2025-01-27"
}

