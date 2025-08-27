#!/usr/bin/env python3
"""FSM task and communication operations mixin."""

import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .fsm_utils import (
    BridgeState,
    FSMCommunicationEvent,
    FSMTask,
    FSMUpdate,
    TaskPriority,
    TaskState,
)

logger = logging.getLogger(__name__)


class FSMOperationsMixin:
    """Mixin providing task and communication operations for the FSM system."""

    def create_task(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: TaskPriority = TaskPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Create a new FSM task."""
        try:
            task_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            task = FSMTask(
                id=task_id,
                title=title,
                description=description,
                state=TaskState.NEW,
                priority=priority,
                assigned_agent=assigned_agent,
                created_at=now,
                updated_at=now,
                metadata=metadata or {},
            )

            self._tasks[task_id] = task
            self._save_task(task)

            self._send_fsm_update(
                task_id, assigned_agent, TaskState.NEW, f"New task assigned: {title}"
            )

            logger.info("Created FSM task: %s", task_id)
            return task_id
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to create FSM task: {e}")
            return ""

    def send_communication_event(
        self,
        event_type: str,
        source_agent: str,
        target_agent: str,
        message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Send a communication event."""
        try:
            event_id = str(uuid.uuid4())
            now = datetime.now().isoformat()

            event = FSMCommunicationEvent(
                event_id=event_id,
                event_type=event_type,
                source_agent=source_agent,
                target_agent=target_agent,
                message=message,
                timestamp=now,
                metadata=metadata or {},
            )

            self._communication_events.append(event)
            self._save_communication_event(event)

            logger.info("Sent communication event: %s", event_id)
            return event_id
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to send communication event: {e}")
            return ""

    def get_communication_events(
        self,
        source_agent: Optional[str] = None,
        target_agent: Optional[str] = None,
        event_type: Optional[str] = None,
    ) -> List[FSMCommunicationEvent]:
        """Get communication events with optional filtering."""
        events = self._communication_events
        if source_agent:
            events = [e for e in events if e.source_agent == source_agent]
        if target_agent:
            events = [e for e in events if e.target_agent == target_agent]
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return events

    def update_bridge_state(self, bridge_id: str, new_state: BridgeState) -> bool:
        """Update bridge state."""
        try:
            self._bridge_states[bridge_id] = new_state
            logger.info("Updated bridge %s state: %s", bridge_id, new_state.value)
            return True
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to update bridge state: {e}")
            return False

    def get_bridge_state(self, bridge_id: str) -> Optional[BridgeState]:
        """Get bridge state."""
        return self._bridge_states.get(bridge_id)

    def get_all_bridge_states(self) -> Dict[str, BridgeState]:
        """Get all bridge states."""
        return dict(self._bridge_states)

    def _send_fsm_update(
        self,
        task_id: str,
        agent_id: str,
        state: TaskState,
        summary: str,
    ) -> None:
        """Send FSM update notification."""
        try:
            update = FSMUpdate(
                update_id=str(uuid.uuid4()),
                task_id=task_id,
                agent_id=agent_id,
                state=state,
                summary=summary,
                timestamp=datetime.now().isoformat(),
            )
            self._task_updates.append(update)
            logger.debug("FSM update sent: %s", update.update_id)
        except Exception as e:  # pragma: no cover - log failure path
            logger.error(f"Failed to send FSM update: {e}")
