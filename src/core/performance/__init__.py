#!/usr/bin/env python3
"""
Performance Package - Unified Performance Management System

This package provides modular performance management functionality
extracted from the massive unified_performance_system.py file to
achieve V2 compliance standards.

**SSOT IMPLEMENTATION**: All performance monitoring classes are now
consolidated into this package to eliminate duplication across the codebase.

Author: Agent-8 (Technical Debt Specialist)
License: MIT
"""

# SSOT: Single source of truth for all performance monitoring classes
from .monitoring.performance_monitor import (
    PerformanceMonitor,
    MetricType,
    MonitorMetric,
    MonitorSnapshot,
    PerformanceLevel
)

from .performance_core import (
    PerformanceLevel as CorePerformanceLevel,
    ValidationSeverity,
    BenchmarkType,
    MetricType as CoreMetricType,
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

# SSOT: Unified interface - all other performance monitors should import from here
__all__ = [
    # Core unified performance monitor (SSOT)
    'PerformanceMonitor',
    'MetricType', 
    'MonitorMetric',
    'MonitorSnapshot',
    'PerformanceLevel',
    
    # Core performance system
    'CorePerformanceLevel',
    'ValidationSeverity',
    'BenchmarkType',
    'CoreMetricType',
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
]

# SSOT: Deprecation warnings for old imports
import warnings

def _deprecation_warning(old_path: str, new_path: str):
    """Generate deprecation warning for old import paths"""
    warnings.warn(
        f"Import from '{old_path}' is deprecated. Use '{new_path}' instead for SSOT compliance.",
        DeprecationWarning,
        stacklevel=2
    )

# SSOT: Backward compatibility aliases (with deprecation warnings)
def get_performance_monitor(*args, **kwargs):
    """SSOT: Get unified performance monitor instance"""
    _deprecation_warning(
        "src.services.performance_monitor.PerformanceMonitor",
        "src.core.performance.PerformanceMonitor"
    )
    return PerformanceMonitor(*args, **kwargs)

def get_metrics_collector(*args, **kwargs):
    """SSOT: Get unified metrics collector"""
    _deprecation_warning(
        "src.services.performance_monitor.MetricsCollector", 
        "src.core.performance.monitoring.performance_monitor.PerformanceMonitor"
    )
    return PerformanceMonitor(*args, **kwargs)