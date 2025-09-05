#!/usr/bin/env python3
"""
DRY Eliminator Package - V2 Compliance
======================================

Modular advanced DRY violation elimination system with V2 compliance.
Replaces the monolithic advanced_dry_eliminator.py.

Package Structure:
- dry_eliminator_models.py: Data models and configuration
- dry_elimination_engine.py: Core engine for violation detection and elimination
- dry_eliminator_orchestrator.py: Main orchestrator and unified interface

V2 Compliance: Modular design, single responsibility, dependency injection.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

# Import main classes for easy access
from .dry_eliminator_models import (
    DRYEliminatorConfig,
    DRYViolation,
    EliminationResult,
    EliminationMetrics,
    DRYViolationType,
    EliminationStrategy,
    ViolationSeverity,
    create_default_config,
    create_dry_violation,
    create_elimination_result,
    create_elimination_metrics,
    DEFAULT_VIOLATION_TYPES,
    ELIMINATION_EFFORT_LEVELS,
    VIOLATION_SEVERITY_SCORES
)

from .dry_elimination_engine import DRYEliminationEngine

from .dry_eliminator_orchestrator import (
    AdvancedDRYEliminator,
    UnifiedEntryPoint,
    get_advanced_dry_eliminator,
    eliminate_advanced_dry_violations,
    main
)

# Package metadata
__version__ = "2.0.0"
__author__ = "Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager"
__description__ = "Modular advanced DRY violation elimination system with V2 compliance"

# Export main interface functions
__all__ = [
    # Core classes
    "AdvancedDRYEliminator",
    "DRYEliminationEngine",
    "UnifiedEntryPoint",
    
    # Data models
    "DRYEliminatorConfig",
    "DRYViolation",
    "EliminationResult",
    "EliminationMetrics",
    
    # Enums
    "DRYViolationType",
    "EliminationStrategy",
    "ViolationSeverity",
    
    # Factory functions
    "create_default_config",
    "create_dry_violation",
    "create_elimination_result",
    "create_elimination_metrics",
    
    # Constants
    "DEFAULT_VIOLATION_TYPES",
    "ELIMINATION_EFFORT_LEVELS",
    "VIOLATION_SEVERITY_SCORES",
    
    # Main interface functions
    "get_advanced_dry_eliminator",
    "eliminate_advanced_dry_violations",
    "main"
]
