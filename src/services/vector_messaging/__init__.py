#!/usr/bin/env python3
"""
Vector Messaging Package - V2 Compliant
=======================================

Modular vector messaging integration system.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
Created: 2025-01-27
Purpose: V2 compliant vector messaging package
"""

from .vector_messaging_orchestrator import (
    VectorMessagingOrchestrator,
    get_vector_messaging_orchestrator
)
from .vector_messaging_models import (
    VectorDatabaseConfig,
    VectorDatabaseValidator,
    IndexingResult,
    SearchResultSummary,
    BatchIndexingResult,
    VectorMessagingMetrics
)
from .agent_enhancement_integrator import AgentEnhancementIntegrator
from .document_indexing_engine import DocumentIndexingEngine
from .search_query_engine import SearchQueryEngine

# Export main interfaces
__all__ = [
    'VectorMessagingOrchestrator',
    'get_vector_messaging_orchestrator',
    'VectorDatabaseConfig',
    'VectorDatabaseValidator',
    'IndexingResult',
    'SearchResultSummary',
    'BatchIndexingResult',
    'VectorMessagingMetrics',
    'AgentEnhancementIntegrator',
    'DocumentIndexingEngine',
    'SearchQueryEngine'
]
