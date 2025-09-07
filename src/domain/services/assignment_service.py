"""
Assignment Service - Domain Service
===================================

Domain service for task assignment logic.
Handles complex business rules that don't belong to individual entities.
"""

from typing import List, Optional
from src.domain.entities.task import Task
from src.domain.entities.agent import Agent
from src.domain.value_objects.ids import TaskId, AgentId
from src.domain.ports.logger import Logger


class AssignmentService:
    """
    Domain service for task assignment logic.

    This service contains business rules for assigning tasks to agents
    that involve multiple entities and complex logic.
    """

    def __init__(self, logger: Logger):
        self.logger = logger

    def find_best_agent_for_task(self, task: Task, available_agents: List[Agent]) -> Optional[Agent]:
        """
        Find the best agent for a given task based on business rules.

        Business Rules:
        - Agent must have required capabilities (if any)
        - Agent must be active and available
        - Prefer agents with lower workload
        - Consider agent specialization/role match

        Args:
            task: The task to assign
            available_agents: List of available agents

        Returns:
            Best matching agent or None if no suitable agent found
        """
        if not available_agents:
            return None

        # Filter agents that can handle the task
        suitable_agents = []
        for agent in available_agents:
            if self._can_agent_handle_task(agent, task):
                suitable_agents.append(agent)

        if not suitable_agents:
            return None

        # Score agents based on suitability
        scored_agents = []
        for agent in suitable_agents:
            score = self._calculate_agent_score(agent, task)
            scored_agents.append((agent, score))

        # Sort by score (higher is better)
        scored_agents.sort(key=lambda x: x[1], reverse=True)

        best_agent = scored_agents[0][0]
        self.logger.info(
            "Selected best agent for task",
            task_id=task.id,
            agent_id=best_agent.id,
            score=scored_agents[0][1]
        )

        return best_agent

    def validate_assignment(self, task: Task, agent: Agent) -> bool:
        """
        Validate if a task can be assigned to an agent.

        Args:
            task: The task to assign
            agent: The target agent

        Returns:
            True if assignment is valid
        """
        return self._can_agent_handle_task(agent, task)

    def _can_agent_handle_task(self, agent: Agent, task: Task) -> bool:
        """
        Check if an agent can handle a specific task.

        Business Rules:
        - Agent must be active
        - Agent must have capacity for more tasks
        - Agent must have required capabilities (future enhancement)
        """
        if not agent.is_active:
            return False

        if not agent.can_accept_more_tasks:
            return False

        # Future: Check for specific capabilities based on task requirements
        # For now, any active agent with capacity can handle any task

        return True

    def _calculate_agent_score(self, agent: Agent, task: Task) -> float:
        """
        Calculate how suitable an agent is for a task.

        Scoring factors:
        - Current workload (lower is better)
        - Agent specialization match (future enhancement)
        - Task priority alignment

        Returns:
            Score between 0.0 and 1.0 (higher is better)
        """
        # Base score from workload (inverse relationship)
        workload_factor = 1.0 - (agent.workload_percentage / 100.0)

        # Priority alignment (agents with higher capacity get priority tasks)
        capacity_factor = min(1.0, agent.max_concurrent_tasks / 5.0)

        # Task priority factor (higher priority tasks get slight preference)
        priority_factor = min(1.0, task.priority / 4.0)

        # Combine factors (weighted average)
        score = (workload_factor * 0.5) + (capacity_factor * 0.3) + (priority_factor * 0.2)

        return min(1.0, max(0.0, score))
