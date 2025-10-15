"""
Autonomous Task Engine - Modular Architecture
=============================================

Refactored from 781-line monolith to clean modular system.

Modules:
- task_models.py: Data models (Task, AgentProfile, TaskRecommendation)
- task_discovery.py: Codebase scanning & task discovery
- task_scoring.py: ROI calculation & skill matching
- task_reporting.py: Recommendations & task claiming

Author: Agent-5 (Business Intelligence & Memory Safety)
Refactored: 2025-10-15 (Lean Excellence V2 Compliance)
"""

from .task_models import Task, AgentProfile, TaskRecommendation

__all__ = ['Task', 'AgentProfile', 'TaskRecommendation']

