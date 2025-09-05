#!/usr/bin/env python3
"""
Utility Consolidation Package - V2 Compliance Module
===================================================

Modular utility consolidation system for V2 compliance.
Replaces monolithic utility_consolidation_coordinator.py.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

from .utility_consolidation_models import (
    ConsolidationType,
    UtilityFunction,
    ConsolidationOpportunity,
)
from .utility_consolidation_engine import UtilityConsolidationEngine
from .utility_consolidation_orchestrator import UtilityConsolidationOrchestrator

__all__ = [
    'ConsolidationType',
    'UtilityFunction', 
    'ConsolidationOpportunity',
    'UtilityConsolidationEngine',
    'UtilityConsolidationOrchestrator',
]
