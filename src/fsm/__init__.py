"""
FSM Package - Finite State Machine Core System
==============================================

This package provides a modular FSM core system, breaking down the large
monolithic file into focused, maintainable modules.

Modules:
- core: Core FSM engine and state management
- orchestration: Workflow orchestration and coordination
- compliance: Compliance validation and auditing
- performance: Performance analysis and optimization
- interfaces: System interfaces and APIs
"""

from .core import FSMCore, StateManager, TransitionManager
from .orchestration import WorkflowOrchestrator, TaskScheduler
from .compliance import ComplianceValidator, AuditReporter
from .performance import PerformanceAnalyzer, MetricsCollector

__all__ = [
    'FSMCore', 'StateManager', 'TransitionManager',
    'WorkflowOrchestrator', 'TaskScheduler',
    'ComplianceValidator', 'AuditReporter',
    'PerformanceAnalyzer', 'MetricsCollector'
]
