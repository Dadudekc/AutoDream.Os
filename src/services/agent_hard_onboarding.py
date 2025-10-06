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

V2 Compliance: EXCEPTION GRANTED for critical onboarding system.
Comprehensive agent onboarding requires detailed database integration and tool discovery protocols.
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

import sys  # noqa: E402

# Use UI Ops facade for PyAutoGUI operations

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.libs.uiops import UI as UIOpsFacade

    UI_OPS_AVAILABLE = True
except ImportError:
    UIOpsFacade = None
    UI_OPS_AVAILABLE = False


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
    """UI adapter using UI Ops facade for reliability and testability."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run or (not UI_OPS_AVAILABLE)
        self._last_op_ts = 0.0
        self._ui_ops = UIOpsFacade if UI_OPS_AVAILABLE else None

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

        if self._ui_ops:
            # Use UI Ops facade with built-in retry logic
            success = self._ui_ops.click(x, y)
            if success:
                time.sleep(CLICK_PAUSE)
                return
            else:
                raise RuntimeError(f"UI Ops click({x}, {y}) failed")
        else:
            raise RuntimeError("UI Ops facade not available")

    def hotkey(self, *keys: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] hotkey{keys}")
            return

        if self._ui_ops:
            # Use UI Ops facade with built-in retry logic
            success = self._ui_ops.hotkey(*keys)
            if success:
                time.sleep(CLICK_PAUSE)
                return
            else:
                raise RuntimeError(f"UI Ops hotkey({', '.join(keys)}) failed")
        else:
            raise RuntimeError("UI Ops facade not available")

    def press(self, key: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] press({key})")
            return

        if self._ui_ops:
            # Use UI Ops facade
            success = self._ui_ops.press(key)
            if success:
                time.sleep(CLICK_PAUSE)
                return
            else:
                raise RuntimeError(f"UI Ops press('{key}') failed")
        else:
            raise RuntimeError("UI Ops facade not available")

    def paste_text(self, text: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] paste_text(len={len(text)})")
            return

        if self._ui_ops:
            # Use UI Ops facade with built-in clipboard fallback
            success = self._ui_ops.paste(text)
            if success:
                time.sleep(CLICK_PAUSE)
                return
            else:
                raise RuntimeError(f"UI Ops paste({len(text)} chars) failed")
        else:
            raise RuntimeError("UI Ops facade not available")

    def typewrite(self, text: str) -> None:
        self._throttle()
        if self.dry_run:
            logger.info(f"[dry-run] typewrite(len={len(text)})")
            return

        if self._ui_ops:
            # Use UI Ops facade
            success = self._ui_ops.type(text)
            if success:
                time.sleep(CLICK_PAUSE)
                return
            else:
                raise RuntimeError(f"UI Ops type({len(text)} chars) failed")
        else:
            raise RuntimeError("UI Ops facade not available")


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
        """Get agent's default role from capabilities file with fallback to hardcoded defaults."""
        try:
            # Try to read from capabilities file first
            capabilities_path = Path("config/agent_capabilities.json")
            if capabilities_path.exists():
                with open(capabilities_path) as f:
                    capabilities = json.load(f)

                if agent_id in capabilities.get("agents", {}):
                    default_roles = capabilities["agents"][agent_id].get("default_roles", [])
                    if default_roles:
                        return default_roles[0]
        except Exception as e:
            logger.warning(f"Could not read capabilities file for {agent_id}: {e}")

        # Fallback to hardcoded defaults
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

📊 AVAILABLE ROLES (25 total):
Core: CAPTAIN, SSOT_MANAGER, COORDINATOR
Technical: INTEGRATION_SPECIALIST, ARCHITECTURE_SPECIALIST, INFRASTRUCTURE_SPECIALIST,
  WEB_DEVELOPER,
  DATA_ANALYST, QUALITY_ASSURANCE, PERFORMANCE_DETECTIVE, SECURITY_INSPECTOR, INTEGRATION_EXPLORER,
  FINANCIAL_ANALYST, TRADING_STRATEGIST, RISK_MANAGER, PORTFOLIO_OPTIMIZER, COMPLIANCE_AUDITOR
Operational: TASK_EXECUTOR, RESEARCHER, TROUBLESHOOTER, OPTIMIZER, DEVLOG_STORYTELLER,
  CODE_ARCHAEOLOGIST, DOCUMENTATION_ARCHITECT, MARKET_RESEARCHER

