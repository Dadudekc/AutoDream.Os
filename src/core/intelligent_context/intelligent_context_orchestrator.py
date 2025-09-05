#!/usr/bin/env python3
"""
Intelligent Context Orchestrator - V2 Compliant Redirect
========================================================

V2 compliance redirect to modular intelligent context system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: V2 compliant modular intelligent context orchestration
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_intelligent_context import (
    IntelligentContextRetrieval,
    IntelligentContextModels,
    IntelligentContextEngine,
    IntelligentContextSearch
)

# Re-export for backward compatibility
__all__ = [
    'IntelligentContextRetrieval',
    'IntelligentContextModels',
    'IntelligentContextEngine',
    'IntelligentContextSearch'
]