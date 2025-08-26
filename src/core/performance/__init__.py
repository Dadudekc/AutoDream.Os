#!/usr/bin/env python3
"""
Performance Module - Agent Cellphone V2
======================================

Modular performance system with monitoring, validation, benchmarking, and reporting.
Follows V2 standards: SRP, OOP design, modular architecture.

Author: Agent-1 (Phase 3 Modularization)
License: MIT
"""

# Core performance system
from .performance_core import PerformanceCore, PerformanceCoreConfig

# Specialized components
from .performance_monitoring import PerformanceMonitoringManager
from .performance_validation import PerformanceValidationManager
from .performance_benchmarking import PerformanceBenchmarkingManager
from .performance_reporting import PerformanceReportingManager

# Main orchestrator (replaces large unified system)
from .unified_performance_orchestrator import UnifiedPerformanceOrchestrator, UnifiedPerformanceSystem

# Models and types
from .performance_models import (
    PerformanceMetric, ValidationRule, ValidationThreshold, ConnectionPool,
    BenchmarkResult, SystemPerformanceReport, PerformanceConfig, PerformanceLevel,
    ValidationSeverity, BenchmarkType, MetricType, PerformanceAlert,
    PerformanceOptimization, PerformanceTrend, ResourceUtilization, PerformanceBaseline
)

# Factory functions for easy component creation
def create_performance_core(manager_id: str, name: str = "Performance Core", description: str = "") -> PerformanceCore:
    """Create a new performance core instance."""
    return PerformanceCore(manager_id, name, description)

def create_performance_monitoring_manager() -> PerformanceMonitoringManager:
    """Create a new performance monitoring manager instance."""
    return PerformanceMonitoringManager()

def create_performance_validation_manager() -> PerformanceValidationManager:
    """Create a new performance validation manager instance."""
    return PerformanceValidationManager()

def create_performance_benchmarking_manager() -> PerformanceBenchmarkingManager:
    """Create a new performance benchmarking manager instance."""
    return PerformanceBenchmarkingManager()

def create_performance_reporting_manager() -> PerformanceReportingManager:
    """Create a new performance reporting manager instance."""
    return PerformanceReportingManager()

def create_unified_performance_orchestrator() -> UnifiedPerformanceOrchestrator:
    """Create a new unified performance orchestrator instance."""
    return UnifiedPerformanceOrchestrator()

# Backward compatibility aliases
UnifiedPerformanceSystemV2 = UnifiedPerformanceOrchestrator
PerformanceSystem = UnifiedPerformanceOrchestrator

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