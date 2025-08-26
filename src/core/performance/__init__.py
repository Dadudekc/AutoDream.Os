#!/usr/bin/env python3
"""
Performance Module - Agent Cellphone V2
======================================

Modular performance system with monitoring, validation, benchmarking, and reporting.
Follows V2 standards: SRP, OOP design, modular architecture.

Author: Agent-1 (Phase 3 Modularization)
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
    # Core system
    "PerformanceCore",
    "PerformanceCoreConfig",
    "UnifiedPerformanceOrchestrator",
    "UnifiedPerformanceSystem",
    
    # Specialized components
    "PerformanceMonitoringManager",
    "PerformanceValidationManager",
    "PerformanceBenchmarkingManager",
    "PerformanceReportingManager",
    
    # Models and types
    "PerformanceMetric",
    "ValidationRule",
    "ValidationThreshold",
    "ConnectionPool",
    "BenchmarkResult",
    "SystemPerformanceReport",
    "PerformanceConfig",
    "PerformanceLevel",
    "ValidationSeverity",
    "BenchmarkType",
    "MetricType",
    "PerformanceAlert",
    "PerformanceOptimization",
    "PerformanceTrend",
    "ResourceUtilization",
    "PerformanceBaseline",
    
    # Factory functions
    "create_performance_core",
    "create_performance_monitoring_manager",
    "create_performance_validation_manager",
    "create_performance_benchmarking_manager",
    "create_performance_reporting_manager",
    "create_unified_performance_orchestrator",
    
    # Backward compatibility
    "UnifiedPerformanceSystemV2",
    "PerformanceSystem"
]