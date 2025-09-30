#!/usr/bin/env python3
"""
Enhanced Agent Onboarding Service
================================

Comprehensive onboarding sequence for V2_SWARM agents.
V2 Compliant: ≤400 lines, focused onboarding functionality.

Author: Agent-7 (Implementation Specialist)
License: MIT
"""

import json
import logging
import time
from typing import Any

# Lazy import to prevent hard dep at import time
try:
    import pyautogui  # noqa: F401
    import pyperclip  # noqa: F401
except Exception as e:
    pyautogui = None  # type: ignore
    pyperclip = None  # type: ignore
    logging.warning(f"PyAutoGUI import failed: {e}")

logger = logging.getLogger(__name__)


class EnhancedOnboardingService:
    """Enhanced onboarding service with comprehensive agent initialization."""

    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize the enhanced onboarding service."""
        self.coord_path = coord_path
        self.coordinates = self._load_coordinates()

    def _load_coordinates(self) -> dict[str, Any]:
        """Load agent coordinates from config file."""
        try:
            with open(self.coord_path) as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load coordinates: {e}")
            return {}

    def get_agent_coordinates(self, agent_id: str) -> dict[str, Any] | None:
        """Get coordinates for specific agent."""
        agents = self.coordinates.get("agents", {})
        return agents.get(agent_id)

    def create_onboarding_message(self, agent_id: str, role_assignment: str = None) -> str:
        """Create comprehensive onboarding message."""

        # Get agent info
        agent_info = self.get_agent_coordinates(agent_id)
        agent_name = agent_info.get("description", "Agent") if agent_info else "Agent"

        # Default role assignment if not provided
        if not role_assignment:
            role_assignment = "TASK_EXECUTOR"  # Default operational role

        onboarding_message = f"""🤖 AGENT ONBOARDING PROTOCOL - {agent_id}

============================================================
[A2A] ONBOARDING - SYSTEM INITIALIZATION
============================================================
📤 FROM: System
📥 TO: {agent_id} ({agent_name})
Priority: HIGH
Tags: ONBOARDING, INITIALIZATION, ROLE_ASSIGNMENT
------------------------------------------------------------

🎯 ONBOARDING INSTRUCTIONS:
1. Review AGENTS.md file for complete system overview
2. Load your agent capabilities from config/agent_capabilities.json
3. Initialize your workspace and inbox system
4. Discover and integrate available tools
5. Begin autonomous workflow cycle
6. Report status to Captain Agent-4

🎭 ROLE ASSIGNMENT: {role_assignment}
📋 Available Roles: Check config/protocols/ directory
🔧 Tools: Check tools/ directory for role-specific CLI tools

🛠️ TOOL DISCOVERY PROTOCOL:
1. Core Communication: src/services/consolidated_messaging_service.py
2. Captain Tools: tools/captain_cli.py, tools/captain_directive_manager.py
3. Analysis Tools: tools/analysis_cli.py, tools/overengineering_detector.py
4. Workflow Tools: tools/agent_workflow_manager.py, tools/simple_workflow_automation.py
5. Static Analysis: tools/static_analysis/ (code_quality_analyzer.py, dependency_scanner.py, security_scanner.py)
6. Protocol Tools: tools/protocol_compliance_checker.py, tools/protocol_governance_system.py
7. DevOps Tools: scripts/deployment_dashboard.py, tools/performance_detective_cli.py
8. Specialized Tools: tools/financial_analyst_cli.py, tools/trading_strategist_cli.py, tools/risk_manager_cli.py
9. THEA Integration: src/services/thea/ (strategic_consultation_cli.py, thea_autonomous_system.py)
10. Alerting Tools: tools/intelligent_alerting_cli.py, tools/predictive_analytics_cli.py

🔧 TOOL INTEGRATION IN GENERAL CYCLE:
- PHASE 1 (CHECK_INBOX): Use messaging tools, check tool status
- PHASE 2 (EVALUATE_TASKS): Use analysis tools, workflow tools
- PHASE 3 (EXECUTE_ROLE): Use role-specific tools, specialized tools
- PHASE 4 (QUALITY_GATES): Use quality tools, static analysis tools
- PHASE 5 (CYCLE_DONE): Use reporting tools, update tool status

📚 REQUIRED READING:
- AGENTS.md (complete tool integration in General Cycle)
- config/agent_capabilities.json (your capabilities)
- config/protocols/{role_assignment.lower()}.json (role protocols)
- tools/ directory (all available CLI tools)
- src/services/ directory (all available services)

🔄 ONBOARDING SEQUENCE:
1. Load role protocols and adapt behavior
2. Initialize autonomous workflow components
3. Discover and integrate available tools
4. Check inbox for pending messages
5. Begin first general cycle
6. Report "ONBOARDING_COMPLETE" to Agent-4

⚠️ CRITICAL: Ensure V2 compliance (≤400 lines, proper structure)
📝 DEVLOG: Create onboarding devlog entry

