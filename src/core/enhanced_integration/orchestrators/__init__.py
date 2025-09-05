"""
Enhanced Integration Orchestrators - V2 Compliant Modular Architecture
=====================================================================

Modular enhanced integration orchestration system with clean separation of concerns.
Each module handles a specific aspect of integration orchestration.

V2 Compliance: < 300 lines per module, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from .enhanced_integration_orchestrator import EnhancedIntegrationOrchestrator
from .task_processor import IntegrationTaskProcessor
from .performance_monitor import PerformanceMonitor
from .coordination_engine import CoordinationEngine

__all__ = [
    'EnhancedIntegrationOrchestrator',
    'IntegrationTaskProcessor',
    'PerformanceMonitor', 
    'CoordinationEngine'
]
