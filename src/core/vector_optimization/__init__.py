#!/usr/bin/env python3
"""
Vector Optimization Package - V2 Compliance Module
=================================================

Modular vector database optimization system for V2 compliance.
Replaces monolithic vector_database_optimizer.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .vector_optimization_models import (
    CacheStrategy,
    VectorSearchConfig,
    VectorSearchResult,
    PerformanceMetrics,
)
from .vector_optimization_engine import VectorOptimizationEngine
from .vector_optimization_orchestrator import (
    VectorDatabaseOptimizer,
    get_vector_database_optimizer,
    create_optimized_vector_search,
    vector_search_cached,
    vector_search_async,
    performance_monitored,
)

__all__ = [
    'CacheStrategy',
    'VectorSearchConfig',
    'VectorSearchResult',
    'PerformanceMetrics',
    'VectorOptimizationEngine',
    'VectorDatabaseOptimizer',
    'get_vector_database_optimizer',
    'create_optimized_vector_search',
    'vector_search_cached',
    'vector_search_async',
    'performance_monitored',
]
