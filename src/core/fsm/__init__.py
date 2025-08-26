#!/usr/bin/env python3
"""
FSM Package - V2 Modular Architecture
=====================================

Modular FSM system following V2 standards.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

# Core FSM components
from .fsm_core import FSMCore, FSMCoreV2
from .workflow_executor import WorkflowExecutor
from .task_manager import TaskManager
from .communication_bridge import CommunicationBridge
from .performance_analyzer import PerformanceAnalyzer
from .system_orchestrator import SystemOrchestrator

# Data models and types
from .models import StateStatus, TransitionType, WorkflowPriority, TaskState, TaskPriority
from .types import FSMConfig, FSMStrategy

__all__ = [
    # Core components
    'FSMCore',
    'WorkflowExecutor', 
    'TaskManager',
    'CommunicationBridge',
    'PerformanceAnalyzer',
    'SystemOrchestrator',

    # Data models
    'StateStatus',
    'TransitionType', 
    'WorkflowPriority',
    'TaskState',
    'TaskPriority',

    # Types
    'FSMConfig',
    'FSMStrategy',
    'FSMCoreV2'
]
