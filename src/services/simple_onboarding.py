import logging

logger = logging.getLogger(__name__)
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
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import pyautogui as pg
except Exception:
    from unittest.mock import MagicMock

    pg = MagicMock()

try:
    import pygetwindow as gw
except Exception:
    gw = None
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
        role_map: dict[str, str] | None = None,
        dry_run: bool = False,
        status_file: str | Path = "status.json",
    ):
        """
        Enhanced Simple Onboarding with Mode QA Pack Features:
          1) Focus chat input → paste WRAP-UP message (template-driven)
          2) Ctrl+T → focus onboarding input → paste ONBOARDING message

        ✨ Mode QA Pack Features:
          - Agent subset control (--agent-subset)
          - Selective operations (--wrapup-only, --onboarding-only)
          - Style selection (friendly/professional)
        """
        self.role_map = role_map or SIMPLE_ROLES_DEFAULT
        self.dry_run = dry_run
        self.status_file = Path(status_file)
        self.subset = set(subset_agents or [])
        self.wrapup_only = wrapup_only
        self.onboarding_only = onboarding_only
        self.style = style
        if self.wrapup_only and self.onboarding_only:
            raise ValueError("Cannot specify both wrapup_only and onboarding_only")

    def execute(self) -> dict[str, Any]:
        """Execute the enhanced simple UI onboarding flow with Mode QA Pack features."""
        logger.info("[onboarding:simple] starting (Mode QA Pack Enhanced)")
        logger.info(f"  Style: {self.style}")
        logger.info(f"  Dry run: {self.dry_run}")
        logger.info(f"  Agent subset: {list(self.subset) if self.subset else 'ALL'}")
        logger.info(f"  Wrap-up only: {self.wrapup_only}")
        logger.info(f"  Onboarding only: {self.onboarding_only}")
        coord_map = self._load_coordinates()
        if not coord_map:
            return {"success": False, "error": "Failed to load coordinates"}
        self._reset_agent_statuses()
        results = []
        processed_count = 0
        for agent_id, role in self.role_map.items():
            if not self._should_process_agent(agent_id):
                continue
            processed_count += 1
            try:
                result = self._onboard_agent(agent_id, role, coord_map)
                results.append(result)
            except Exception as e:
                logger.info(f"❌ {agent_id}: onboarding error - {e}")
                results.append({"agent": agent_id, "success": False, "error": str(e)})
        success_count = sum(1 for r in results if r.get("success", False))
        total_count = len(results)
        operation_desc = self._get_operation_description()
        logger.info(
            f"[onboarding:simple] ✅ complete - {success_count}/{total_count} successful ({operation_desc})"
        )
        return {
            "success": success_count > 0,
            "results": results,
            "success_count": success_count,
            "total_count": total_count,
            "processed_count": processed_count,
            "subset_used": bool(self.subset),
            "operation_mode": operation_desc,
            "style": self.style,
        }

    def _should_process_agent(self, agent_id: str) -> bool:
        """Determine if an agent should be processed based on subset settings.

        Args:
            agent_id: The agent identifier

        Returns:
            True if agent should be processed, False otherwise
        """
        if not self.subset:
            return True
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

    def _execute_wrapup(self, agent_id: str, message: str, coords: list[int]) -> bool:
        """Execute wrap-up operation for an agent.

        Args:
            agent_id: Agent identifier
            message: Wrap-up message
            coords: Chat input coordinates

        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_tab(agent_id)
            if not self._click_xy(coords[0], coords[1]):
                return False
            self._type_clipboard(message)
            logger.info(f"    ✅ Wrap-up message sent to {agent_id}")
            return True
        except Exception as e:
            logger.info(f"    ❌ Wrap-up failed for {agent_id}: {e}")
            return False

    def _execute_onboarding(self, agent_id: str, message: str, coords: list[int]) -> bool:
        """Execute onboarding operation for an agent.

        Args:
            agent_id: Agent identifier
            message: Onboarding message
            coords: Onboarding input coordinates

        Returns:
            True if successful, False otherwise
        """
        try:
            self._ensure_tab(agent_id, method="ctrl_t")
            if not self._click_xy(coords[0], coords[1]):
                return False
            self._type_clipboard(message)
            logger.info(f"    ✅ Onboarding message sent to {agent_id}")
            return True
        except Exception as e:
            logger.info(f"    ❌ Onboarding failed for {agent_id}: {e}")
            return False

    def _load_coordinates(self) -> dict[str, Any] | None:
        """Load coordinates using SSOT coordinate loader."""
        try:
            from ..core.coordinate_loader import get_coordinate_loader

            loader = get_coordinate_loader()
            converted = {}
            for agent_id in loader.get_all_agents():
                try:
                    converted[agent_id] = {
                        "chat_input": loader.get_chat_coordinates(agent_id),
                        "onboarding_input": loader.get_onboarding_coordinates(agent_id),
                    }
                except ValueError:
                    continue
            return converted
        except Exception as e:
            logger.info(f"❌ Failed to load coordinates: {e}")
            return None

    def _reset_agent_statuses(self) -> None:
        """Reset agent statuses in the SSOT status file."""
        if self.dry_run:
            return
        logger.info("🔄 Resetting agent statuses...")
        data: dict[str, Any] = {}
        if self.status_file.exists():
            try:
                data = json.loads(self.status_file.read_text(encoding="utf-8"))
            except Exception:
                data = {}
        data["agent_status"] = dict.fromkeys(self.role_map, "PENDING")
        data["last_updated"] = self._now_iso()
        self.status_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _onboard_agent(self, agent_id: str, role: str, coord_map: dict[str, Any]) -> dict[str, Any]:
        """Onboard a single agent using UI actions with Mode QA Pack selective operations."""
        operation_desc = self._get_operation_description()
        logger.info(f"🎯 Processing {agent_id} as {role} ({operation_desc})")
        agent_coords = coord_map.get(agent_id, {})
        chat_coords = agent_coords.get("chat_input", [0, 0])
        onboarding_coords = agent_coords.get("onboarding_input", [0, 0])
        if not self.onboarding_only and chat_coords == [0, 0]:
            return {
                "agent": agent_id,
                "success": False,
                "error": f"Missing chat coordinates for {agent_id}",
            }
        if not self.wrapup_only and onboarding_coords == [0, 0]:
            return {
                "agent": agent_id,
                "success": False,
                "error": f"Missing onboarding coordinates for {agent_id}",
            }
        wrap_msg = self._wrap_up_msg(agent_id, role, self.style)
        ob_msg = self._onboarding_msg(agent_id, role, self.style)
        if self.dry_run:
            flow_desc = self._get_dry_run_flow_description()
            logger.info(f"[dry-run] {agent_id}: {flow_desc}")
            return {
                "agent": agent_id,
                "success": True,
                "dry_run": True,
                "operation": operation_desc,
                "style": self.style,
                "wrap_msg_preview": wrap_msg[:50] + "..." if not self.onboarding_only else None,
                "ob_msg_preview": ob_msg[:50] + "..." if not self.wrapup_only else None,
            }
        try:
            operations_performed = []
            if not self.onboarding_only:
                logger.info(f"    📝 Executing wrap-up for {agent_id}")
                success = self._execute_wrapup(agent_id, wrap_msg, chat_coords)
                if success:
                    operations_performed.append("wrapup")
                else:
                    return {
                        "agent": agent_id,
                        "success": False,
                        "error": "Wrap-up operation failed",
                        "operations_completed": operations_performed,
                    }
            if not self.wrapup_only:
                logger.info(f"    🎯 Executing onboarding for {agent_id}")
                success = self._execute_onboarding(agent_id, ob_msg, onboarding_coords)
                if success:
                    operations_performed.append("onboarding")
                else:
                    return {
                        "agent": agent_id,
                        "success": False,
                        "error": "Onboarding operation failed",
                        "operations_completed": operations_performed,
                    }
            logger.info(
                f"✅ {agent_id}: UI onboarding complete ({', '.join(operations_performed)})"
            )
            return {"agent": agent_id, "success": True, "role": role}
        except Exception as e:
            return {"agent": agent_id, "success": False, "error": str(e)}

    def _ensure_tab(self, agent_id: str, method: str | None = None) -> None:
        """Focus the agent window and optionally open a new tab."""
        if self.dry_run:
            return
        logger.info(f"🔍 Focusing {agent_id} window...")
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
        if not self._validate_coordinates(x, y):
            logger.info(f"❌ Invalid coordinates: ({x}, {y})")
            return False
        pg.click(x, y)
        time.sleep(0.1)
        return True

    def _type_clipboard(self, text: str):
        """Type text into the focused field."""
        pg.hotkey("ctrl", "a")
        pg.typewrite(["backspace"])
        pg.write(text)
        time.sleep(0.1)

    def _validate_coordinates(self, x: int, y: int) -> bool:
        """Validate that coordinates are reasonable for screen interaction.

        Args:
            x: X coordinate
            y: Y coordinate

        Returns:
            True if coordinates are valid, False otherwise
        """
        if x < 0 or y < 0:
            return False
        if x > 5000 or y > 5000:
            return False
        if x == 0 and y == 0:
            logger.info("⚠️  Using default coordinates (0,0) - may not be accurate")
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
        if not message.startswith(f"YOU ARE {agent_id}"):
            logger.info(f"❌ Message does not start with 'YOU ARE {agent_id}'")
            return False
        if "[S2A]" in message:
            logger.info("❌ Message contains [S2A] format - should use 'YOU ARE AGENT X' format")
            return False
        if "ROLE:" not in message:
            logger.info("❌ Message missing ROLE information")
            return False
        if "PRIMARY RESPONSIBILITIES:" not in message:
            logger.info("❌ Message missing PRIMARY RESPONSIBILITIES")
            return False
        return True

    def _wrap_up_msg(self, agent_id: str, role: str, style: str = "strict") -> str:
        """Generate wrap-up message for the agent with style support."""
        template = self._get_wrapup_template()
        timestamp = self._now_iso()
        if style == "friendly":
            tone = "🤝 FRIENDLY WRAP-UP REQUEST"
            instruction = (
                "Hey there! Could you please wrap up your current tasks using the template below?"
            )
        else:
            tone = "💼 STRICT WRAP-UP REQUEST"
            instruction = "Execute standard wrap-up protocol using the template below."
        return f"""[{tone}] {agent_id} ({role})
{instruction}
Style: {style}
Timestamp: {timestamp}

