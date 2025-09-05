#!/usr/bin/env python3
"""
DRY Elimination Engines Package
===============================

Modular DRY elimination engine system.
V2 COMPLIANT: Clean, focused, modular architecture.

@version 1.0.0 - V2 COMPLIANCE MODULAR PACKAGE
@license MIT
"""

# Import main orchestrator
from .dry_elimination_engine_orchestrator import (
    DRYEliminationEngineOrchestrator,
    create_dry_elimination_engine_orchestrator
)

# Import individual engines
from .file_discovery_engine import (
    FileDiscoveryEngine,
    create_file_discovery_engine
)

from .code_analysis_engine import (
    CodeAnalysisEngine,
    create_code_analysis_engine
)

from .violation_detection_engine import (
    ViolationDetectionEngine,
    create_violation_detection_engine
)

from .elimination_strategy_engine import (
    EliminationStrategyEngine,
    create_elimination_strategy_engine
)

from .metrics_reporting_engine import (
    MetricsReportingEngine,
    create_metrics_reporting_engine
)

# Export all public interfaces
__all__ = [
    # Main orchestrator
    'DRYEliminationEngineOrchestrator',
    'create_dry_elimination_engine_orchestrator',
    
    # Individual engines
    'FileDiscoveryEngine',
    'create_file_discovery_engine',
    'CodeAnalysisEngine',
    'create_code_analysis_engine',
    'ViolationDetectionEngine',
    'create_violation_detection_engine',
    'EliminationStrategyEngine',
    'create_elimination_strategy_engine',
    'MetricsReportingEngine',
    'create_metrics_reporting_engine'
]
