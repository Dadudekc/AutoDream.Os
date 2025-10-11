"""
Orchestrator Event Management
==============================

Event system for orchestrator event coordination extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OrchestratorEvents:
    """Manages orchestrator event system."""

    def __init__(self, orchestrator_name: str):
        """Initialize event manager."""
        self.orchestrator_name = orchestrator_name
        self._event_listeners: dict[str, list[callable]] = {}
        self.logger = logging.getLogger(f"orchestrator.{orchestrator_name}.events")

    def on(self, event: str, callback: callable) -> None:
        """Register event listener."""
        if event not in self._event_listeners:
            self._event_listeners[event] = []

        if callback not in self._event_listeners[event]:
            self._event_listeners[event].append(callback)
            self.logger.debug(f"Event listener registered: {event}")

    def off(self, event: str, callback: callable) -> None:
        """Unregister event listener."""
        if event in self._event_listeners and callback in self._event_listeners[event]:
            self._event_listeners[event].remove(callback)
            self.logger.debug(f"Event listener removed: {event}")

            if not self._event_listeners[event]:
                del self._event_listeners[event]

    def emit(self, event: str, data: Any = None) -> None:
        """Emit event to all registered listeners."""
        if event not in self._event_listeners:
            return

        for callback in self._event_listeners[event]:
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in event handler for {event}: {e}")

    def clear_listeners(self, event: str | None = None) -> None:
        """Clear event listeners."""
        if event:
            if event in self._event_listeners:
                del self._event_listeners[event]
                self.logger.debug(f"Cleared listeners for event: {event}")
        else:
            self._event_listeners.clear()
            self.logger.debug("Cleared all event listeners")
