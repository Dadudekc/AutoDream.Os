#!/usr/bin/env python3
"""
Autonomous Development Module - Agent Cellphone V2
=================================================

Autonomous agent development and coordination system.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

from .core import DevelopmentTask, TaskPriority, TaskComplexity, TaskStatus, AgentRole
from core.task_manager import DevelopmentTaskManager as TaskManager
from .tasks import TaskRegistry
from .agents import AgentCoordinator, AgentWorkflow
from .workflow import WorkflowEngine, WorkflowMonitor
from .communication import DevelopmentCommunication

__all__ = [
    # Core data models
    'DevelopmentTask', 'TaskPriority', 'TaskComplexity', 'TaskStatus', 'AgentRole',
    
    # Task management
    'TaskManager', 'TaskRegistry',
    
    # Agent coordination
    'AgentCoordinator', 'AgentWorkflow',
    
    # Workflow systems
    'WorkflowEngine', 'WorkflowMonitor',
    
    # Communication
    'DevelopmentCommunication'
]
