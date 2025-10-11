"""
Base GUI Controller - V2 Compliant
==================================

Base controller for GUI applications with PyAutoGUI integration.
Provides common functionality for agent selection and command execution.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - GUI Specialist
License: MIT
"""

import logging
from collections.abc import Callable
from typing import Any

# V2 Integration imports (uses shared utils for fallbacks)
from ..utils import get_coordinate_loader, get_logger

# Messaging integration
try:
    from ...core.messaging_pyautogui import send_message_to_agent
except ImportError:

    def send_message_to_agent(*args, **kwargs):
        logging.info(f"Mock message send: {args}, {kwargs}")
        return True


class BaseGUIController:
    """
    Base controller for GUI applications.

    Provides common functionality for:
    - Agent selection management
    - Command execution framework
    - PyAutoGUI integration
    - Logging and status updates
    """

    def __init__(self):
        """Initialize base GUI controller."""
        self.logger = get_logger(__name__)

        # V2 Integration
        self.coordinate_loader = get_coordinate_loader()

        # State
        self.selected_agents: list[str] = []
        self.agent_widgets: dict[str, Any] = {}
        self.log_display = None
        self.status_timer = None

        self.logger.info("Base GUI Controller initialized")

    def select_all_agents(self) -> None:
        """Select all agents."""
        self.selected_agents = [f"Agent-{i}" for i in range(1, 9)]
        self._update_agent_selection()
        self.log_message("System", "All agents selected")

    def clear_selection(self) -> None:
        """Clear agent selection."""
        self.selected_agents.clear()
        self._update_agent_selection()
        self.log_message("System", "Agent selection cleared")

    def toggle_agent_selection(self, agent_id: str) -> None:
        """Toggle agent selection."""
        if agent_id in self.selected_agents:
            self.selected_agents.remove(agent_id)
            self.log_message("System", f"{agent_id} deselected")
        else:
            self.selected_agents.append(agent_id)
            self.log_message("System", f"{agent_id} selected")

        self._update_agent_selection()

    def execute_selected_agents_action(
        self,
        action_type: str,
        action_name: str,
        action_func: Callable[[str], None] | None = None,
    ) -> None:
        """
        Execute action on selected agents.

        Args:
            action_type: Type of action (e.g., "ping", "status")
            action_name: Display name for the action
            action_func: Optional custom action function
        """
        if not self.selected_agents:
            self.log_message("System", f"No agents selected for {action_name}")
            return

        self.log_message("System", f"{action_name} → {len(self.selected_agents)} agents")

        for agent_id in self.selected_agents:
            try:
                if action_func:
                    action_func(agent_id)
                else:
                    self._default_agent_action(agent_id, action_type)
            except Exception as e:
                self.logger.error(f"Action failed for {agent_id}: {e}")
                self.log_message("Error", f"{action_name} failed for {agent_id}")

    def broadcast_action(
        self,
        action_type: str,
        action_name: str,
        default_command: str | None = None,
        action_func: Callable[[str], None] | None = None,
    ) -> None:
        """
        Broadcast action to all agents.

        Args:
            action_type: Type of action
            action_name: Display name for the action
            default_command: Default command to send
            action_func: Optional custom action function
        """
        self.log_message("Broadcast", f"{action_name} → all agents")

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            try:
                if action_func:
                    action_func(agent_id)
                else:
                    self._default_broadcast_action(action_type, default_command)
            except Exception as e:
                self.logger.error(f"Broadcast failed for {agent_id}: {e}")

    def _default_agent_action(self, agent_id: str, action_type: str) -> None:
        """Default action implementation using V2 messaging."""
        message = self._create_action_message(action_type)
        success = send_message_to_agent(agent_id, message)

        if success:
            self.log_message("Action", f"{action_type} → {agent_id}")
        else:
            self.log_message("Error", f"{action_type} failed → {agent_id}")

    def _default_broadcast_action(
        self, action_type: str, default_command: str | None = None
    ) -> None:
        """Default broadcast action implementation."""
        message = default_command or self._create_action_message(action_type)

        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            send_message_to_agent(agent_id, message)

    def _create_action_message(self, action_type: str) -> str:
        """Create action message based on type."""
        action_messages = {
            "ping": "[PING] Respond with status",
            "status": "[STATUS] Report current status",
            "resume": "[RESUME] Resume operations",
            "pause": "[PAUSE] Pause current operations",
            "sync": "[SYNC] Synchronize state",
            "task": "[TASK] Execute highest priority task",
        }

        return action_messages.get(action_type, f"[{action_type.upper()}] Execute action")

    def _update_agent_selection(self) -> None:
        """Update agent widget selection states."""
        for agent_id, widget in self.agent_widgets.items():
            if hasattr(widget, "set_selected"):
                is_selected = agent_id in self.selected_agents
                widget.set_selected(is_selected)

    def log_message(self, sender: str, message: str) -> None:
        """
        Add a message to the log display.

        Args:
            sender: Message sender
            message: Message content
        """
        if not self.log_display:
            return

        from datetime import datetime

        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}"

        # Add to log display (implementation varies by GUI framework)
        if hasattr(self.log_display, "append"):
            self.log_display.append(log_entry)

    def setup_status_updates(self, update_interval: int = 5000) -> None:
        """
        Setup periodic status updates.

        Args:
            update_interval: Update interval in milliseconds
        """
        # This would be implemented by subclasses using their GUI framework
        self.logger.info(f"Status updates configured: {update_interval}ms interval")

    # Agent action shortcuts (delegated to generic execute/broadcast methods)
    def ping_selected_agents(self) -> None:
        """Ping selected agents."""
        self.execute_selected_agents_action("ping", "Ping")

    def get_status_selected_agents(self) -> None:
        """Get status from selected agents."""
        self.execute_selected_agents_action("status", "Status")

    def resume_selected_agents(self) -> None:
        """Resume selected agents."""
        self.execute_selected_agents_action("resume", "Resume")

    def pause_selected_agents(self) -> None:
        """Pause selected agents."""
        self.execute_selected_agents_action("pause", "Pause")

    def clear_log(self) -> None:
        """Clear the log display."""
        if self.log_display and hasattr(self.log_display, "clear"):
            self.log_display.clear()
            self.log_message("System", "Log cleared")

    def save_log(self) -> None:
        """Save log to file."""
        try:
            from datetime import datetime

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/gui_log_{timestamp}.txt"

            if self.log_display and hasattr(self.log_display, "toPlainText"):
                log_content = self.log_display.toPlainText()

                from pathlib import Path

                log_path = Path(filename)
                log_path.parent.mkdir(parents=True, exist_ok=True)

                with open(log_path, "w") as f:
                    f.write(log_content)

                self.log_message("System", f"Log saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save log: {e}")
