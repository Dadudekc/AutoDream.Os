"""High level orchestrator for AI agent coordination.

This module stitches together the core coordination logic, task
management utilities and workload balancing.  External systems should
interact with :class:`AIAgentCoordinator` rather than individual
components to simplify integration and maintain a clear separation of
concerns.
"""
from __future__ import annotations

from typing import Dict, List

from .ai_agent_tasks import AIAgentTask
from .ai_agent_coordinator_core import AIAgentCoordinatorCore


class AIAgentCoordinator:
    """Facade providing a simplified interface for coordinating agents."""

    def __init__(self) -> None:
        self.core = AIAgentCoordinatorCore()

    def register_agent(self, agent_id: str) -> None:
        """Register an agent with the coordinator."""
        self.core.register_agent(agent_id)

    def add_task(self, task: AIAgentTask) -> None:
        """Submit a task for distribution."""
        self.core.submit_task(task)

    def distribute_tasks(self) -> Dict[str, List[AIAgentTask]]:
        """Distribute queued tasks among registered agents."""
        return self.core.distribute()

    def balance_workload(self) -> Dict[str, List[AIAgentTask]]:
        """Trigger workload balancing across agents."""
        return self.core.balance_workload()