{template}
"""

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
                "💡 Pro tip: Use the wrap-up template at the end of each cycle",
            ]
        else:
            tone = "💼 STRICT OPERATIONAL MODE"
            greeting = "Agent activation sequence initiated."
            responsibilities = [
                "🎯 PRIMARY DIRECTIVE: Execute assigned tasks with precision",
                "📋 OPERATIONAL PROTOCOL: Check inbox, process tasks, update status",
                "💼 COMMUNICATION STANDARD: Professional, concise, results-oriented",
                "✅ PERFORMANCE METRICS: Task completion rate, status accuracy",
                "📝 REQUIREMENT: Use WRAP-UP template for end-of-cycle summaries",
            ]
        resp_text = "\n".join(f"  {resp}" for resp in responsibilities)
        return f"""{tone}
🚨 AGENT IDENTITY: You are {agent_id} - {role}
⏱️ Activation Time: {timestamp}

{greeting}

📋 Core Responsibilities:
{resp_text}

🔧 Essential Commands:
  • --get-next-task (Get your next assignment)
  • --check-status (Check system status)
  • Update status.json (Track your progress)
  • Check inbox regularly (Receive communications)

🎯 Mission Success Criteria:
  • Execute assigned tasks efficiently
  • Maintain accurate status reporting
  • Collaborate effectively with team members
  • Follow operational protocols precisely
"""

    def _get_wrapup_template(self) -> str:
        """Load wrap-up template from the SSOT."""
        template_path = Path("prompts/agents/wrapup.md")
        try:
            if template_path.exists():
                return template_path.read_text(encoding="utf-8")
        except Exception:
            pass
        return """## Session Wrap-Up
**Agent**: {agent_id}
**Role**: {role}
**Completed Tasks**: [List completed tasks]
**Current Status**: [Current status]
**Next Actions**: [Planned next actions]
**Issues/Blockers**: [Any issues encountered]
**Achievements**: [Key achievements this session]
"""

    def _now_iso(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now().isoformat()
