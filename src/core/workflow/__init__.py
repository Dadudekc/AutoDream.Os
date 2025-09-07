#!/usr/bin/env python3
"""
Workflow System - Unified Workflow Management
============================================

Unified workflow management system following V2 standards.
Provides workflow orchestration, execution, and monitoring capabilities.

Author: Agent-8 (Integration Enhancement Manager)
License: MIT
"""

# Core workflow components
from .base_workflow_engine import BaseWorkflowEngine
from .core.workflow_engine import WorkflowEngine
from .core.workflow_monitor import WorkflowMonitor
from .types.workflow_models import WorkflowExecution, WorkflowTask, WorkflowStep
from .types.workflow_enums import WorkflowStatus, TaskStatus, WorkflowType

# Optimization components
from .optimizers.task_assignment_optimizer import TaskAssignmentOptimizer
from .optimization.phase_transition_workflow_analyzer import PhaseTransitionWorkflowAnalyzer

# Specialized workflows
from .specialized.business_process_workflow import BusinessProcessWorkflow

# Consolidated workflow manager (SSOT violation resolution)
from .consolidated_workflow_manager import ConsolidatedWorkflowManager

# Export main classes
__all__ = [
    "BaseWorkflowEngine",
    "WorkflowEngine", 
    "WorkflowMonitor",
    "WorkflowExecution",
    "WorkflowTask",
    "WorkflowStep",
    "WorkflowStatus",
    "TaskStatus",
    "WorkflowType",
    "TaskAssignmentOptimizer",
    "PhaseTransitionWorkflowAnalyzer",
    "BusinessProcessWorkflow",
    "ConsolidatedWorkflowManager"  # New consolidated manager
]
