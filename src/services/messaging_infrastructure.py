#!/usr/bin/env python3
"""
UNIFIED MESSAGING INFRASTRUCTURE - Services Layer Consolidation
===============================================================
Consolidates messaging CLI support (7 files → 1): parser, formatters, handlers, service adapters
V2 Compliance | Author: Agent-2 | Date: 2025-10-15
"""

from __future__ import annotations

import argparse
import logging
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pyautogui

from src.core.coordinate_loader import get_coordinate_loader
from src.core.gamification.autonomous_competition_system import get_competition_system
from src.core.messaging_core import (
    UnifiedMessagePriority,
    UnifiedMessageTag,
    UnifiedMessageType,
    send_message,
)

logger = logging.getLogger(__name__)

# ============================================================================
# MESSAGE TEMPLATES & FORMATTERS
# ============================================================================

CLI_HELP_EPILOG = "🐝 SWARM MESSAGING CLI\nExamples: --message '...' --agent Agent-1 | --broadcast"

SURVEY_MESSAGE_TEMPLATE = """
🐝 SWARM SURVEY INITIATED - SRC/ DIRECTORY ANALYSIS
================================================

**OBJECTIVE:** Comprehensive analysis of src/ directory for consolidation planning
**TARGET:** 683 → ~250 files with full functionality preservation

**PHASES:**
1. Structural Analysis (Directories, files, dependencies)
2. Functional Analysis (Services, capabilities, relationships)
3. Quality Assessment (V2 compliance, violations, anti-patterns)
4. Consolidation Planning (Opportunities, risks, rollback strategies)

**COORDINATION:** Real-time via PyAutoGUI messaging system
**COMMANDER:** Captain Agent-4 (Quality Assurance Specialist)

🐝 WE ARE SWARM - UNITED IN ANALYSIS!
"""

ASSIGNMENT_MESSAGE_TEMPLATE = """
🐝 SURVEY ASSIGNMENT - {agent}
============================

**ROLE:** {assignment}

**DELIVERABLES:**
1. Structural Analysis Report
2. Functional Analysis Report
3. Quality Assessment Report
4. Consolidation Recommendations

**TIMELINE:** 8 days total survey
**COORDINATION:** Real-time via PyAutoGUI

🐝 YOUR EXPERTISE IS CRUCIAL FOR SUCCESSFUL CONSOLIDATION!
"""

CONSOLIDATION_MESSAGE_TEMPLATE = """
🔧 CONSOLIDATION UPDATE
======================

**BATCH:** {batch}
**STATUS:** {status}
**TIMESTAMP:** {timestamp}

**COORDINATION:** Real-time swarm coordination active
**COMMANDER:** Captain Agent-4

🔧 CONSOLIDATION PROGRESS CONTINUES...
"""

AGENT_ASSIGNMENTS = {
    "Agent-1": "Service Layer Specialist - Analyze src/services/",
    "Agent-2": "Core Systems Architect - Analyze src/core/",
    "Agent-3": "Web & API Integration - Analyze src/web/ and src/infrastructure/",
    "Agent-4": "Domain & Quality Assurance - Cross-cutting analysis + coordination",
    "Agent-5": "Trading & Gaming Systems - Analyze specialized systems",
    "Agent-6": "Testing & Infrastructure - Analyze tests/ and tools/",
    "Agent-7": "Performance & Monitoring - Analyze monitoring components",
    "Agent-8": "Integration & Coordination - Analyze integration points",
}

SWARM_AGENTS = [
    "Agent-1",
    "Agent-2",
    "Agent-3",
    "Agent-4",
    "Agent-5",
    "Agent-6",
    "Agent-7",
    "Agent-8",
]

# ============================================================================
# ARGUMENT PARSER
# ============================================================================


