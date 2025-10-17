"""
Autonomous Task Engine - Modular Implementation
==============================================
V2-compliant modular refactoring of autonomous_task_engine.py

This package enables agents to autonomously discover and select their optimal next task.

Usage (backward compatible):
    from tools.autonomous_task_engine import AutonomousTaskEngine
    
    engine = AutonomousTaskEngine()
    task = engine.get_optimal_task_for_agent("Agent-2")

Author: Agent-2 (Architecture & Design Specialist)
Date: 2025-10-16
License: MIT
"""

from .models import Task, AgentProfile, TaskRecommendation
from .engine import AutonomousTaskEngine
from .discovery import TaskDiscovery
from .scoring import TaskScoring

__all__ = [
    "Task",
    "AgentProfile", 
    "TaskRecommendation",
    "AutonomousTaskEngine",
    "TaskDiscovery",
    "TaskScoring",
]

