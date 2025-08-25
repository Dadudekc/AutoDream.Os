"""Core coordination logic for AI agents.

This module encapsulates the central operations for coordinating
multiple AI agents.  It combines a task queue with workload management to
provide registration, task submission and distribution features.  The
higher level orchestrator can build upon this core to integrate with
specific agent implementations or communication layers.
"""
from __future__ import annotations

from typing import Dict, Iterable, List, Tuple

from .ai_agent_tasks import AIAgentTask, TaskQueue
from .ai_agent_workload import WorkloadManager


class AIAgentCoordinatorCore:
    """Coordinate agents and distribute tasks among them."""

    def __init__(self) -> None:
        self.task_queue = TaskQueue()
        self.workload = WorkloadManager()
        self.agents: List[str] = []

    def register_agent(self, agent_id: str) -> None:
        """Register a new agent with the coordinator."""
        if agent_id not in self.agents:
            self.agents.append(agent_id)
            self.workload.register_agent(agent_id)

    def submit_task(self, task: AIAgentTask) -> None:
        """Add a task to the central queue."""
        self.task_queue.add_task(task)

    def distribute(self) -> Dict[str, List[AIAgentTask]]:
        """Assign queued tasks to registered agents.

        Tasks are dequeued in FIFO order and assigned in a round-robin
        fashion.  After distribution, a snapshot of the workloads is
        returned.
        """
        if not self.agents:
            return {}

        agent_index = 0
        while self.task_queue.has_tasks():
            task = self.task_queue.get_next_task()
            if task is None:
                break
            agent_id = self.agents[agent_index]
            self.workload.assign_task(agent_id, task)
            agent_index = (agent_index + 1) % len(self.agents)

        return self.workload.workloads()

    def balance_workload(self) -> Dict[str, List[AIAgentTask]]:
        """Rebalance tasks across agents for even distribution."""
        return self.workload.balance()
