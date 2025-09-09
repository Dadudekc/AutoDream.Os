"""
Assign Task Use Case - Application Layer
========================================

Use case for assigning tasks to agents.
Orchestrates domain objects to fulfill the business requirement.
"""

from dataclasses import dataclass

from ...domain.domain_events import TaskAssigned
from ...domain.entities.agent import Agent
from ...domain.entities.task import Task
from ...domain.ports.agent_repository import AgentRepository
from ...domain.ports.logger import Logger
from ...domain.ports.message_bus import MessageBus
from ...domain.ports.task_repository import TaskRepository
from ...domain.services.assignment_service import AssignmentService
from ...domain.value_objects.ids import AgentId, TaskId


@dataclass
class AssignTaskRequest:
    """Request DTO for task assignment."""

    task_id: str
    agent_id: str | None = None  # If None, auto-assign best agent


@dataclass
class AssignTaskResponse:
    """Response DTO for task assignment."""

    success: bool
    task: Task | None = None
    agent: Agent | None = None
    error_message: str | None = None


class AssignTaskUseCase:
    """
    Use case for assigning tasks to agents.

    This use case orchestrates the domain objects to fulfill
    the business requirement of task assignment.
    """

    def __init__(
        self,
        tasks: TaskRepository,
        agents: AgentRepository,
        message_bus: MessageBus,
        logger: Logger,
        assignment_service: AssignmentService,
    ):
        self.tasks = tasks
        self.agents = agents
        self.message_bus = message_bus
        self.logger = logger
        self.assignment_service = assignment_service

    def execute(self, request: AssignTaskRequest) -> AssignTaskResponse:
        """
        Execute the task assignment use case.

        Args:
            request: The assignment request

        Returns:
            Response indicating success/failure and relevant data
        """
        try:
            # Retrieve the task
            task = self.tasks.get(TaskId(request.task_id))
            if not task:
                return AssignTaskResponse(
                    success=False, error_message=f"Task {request.task_id} not found"
                )

            # Determine target agent
            if request.agent_id:
                # Manual assignment
                agent = self.agents.get(AgentId(request.agent_id))
                if not agent:
                    return AssignTaskResponse(
                        success=False, error_message=f"Agent {request.agent_id} not found"
                    )

                # Validate assignment
                if not self.assignment_service.validate_assignment(task, agent):
                    return AssignTaskResponse(
                        success=False,
                        error_message=f"Agent {request.agent_id} cannot handle task {request.task_id}",
                    )
            else:
                # Auto-assignment - find best agent
                available_agents = list(self.agents.get_available())
                agent = self.assignment_service.find_best_agent_for_task(task, available_agents)

                if not agent:
                    return AssignTaskResponse(
                        success=False, error_message="No suitable agent available for task"
                    )

            # Perform assignment
            task.assign_to(agent.id)
            agent.assign_task(task.id)

            # Save changes
            self.tasks.save(task)
            self.agents.save(agent)

            # Publish domain event
            event = TaskAssigned(
                event_id=f"task-assigned-{task.id}-{agent.id}",
                task_id=task.id,
                agent_id=agent.id,
                assigned_at=task.assigned_at,
            )

            self.message_bus.publish("task.assigned", event.to_dict())

            # Log success
            self.logger.info(
                "Task assigned successfully",
                task_id=task.id,
                agent_id=agent.id,
                assignment_type="manual" if request.agent_id else "auto",
            )

            return AssignTaskResponse(success=True, task=task, agent=agent)

        except Exception as e:
            self.logger.error(
                "Task assignment failed",
                task_id=request.task_id,
                agent_id=request.agent_id,
                error=str(e),
                exception=e,
            )
            return AssignTaskResponse(success=False, error_message=f"Assignment failed: {str(e)}")