🐝 WE ARE SWARM - {agent_id} Initialization Complete
============================================================"""

        return onboarding_message

    def execute_enhanced_onboarding(self, agent_id: str, role_assignment: str = None) -> bool:
        """Execute the enhanced 7-step onboarding sequence."""

        if not pyautogui or not pyperclip:
            logger.error("PyAutoGUI or pyperclip not available")
            return False

        try:
            # Get agent coordinates
            agent_coords = self.get_agent_coordinates(agent_id)
            if not agent_coords:
                logger.error(f"Agent {agent_id} coordinates not found")
                return False

            chat_coords = agent_coords.get("chat_input_coordinates", [0, 0])
            onboarding_coords = agent_coords.get("onboarding_coordinates", [0, 0])

            # Create onboarding message
            onboarding_message = self.create_onboarding_message(agent_id, role_assignment)

            logger.info(f"Starting enhanced onboarding for {agent_id}")
            logger.info(f"Chat coordinates: {chat_coords}")
            logger.info(f"Onboarding coordinates: {onboarding_coords}")

            # Step 1: Click chat input coordinates (get attention of correct agent IDE)
            logger.info("Step 1: Clicking chat input coordinates to get agent attention")
            pyautogui.click(chat_coords[0], chat_coords[1])
            time.sleep(0.5)

            # Step 2: Press ctrl+shift+backspace to stop agents that are running
            logger.info("Step 2: Stopping any running agents")
            pyautogui.hotkey("ctrl", "shift", "backspace")
            time.sleep(0.5)

            # Step 3: Press ctrl+enter to save all changes
            logger.info("Step 3: Saving all changes")
            pyautogui.hotkey("ctrl", "enter")
            time.sleep(0.5)

            # Step 4: Press ctrl+N to open a new chat
            logger.info("Step 4: Opening new chat")
            pyautogui.hotkey("ctrl", "n")
            time.sleep(1.0)  # Wait for new chat to load

            # Step 5: Navigate to the onboarding coordinates
            logger.info("Step 5: Navigating to onboarding coordinates")
            pyautogui.click(onboarding_coords[0], onboarding_coords[1])
            time.sleep(0.5)

            # Step 6: Paste the onboarding message
            logger.info("Step 6: Pasting onboarding message")
            pyperclip.copy(onboarding_message)
            time.sleep(0.2)
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.5)

            # Step 7: Press enter to send the onboarding message
            logger.info("Step 7: Sending onboarding message")
            pyautogui.press("enter")
            time.sleep(0.5)

            logger.info(f"✅ Enhanced onboarding completed for {agent_id}")
            return True

        except Exception as e:
            logger.error(f"Enhanced onboarding failed for {agent_id}: {e}")
            return False

    def onboard_all_active_agents(self, role_assignments: dict[str, str] = None) -> dict[str, bool]:
        """Onboard all active agents with the enhanced sequence."""

        if not role_assignments:
            role_assignments = {
                "Agent-4": "CAPTAIN",
                "Agent-5": "DATA_ANALYST",
                "Agent-6": "QUALITY_ASSURANCE",
                "Agent-7": "WEB_DEVELOPER",
                "Agent-8": "SSOT_MANAGER",
            }

        results = {}
        agents = self.coordinates.get("agents", {})

        for agent_id, agent_info in agents.items():
            if agent_info.get("active", False):
                role = role_assignments.get(agent_id, "TASK_EXECUTOR")
                logger.info(f"Onboarding {agent_id} with role {role}")

                # Add delay between agents to avoid conflicts
                if results:  # Not the first agent
                    time.sleep(2.0)

                success = self.execute_enhanced_onboarding(agent_id, role)
                results[agent_id] = success

        return results


def main():
    """Main function for testing enhanced onboarding."""
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced Agent Onboarding Service")
    parser.add_argument("--agent", help="Agent ID to onboard")
    parser.add_argument("--role", help="Role assignment for agent")
    parser.add_argument("--onboard-all", action="store_true", help="Onboard all active agents")
    parser.add_argument("--test-sequence", action="store_true", help="Test onboarding sequence")

    args = parser.parse_args()

    service = EnhancedOnboardingService()

    if args.test_sequence:
        print("🧪 Testing enhanced onboarding sequence...")
        print(
            "Sequence: 1) Chat click 2) Stop agents 3) Save 4) New chat 5) Navigate 6) Paste 7) Send"
        )

    elif args.agent:
        success = service.execute_enhanced_onboarding(args.agent, args.role)
        print(f"Onboarding result for {args.agent}: {'✅ Success' if success else '❌ Failed'}")

    elif args.onboard_all:
        print("🚀 Starting enhanced onboarding for all active agents...")
        results = service.onboard_all_active_agents()

        print("\n📊 Onboarding Results:")
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {agent_id}: {status}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
