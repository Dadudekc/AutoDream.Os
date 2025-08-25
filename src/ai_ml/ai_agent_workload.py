"""Workload tracking and balancing for AI agents.

The :class:`WorkloadManager` maintains a simple mapping of agent IDs to
assigned tasks.  It supports basic assignment and a naive balancing
strategy that redistributes tasks when one agent has significantly more
work than others.
"""
from __future__ import annotations

from collections import defaultdict, deque
from typing import DefaultDict, Deque, Dict, Iterable, List

from .ai_agent_tasks import AIAgentTask


class WorkloadManager:
    """Track and balance tasks across registered agents."""

    def __init__(self) -> None:
        self._workloads: DefaultDict[str, Deque[AIAgentTask]] = defaultdict(deque)

    def register_agent(self, agent_id: str) -> None:
        """Ensure an agent has an entry in the workload mapping."""
        self._workloads.setdefault(agent_id, deque())

    def assign_task(self, agent_id: str, task: AIAgentTask) -> None:
        """Assign a task to a specific agent."""
        self.register_agent(agent_id)
        self._workloads[agent_id].append(task)

    def get_workload(self, agent_id: str) -> List[AIAgentTask]:
        """Return a list of tasks for the given agent."""
        return list(self._workloads.get(agent_id, []))

    def balance(self) -> Dict[str, List[AIAgentTask]]:
        """Redistribute tasks so each agent has roughly equal work.

        The algorithm is intentionally simple: tasks are pooled and then
        round-robin assigned to agents.  The resulting mapping is
        returned for convenience.
        """
        agents = list(self._workloads)
        if not agents:
            return {}

        pool: Deque[AIAgentTask] = deque()
        for tasks in self._workloads.values():
            pool.extend(tasks)
            tasks.clear()

        while pool:
            for agent in agents:
                if pool:
                    self._workloads[agent].append(pool.popleft())
                else:
                    break
        return {agent: list(tasks) for agent, tasks in self._workloads.items()}

    def workloads(self) -> Dict[str, List[AIAgentTask]]:
        """Return a snapshot of all workloads without modification."""
        return {agent: list(tasks) for agent, tasks in self._workloads.items()}