def create_messaging_parser() -> argparse.ArgumentParser:
    """Create the argument parser for messaging CLI."""
    parser = argparse.ArgumentParser(
        description="🐝 SWARM Messaging CLI - Command the swarm through PyAutoGUI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=CLI_HELP_EPILOG,
    )

    # Core messaging arguments
    parser.add_argument("--message", "-m", type=str, help="Message content to send")

    parser.add_argument("--agent", "-a", type=str, help="Target agent ID (e.g., Agent-1, Agent-2)")

    parser.add_argument(
        "--broadcast", "-b", action="store_true", help="Broadcast message to all agents"
    )

    # Message options
    parser.add_argument(
        "--priority",
        "-p",
        choices=["regular", "urgent"],
        default="regular",
        help="Message priority (default: regular)",
    )

    parser.add_argument("--tags", "-t", nargs="+", help="Message tags for categorization")

    # PyAutoGUI options
    parser.add_argument(
        "--pyautogui", "--gui", action="store_true", help="Use PyAutoGUI for message delivery"
    )

    # Survey coordination flags
    parser.add_argument(
        "--survey-coordination", action="store_true", help="Initiate survey coordination mode"
    )

    parser.add_argument(
        "--consolidation-coordination",
        action="store_true",
        help="Initiate consolidation coordination mode",
    )

    parser.add_argument("--consolidation-batch", type=str, help="Specify consolidation batch ID")

    parser.add_argument(
        "--consolidation-status", type=str, help="Specify consolidation status update"
    )

    # Coordinate display
    parser.add_argument(
        "--coordinates", action="store_true", help="Display agent coordinates and configuration"
    )

    # Agent start flag
    parser.add_argument(
        "--start",
        nargs="+",
        type=int,
        metavar="N",
        help="Start agents (1-8, e.g., --start 1 2 3) - sends to onboarding coordinates",
    )

    parser.add_argument(
        "--save",
        action="store_true",
        help="Send message to all agents' chat input coords and press Ctrl+Enter to save",
    )

    parser.add_argument(
        "--leaderboard",
        action="store_true",
        help="Display the autonomous competition leaderboard",
    )

    # Task system flags (SSOT Blocker Resolution - Agent-8)
    parser.add_argument(
        "--get-next-task",
        action="store_true",
        help="Claim next available assigned task (requires --agent)",
    )

    parser.add_argument(
        "--list-tasks",
        action="store_true",
        help="List all available tasks in queue",
    )

    parser.add_argument(
        "--task-status",
        type=str,
        metavar="TASK_ID",
        help="Check status of specific task",
    )

    parser.add_argument(
        "--complete-task",
        type=str,
        metavar="TASK_ID",
        help="Mark task as complete",
    )

    return parser


# ============================================================================
# MESSAGE HANDLERS
# ============================================================================


