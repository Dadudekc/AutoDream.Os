#!/usr/bin/env python3
"""
Pattern Analysis Engine - V2 Compliant Redirect
===============================================

V2 compliance redirect to modular pattern analysis system.
Original monolithic implementation refactored into focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist (V2 Refactoring)
Created: 2025-01-28
Purpose: V2 compliant modular pattern analysis
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .orchestrator import PatternAnalysisOrchestrator
from .models import PatternAnalysisModels
from .engine_core import PatternAnalysisEngine
from .analyzer import PatternAnalyzer

# Re-export for backward compatibility
__all__ = [
    'PatternAnalysisOrchestrator',
    'PatternAnalysisModels',
    'PatternAnalysisEngine',
    'PatternAnalyzer'
]