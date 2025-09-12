from __future__ import annotations

"""
UI Onboarding — Hard Onboarding Sequence (V2 Compliant)
=======================================================

Sequence (per spec):
1) Click CHAT INPUT coordinates
2) Press Ctrl+N (open new chat)
3) Click ONBOARDING INPUT coordinates
4) Type the onboarding role message
5) Press Enter to send

Notes:
- Tolerant to negative (multi-monitor) coordinates.
- Dry-run logs the exact plan without moving the mouse.
- Clipboard paste preferred (fast + robust), falls back to typewrite.
- Retries per step with small sleeps based on tolerance.

Author: Agent-7
License: MIT
"""

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


class UIUnavailableError(RuntimeError):
    pass


@dataclass
class OnboardCoords:
    chat_input: tuple[int, int]
    onboarding_input: tuple[int, int]

    @staticmethod
    def from_any(coords: Any) -> OnboardCoords:
        """
        Accepts:
          - dict with keys: chat_input_coordinates, onboarding_coordinates
          - dict with keys: chat_input, onboarding_input
          - object with same attributes
        """

        def _get(obj: Any, *names: str) -> tuple[int, int] | None:
            for n in names:
                if isinstance(obj, dict) and n in obj:
                    return tuple(obj[n])  # type: ignore
                if hasattr(obj, n):
                    return tuple(getattr(obj, n))  # type: ignore
            return None

        chat = _get(coords, "chat_input_coordinates", "chat_input")
        ob = _get(coords, "onboarding_coordinates", "onboarding_input")
        if not chat or not ob:
            raise ValueError("Invalid coords; expected chat_input + onboarding_input")
        return OnboardCoords(chat_input=tuple(map(int, chat)), onboarding_input=tuple(map(int, ob)))


class UIOnboarder:
    def __init__(self, *, tolerance: int = 200, retries: int = 2, dry_run: bool = False):
        """
        tolerance: base sleep in ms between UI actions
        retries:   per-step retry count
        dry_run:   log-only; do not move cursor or type
        """
        self.tolerance = max(50, int(tolerance))
        self.retries = max(0, int(retries))
        self.dry_run = bool(dry_run)

        # import late so module import never crashes
        self._pg = None
        self._clip_ok = False
        if not self.dry_run:
            try:
                import pyautogui as _pg  # type: ignore

                self._pg = _pg
                # Fail-safe off to avoid aborts when moving to 0,0
                try:
                    self._pg.FAILSAFE = False
                except Exception:
                    pass
            except Exception as e:
                raise UIUnavailableError(f"pyautogui unavailable: {e}")

            # Optional clipboard paste
            try:
                import pyperclip as _pc  # type: ignore

                self._pc = _pc
                self._clip_ok = True
            except Exception:
                self._clip_ok = False

    # ---------- low level helpers ----------

    def _sleep(self, ms: int | None = None):
        time.sleep((ms or self.tolerance) / 1000.0)

    def _attempt(self, name: str, fn: Callable[[], None]):
        last = None
        for i in range(self.retries + 1):
            try:
                logger.debug(f"[UI] {name} (try {i + 1}/{self.retries + 1})")
                if not self.dry_run:
                    fn()
                else:
                    logger.info(f"[DRY-RUN] {name}")
                return
            except Exception as e:
                last = e
                self._sleep(self.tolerance)
        raise RuntimeError(f"Step failed: {name}; last_error={last}")

    def _click(self, x: int, y: int):
        def _do():
            self._pg.moveTo(x, y)  # type: ignore
            self._pg.click()  # type: ignore

        self._attempt(f"click({x},{y})", _do)
        self._sleep()

    def _hotkey(self, *keys: str):
        def _do():
            self._pg.hotkey(*keys)  # type: ignore

        self._attempt(f"hotkey({'+'.join(keys)})", _do)
        self._sleep()

    def _type(self, text: str):
        if self._clip_ok:

            def _do():
                self._pc.copy(text)  # type: ignore
                self._pg.hotkey("ctrl", "v")  # type: ignore

            self._attempt("paste(message)", _do)
        else:

            def _do():
                self._pg.typewrite(text, interval=0.01)  # type: ignore

            self._attempt("typewrite(message)", _do)
        self._sleep()

    def _press(self, key: str):
        def _do():
            self._pg.press(key)  # type: ignore

        self._attempt(f"press({key})", _do)
        self._sleep()

    # ---------- public API ----------

    def perform(self, *, agent_id: str, coords: Any, message: str) -> bool:
        """
        Executes the hard onboarding sequence:
          click(chat_input) -> Ctrl+N -> click(onboarding_input) -> type(message) -> Enter
        Returns True if all steps executed.
        """
        oc = OnboardCoords.from_any(coords)

        logger.info(f"🧭 Hard Onboarding: {agent_id}")
        logger.info(f"   chat_input={oc.chat_input}  onboarding_input={oc.onboarding_input}")
        logger.info(f"   msg_len={len(message)} dry_run={self.dry_run} retries={self.retries}")

        # 1) Focus chat input
        self._click(*oc.chat_input)

        # 2) New chat
        self._hotkey("ctrl", "n")

        # 3) Focus onboarding input
        self._click(*oc.onboarding_input)

        # 4) Type role message
        self._type(message)

        # 5) Send
        self._press("enter")

        logger.info("✅ Onboarding sequence completed")
        return True