def send_message_pyautogui(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Send a message via PyAutoGUI using unified messaging core."""
    return send_message(
        content=message,
        sender="CAPTAIN",
        recipient=agent_id,
        message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
        priority=UnifiedMessagePriority.REGULAR,
        tags=[UnifiedMessageTag.SYSTEM],
    )


def send_message_to_onboarding_coords(agent_id: str, message: str, timeout: int = 30) -> bool:
    """Alias for send_message_pyautogui to handle onboarding messaging."""
    return send_message_pyautogui(agent_id, message, timeout)


class MessageCoordinator:
    """Unified message coordination system."""

    @staticmethod
    def send_to_agent(
        agent: str, message: str, priority=UnifiedMessagePriority.REGULAR, use_pyautogui=False
    ):
        try:
            # Always use inbox delivery since PyAutoGUI module missing
            return send_message(
                content=message,
                sender="CAPTAIN",
                recipient=agent,
                message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
                priority=priority,
                tags=[UnifiedMessageTag.SYSTEM],
            )
        except Exception:
            return False

    @staticmethod
    def broadcast_to_all(message: str, priority=UnifiedMessagePriority.REGULAR):
        return sum(
            1
            for agent in SWARM_AGENTS
            if send_message(
                content=message,
                sender="CAPTAIN",
                recipient=agent,
                message_type=UnifiedMessageType.BROADCAST,
                priority=priority,
                tags=[UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION],
            )
        )

    @staticmethod
    def coordinate_survey():
        logger.info("🐝 INITIATING SWARM SURVEY COORDINATION...")
        success_count = MessageCoordinator.broadcast_to_all(
            SURVEY_MESSAGE_TEMPLATE, UnifiedMessagePriority.URGENT
        )
        if success_count > 0:
            logger.info(f"✅ Survey coordination broadcast to {success_count} agents")
            return True
        else:
            logger.error("❌ Survey coordination failed - no agents reached")
            return False

    @staticmethod
    def coordinate_consolidation(batch: str, status: str):
        message = CONSOLIDATION_MESSAGE_TEMPLATE.format(
            batch=batch or "DEFAULT",
            status=status or "IN_PROGRESS",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        success_count = MessageCoordinator.broadcast_to_all(message, UnifiedMessagePriority.REGULAR)
        if success_count > 0:
            logger.info(f"✅ Consolidation update broadcast to {success_count} agents")
            return True
        else:
            logger.error("❌ Consolidation update failed")
            return False


def handle_message(args, parser) -> int:
    """Handle message sending."""
    try:
        if not args.agent and not args.broadcast:
            print("❌ ERROR: Either --agent or --broadcast must be specified")
            parser.print_help()
            return 1

        priority = (
            UnifiedMessagePriority.URGENT
            if args.priority == "urgent"
            else UnifiedMessagePriority.REGULAR
        )

        if args.broadcast:
            success_count = MessageCoordinator.broadcast_to_all(args.message, priority)
            if success_count > 0:
                print(f"✅ Broadcast to {success_count} agents successful")
                return 0
            else:
                print("❌ Broadcast failed")
                return 1
        else:
            if MessageCoordinator.send_to_agent(args.agent, args.message, priority):
                print(f"✅ Message sent to {args.agent}")
                return 0
            else:
                print(f"❌ Failed to send message to {args.agent}")
                return 1

    except Exception as e:
        logger.error(f"Message handling error: {e}")
        return 1


def handle_survey() -> int:
    """Handle survey coordination initiation."""
    try:
        if MessageCoordinator.coordinate_survey():
            print("✅ Survey coordination initiated successfully")
            return 0
        else:
            print("❌ Survey coordination failed")
            return 1
    except Exception as e:
        logger.error(f"Survey coordination error: {e}")
        return 1


def handle_consolidation(args) -> int:
    """Handle consolidation coordination."""
    try:
        if MessageCoordinator.coordinate_consolidation(
            args.consolidation_batch, args.consolidation_status
        ):
            print("✅ Consolidation coordination successful")
            return 0
        else:
            print("❌ Consolidation coordination failed")
            return 1
    except Exception as e:
        logger.error(f"Consolidation coordination error: {e}")
        return 1


def handle_coordinates() -> int:
    """Display agent coordinates."""
    try:
        coord_loader = get_coordinate_loader()
        print("\n🐝 SWARM AGENT COORDINATES")
        print("=" * 50)
        for agent in SWARM_AGENTS:
            chat_coords = coord_loader.get_chat_coordinates(agent)
            onboard_coords = coord_loader.get_onboarding_coordinates(agent)
            print(f"\n{agent}:")
            print(f"  Chat:      {chat_coords}")
            print(f"  Onboarding: {onboard_coords}")
        print("\n" + "=" * 50)
        return 0
    except Exception as e:
        logger.error(f"Coordinates display error: {e}")
        return 1


def handle_start_agents(args) -> int:
    """Handle starting agents via onboarding coordinates."""
    try:
        agent_numbers = args.start
        message = args.message if hasattr(args, "message") and args.message else "START"

        for num in agent_numbers:
            agent_id = f"Agent-{num}"
            if agent_id not in SWARM_AGENTS:
                print(f"⚠️  Invalid agent: {agent_id}")
                continue

            if send_message_to_onboarding_coords(agent_id, message):
                print(f"✅ Started {agent_id}")
            else:
                print(f"❌ Failed to start {agent_id}")

        return 0
    except Exception as e:
        logger.error(f"Start agents error: {e}")
        return 1


def handle_save(args, parser) -> int:
    """Handle save operation (Ctrl+Enter to all agents)."""
    try:
        if not args.message:
            print("❌ ERROR: --message required for save operation")
            return 1

        coord_loader = get_coordinate_loader()
        for agent in SWARM_AGENTS:
            try:
                chat_coords = coord_loader.get_chat_coordinates(agent)
                pyautogui.click(chat_coords[0], chat_coords[1])
                time.sleep(0.2)
                pyautogui.write(args.message, interval=0.01)
                pyautogui.hotkey("ctrl", "enter")
                print(f"✅ Saved to {agent}")
                time.sleep(0.5)
            except Exception as e:
                print(f"❌ Failed to save to {agent}: {e}")

        return 0
    except Exception as e:
        logger.error(f"Save operation error: {e}")
        return 1


def handle_leaderboard() -> int:
    """Display the autonomous competition leaderboard."""
    try:
        competition_system = get_competition_system()
        leaderboard = competition_system.get_leaderboard()

        print("\n🏆 AUTONOMOUS COMPETITION LEADERBOARD")
        print("=" * 60)
        for rank, entry in enumerate(leaderboard, start=1):
            agent = entry["agent_id"]
            score = entry["score"]
            completed = entry.get("contracts_completed", 0)
            print(f"{rank}. {agent:10s} - {score:5d} pts ({completed} contracts)")
        print("=" * 60)
        return 0
    except Exception as e:
        logger.error(f"Leaderboard error: {e}")
        print("❌ Failed to display leaderboard")
        return 1


# ============================================================================
# SERVICE ADAPTERS (formerly messaging_service.py, messaging_discord.py)
# ============================================================================


class ConsolidatedMessagingService:
    """Consolidated messaging service adapter for Discord bot."""

    def __init__(self):
        """Initialize messaging service."""
        self.project_root = Path(__file__).parent.parent.parent
        self.messaging_cli = self.project_root / "src" / "services" / "messaging_cli.py"
        logger.info("ConsolidatedMessagingService initialized")

    def send_message(
        self, agent: str, message: str, priority: str = "regular", use_pyautogui: bool = True
    ) -> dict[str, Any]:
        """
        Send message to agent via messaging_cli.py subprocess.

        Args:
            agent: Target agent ID (e.g., "Agent-1")
            message: Message content
            priority: Message priority ("regular" or "urgent")
            use_pyautogui: Whether to use PyAutoGUI delivery

        Returns:
            Dictionary with success status and message
        """
        try:
            cmd = [
                "python",
                str(self.messaging_cli),
                "--agent",
                agent,
                "--message",
                message,
                "--priority",
                priority,
            ]

            if use_pyautogui:
                cmd.append("--pyautogui")

            # Set PYTHONPATH
            env = {"PYTHONPATH": str(self.project_root)}

            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=30, env=env, cwd=str(self.project_root)
            )

            if result.returncode == 0:
                logger.info(f"Message sent to {agent}: {message[:50]}...")
                return {"success": True, "message": f"Message sent to {agent}", "agent": agent}
            else:
                error_msg = result.stderr or "Unknown error"
                logger.error(f"Failed to send message to {agent}: {error_msg}")
                return {
                    "success": False,
                    "message": f"Failed to send message: {error_msg}",
                    "agent": agent,
                }

        except subprocess.TimeoutExpired:
            logger.error(f"Timeout sending message to {agent}")
            return {"success": False, "message": "Message timeout", "agent": agent}
        except Exception as e:
            logger.error(f"Error sending message to {agent}: {e}")
            return {"success": False, "message": str(e), "agent": agent}

    def broadcast_message(self, message: str, priority: str = "regular") -> dict[str, Any]:
        """
        Broadcast message to all agents.

        Args:
            message: Message content
            priority: Message priority

        Returns:
            Dictionary with success status
        """
        agents = [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]

        results = []
        for agent in agents:
            result = self.send_message(agent, message, priority, use_pyautogui=True)
            results.append(result)

        success_count = sum(1 for r in results if r.get("success"))

        return {
            "success": success_count > 0,
            "message": f"Broadcast to {success_count}/{len(agents)} agents",
            "results": results,
        }


# Discord integration adapter
def send_discord_message(agent: str, message: str, priority: str = "regular") -> bool:
    """Send message via Discord integration (wraps ConsolidatedMessagingService)."""
    service = ConsolidatedMessagingService()
    result = service.send_message(agent, message, priority, use_pyautogui=False)
    return result.get("success", False)


def broadcast_discord_message(message: str, priority: str = "regular") -> dict[str, Any]:
    """Broadcast message via Discord integration."""
    service = ConsolidatedMessagingService()
    return service.broadcast_message(message, priority)
