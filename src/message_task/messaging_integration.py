#!/usr/bin/env python3
"""
Messaging System Integration
=============================

Hooks message-task pipeline into existing messaging infrastructure.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging

from src.infrastructure.persistence.sqlite_task_repo import SqliteTaskRepository

from .ingestion_pipeline import MessageTaskPipeline
from .schemas import InboundMessage

logger = logging.getLogger(__name__)

# Global pipeline instance
_pipeline: MessageTaskPipeline | None = None


def get_pipeline() -> MessageTaskPipeline:
    """Get or create global message-task pipeline."""
    global _pipeline
    if _pipeline is None:
        repo = SqliteTaskRepository("data/tasks.db")
        _pipeline = MessageTaskPipeline(repo)
    return _pipeline


def process_message_for_task(
    message_id: str,
    content: str,
    author: str,
    channel: str = "messaging",
) -> str | None:
    """
    Process message and potentially create task.

    Args:
        message_id: Message ID
        content: Message content
        author: Message author
        channel: Message channel

    Returns:
        Task ID if task created, None otherwise
    """
    # Create inbound message
    msg = InboundMessage(
        id=message_id,
        channel=channel,
        author=author,
        content=content,
    )

    # Process via pipeline
    pipeline = get_pipeline()
    return pipeline.process(msg)


def should_create_task_from_message(content: str) -> bool:
    """
    Determine if message should create a task.

    Args:
        content: Message content

    Returns:
        True if message looks like task request
    """
    content_lower = content.lower()

    # Task indicators
    task_keywords = [
        "task:",
        "todo:",
        "fix:",
        "implement",
        "create",
        "add",
        "build",
        "refactor",
        "bug:",
        "feature:",
    ]

    return any(keyword in content_lower for keyword in task_keywords)
