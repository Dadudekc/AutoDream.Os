#!/usr/bin/env python3
"""
Vector Strategic Oversight Orchestrator - V2 Compliant Redirect
==============================================================

V2 compliance redirect to modular strategic oversight system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-27
Purpose: V2 compliant modular strategic oversight orchestration
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_strategic_oversight import (
    VectorStrategicOversightOrchestrator,
    StrategicOversightModels,
    StrategicOversightEngine,
    StrategicOversightAnalyzer
)

# Re-export for backward compatibility
__all__ = [
    'VectorStrategicOversightOrchestrator',
    'StrategicOversightModels',
    'StrategicOversightEngine',
    'StrategicOversightAnalyzer'
]