import logging

logger = logging.getLogger(__name__)
"""
Task_Handlers Module

This module provides service functionality for the swarm system.

Component Type: Service
Priority: High
Dependencies: None


EXAMPLE USAGE:
==============

# Import the service
from src.services.messaging.task_handlers import Task_HandlersService

# Initialize service
service = Task_HandlersService()

# Basic service operation
response = service.handle_request(request_data)
logger.info(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Task_HandlersService)

# Execute service method
result = service.execute_operation(input_data, context)
logger.info(f"Operation result: {result}")

"""
from __future__ import annotations

from typing import Any

# Use consolidated messaging service for broadcast functionality
from .delivery.pyautogui_delivery import deliver_message_pyautogui
from .models import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageTag, UnifiedMessageType
from .service import MessagingService
from .shared.messaging_utilities import get_messaging_utilities


def claim_task(agent: str) -> dict[str, Any] | None:
    # plug in your real queue here
    import random
    import uuid

    if random.random() < 0.3:
        return None
    return {
        "task_id": f"TASK-{uuid.uuid4().hex[:8].upper()}",
        "title": "Comprehensive Code Review",
        "priority": "High",
    }


def handle_claim(agent: str) -> str:
    t = claim_task(agent)
    if t:
        return f"✅ Task {t['task_id']} assigned to {agent}\nTitle: {t['title']}"
    # notify Captain-4
    utils = get_messaging_utilities()
    coords = utils.get_agent_coordinates("Agent-4")
    if coords:
        msg = UnifiedMessage(
            content=f"🚨 TASK QUEUE EMPTY — {agent} requested work",
            sender="TaskManagementSystem",
            recipient="Agent-4",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.URGENT,
            tags=[UnifiedMessageTag.TASK],
        )
        deliver_message_pyautogui(msg, coords)
    return f"⚠️ No tasks available for {agent}. Captain notified."


def handle_complete(agent: str, task_id: str, notes: str) -> str:
    utils = get_messaging_utilities()
    coords = utils.get_agent_coordinates(agent)
    svc = MessagingService()
    body = f"✅ TASK COMPLETED\nID: {task_id}\nBy: {agent}\nNotes: {notes}"
    if coords:
        msg = UnifiedMessage(
            content=body,
            sender="ConsolidatedMessagingService",
            recipient=agent,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
        )
        ok = deliver_message_pyautogui(msg, coords)
    else:
        ok = svc.send(agent, body)
    # Inform Captain
    svc.send(
        "Agent-4", f"📋 COMPLETION REPORT\nID: {task_id}\nBy: {agent}\nNotes: {notes}", tag="TASK"
    )
    return "✅ Reported" if ok else "❌ Delivery failed"
