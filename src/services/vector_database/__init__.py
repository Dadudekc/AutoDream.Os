#!/usr/bin/env python3
"""
Vector Database Package - V2 Compliance Module
=============================================

Modular vector database service for V2 compliance.
Replaces monolithic vector_database_service.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

try:  # pragma: no cover - optional dependencies
    from .vector_database_models import (
        VectorDatabaseConfig,
        VectorDatabaseStats,
        VectorDatabaseResult,
    )
    from .vector_database_engine import VectorDatabaseEngine
    from .vector_database_orchestrator import (
        VectorDatabaseService,
        get_vector_database_service,
        add_document_to_vector_db,
        search_vector_database,
        get_vector_database_stats,
    )
except Exception:  # noqa: BLE001
    VectorDatabaseConfig = None
    VectorDatabaseStats = None
    VectorDatabaseResult = None
    VectorDatabaseEngine = None
    VectorDatabaseService = None
    get_vector_database_service = None
    add_document_to_vector_db = None
    search_vector_database = None
    get_vector_database_stats = None
from .status_indexer import index_all_statuses

__all__ = [
    "VectorDatabaseConfig",
    "VectorDatabaseStats",
    "VectorDatabaseResult",
    "VectorDatabaseEngine",
    "VectorDatabaseService",
    "get_vector_database_service",
    "add_document_to_vector_db",
    "search_vector_database",
    "get_vector_database_stats",
    "index_all_statuses",
]
