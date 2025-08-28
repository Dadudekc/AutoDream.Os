"""Coordination layer tying parsing, routing and scheduling together."""

import logging
from typing import Dict, List, Any, Optional

from .coordinator_types import (
    AgentCapability,
    CommunicationMode,
    CoordinationMessage,
    CoordinationSession,
    TaskPriority,
    TaskStatus,
)
from .message_parser import MessageParser
from .message_router import MessageRouter
from .task_scheduler import TaskScheduler
from .utils import generate_id, current_timestamp

logger = logging.getLogger(__name__)


class MessageCoordinator:
    """High level coordination service for agents."""

    def __init__(self):
        self.parser = MessageParser()
        self.router = MessageRouter()
        self.scheduler = TaskScheduler()
        self.agents: Dict[str, AgentCapability] = {}
        self.tasks = self.scheduler.tasks
        self.messages: Dict[str, CoordinationMessage] = {}
        self.sessions: Dict[str, CoordinationSession] = {}

    # ------------------------------------------------------------------
    # Agent management
    # ------------------------------------------------------------------
    def register_agent(
        self, agent_id: str, capabilities: List[str], specializations: List[str]
    ) -> bool:
        """Register an agent with capabilities."""
        self.agents[agent_id] = AgentCapability(
            agent_id=agent_id,
            capabilities=capabilities,
            specializations=specializations,
            availability=True,
            current_load=0,
            max_capacity=1,
        )
        logger.info("Registered agent %s", agent_id)
        return True

    # ------------------------------------------------------------------
    # Task operations (delegated to scheduler)
    # ------------------------------------------------------------------
    def create_task(
        self,
        title: str,
        description: str,
        priority: TaskPriority,
        assigned_agents: List[str],
    ) -> str:
        return self.scheduler.create_task(title, description, priority, assigned_agents)

    def assign_task(self, task_id: str, agent_id: str) -> bool:
        return self.scheduler.assign_task(task_id, agent_id)

    def update_task_status(
        self, task_id: str, status: TaskStatus, progress: float
    ) -> bool:
        return self.scheduler.update_task_status(task_id, status, progress)

    # ------------------------------------------------------------------
    # Messaging
    # ------------------------------------------------------------------
    def send_message(
        self,
        sender_id: str,
        recipient_ids: List[str],
        message_type: str,
        content: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Parse, route and schedule a message."""
        message = self.parser.parse(
            sender_id,
            recipient_ids,
            message_type,
            content,
            priority,
            metadata,
        )
        routed = self.router.route(message, self.agents)
        message.recipient_ids = routed
        self.scheduler.schedule_message(message)
        self.messages[message.message_id] = message
        logger.info(
            "Queued message %s from %s to %s",
            message.message_id,
            sender_id,
            ",".join(routed),
        )
        return message.message_id

    # ------------------------------------------------------------------
    # Coordination sessions
    # ------------------------------------------------------------------
    def create_coordination_session(
        self, mode: CommunicationMode, participants: List[str], agenda: List[str]
    ) -> str:
        """Create a coordination session record."""
        session_id = generate_id()
        session = CoordinationSession(
            session_id=session_id,
            mode=mode,
            participants=participants,
            start_time=current_timestamp(),
            end_time=None,
            agenda=agenda,
            decisions=[],
        )
        self.sessions[session_id] = session
        logger.info("Created coordination session %s", session_id)
        return session_id
