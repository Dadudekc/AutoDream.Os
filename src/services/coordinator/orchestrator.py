"""Coordinator orchestrator that delegates message delivery."""
from __future__ import annotations

from .pyautogui_interface import PyAutoGUIInterface
from .message_queue_client import MessageQueueClient
from .coordination_strategy import CoordinationStrategy


class CoordinatorOrchestrator:
    """High-level orchestrator coordinating message delivery."""

    def __init__(
        self,
        gui_interface: PyAutoGUIInterface,
        queue_client: MessageQueueClient,
        strategy: CoordinationStrategy,
    ) -> None:
        self.gui_interface = gui_interface
        self.queue_client = queue_client
        self.strategy = strategy

    def deliver(self, message: str) -> None:
        """Deliver ``message`` using the configured strategy."""
        method = self.strategy.choose(message)
        if method == "queue":
            self.queue_client.send(message)
        else:
            self.gui_interface.send_text(message)
