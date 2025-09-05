"""
Unified Integration Coordinator - V2 Compliance
==============================================

V2 compliant modular integration coordination system.
Refactored from monolithic 16.6 KB file to focused modules.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

# V2 COMPLIANCE REDIRECT - Import from modular system
from .unified_integration import (
    UnifiedIntegrationCoordinator,
    IntegrationModels,
    IntegrationOptimizer,
    IntegrationMonitor
)

# Re-export for backward compatibility
__all__ = [
    'UnifiedIntegrationCoordinator',
    'IntegrationModels',
    'IntegrationOptimizer',
    'IntegrationMonitor'
]