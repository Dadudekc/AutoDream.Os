#!/usr/bin/env python3
"""
DRY Elimination Engine - V2 Compliant Redirect
==============================================

V2 COMPLIANT: Modular architecture with clean separation of concerns.
Original monolithic implementation refactored into focused modules.

@version 2.0.0 - V2 COMPLIANCE MODULAR REFACTOR
@license MIT
"""

# Import the new modular orchestrator
from .engines import (
    DRYEliminationEngineOrchestrator,
    create_dry_elimination_engine_orchestrator,
    FileDiscoveryEngine,
    CodeAnalysisEngine,
    ViolationDetectionEngine,
    EliminationStrategyEngine,
    MetricsReportingEngine
)

# Re-export for backward compatibility
DRYEliminationEngine = DRYEliminationEngineOrchestrator

# Export all public interfaces
__all__ = [
    'DRYEliminationEngine',
    'DRYEliminationEngineOrchestrator',
    'create_dry_elimination_engine_orchestrator',
    'FileDiscoveryEngine',
    'CodeAnalysisEngine',
    'ViolationDetectionEngine',
    'EliminationStrategyEngine',
    'MetricsReportingEngine'
]
