#!/usr/bin/env python3
"""
Performance Module - V2 Compliance Package
==========================================

Comprehensive performance monitoring, optimization, and dashboard system.
Provides real-time metrics, automatic optimization, and performance analytics.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from .performance_monitoring_system import (
    PerformanceMonitoringSystem,
    PerformanceMetric,
    PerformanceReport,
    create_performance_monitoring_system
)

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_performance import (
    PerformanceOptimizationOrchestrator,
    PerformanceModels,
    PerformanceEngine,
    PerformanceOptimizer
)

# Backward compatibility - re-export models
from .unified_performance.models import (
    OptimizationRule,
    OptimizationResult,
    PerformanceMetrics,
    OptimizationConfig,
    OptimizationType,
    OptimizationStatus,
    OptimizationPriority
)

# Backward compatibility functions
def get_optimization_engine():
    """Get optimization engine instance."""
    return PerformanceOptimizationOrchestrator()

def start_performance_optimization():
    """Start performance optimization."""
    return True  # Mock implementation

def stop_performance_optimization():
    """Stop performance optimization."""
    return True  # Mock implementation

from .performance_dashboard import (
    PerformanceDashboard,
    get_performance_dashboard
)

__all__ = [
    # Monitoring
    'PerformanceMonitoringSystem',
    'PerformanceMetric',
    'PerformanceReport',
    'create_performance_monitoring_system',
    
    # Optimization (V2 Compliant)
    'PerformanceOptimizationOrchestrator',
    'PerformanceModels',
    'PerformanceEngine',
    'PerformanceOptimizer',
    'OptimizationRule',
    'OptimizationResult',
    'PerformanceMetrics',
    'OptimizationConfig',
    'OptimizationType',
    'OptimizationStatus',
    'OptimizationPriority',
    'get_optimization_engine',
    'start_performance_optimization',
    'stop_performance_optimization',
    
    # Dashboard
    'PerformanceDashboard',
    'get_performance_dashboard'
]

__version__ = "1.0.0"
__author__ = "Agent-2 - Architecture & Design Specialist"
