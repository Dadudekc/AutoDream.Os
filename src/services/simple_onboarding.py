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
<<<<<<< Updated upstream
=======
import pyautogui as pg
from pathlib import Path
from typing import Optional, Dict, Any, List
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
    """Default UI onboarding flow for agents."""

    def __init__(
        self,
        role_map: Optional[Dict[str, str]] = None,
        dry_run: bool = False,
        status_file: str | Path = "status.json",
    ):
=======
    """
    Enhanced Simple Onboarding with Mode QA Pack Features:
      1) Focus chat input → paste WRAP-UP message (template-driven)
      2) Ctrl+T → focus onboarding input → paste ONBOARDING message

    ✨ Mode QA Pack Features:
      - Agent subset control (--agent-subset)
      - Selective operations (--wrapup-only, --onboarding-only)
      - Style selection (friendly/professional)
    """

    def __init__(self, role_map: Optional[Dict[str, str]] = None, dry_run: bool = False,
                 subset_agents: Optional[List[str]] = None,
                 wrapup_only: bool = False,
                 onboarding_only: bool = False,
                 style: str = "strict"):
>>>>>>> Stashed changes
        self.role_map = role_map or SIMPLE_ROLES_DEFAULT
        self.dry_run = dry_run
        self.status_file = Path(status_file)

        # ✨ Mode QA Pack Features
        self.subset = set(subset_agents or [])
        self.wrapup_only = wrapup_only
        self.onboarding_only = onboarding_only
        self.style = style

        # Validate conflicting options
        if self.wrapup_only and self.onboarding_only:
            raise ValueError("Cannot specify both wrapup_only and onboarding_only")

    def execute(self) -> Dict[str, Any]:
        """Execute the enhanced simple UI onboarding flow with Mode QA Pack features."""
        print("[onboarding:simple] starting (Mode QA Pack Enhanced)")
        print(f"  Style: {self.style}")
        print(f"  Dry run: {self.dry_run}")
        print(f"  Agent subset: {list(self.subset) if self.subset else 'ALL'}")
        print(f"  Wrap-up only: {self.wrapup_only}")
        print(f"  Onboarding only: {self.onboarding_only}")
        
        # Load coordinates
        coord_map = self._load_coordinates()
        if not coord_map:
            return {"success": False, "error": "Failed to load coordinates"}
        
        # System reset
        self._reset_agent_statuses()
        
        results = []
        processed_count = 0

        for agent_id, role in self.role_map.items():
            # ✨ Mode QA Pack: Agent subset control
            if not self._should_process_agent(agent_id):
                continue

            processed_count += 1
            try:
                result = self._onboard_agent(agent_id, role, coord_map)
                results.append(result)
            except Exception as e:
                print(f"❌ {agent_id}: onboarding error - {e}")
                results.append({"agent": agent_id, "success": False, "error": str(e)})
        
        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)
        
        # Enhanced result reporting
        operation_desc = self._get_operation_description()
        print(f"[onboarding:simple] ✅ complete - {success_count}/{total_count} successful ({operation_desc})")

        return {
            "success": success_count > 0,
            "results": results,
            "success_count": success_count,
            "total_count": total_count,
            "processed_count": processed_count,
            "subset_used": bool(self.subset),
            "operation_mode": operation_desc,
            "style": self.style
        }

    def _should_process_agent(self, agent_id: str) -> bool:
        """Determine if an agent should be processed based on subset settings.

        Args:
            agent_id: The agent identifier

        Returns:
            True if agent should be processed, False otherwise
        """
        if not self.subset:
            return True  # Process all agents if no subset specified
        return agent_id in self.subset

    def _get_operation_description(self) -> str:
        """Get a description of the current operation mode.

        Returns:
            String describing the operation mode
        """
        if self.wrapup_only:
            return "Wrap-up only"
        elif self.onboarding_only:
            return "Onboarding only"
        else:
            return "Full onboarding (wrap-up + onboarding)"

    def _get_dry_run_flow_description(self) -> str:
        """Get description of the dry run flow.

        Returns:
            String describing the dry run flow
        """
        if self.wrapup_only:
            return "WRAP-UP only (no UI actions)"
        elif self.onboarding_only:
            return "ONBOARDING only (no UI actions)"
        else:
            return "WRAP-UP → Ctrl+T → ONBOARDING (no UI actions)"

    def _execute_wrapup(self, agent_id: str, message: str, coords: List[int]) -> bool:
        """Execute wrap-up operation for an agent.

        Args:
            agent_id: Agent identifier
            message: Wrap-up message
            coords: Chat input coordinates

        Returns:
            True if successful, False otherwise
        """
        try:
            # Focus on agent's chat interface
            self._ensure_tab(agent_id)

            # Click on chat input
            if not self._click_xy(coords[0], coords[1]):
                return False

            # Paste wrap-up message
            self._type_clipboard(message)
            print(f"    ✅ Wrap-up message sent to {agent_id}")
            return True

        except Exception as e:
            print(f"    ❌ Wrap-up failed for {agent_id}: {e}")
            return False

    def _execute_onboarding(self, agent_id: str, message: str, coords: List[int]) -> bool:
        """Execute onboarding operation for an agent.

        Args:
            agent_id: Agent identifier
            message: Onboarding message
            coords: Onboarding input coordinates

        Returns:
            True if successful, False otherwise
        """
        try:
            # Open new tab for onboarding
            self._ensure_tab(agent_id, method="ctrl_t")

            # Click on onboarding input
            if not self._click_xy(coords[0], coords[1]):
                return False

            # Paste onboarding message
            self._type_clipboard(message)
            print(f"    ✅ Onboarding message sent to {agent_id}")
            return True

        except Exception as e:
            print(f"    ❌ Onboarding failed for {agent_id}: {e}")
            return False

    def _load_coordinates(self) -> Optional[Dict[str, Any]]:
        """Load coordinates using SSOT coordinate loader."""
        try:
            from src.core.coordinate_loader import get_coordinate_loader
            loader = get_coordinate_loader()

            # Convert to the expected format for our system
            converted = {}
            for agent_id in loader.get_all_agents():
                try:
                    converted[agent_id] = {
                        "chat_input": loader.get_chat_coordinates(agent_id),
                        "onboarding_input": loader.get_onboarding_coordinates(agent_id)
                    }
                except ValueError:
                    # Skip agents with invalid coordinates
                    continue

            return converted
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
        """Onboard a single agent using UI actions with Mode QA Pack selective operations."""
        operation_desc = self._get_operation_description()
        print(f"🎯 Processing {agent_id} as {role} ({operation_desc})")
        
        # Get coordinates for this agent
        agent_coords = coord_map.get(agent_id, {})
        chat_coords = agent_coords.get("chat_input", [0, 0])
        onboarding_coords = agent_coords.get("onboarding_input", [0, 0])
        
        # Validate coordinates based on operation mode
        if not self.onboarding_only and chat_coords == [0, 0]:
            return {
                "agent": agent_id,
                "success": False,
                "error": f"Missing chat coordinates for {agent_id}"
            }

        if not self.wrapup_only and onboarding_coords == [0, 0]:
            return {
                "agent": agent_id,
                "success": False,
                "error": f"Missing onboarding coordinates for {agent_id}"
            }

        # Generate messages based on style
        wrap_msg = self._wrap_up_msg(agent_id, role, self.style)
        ob_msg = self._onboarding_msg(agent_id, role, self.style)
        
        if self.dry_run:
            flow_desc = self._get_dry_run_flow_description()
            print(f"[dry-run] {agent_id}: {flow_desc}")
            return {
                "agent": agent_id,
                "success": True,
                "dry_run": True,
                "operation": operation_desc,
                "style": self.style,
                "wrap_msg_preview": wrap_msg[:50] + "..." if not self.onboarding_only else None,
                "ob_msg_preview": ob_msg[:50] + "..." if not self.wrapup_only else None
            }
        
        try:
            # ✨ Mode QA Pack: Selective operations
            operations_performed = []

            # 1) WRAP-UP: Only if not onboarding-only
            if not self.onboarding_only:
                print(f"    📝 Executing wrap-up for {agent_id}")
                success = self._execute_wrapup(agent_id, wrap_msg, chat_coords)
                if success:
                    operations_performed.append("wrapup")
                else:
                    return {
                        "agent": agent_id,
                        "success": False,
                        "error": "Wrap-up operation failed",
                        "operations_completed": operations_performed
                    }

            # 2) ONBOARDING: Only if not wrapup-only
            if not self.wrapup_only:
                print(f"    🎯 Executing onboarding for {agent_id}")
                success = self._execute_onboarding(agent_id, ob_msg, onboarding_coords)
                if success:
                    operations_performed.append("onboarding")
                else:
                    return {
                        "agent": agent_id,
                        "success": False,
                        "error": "Onboarding operation failed",
                        "operations_completed": operations_performed
                    }
            
            print(f"✅ {agent_id}: UI onboarding complete ({', '.join(operations_performed)})")
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
        # Validate coordinates before clicking
        if not self._validate_coordinates(x, y):
            print(f"❌ Invalid coordinates: ({x}, {y})")
            return False
        
        pg.click(x, y)
        time.sleep(0.1)
        return True

    def _type_clipboard(self, text: str):
        """Type text into the focused field."""
        pg.hotkey("ctrl", "a")  # select all
        pg.typewrite(["backspace"])  # clear
        pg.write(text)  # type the text
        time.sleep(0.1)

    def _validate_coordinates(self, x: int, y: int) -> bool:
        """Validate that coordinates are reasonable for screen interaction.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if coordinates are valid, False otherwise
        """
        # Check if coordinates are within reasonable screen bounds
        if x < 0 or y < 0:
            return False
        if x > 5000 or y > 5000:  # Reasonable upper bound
            return False
        if x == 0 and y == 0:  # Default/fallback coordinates
            print("⚠️  Using default coordinates (0,0) - may not be accurate")
            return True
        return True

    def _validate_message_format(self, agent_id: str, message: str) -> bool:
        """Validate that the message has the correct format.
        
        Args:
            agent_id: The agent identifier
            message: The message to validate
            
        Returns:
            True if message format is valid, False otherwise
        """
        # Check for proper agent identification format
        if not message.startswith(f"YOU ARE {agent_id}"):
            print(f"❌ Message does not start with 'YOU ARE {agent_id}'")
            return False
        
        # Check for [S2A] format (should not be present)
        if "[S2A]" in message:
            print("❌ Message contains [S2A] format - should use 'YOU ARE AGENT X' format")
            return False
        
        # Check for role information
        if "ROLE:" not in message:
            print("❌ Message missing ROLE information")
            return False
        
        # Check for responsibilities
        if "PRIMARY RESPONSIBILITIES:" not in message:
            print("❌ Message missing PRIMARY RESPONSIBILITIES")
            return False
        
        return True

    def _wrap_up_msg(self, agent_id: str, role: str, style: str = "strict") -> str:
        """Generate wrap-up message for the agent with style support."""
        template = self._get_wrapup_template()
        timestamp = self._now_iso()

        if style == "friendly":
            tone = "🤝 FRIENDLY WRAP-UP REQUEST"
            instruction = "Hey there! Could you please wrap up your current tasks using the template below?"
        else:
            tone = "💼 STRICT WRAP-UP REQUEST"
            instruction = "Execute standard wrap-up protocol using the template below."

        return (
            f"[{tone}] {agent_id} ({role})\n"
            f"{instruction}\n"
            f"Style: {style}\n"
            f"Timestamp: {timestamp}\n\n"
            f"{template}\n"
        )

    def _onboarding_msg(self, agent_id: str, role: str, style: str = "strict") -> str:
        """Generate onboarding message for the agent with style support."""
        timestamp = self._now_iso()

        if style == "friendly":
            tone = "🤝 FRIENDLY TRAINING MODE"
            greeting = "Welcome to the team! Let's get you set up properly."
            responsibilities = [
                "🎯 Your main role: Help coordinate and manage team tasks",
                "📋 Daily routine: Check inbox, execute tasks, update your status",
                "🤝 Communication: Be helpful and collaborative with other team members",
                "✅ Success focus: Complete assigned tasks and maintain status updates",
                "💡 Pro tip: Use the wrap-up template at the end of each cycle"
            ]
        else:
            tone = "💼 STRICT OPERATIONAL MODE"
            greeting = "Agent activation sequence initiated."
            responsibilities = [
                "🎯 PRIMARY DIRECTIVE: Execute assigned tasks with precision",
                "📋 OPERATIONAL PROTOCOL: Check inbox, process tasks, update status",
                "💼 COMMUNICATION STANDARD: Professional, concise, results-oriented",
                "✅ PERFORMANCE METRICS: Task completion rate, status accuracy",
                "📝 REQUIREMENT: Use WRAP-UP template for end-of-cycle summaries"
            ]

        resp_text = "\n".join(f"  {resp}" for resp in responsibilities)

        return (
            f"{tone}\n"
            f"🚨 AGENT IDENTITY: You are {agent_id} - {role}\n"
            f"⏱️ Activation Time: {timestamp}\n\n"
            f"{greeting}\n\n"
            f"📋 Core Responsibilities:\n{resp_text}\n\n"
            "🔧 Essential Commands:\n"
            "  • --get-next-task (Get your next assignment)\n"
            "  • --check-status (Check system status)\n"
            "  • Update status.json (Track your progress)\n"
            "  • Check inbox regularly (Receive communications)\n\n"
            "🎯 Mission Success Criteria:\n"
            "  • Execute assigned tasks efficiently\n"
            "  • Maintain accurate status reporting\n"
            "  • Collaborate effectively with team members\n"
            "  • Follow operational protocols precisely\n"
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
