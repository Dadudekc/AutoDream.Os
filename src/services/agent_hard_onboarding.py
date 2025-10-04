#!/usr/bin/env python3
"""
Agent Hard Onboarding Module - Direct Activation Protocol (Hardened)
===================================================================

- Safe PyAutoGUI wrappers with retry/backoff
- Dry-run mode for headless / CI runs
- Coordinate file validation with clear errors
- Configurable window-open step (disabled by default)
- Proper typing + richer return payloads
- Per-agent cooldown + global throttle

V2 Compliance: ≤400 lines, focused and testable.
"""

from __future__ import annotations

import json
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

try:
    import pyautogui
    import pyperclip

    PYAUTOGUI_AVAILABLE = True
except Exception:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    PYAUTOGUI_AVAILABLE = False


# ---------- Small config block (tweak without code changes) ----------
DEFAULT_COORD_PATH = "config/coordinates.json"
OPEN_NEW_WINDOW = False  # formerly ctrl+n; off by default
CLICK_PAUSE = 0.5  # seconds between clicks/keys
RETRY_ATTEMPTS = 3
RETRY_BACKOFF = 0.4  # additive backoff
GLOBAL_THROTTLE = 0.15  # pause between UI ops
COOLDOWN_SEC = 300  # per-agent cooldown window


@dataclass(frozen=True)
class AgentCoords:
    chat_input: tuple[int, int]
    onboarding: tuple[int, int] | None = None


class UI:
    """Minimal UI adapter for PyAutoGUI with dry-run fallback."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run or (not PYAUTOGUI_AVAILABLE)
        self._last_op_ts = 0.0

    def _throttle(self) -> None:
        now = time.time()
        if now - self._last_op_ts < GLOBAL_THROTTLE:
            time.sleep(GLOBAL_THROTTLE)
        self._last_op_ts = time.time()

    def click(self, x: int, y: int) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] click({x},{y})")
            return
        for i in range(RETRY_ATTEMPTS):
            try:
                pyautogui.click(x, y)  # type: ignore
                time.sleep(CLICK_PAUSE)
                return
            except Exception as e:
                if i == RETRY_ATTEMPTS - 1:
                    raise
                time.sleep(CLICK_PAUSE + i * RETRY_BACKOFF)
                logger.warning(f"click retry {i+1}/{RETRY_ATTEMPTS}: {e}")

    def hotkey(self, *keys: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] hotkey{keys}")
            return
        for i in range(RETRY_ATTEMPTS):
            try:
                pyautogui.hotkey(*keys)  # type: ignore
                time.sleep(CLICK_PAUSE)
                return
            except Exception as e:
                if i == RETRY_ATTEMPTS - 1:
                    raise
                time.sleep(CLICK_PAUSE + i * RETRY_BACKOFF)
                logger.warning(f"hotkey retry {i+1}/{RETRY_ATTEMPTS}: {e}")

    def press(self, key: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] press({key})")
            return
        pyautogui.press(key)  # type: ignore
        time.sleep(CLICK_PAUSE)

    def paste_text(self, text: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] paste_text(len={len(text)})")
            return
        try:
            pyperclip.copy(text)  # type: ignore
        except Exception as e:
            logger.warning(f"Clipboard not available; simulating paste: {e}")
            # Fall back to typing (slower, but keeps going)
            self.typewrite(text)
            return
        self.hotkey("ctrl", "v")

    def typewrite(self, text: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] typewrite(len={len(text)})")
            return
        pyautogui.typewrite(text)  # type: ignore
        time.sleep(CLICK_PAUSE)


class AgentHardOnboarder:
    """Handle direct agent activation operations with guard rails."""

    def __init__(self, coord_path: str = DEFAULT_COORD_PATH, *, dry_run: bool = False):
        self.coord_path = Path(coord_path)
        self.ui = UI(dry_run=dry_run)
        self.recently_onboarded: set[str] = set()
        self._onboarding_lock = threading.Lock()
        self._coords = self._load_and_validate_coords(self.coord_path)

    # -------------- Coordinates handling --------------

    @staticmethod
    def _load_and_validate_coords(path: Path) -> dict[str, AgentCoords]:
        if not path.exists():
            raise FileNotFoundError(f"Coordinates file not found: {path}")
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        if "agents" not in data or not isinstance(data["agents"], dict):
            raise ValueError("Invalid coordinates schema: missing 'agents' object")

        parsed: dict[str, AgentCoords] = {}
        for agent_id, cfg in data["agents"].items():
            if "chat_input_coordinates" not in cfg or not isinstance(
                cfg["chat_input_coordinates"], list
            ):
                raise ValueError(f"{agent_id}: missing chat_input_coordinates [x,y]")
            chat = tuple(cfg["chat_input_coordinates"])
            if len(chat) != 2 or not all(isinstance(v, int) for v in chat):
                raise ValueError(f"{agent_id}: chat_input_coordinates must be [int,int]")

            onboarding = None
            if "onboarding_coordinates" in cfg and isinstance(cfg["onboarding_coordinates"], list):
                ob = tuple(cfg["onboarding_coordinates"])
                if len(ob) == 2 and all(isinstance(v, int) for v in ob):
                    onboarding = ob  # optional, OK if absent

            parsed[agent_id] = AgentCoords(chat_input=chat, onboarding=onboarding)

        return parsed

    def get_agent_default_role(self, agent_id: str) -> str:
        try:
            default_roles = {
                "Agent-1": "INTEGRATION_SPECIALIST",
                "Agent-2": "ARCHITECTURE_SPECIALIST",
                "Agent-3": "WEB_DEVELOPER",
                "Agent-4": "CAPTAIN",
                "Agent-5": "COORDINATOR",
                "Agent-6": "QUALITY_ASSURANCE",
                "Agent-7": "IMPLEMENTATION_SPECIALIST",
                "Agent-8": "INTEGRATION_SPECIALIST",
            }
            return default_roles.get(agent_id, "TASK_EXECUTOR")
        except Exception as e:
            logger.warning(f"Could not determine default role for {agent_id}: {e}")
            return "TASK_EXECUTOR"

    def create_onboarding_message(self, agent_id: str, default_role: str) -> str:
        return f"""🔔 HARD ONBOARD SEQUENCE INITIATED
