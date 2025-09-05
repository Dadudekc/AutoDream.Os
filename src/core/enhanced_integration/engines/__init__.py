"""
Enhanced Integration Engines Package
====================================

Modular integration engines for V2 compliance.
Extracted from monolithic enhanced_integration_orchestrator.py.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

from .integration_optimization_engine import IntegrationOptimizationEngine
from .integration_coordination_engine import IntegrationCoordinationEngine

__all__ = [
    'IntegrationOptimizationEngine',
    'IntegrationCoordinationEngine'
]
