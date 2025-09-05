#!/usr/bin/env python3
"""
ML Learning Engine Orchestrator - V2 Compliant Redirect
======================================================

V2 compliance redirect to modular ML learning engine system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular ML learning engine
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_ml_learning import (
    MLLearningEngineOrchestrator,
    MLLearningEngine,
    MLLearningCoordinator
)

# Factory function for backward compatibility
def create_ml_learning_engine_orchestrator():
    """Create ML learning engine orchestrator."""
    return MLLearningEngineOrchestrator()

# Re-export for backward compatibility
__all__ = [
    'MLLearningEngineOrchestrator',
    'MLLearningEngine',
    'MLLearningCoordinator',
    'create_ml_learning_engine_orchestrator'
]