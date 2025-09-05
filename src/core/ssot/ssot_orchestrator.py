#!/usr/bin/env python3
"""
SSOT Orchestrator - V2 Compliant Redirect
=========================================

V2 compliance redirect to modular SSOT system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: V2 compliant modular SSOT orchestration
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_ssot import (
    UnifiedSSOTOrchestrator,
    SSOTModels,
    SSOTExecutor,
    SSOTValidator
)

# Backward compatibility function
def get_unified_ssot_orchestrator():
    """Get unified SSOT orchestrator instance."""
    return UnifiedSSOTOrchestrator()

# Re-export for backward compatibility
__all__ = [
    'UnifiedSSOTOrchestrator',
    'SSOTModels',
    'SSOTExecutor', 
    'SSOTValidator',
    'get_unified_ssot_orchestrator'
]
