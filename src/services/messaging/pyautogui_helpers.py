import logging
import time

try:
    import pyautogui

    PYAUTOGUI_AVAILABLE = True
except Exception as e:  # pragma: no cover - safety in environments without GUI
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False
    logging.getLogger(__name__).warning(f"PyAutoGUI not available: {e}")

try:
    import pyperclip

    PYPERCLIP_AVAILABLE = True
except Exception as e:  # pragma: no cover - clipboard library may not exist
    pyperclip = None
    PYPERCLIP_AVAILABLE = False
    logging.getLogger(__name__).warning(f"pyperclip not available: {e}")

logger = logging.getLogger(__name__)


def setup_pyautogui() -> None:
    """Configure PyAutoGUI defaults if available."""
    if not PYAUTOGUI_AVAILABLE:  # pragma: no cover - defensive
        return
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.5


def move_and_click(x: int, y: int, duration: float = 0.3) -> None:
    """Move the cursor and perform a click."""
    if not PYAUTOGUI_AVAILABLE:  # pragma: no cover - defensive
        return
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()


def paste_text(text: str) -> None:
    """Paste text using clipboard when available, otherwise type it."""
    if not PYAUTOGUI_AVAILABLE:  # pragma: no cover - defensive
        return
    if PYPERCLIP_AVAILABLE:
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    else:  # pragma: no cover - rarely executed
        pyautogui.write(text)


def press_enter() -> None:
    """Press the Enter key."""
    if not PYAUTOGUI_AVAILABLE:  # pragma: no cover - defensive
        return
    pyautogui.press("enter")


def press_hotkey(*keys: str) -> None:
    """Press a combination of hotkeys."""
    if not PYAUTOGUI_AVAILABLE:  # pragma: no cover - defensive
        return
    pyautogui.hotkey(*keys)
