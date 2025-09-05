"""
Unified Strategic Oversight Package
==================================

Modular strategic oversight system.
V2 Compliance: Clean, focused, single-responsibility modules.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from .orchestrator import StrategicOversightOrchestrator
from .models import StrategicOversightModels
from .engine import StrategicOversightEngine
from .analyzer import StrategicOversightAnalyzer

# Backward compatibility aliases
VectorStrategicOversightOrchestrator = StrategicOversightOrchestrator

__all__ = [
    'StrategicOversightOrchestrator',
    'StrategicOversightModels',
    'StrategicOversightEngine',
    'StrategicOversightAnalyzer',
    'VectorStrategicOversightOrchestrator'
]