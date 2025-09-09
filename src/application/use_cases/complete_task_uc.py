"""
Complete Task Use Case - Application Layer
==========================================

Use case for completing tasks.
Handles the business logic of task completion.
"""

from dataclasses import dataclass

from ...domain.domain_events import TaskCompleted
from ...domain.entities.agent import Agent
from ...domain.entities.task import Task
from ...domain.ports.agent_repository import AgentRepository
from ...domain.ports.logger import Logger
from ...domain.ports.message_bus import MessageBus
from ...domain.ports.task_repository import TaskRepository
from ...domain.value_objects.ids import AgentId, TaskId


@dataclass
class CompleteTaskRequest:
    """Request DTO for task completion."""

    task_id: str
    agent_id: str  # Agent completing the task


@dataclass
class CompleteTaskResponse:
    """Response DTO for task completion."""

    success: bool
    task: Task | None = None
    agent: Agent | None = None
    error_message: str | None = None


class CompleteTaskUseCase:
    """
    Use case for completing tasks.

    This use case handles the business logic of marking tasks as complete
    and updating the relevant entities.
    """

    def __init__(
        self,
        tasks: TaskRepository,
        agents: AgentRepository,
        message_bus: MessageBus,
        logger: Logger,
    ):
        self.tasks = tasks
        self.agents = agents
        self.message_bus = message_bus
        self.logger = logger

    def execute(self, request: CompleteTaskRequest) -> CompleteTaskResponse:
        """
        Execute the task completion use case.

        Args:
            request: The completion request

        Returns:
            Response indicating success/failure and relevant data
        """
        try:
            # Retrieve the task
            task = self.tasks.get(TaskId(request.task_id))
            if not task:
                return CompleteTaskResponse(
                    success=False, error_message=f"Task {request.task_id} not found"
                )

            # Verify task is assigned to the requesting agent
            if task.assigned_agent_id != AgentId(request.agent_id):
                return CompleteTaskResponse(
                    success=False,
                    error_message=f"Task {request.task_id} is not assigned to agent {request.agent_id}",
                )

            # Retrieve the agent
            agent = self.agents.get(AgentId(request.agent_id))
            if not agent:
                return CompleteTaskResponse(
                    success=False, error_message=f"Agent {request.agent_id} not found"
                )

            # Complete the task
            task.complete()
            agent.complete_task(task.id)

            # Save changes
            self.tasks.save(task)
            self.agents.save(agent)

            # Publish domain event
            event = TaskCompleted(
                event_id=f"task-completed-{task.id}-{agent.id}",
                task_id=task.id,
                agent_id=agent.id,
                completed_at=task.completed_at,
            )

            self.message_bus.publish("task.completed", event.to_dict())

            # Log success
            self.logger.info(
                "Task completed successfully",
                task_id=task.id,
                agent_id=agent.id,
                completion_time=task.completed_at.isoformat(),
            )

            return CompleteTaskResponse(success=True, task=task, agent=agent)

        except Exception as e:
            self.logger.error(
                "Task completion failed",
                task_id=request.task_id,
                agent_id=request.agent_id,
                error=str(e),
                exception=e,
            )
            return CompleteTaskResponse(success=False, error_message=f"Completion failed: {str(e)}")
