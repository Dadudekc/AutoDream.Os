"""
Unified Integration Coordinator Package
=====================================

Modular integration coordination system.
V2 Compliance: Clean, focused, single-responsibility modules.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from .coordinator import UnifiedIntegrationCoordinator
from .models import IntegrationModels
from .optimizer import IntegrationOptimizer
from .monitor import IntegrationMonitor

__all__ = [
    'UnifiedIntegrationCoordinator',
    'IntegrationModels', 
    'IntegrationOptimizer',
    'IntegrationMonitor'
]
