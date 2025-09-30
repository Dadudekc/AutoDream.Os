#!/usr/bin/env python3
"""
Discord Commander Bot Events - Event handling
===========================================

Event handling extracted from bot.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


class DiscordBotEvents:
    """Discord bot event handling system."""

    def __init__(self, bot_core):
        """Initialize bot events."""
        self.bot_core = bot_core
        self.event_handlers: dict[str, list[Callable]] = {}
        self.event_stats: dict[str, int] = {}
        self._register_default_events()
        logger.info("Discord bot events initialized")

    def _register_default_events(self):
        """Register default event handlers."""
        self.register_event("on_ready", self.handle_ready)
        self.register_event("on_message", self.handle_message)
        self.register_event("on_error", self.handle_error)
        self.register_event("on_disconnect", self.handle_disconnect)
        self.register_event("on_reconnect", self.handle_reconnect)

    def register_event(self, event_name: str, handler: Callable):
        """Register an event handler."""
        if event_name not in self.event_handlers:
            self.event_handlers[event_name] = []
            self.event_stats[event_name] = 0

        self.event_handlers[event_name].append(handler)
        logger.info(f"Event handler registered for '{event_name}'")

    def unregister_event(self, event_name: str, handler: Callable):
        """Unregister an event handler."""
        if event_name in self.event_handlers:
            if handler in self.event_handlers[event_name]:
                self.event_handlers[event_name].remove(handler)
                logger.info(f"Event handler unregistered for '{event_name}'")

    async def trigger_event(self, event_name: str, *args, **kwargs) -> dict[str, Any]:
        """Trigger an event and call all registered handlers."""
        if event_name not in self.event_handlers:
            return {
                "success": False,
                "error": f"Event '{event_name}' not registered",
                "handlers_called": 0,
            }

        handlers_called = 0
        errors = []

        # Record event occurrence
        self.event_stats[event_name] += 1

        # Call all handlers for this event
        for handler in self.event_handlers[event_name]:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(*args, **kwargs)
                else:
                    handler(*args, **kwargs)
                handlers_called += 1
            except Exception as e:
                logger.error(f"Error in event handler for '{event_name}': {e}")
                errors.append(str(e))
                self.bot_core.record_error()

        return {
            "success": len(errors) == 0,
            "event_name": event_name,
            "handlers_called": handlers_called,
            "errors": errors,
            "timestamp": datetime.now().isoformat(),
        }

    def get_event_stats(self) -> dict[str, Any]:
        """Get event statistics."""
        return {
            "total_events": len(self.event_handlers),
            "event_occurrences": dict(self.event_stats),
            "most_frequent_event": max(self.event_stats.items(), key=lambda x: x[1])[0]
            if self.event_stats
            else None,
            "total_event_calls": sum(self.event_stats.values()),
            "timestamp": datetime.now().isoformat(),
        }

    def list_registered_events(self) -> list[str]:
        """List all registered events."""
        return list(self.event_handlers.keys())

    def get_event_handlers(self, event_name: str) -> list[Callable]:
        """Get handlers for a specific event."""
        return self.event_handlers.get(event_name, [])

    # Default event handlers
    async def handle_ready(self, *args, **kwargs):
        """Handle bot ready event."""
        logger.info("Discord Commander Bot is ready!")
        self.bot_core.set_status_message("Bot Ready - All Systems Operational")
        self.bot_core.set_healthy(True)

    async def handle_message(self, message=None, *args, **kwargs):
        """Handle message event."""
        if message:
            self.bot_core.record_message_processed()
            self.bot_core.update_activity()

            # Log message processing
            logger.debug(f"Message processed: {message.content[:50]}...")

    async def handle_error(self, error=None, *args, **kwargs):
        """Handle error event."""
        if error:
            logger.error(f"Bot error occurred: {error}")
            self.bot_core.record_error()
            self.bot_core.set_healthy(False)

    async def handle_disconnect(self, *args, **kwargs):
        """Handle disconnect event."""
        logger.warning("Bot disconnected from Discord")
        self.bot_core.set_status_message("Disconnected - Attempting Reconnection")
        self.bot_core.set_healthy(False)

    async def handle_reconnect(self, *args, **kwargs):
        """Handle reconnect event."""
        logger.info("Bot reconnected to Discord")
        self.bot_core.set_status_message("Reconnected - Systems Restored")
        self.bot_core.set_healthy(True)

    def create_custom_event(self, event_name: str, description: str = "") -> bool:
        """Create a custom event."""
        if event_name in self.event_handlers:
            logger.warning(f"Event '{event_name}' already exists")
            return False

        self.event_handlers[event_name] = []
        self.event_stats[event_name] = 0

        logger.info(f"Custom event '{event_name}' created: {description}")
        return True

    def remove_custom_event(self, event_name: str) -> bool:
        """Remove a custom event."""
        if event_name not in self.event_handlers:
            logger.warning(f"Event '{event_name}' does not exist")
            return False

        # Don't remove default events
        default_events = ["on_ready", "on_message", "on_error", "on_disconnect", "on_reconnect"]
        if event_name in default_events:
            logger.warning(f"Cannot remove default event '{event_name}'")
            return False

        del self.event_handlers[event_name]
        del self.event_stats[event_name]

        logger.info(f"Custom event '{event_name}' removed")
        return True

    def get_event_summary(self) -> dict[str, Any]:
        """Get event system summary."""
        return {
            "registered_events": len(self.event_handlers),
            "total_handlers": sum(len(handlers) for handlers in self.event_handlers.values()),
            "event_occurrences": self.event_stats,
            "most_active_event": max(self.event_stats.items(), key=lambda x: x[1])[0]
            if self.event_stats
            else None,
            "system_health": "Good" if self.bot_core.is_healthy else "Degraded",
            "timestamp": datetime.now().isoformat(),
        }

    def validate_event_system(self) -> dict[str, Any]:
        """Validate event system integrity."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "events_checked": len(self.event_handlers),
        }

        # Check for required default events
        required_events = ["on_ready", "on_message", "on_error"]
        for event in required_events:
            if event not in self.event_handlers:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Required event '{event}' not registered")

        # Check for events with no handlers
        for event_name, handlers in self.event_handlers.items():
            if not handlers:
                validation_result["warnings"].append(f"Event '{event_name}' has no handlers")

        # Check event naming convention
        for event_name in self.event_handlers.keys():
            if not event_name.startswith("on_"):
                validation_result["warnings"].append(
                    f"Event '{event_name}' doesn't follow naming convention"
                )

        return validation_result
