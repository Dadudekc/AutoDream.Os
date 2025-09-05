"""
DRY Eliminator Orchestrators - V2 Compliant Modular Architecture
================================================================

Modular orchestrator system for DRY violation elimination.
Each module handles a specific aspect of orchestration.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .dry_eliminator_orchestrator import AdvancedDRYEliminator
from .elimination_coordinator import EliminationCoordinator
from .results_manager import ResultsManager

__all__ = [
    'AdvancedDRYEliminator',
    'EliminationCoordinator', 
    'ResultsManager'
]
