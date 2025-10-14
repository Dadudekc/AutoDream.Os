#!/usr/bin/env python3
"""
Task Message Emitters
=====================

Emits messages for task state changes and completions.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging
from typing import Any

from .schemas import TaskCompletionReport, TaskStateTransition

logger = logging.getLogger(__name__)


class TaskEmitter:
    """Emits task-related messages to messaging bus."""

    def __init__(self, messaging_bus=None):
        """
        Initialize emitter.

        Args:
            messaging_bus: Messaging system instance
        """
        self.bus = messaging_bus

    def emit(self, content: str, recipient: str = "CAPTAIN", priority: str = "regular"):
        """
        Emit message via messaging bus.

        Args:
            content: Message content
            recipient: Message recipient
            priority: Message priority
        """
        if not self.bus:
            logger.warning("No messaging bus configured - message not sent")
            logger.info(f"Would send: {content[:100]}...")
            return

        try:
            # Use messaging core to send
            from src.core.messaging_core import (
                UnifiedMessagePriority,
                UnifiedMessageType,
                send_message,
            )

            priority_enum = (
                UnifiedMessagePriority.URGENT
                if priority == "urgent"
                else UnifiedMessagePriority.REGULAR
            )

            send_message(
                content=content,
                sender="TASK_SYSTEM",
                recipient=recipient,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=priority_enum,
            )

            logger.info(f"✅ Message emitted to {recipient}")

        except Exception as e:
            logger.error(f"❌ Failed to emit message: {e}")


def on_task_state_change(
    task: Any, transition: TaskStateTransition, bus: TaskEmitter | None = None
):
    """
    Notify on task state change.

    Args:
        task: Task object
        transition: State transition details
        bus: Message emitter
    """
    if not bus:
        bus = TaskEmitter()

    status_emoji = {
        "todo": "📋",
        "doing": "🔄",
        "blocked": "🚧",
        "done": "✅",
        "cancelled": "❌",
    }

    emoji = status_emoji.get(transition.to_state, "📝")

    message = f"""{emoji} Task State Changed: {transition.to_state.upper()}

Task ID: {transition.task_id}
From: {transition.from_state} → To: {transition.to_state}
Event: {transition.event}

Task: {getattr(task, 'title', 'Unknown')}
"""

    # Determine recipient (assignee or captain)
    recipient = getattr(task, "assigned_agent_id", None) or "CAPTAIN"

    bus.emit(message, recipient=recipient, priority="regular")


def send_completion_report(
    task: Any,
    result: dict[str, Any],
    agent_id: str,
    bus: TaskEmitter | None = None,
):
    """
    Send task completion report.

    Args:
        task: Task object
        result: Completion result dict
        agent_id: Agent who completed task
        bus: Message emitter
    """
    if not bus:
        bus = TaskEmitter()

    # Create completion report
    report = TaskCompletionReport(
        task_id=str(getattr(task, "id", "unknown")),
        title=getattr(task, "title", "Unknown Task"),
        agent_id=agent_id,
        status=result.get("status", "completed"),
        summary=result.get("summary", "Task completed"),
        metadata=result.get("metadata", {}),
    )

    # Format and send message
    message = report.format_message()

    # Send to captain
    priority = "urgent" if result.get("status") == "failed" else "regular"
    bus.emit(message, recipient="CAPTAIN", priority=priority)

    # Also send ack to agent
    if agent_id != "CAPTAIN":
        ack_message = f"✅ Task completion acknowledged: {report.title}"
        bus.emit(ack_message, recipient=agent_id, priority="regular")


def send_task_created_ack(task_id: str, title: str, msg_id: str, bus: TaskEmitter | None = None):
    """
    Send acknowledgment that task was created from message.

    Args:
        task_id: Created task ID
        title: Task title
        msg_id: Source message ID
        bus: Message emitter
    """
    if not bus:
        bus = TaskEmitter()

    message = f"""📝 Task Created from Message

Task ID: {task_id}
Title: {title}
Source Message: {msg_id}

Use --get-next-task to claim this task.
"""

    bus.emit(message, recipient="CAPTAIN", priority="regular")
