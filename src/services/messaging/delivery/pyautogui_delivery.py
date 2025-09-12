from __future__ import annotations
import time, logging
from typing import Tuple
from ..models import UnifiedMessage

logger = logging.getLogger(__name__)


def _lazy_import():
    try:
        import pyautogui as pg  # type: ignore

        try:
            pg.FAILSAFE = False
        except Exception:
            pass
        try:
            import pyperclip as pc  # type: ignore
        except Exception:
            pc = None
        return pg, pc
    except Exception as e:
        raise RuntimeError(f"pyautogui unavailable: {e}")


def _focus_and_clear(pg, x: int, y: int):
    pg.click(x, y, duration=0.4)
    time.sleep(0.05)
    pg.hotkey("ctrl", "a")
    time.sleep(0.02)
    pg.press("backspace")
    time.sleep(0.02)


def _paste_or_type(pg, pc, text: str):
    if pc is not None:
        try:
            pc.copy(text)
            pg.hotkey("ctrl", "v")
            return
        except Exception:
            pass
    pg.typewrite(text, interval=0.01)


def deliver_message_pyautogui(message: UnifiedMessage, coords: Tuple[int, int]) -> bool:
    pg, pc = _lazy_import()
    x, y = coords
    formatted = f"[{message.sender}] {message.content}"
    for attempt in range(1, 3):
        try:
            _focus_and_clear(pg, x, y)
            _paste_or_type(pg, pc, formatted)
            time.sleep(0.03)
            pg.press("enter")
            logger.info(f"[pyautogui] delivered to {message.recipient} at {coords}")
            return True
        except Exception as e:
            logger.warning(f"[pyautogui] attempt {attempt} failed: {e}")
            time.sleep(0.3)
    return False
