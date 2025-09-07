#!/usr/bin/env python3
"""
Simple Onboarding - UI-Based Agent Onboarding
=============================================

Default onboarding now performs REAL UI actions:
1) Focus chat input → paste WRAP-UP message (template-driven)
2) Ctrl+T → focus onboarding input → paste ONBOARDING message

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import pyautogui as pg  # type: ignore
except Exception:  # pragma: no cover - allow tests without GUI libs
    from unittest.mock import MagicMock

    pg = MagicMock()

try:  # Optional dependency used for window activation
    import pygetwindow as gw  # type: ignore
except Exception:  # pragma: no cover - environment may lack GUI support
    gw = None

# 8-agent default roles
SIMPLE_ROLES_DEFAULT = {
    "Agent-1": "SSOT",
    "Agent-2": "SOLID", 
    "Agent-3": "DRY",
    "Agent-4": "KISS",
    "Agent-5": "TDD",
    "Agent-6": "Observability",
    "Agent-7": "CLI-Orchestrator",
    "Agent-8": "Docs-Governor",
}


class SimpleOnboarding:
    """Default UI onboarding flow for agents."""

    def __init__(
        self,
        role_map: Optional[Dict[str, str]] = None,
        dry_run: bool = False,
        status_file: str | Path = "status.json",
    ):
        self.role_map = role_map or SIMPLE_ROLES_DEFAULT
        self.dry_run = dry_run
        self.status_file = Path(status_file)

    def execute(self) -> Dict[str, Any]:
        """Execute the simple UI onboarding flow."""
        print("[onboarding:simple] starting (UI mode)")
        
        # Load coordinates
        coord_map = self._load_coordinates()
        if not coord_map:
            return {"success": False, "error": "Failed to load coordinates"}
        
        # System reset
        self._reset_agent_statuses()
        
        results = []
        for agent_id, role in self.role_map.items():
            try:
                result = self._onboard_agent(agent_id, role, coord_map)
                results.append(result)
            except Exception as e:
                print(f"❌ {agent_id}: onboarding error - {e}")
                results.append({"agent": agent_id, "success": False, "error": str(e)})
        
        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)
        
        print(f"[onboarding:simple] ✅ complete (UI) - {success_count}/{total_count} successful")
        return {
            "success": success_count > 0,
            "results": results,
            "success_count": success_count,
            "total_count": total_count
        }

    def _load_coordinates(self) -> Optional[Dict[str, Any]]:
        """Load coordinates from cursor_agent_coords.json."""
        try:
            import json
            with open("cursor_agent_coords.json", "r") as f:
                coords_data = json.load(f)
                # Convert to the expected format for our system
                if "agents" in coords_data:
                    # Convert from old format to new format
                    converted = {}
                    for agent_id, agent_data in coords_data["agents"].items():
                        converted[agent_id] = {
                            "chat_input": agent_data.get("chat_input_coordinates", [0, 0]),
                            "onboarding_input": agent_data.get("onboarding_input_coords", [0, 0])
                        }
                    return converted
                else:
                    # Already in new format
                    return coords_data
        except Exception as e:
            print(f"❌ Failed to load coordinates: {e}")
            return None

    def _reset_agent_statuses(self) -> None:
        """Reset agent statuses in the SSOT status file."""
        if self.dry_run:
            return

        print("🔄 Resetting agent statuses...")
        data: Dict[str, Any] = {}
        if self.status_file.exists():
            try:
                data = json.loads(self.status_file.read_text(encoding="utf-8"))
            except Exception:
                data = {}

        data["agent_status"] = {agent: "PENDING" for agent in self.role_map}
        data["last_updated"] = self._now_iso()
        self.status_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _onboard_agent(self, agent_id: str, role: str, coord_map: Dict[str, Any]) -> Dict[str, Any]:
        """Onboard a single agent using UI actions."""
        print(f"🎯 Onboarding {agent_id} as {role}")
        
        # Get coordinates for this agent
        agent_coords = coord_map.get(agent_id, {})
        chat_coords = agent_coords.get("chat_input", [0, 0])
        onboarding_coords = agent_coords.get("onboarding_input", [0, 0])
        
        if chat_coords == [0, 0] or onboarding_coords == [0, 0]:
            return {
                "agent": agent_id,
                "success": False,
                "error": f"Missing coordinates for {agent_id}"
            }
        
        # Generate messages
        wrap_msg = self._wrap_up_msg(agent_id, role)
        ob_msg = self._onboarding_msg(agent_id, role)
        
        if self.dry_run:
            print(f"[dry-run] {agent_id}: paste WRAP-UP → Ctrl+T → paste ONBOARDING")
            return {
                "agent": agent_id,
                "success": True,
                "dry_run": True,
                "wrap_msg": wrap_msg[:50] + "...",
                "ob_msg": ob_msg[:50] + "..."
            }
        
        try:
            # 1) Chat input: paste WRAP-UP message
            self._ensure_tab(agent_id)
            self._click_xy(chat_coords[0], chat_coords[1])
            self._type_clipboard(wrap_msg)
            
            # 2) New tab + Onboarding input: paste ONBOARDING message
            self._ensure_tab(agent_id, method="ctrl_t")
            self._click_xy(onboarding_coords[0], onboarding_coords[1])
            self._type_clipboard(ob_msg)
            
            print(f"✅ {agent_id}: UI onboarding complete")
            return {
                "agent": agent_id,
                "success": True,
                "role": role
            }
            
        except Exception as e:
            return {
                "agent": agent_id,
                "success": False,
                "error": str(e)
            }

    def _ensure_tab(self, agent_id: str, method: str | None = None) -> None:
        """Focus the agent window and optionally open a new tab."""
        if self.dry_run:
            return

        print(f"🔍 Focusing {agent_id} window...")
        try:
            if gw:
                windows = gw.getWindowsWithTitle(agent_id)
                if windows:
                    windows[0].activate()
                else:
                    pg.hotkey("alt", "tab")
            else:
                pg.hotkey("alt", "tab")
        except Exception:
            pg.hotkey("alt", "tab")
        time.sleep(0.1)

        if method == "ctrl_t":
            pg.hotkey("ctrl", "t")
            time.sleep(0.1)

    def _click_xy(self, x: int, y: int):
        """Click at the specified coordinates."""
        pg.click(x, y)
        time.sleep(0.1)

    def _type_clipboard(self, text: str):
        """Type text into the focused field."""
        pg.hotkey("ctrl", "a")  # select all
        pg.typewrite(["backspace"])  # clear
        pg.write(text)  # type the text
        time.sleep(0.1)

    def _wrap_up_msg(self, agent_id: str, role: str) -> str:
        """Generate wrap-up message for the agent."""
        template = self._get_wrapup_template()
        return (
            f"[WRAP-UP REQUEST] {agent_id} ({role})\n"
            f"Please generate your session wrap-up USING the standard template below.\n"
            f"Timestamp: {self._now_iso()}\n\n"
            f"{template}\n"
        )

    def _onboarding_msg(self, agent_id: str, role: str) -> str:
        """Generate onboarding message for the agent."""
        return (
            f"🚨 AGENT IDENTITY CONFIRMATION: You are {agent_id} - {role}\n"
            f"🎯 ROLE: {role}\n"
            "📋 PRIMARY RESPONSIBILITIES:\n"
            "1) --get-next-task  2) Update status.json  3) Check inbox  4) Respond to agents\n"
            "5) Maintain continuous workflow  6) Report with --captain  7) Use enhanced help\n"
            "Note: Use the WRAP-UP template for end-of-cycle summaries.\n"
            f"⏱️ TS: {self._now_iso()}\n"
        )

    def _get_wrapup_template(self) -> str:
        """Load wrap-up template from the SSOT."""
        template_path = Path("prompts/agents/wrapup.md")
        try:
            if template_path.exists():
                return template_path.read_text(encoding="utf-8")
        except Exception:
            pass

        return (
            "## Session Wrap-Up\n"
            "**Agent**: {agent_id}\n"
            "**Role**: {role}\n"
            "**Completed Tasks**: [List completed tasks]\n"
            "**Current Status**: [Current status]\n"
            "**Next Actions**: [Planned next actions]\n"
            "**Issues/Blockers**: [Any issues encountered]\n"
            "**Achievements**: [Key achievements this session]\n"
        )

    def _now_iso(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
