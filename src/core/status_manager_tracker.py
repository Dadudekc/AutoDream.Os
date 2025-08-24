#!/usr/bin/env python3
"""Status tracking utilities for the Status Manager.

Provides methods for monitoring agent status changes and generating
associated alerts and events.
"""

import json
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .agent_manager import AgentStatus
from .health.core import AlertLevel
from .status_manager_config import Alert, StatusEvent, StatusTransition


class StatusTrackerMixin:
    """Mixin providing status tracking behaviour."""

    status_callbacks: Dict[str, List[Callable]]
    status_events: Dict[str, StatusEvent]
    alerts: Dict[str, Alert]

    def _status_monitoring_loop(self) -> None:
        """Main status monitoring loop."""
        while self.running:
            try:
                self._check_agent_status_changes()
                self._process_status_transitions()
                time.sleep(10)
            except Exception as e:  # pragma: no cover - defensive logging
                self.logger.error(f"Status monitoring loop error: {e}")
                time.sleep(30)

    def _check_agent_status_changes(self) -> None:
        """Check for agent status changes."""
        try:
            current_agents = self.agent_manager.get_all_agents()
            for agent_id, agent_info in current_agents.items():
                current_status = agent_info.status
                previous_status = self._get_previous_status(agent_id)
                if previous_status and previous_status != current_status:
                    self._handle_status_change(agent_id, previous_status, current_status)
                self._update_previous_status(agent_id, current_status)
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to check agent status changes: {e}")

    def _get_previous_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get previous status for an agent."""
        try:
            status_file = Path(f"status_cache/{agent_id}_status.json")
            if status_file.exists():
                with open(status_file, "r") as f:
                    data = json.load(f)
                    return AgentStatus(data.get("status"))
            return None
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to get previous status for {agent_id}: {e}")
            return None

    def _update_previous_status(self, agent_id: str, status: AgentStatus) -> None:
        """Update previous status for an agent."""
        try:
            status_dir = Path("status_cache")
            status_dir.mkdir(exist_ok=True)
            status_file = status_dir / f"{agent_id}_status.json"
            with open(status_file, "w") as f:
                json.dump({"status": status.value, "timestamp": datetime.now().isoformat()}, f)
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to update previous status for {agent_id}: {e}")

    def _handle_status_change(self, agent_id: str, old_status: AgentStatus, new_status: AgentStatus) -> None:
        """Handle agent status change."""
        try:
            transition = self._determine_transition(old_status, new_status)
            event = StatusEvent(
                event_id=str(uuid.uuid4()),
                agent_id=agent_id,
                old_status=old_status,
                new_status=new_status,
                transition=transition,
                timestamp=datetime.now().isoformat(),
                metadata={"old_status": old_status.value, "new_status": new_status.value},
            )
            self.status_events[event.event_id] = event
            self._trigger_status_callbacks(agent_id, event)
            if self._should_generate_alert(transition):
                self._generate_status_alert(event)
            self.logger.info(
                f"Status change detected for {agent_id}: {old_status.value} -> {new_status.value}"
            )
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to handle status change for {agent_id}: {e}")

    def _determine_transition(self, old_status: AgentStatus, new_status: AgentStatus) -> StatusTransition:
        """Determine the type of status transition."""
        try:
            if old_status == AgentStatus.ONLINE and new_status == AgentStatus.OFFLINE:
                return StatusTransition.ONLINE_TO_OFFLINE
            if old_status == AgentStatus.OFFLINE and new_status == AgentStatus.ONLINE:
                return StatusTransition.OFFLINE_TO_ONLINE
            if old_status == AgentStatus.IDLE and new_status == AgentStatus.BUSY:
                return StatusTransition.IDLE_TO_BUSY
            if old_status == AgentStatus.BUSY and new_status == AgentStatus.IDLE:
                return StatusTransition.BUSY_TO_IDLE
            if old_status == AgentStatus.HEALTHY and new_status == AgentStatus.WARNING:
                return StatusTransition.HEALTHY_TO_WARNING
            if old_status == AgentStatus.WARNING and new_status == AgentStatus.CRITICAL:
                return StatusTransition.WARNING_TO_CRITICAL
            return StatusTransition.ONLINE_TO_OFFLINE
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to determine transition: {e}")
            return StatusTransition.ONLINE_TO_OFFLINE

    def _should_generate_alert(self, transition: StatusTransition) -> bool:
        """Determine if an alert should be generated for a transition."""
        try:
            critical = {
                StatusTransition.ONLINE_TO_OFFLINE,
                StatusTransition.HEALTHY_TO_WARNING,
                StatusTransition.WARNING_TO_CRITICAL,
            }
            return transition in critical
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to determine alert generation: {e}")
            return False

    def _generate_status_alert(self, event: StatusEvent) -> None:
        """Generate alert for status change."""
        try:
            alert_level = (
                AlertLevel.ERROR
                if event.transition in [
                    StatusTransition.ONLINE_TO_OFFLINE,
                    StatusTransition.WARNING_TO_CRITICAL,
                ]
                else AlertLevel.WARNING
            )
            alert = Alert(
                alert_id=str(uuid.uuid4()),
                level=alert_level,
                message=
                f"Agent {event.agent_id} status changed: {event.old_status.value} -> {event.new_status.value}",
                source="status_manager",
                timestamp=datetime.now().isoformat(),
                acknowledged=False,
                metadata={"event_id": event.event_id, "transition": event.transition.value},
            )
            self.alerts[alert.alert_id] = alert
            self.logger.info(f"Generated status alert: {alert.alert_id}")
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to generate status alert: {e}")

    def _process_status_transitions(self) -> None:
        """Process pending status transitions."""
        try:
            pass
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to process status transitions: {e}")

    def _trigger_status_callbacks(self, agent_id: str, event: StatusEvent) -> None:
        """Trigger status change callbacks."""
        try:
            if agent_id in self.status_callbacks:
                for callback in self.status_callbacks[agent_id]:
                    try:
                        callback(event)
                    except Exception as e:  # pragma: no cover - defensive logging
                        self.logger.error(f"Callback execution failed: {e}")
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to trigger status callbacks: {e}")

    def register_status_callback(self, agent_id: str, callback: Callable[[StatusEvent], None]) -> None:
        """Register callback for status changes."""
        try:
            self.status_callbacks.setdefault(agent_id, []).append(callback)
            self.logger.info(f"Registered status callback for {agent_id}")
        except Exception as e:  # pragma: no cover - defensive logging
            self.logger.error(f"Failed to register status callback: {e}")


__all__ = ["StatusTrackerMixin"]
