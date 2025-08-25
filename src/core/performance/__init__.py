#!/usr/bin/env python3
"""
Performance Validation System - Unified Module Package
=====================================================

This package contains the consolidated performance validation system modules
that have been extracted and unified from multiple scattered files.

Author: Performance Validation Consolidation Team
License: MIT
"""

# Import the main classes for easy access
from .performance_core import (
    PerformanceValidationCore,
    BenchmarkResult,
    ValidationRule
)

from .performance_reporter import (
    PerformanceReporter,
    SystemPerformanceReport
)

from .performance_config import (
    PerformanceConfigManager,
    PerformanceValidationConfig,
    ValidationThreshold,
    BenchmarkConfig
)

from .performance_cli import PerformanceValidationCLI

from .performance_orchestrator import PerformanceValidationOrchestrator

# Import consolidated modules from deduplication effort
from .validation.validation_core import ValidationCore
from .models.data_models import PerformanceDataModel
from .types.enums import PerformanceMetricType, ValidationStatus
from .monitoring.performance_monitor import PerformanceMonitor
from .dashboard.performance_dashboard import PerformanceDashboard
from .models.performance_models import PerformanceModel

# Version information
__version__ = "2.0.0"
__author__ = "Performance Validation Consolidation Team"
__license__ = "MIT"

# Package metadata
__all__ = [
    # Core functionality
    "PerformanceValidationCore",
    "BenchmarkResult", 
    "ValidationRule",
    
    # Reporting
    "PerformanceReporter",
    "SystemPerformanceReport",
    
    # Configuration
    "PerformanceConfigManager",
    "PerformanceValidationConfig",
    "ValidationThreshold",
    "BenchmarkConfig",
    
    # CLI interface
    "PerformanceValidationCLI",
    
    # Main orchestrator
    "PerformanceValidationOrchestrator",
    
    # Consolidated modules from deduplication
    "ValidationCore",
    "PerformanceDataModel", 
    "PerformanceMetricType",
    "ValidationStatus",
    "PerformanceMonitor",
    "PerformanceDashboard",
    "PerformanceModel",
    
    # Version info
    "__version__",
    "__author__",
    "__license__"
]

# Convenience function to create a complete system
def create_performance_system(config_file: str = None):
    """
    Create a complete performance validation system with all components.
    
    Args:
        config_file: Optional path to configuration file
        
    Returns:
        PerformanceValidationOrchestrator instance
    """
    return PerformanceValidationOrchestrator(config_file)

# Quick access to main functionality
def run_smoke_test():
    """Run a quick smoke test to verify the system is working."""
    orchestrator = PerformanceValidationOrchestrator()
    return orchestrator.run_smoke_test()

def run_benchmark(benchmark_type: str = None):
    """
    Run a performance benchmark.
    
    Args:
        benchmark_type: Specific benchmark type or None for all
        
    Returns:
        Benchmark ID if successful
    """
    orchestrator = PerformanceValidationOrchestrator()
    if not orchestrator.start_system():
        return None
    
    try:
        if benchmark_type:
            # Run specific benchmark
            result = orchestrator._run_single_benchmark(benchmark_type)
            return result.benchmark_id if result else None
        else:
            # Run comprehensive benchmark
            return orchestrator.run_comprehensive_benchmark()
    finally:
        orchestrator.stop_system()

def get_system_status():
    """Get the current status of a performance validation system."""
    orchestrator = PerformanceValidationOrchestrator()
    return orchestrator.get_system_status()