"""Coordination decision logic."""
from __future__ import annotations


class CoordinationStrategy:
    """Decides how a message should be delivered."""

    def __init__(self, threshold: int = 20) -> None:
        self.threshold = threshold

    def choose(self, message: str) -> str:
        """Return the delivery method for ``message``.

        Messages with length less than or equal to ``threshold`` are sent via
        the message queue; longer messages use the PyAutoGUI interface.
        """

        return "queue" if len(message) <= self.threshold else "pyautogui"
