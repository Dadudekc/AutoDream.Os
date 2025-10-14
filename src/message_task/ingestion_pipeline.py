#!/usr/bin/env python3
"""
Message Ingestion Pipeline
===========================

Main entry point for message-to-task ingestion.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging

from .emitters import TaskEmitter, send_task_created_ack
from .router import MessageTaskRouter
from .schemas import InboundMessage

logger = logging.getLogger(__name__)


class MessageTaskPipeline:
    """Complete message-to-task ingestion pipeline."""

    def __init__(self, task_repository, messaging_bus=None):
        """
        Initialize pipeline.

        Args:
            task_repository: SqliteTaskRepository instance
            messaging_bus: Messaging system for notifications
        """
        self.router = MessageTaskRouter(task_repository)
        self.emitter = TaskEmitter(messaging_bus)
        self.repo = task_repository

    def process(self, msg: InboundMessage) -> str | None:
        """
        Process inbound message.

        Args:
            msg: Inbound message

        Returns:
            Task ID or None
        """
        logger.info(f"Processing message {msg.id} from {msg.author} via {msg.channel}")

        # Ingest message via router
        task_id = self.router.ingest(msg)

        if task_id:
            # Get task for title
            try:
                task = self.repo.get(task_id)
                title = getattr(task, "title", "Unknown") if task else "Unknown"
            except:
                title = "Unknown"

            # Send acknowledgment
            send_task_created_ack(task_id=task_id, title=title, msg_id=msg.id, bus=self.emitter)

            logger.info(f"✅ Message {msg.id} → Task {task_id}")
            return task_id
        else:
            logger.info(f"Message {msg.id} did not produce a task")
            return None


def handle_inbound(msg: InboundMessage, repo, bus=None) -> str | None:
    """
    Handle inbound message (convenience function).

    Args:
        msg: Inbound message
        repo: Task repository
        bus: Messaging bus

    Returns:
        Task ID or None
    """
    pipeline = MessageTaskPipeline(repo, bus)
    return pipeline.process(msg)
