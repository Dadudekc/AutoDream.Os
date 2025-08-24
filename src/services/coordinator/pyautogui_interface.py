"""Module isolating PyAutoGUI interactions."""
from __future__ import annotations

from typing import Any


class PyAutoGUIInterface:
    """Encapsulates interaction with a PyAutoGUI-like module.

    The actual GUI module is injected to make the class easy to test and to
    isolate third-party dependencies from the rest of the system.
    """

    def __init__(self, gui_module: Any | None = None) -> None:
        if gui_module is None:
            try:  # pragma: no cover - import guarded for environments without pyautogui
                import pyautogui as gui_module  # type: ignore
            except Exception as exc:  # pragma: no cover - ensures informative error
                raise RuntimeError("PyAutoGUI is required but not available") from exc
        self._gui = gui_module

    def send_text(self, text: str) -> None:
        """Send ``text`` using the underlying GUI module."""
        self._gui.write(text)
