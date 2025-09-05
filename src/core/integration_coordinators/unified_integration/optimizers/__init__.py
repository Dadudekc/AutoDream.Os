"""
Unified Integration Optimizers - V2 Compliant Modular Architecture
=================================================================

Modular optimizer system for integration coordination.
Each module handles a specific aspect of optimization.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .optimizer import IntegrationOptimizer
from .basic_optimizer import BasicOptimizer
from .advanced_optimizer import AdvancedOptimizer
from .maximum_optimizer import MaximumOptimizer

__all__ = [
    'IntegrationOptimizer',
    'BasicOptimizer',
    'AdvancedOptimizer',
    'MaximumOptimizer'
]