═══════════════════════════════════════════════════════════════════════════════
🤖 AGENT: {agent_id}
🎭 DEFAULT ROLE: {default_role}
📋 STATUS: ACTIVATING VIA COORDINATE-BASED WORKFLOW
⠀⠀⠀⠀⠀⠀═══════════════════════════════════════════════════════════════

📖 IMMEDIATE ACTIONS REQUIRED:
1. Review AGENTS.md for complete system overview
2. Understand your role: {default_role}
3. Initialize agent workspace and inbox
4. Load role-specific protocols from config/protocols/
5. Discover and integrate available tools
6. Begin autonomous workflow cycle

🎯 COORDINATION PROTOCOL:
- Monitor inbox for role assignments from Captain Agent-4
- Execute General Cycle: CHECK_INBOX → EVALUATE_TASKS → EXECUTE_ROLE → QUALITY_GATES → CYCLE_DONE
- Maintain V2 compliance standards (≤400 lines, proper structure)
- Use PyAutoGUI messaging for agent coordination

🛠️ TOOL DISCOVERY PROTOCOL: See tools/, src/services/, config/protocols/
🚀 BEGIN ONBOARDING PROTOCOLS
============================================================
🐝 WE ARE SWARM - {agent_id} Activation Complete"""

    # -------------- Core flows --------------

    def _run_sequence(self, agent_id: str, message: str) -> None:
        coords = self._coords[agent_id]
        # 1) Focus chat input
        self.ui.click(*coords.chat_input)
        # 2) Clear input area
        self.ui.hotkey("ctrl", "shift", "backspace")
        # 3) Optionally open new window/tab (disabled by default)
        if OPEN_NEW_WINDOW:
            self.ui.hotkey("ctrl", "n")
            time.sleep(1.0)
        # 4) Move to onboarding input location if defined
        if coords.onboarding:
            self.ui.click(*coords.onboarding)
        else:
            self.ui.click(*coords.chat_input)
        time.sleep(0.5)
        # 5) Paste + send
        self.ui.paste_text(message)
        self.ui.press("enter")

    def hard_onboard_agent(self, agent_id: str) -> bool:
        with self._onboarding_lock:
            if agent_id in self.recently_onboarded:
                logger.info(f"Agent {agent_id} within cooldown ({COOLDOWN_SEC}s). Skipping.")
                return True
            if agent_id not in self._coords:
                logger.error(f"Agent {agent_id} not found in coordinates file.")
                return False

            default_role = self.get_agent_default_role(agent_id)
            message = self.create_onboarding_message(agent_id, default_role)

            try:
                self._run_sequence(agent_id, message)
                logger.info(f"Hard onboarded {agent_id} as {default_role}")
                # cooldown management
                self.recently_onboarded.add(agent_id)
                threading.Thread(
                    target=self._cooldown_release, args=(agent_id,), daemon=True
                ).start()
                return True
            except Exception as e:
                logger.error(f"Error during hard onboarding for {agent_id}: {e}")
                return False

    def _cooldown_release(self, agent_id: str) -> None:
        time.sleep(COOLDOWN_SEC)
        self.recently_onboarded.discard(agent_id)

    def hard_onboard_all_agents(self) -> bool:
        success = 0
        for agent_id in self._coords.keys():
            if self.hard_onboard_agent(agent_id):
                success += 1
                time.sleep(1.0)  # brief spacing
        logger.info(f"Hard onboarded {success}/{len(self._coords)} agents")
        return success > 0


def process_hard_onboard_command(
    target_agent_id: str | None = None, *, dry_run: bool = False
) -> dict[str, Any]:
    """
    Execute hard-onboard for one agent or all.
    Returns a structured result for Captain logs.
    """
    try:
        onboarder = AgentHardOnboarder(dry_run=dry_run)
        if target_agent_id:
            ok = onboarder.hard_onboard_agent(target_agent_id)
            return {
                "target_agent": target_agent_id,
                "success": ok,
                "operation": "single_agent_onboarding",
                "dry_run": dry_run,
                "message": f"Hard onboard {'successful' if ok else 'failed'} for {target_agent_id}",
            }
        else:
            ok = onboarder.hard_onboard_all_agents()
            return {
                "target_agent": "ALL_AGENTS",
                "success": ok,
                "operation": "all_agents_onboarding",
                "dry_run": dry_run,
                "message": f"Hard onboard all agents {'successful' if ok else 'failed'}",
            }
    except Exception as e:
        logger.error(f"Onboarding command error: {e}")
        return {
            "target_agent": target_agent_id or "ALL_AGENTS",
            "success": False,
            "operation": "hard_onboarding",
            "dry_run": dry_run,
            "error": str(e),
        }
