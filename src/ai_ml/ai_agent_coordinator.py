"""High level orchestrator for AI agent coordination - MIGRATED TO UNIFIED LEARNING ENGINE.

This module stitches together the unified learning engine coordination capabilities.
External systems should interact with :class:`AIAgentCoordinator` rather than individual
components to simplify integration and maintain a clear separation of
concerns.
"""
from __future__ import annotations

from typing import Dict, List

from .ai_agent_tasks import AIAgentTask
# ARCHITECTURE CORRECTED: Using decision manager from decision module
from ..core.decision import DecisionManager
from ..core.learning import UnifiedLearningEngine


class AIAgentCoordinator:
    """Facade providing a simplified interface for coordinating agents - MIGRATED TO UNIFIED ENGINE."""

    def __init__(self) -> None:
        # MIGRATED: Using unified learning engine instead of local AIAgentCoordinatorCore
        self.learning_engine = UnifiedLearningEngine()
        self.decision_manager = DecisionManager()

    def register_agent(self, agent_id: str) -> None:
        """Register an agent with the coordinator - MIGRATED TO UNIFIED ENGINE."""
        # MIGRATED: Using unified learning engine coordination
        self.learning_engine.register_agent_for_coordination(agent_id)

    def add_task(self, task: AIAgentTask) -> None:
        """Submit a task for distribution - MIGRATED TO UNIFIED ENGINE."""
        # MIGRATED: Using unified learning engine task management
        self.learning_engine.submit_coordination_task(task)

    def distribute_tasks(self) -> Dict[str, List[AIAgentTask]]:
        """Distribute queued tasks among registered agents - MIGRATED TO UNIFIED ENGINE."""
        # MIGRATED: Using unified learning engine distribution
        return self.learning_engine.distribute_coordination_tasks()

    def balance_workload(self) -> Dict[str, List[AIAgentTask]]:
        """Trigger workload balancing across agents - MIGRATED TO UNIFIED ENGINE."""
        # MIGRATED: Using unified learning engine workload balancing
        return self.learning_engine.balance_coordination_workload()
