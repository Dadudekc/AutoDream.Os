#!/usr/bin/env python3
"""
Performance Optimization Engine - V2 Compliant Redirect
=======================================================

V2 compliance redirect to modular performance optimization system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular performance optimization
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_performance import (
    PerformanceOptimizationOrchestrator,
    PerformanceModels,
    PerformanceEngine,
    PerformanceOptimizer
)

# Backward compatibility function
def get_optimization_engine():
    """Get optimization engine instance."""
    return PerformanceOptimizationOrchestrator()

# Re-export for backward compatibility
__all__ = [
    'PerformanceOptimizationOrchestrator',
    'PerformanceModels',
    'PerformanceEngine',
    'PerformanceOptimizer',
    'get_optimization_engine'
]