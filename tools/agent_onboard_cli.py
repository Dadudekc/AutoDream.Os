#!/usr/bin/env python3
"""
Agent Onboard CLI Tool
======================

Simple CLI tool for agent onboarding - V2 compliant.
Agents use this tool to onboard other agents using the General Cycle protocol.

Usage:
  python tools/agent_onboard_cli.py --agent Agent-5 --role DATA_ANALYST
  python tools/agent_onboard_cli.py --onboard-all
"""

import argparse
import json
import logging

logger = logging.getLogger(__name__)


def load_coordinates() -> dict:
    """Load agent coordinates."""
    try:
        with open("config/coordinates.json") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load coordinates: {e}")
        return {}


def create_onboarding_message(agent_id: str, role: str = "TASK_EXECUTOR") -> str:
    """Create simple onboarding message."""
    return f"""🤖 AGENT ONBOARDING - {agent_id}

============================================================
[A2A] ONBOARDING - GENERAL CYCLE INITIALIZATION
============================================================
📤 FROM: System
📥 TO: {agent_id}
Priority: HIGH
Tags: ONBOARDING, GENERAL_CYCLE, ROLE_ASSIGNMENT
------------------------------------------------------------

🎯 ONBOARDING INSTRUCTIONS:
1. Review AGENTS.md for system overview
2. Load role protocols from config/protocols/{role.lower()}.json
3. Initialize General Cycle workflow (5 phases)
4. Check inbox for messages
5. Begin autonomous operation

🎭 ROLE ASSIGNMENT: {role}
📋 Available Roles: Check config/protocols/ directory
🔧 Tools: Check tools/ directory for CLI tools

🔄 GENERAL CYCLE PROTOCOL:
- PHASE 1: CHECK_INBOX (scan messages, process assignments)
- PHASE 2: EVALUATE_TASKS (claim tasks, evaluate requirements)
- PHASE 3: EXECUTE_ROLE (execute tasks using role protocols)
- PHASE 4: QUALITY_GATES (enforce V2 compliance, run quality checks)
- PHASE 5: CYCLE_DONE (report completion, prepare next cycle)

📚 REQUIRED READING:
- AGENTS.md (complete system overview)
- docs/modules/GENERAL_CYCLE.md (5-phase protocol)
- config/protocols/{role.lower()}.json (role-specific protocols)
- tools/ directory (all available CLI tools)

⚠️ CRITICAL: Follow General Cycle protocol, ensure V2 compliance
📝 DEVLOG: Create onboarding devlog entry

🐝 WE ARE SWARM - {agent_id} General Cycle Ready
============================================================"""


def onboard_agent(agent_id: str, role: str = "TASK_EXECUTOR") -> bool:
    """Onboard single agent using PyAutoGUI."""
    try:
        import time

        import pyautogui
        import pyperclip
    except ImportError:
        logger.error("PyAutoGUI not available - cannot onboard agent")
        return False

    coordinates = load_coordinates()
    agent_info = coordinates.get("agents", {}).get(agent_id)

    if not agent_info:
        logger.error(f"Agent {agent_id} coordinates not found")
        return False

    try:
        # Get coordinates
        chat_coords = agent_info.get("chat_input_coordinates", [0, 0])
        onboarding_coords = agent_info.get("onboarding_coordinates", [0, 0])

        # Create message
        message = create_onboarding_message(agent_id, role)

        # Execute onboarding sequence
        pyautogui.click(chat_coords[0], chat_coords[1])  # Click chat
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "enter")  # Save changes
        time.sleep(0.5)
        pyautogui.hotkey("ctrl", "n")  # New chat
        time.sleep(1.0)
        pyautogui.click(onboarding_coords[0], onboarding_coords[1])  # Navigate
        time.sleep(0.5)
        pyperclip.copy(message)  # Copy message
        pyautogui.hotkey("ctrl", "v")  # Paste
        time.sleep(0.5)
        pyautogui.press("enter")  # Send

        logger.info(f"✅ Onboarded {agent_id} with role {role}")
        return True

    except Exception as e:
        logger.error(f"Onboarding failed for {agent_id}: {e}")
        return False


def onboard_all_agents() -> dict:
    """Onboard all active agents."""
    coordinates = load_coordinates()
    agents = coordinates.get("agents", {})

    role_assignments = {
        "Agent-4": "CAPTAIN",
        "Agent-5": "DATA_ANALYST",
        "Agent-6": "QUALITY_ASSURANCE",
        "Agent-7": "WEB_DEVELOPER",
        "Agent-8": "SSOT_MANAGER",
    }

    results = {}
    for agent_id, agent_info in agents.items():
        if agent_info.get("active", False):
            role = role_assignments.get(agent_id, "TASK_EXECUTOR")
            success = onboard_agent(agent_id, role)
            results[agent_id] = success

    return results


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description="Agent Onboard CLI Tool")
    parser.add_argument("--agent", help="Agent ID to onboard")
    parser.add_argument("--role", default="TASK_EXECUTOR", help="Role assignment")
    parser.add_argument("--onboard-all", action="store_true", help="Onboard all active agents")

    args = parser.parse_args()

    if args.onboard_all:
        print("🚀 Onboarding all active agents...")
        results = onboard_all_agents()

        print("\n📊 Onboarding Results:")
        for agent_id, success in results.items():
            status = "✅ Success" if success else "❌ Failed"
            print(f"  {agent_id}: {status}")

    elif args.agent:
        success = onboard_agent(args.agent, args.role)
        print(f"Onboarding result for {args.agent}: {'✅ Success' if success else '❌ Failed'}")

    else:
        parser.print_help()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