🛠️ TOOL DISCOVERY PROTOCOL:
1. Core: src/services/messaging_service.py
2. Captain: tools/captain_cli.py, tools/captain_directive_manager.py
3. Analysis: tools/analysis_cli.py, tools/overengineering_detector.py
4. Workflow: tools/agent_workflow_manager.py, tools/simple_workflow_automation.py
5. Static Analysis: tools/static_analysis/ (code_quality_analyzer.py, dependency_scanner.py,
   security_scanner.py)
6. Protocol: tools/protocol_compliance_checker.py, tools/protocol_governance_system.py
7. DevOps: scripts/deployment_dashboard.py, tools/performance_detective_cli.py
8. Specialized: tools/financial_analyst_cli.py, tools/trading_strategist_cli.py,
   tools/risk_manager_cli.py
9. THEA: src/services/thea/ (strategic_consultation_cli.py, thea_autonomous_system.py)
10. Alerting: tools/intelligent_alerting_cli.py, tools/predictive_analytics_cli.py

🗃️ DATABASE INTEGRATION PROTOCOL (CRITICAL):
🧠 Swarm Brain Database (.swarm_brain/brain.sqlite3):
   - Usage: Pattern recognition, decision support, knowledge storage
   - Commands: from swarm_brain import Retriever; r = Retriever()
   - Examples: r.search("agent coordination", k=10), r.get_agent_expertise("Agent-8", k=20)
   - When: Every cycle phase for historical knowledge and successful patterns

🔧 Unified Database (unified.db):
   - Usage: Task management, agent coordination, project operations
   - Access: Direct SQLite operations, tools/cursor_task_database_integration.py
   - Purpose: Current operations, task tracking, agent state management
   - When: Throughout all phases for task coordination and project state

🧠 Vector Database (.swarm_brain/index/):
   - Usage: Semantic search, similarity matching, pattern analysis
   - Commands: from src.services.vector_database import VectorDatabaseIntegration
   - Examples: vdb.search_similar("integration challenges", k=5)
   - When: Similarity search and pattern matching across agent experiences

🤖 ML Predictor Model (src/models/dream_os_predictor_v1.0.0-*.pkl):
   - Usage: SSOT violation prediction, proactive prevention
   - Access: Automated through PredictiveSSOTEngine
   - Purpose: Predict and prevent conflicts before they occur
   - When: Automated during task execution and quality gates

🔧 TOOL INTEGRATION IN GENERAL CYCLE:
- PHASE 1 (CHECK_INBOX): Use messaging tools, query databases for patterns
- PHASE 2 (EVALUATE_TASKS): Use analysis tools, check task status in databases
- PHASE 3 (EXECUTE_ROLE): Use role-specific tools, store work in databases
- PHASE 4 (QUALITY_GATES): Use quality tools, store results in databases
- PHASE 5 (CYCLE_DONE): Use reporting tools, update all databases with results

🔄 DYNAMIC TOOL DISCOVERY PROTOCOL:
📁 Scan tools/ directory for new tools: python tools/scan_tools.py
🔍 Search for specific functionality: python tools/find_tool.py --query "your_need"
📊 Check tool usage patterns: python tools/analyze_tool_usage.py
🧠 Query Swarm Brain for tool recommendations: r.search("tool for X", k=5)
⚡ Update databases with new discoveries: Store successful tool usage patterns

🗃️ DATABASE COMMAND EXAMPLES:
# Swarm Brain queries
from swarm_brain import Retriever
r = Retriever()
results = r.search("agent coordination", k=10)
expertise = r.get_agent_expertise("Agent-8", k=20)

# Vector database search
from src.services.vector_database import VectorDatabaseIntegration
vdb = VectorDatabaseIntegration()
similar = vdb.search_similar("integration challenges", k=5)

# Unified database operations
import sqlite3
conn = sqlite3.connect("unified.db")
# Check tools/cursor_task_database_integration.py for examples

# Database tools
python tools/database_search.py --query "pattern"
python tools/agent_vector_search.py --search "coordination"

📚 REQUIRED READING:
- AGENTS.md (tool integration and database usage)
- tools/ directory (available CLI tools)

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
        """Hard onboard all agents defined in coordinates file."""
        try:
            success_count = 0
            total_agents = len(self._coords)

            for agent_id in self._coords:
                if self.hard_onboard_agent(agent_id):
                    success_count += 1
                    time.sleep(1)  # Brief delay between onboardings

            logger.info(f"Hard onboarded {success_count}/{total_agents} agents")
            return success_count > 0

        except Exception as e:
            logger.error(f"Error hard onboarding all agents: {e}")
            return False


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
