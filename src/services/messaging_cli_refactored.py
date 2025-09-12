#!/usr/bin/env python3
"""
🐝 UNIFIED MESSAGING CLI - SWARM COMMAND CENTER
==============================================

V2 Compliance: Refactored for <400 lines
SOLID Principles: Single Responsibility, Open-Closed

Author: Agent-6 - V2 Compliance Refactor
"""

import argparse
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from src.core.coordinate_loader import get_coordinate_loader
    from src.services.consolidated_messaging_service import (
        UnifiedMessage,
        UnifiedMessagePriority,
        UnifiedMessageTag,
        UnifiedMessageType,
        broadcast_message,
        get_messaging_core,
        list_agents,
        send_message,
        send_message_inbox,
        send_message_pyautogui,
        send_message_with_fallback,
        show_message_history,
    )

    MESSAGING_AVAILABLE = True
except ImportError as e:
    logger.error(f"❌ Messaging system not available: {e}")
    MESSAGING_AVAILABLE = False


# Constants - extracted for V2 compliance
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

CLI_HELP_EPILOG = """
🐝 SWARM MESSAGING CLI - COMMAND YOUR AGENTS!
==============================================

EXAMPLES:
--------
# Send message to specific agent
python -m src.services.messaging_cli --message "Start survey" --agent Agent-1
# Broadcast to all agents
python -m src.services.messaging_cli --message "SWARM ALERT!" --broadcast
# Send with priority and tags
python -m src.services.messaging_cli --message "URGENT: Fix issue" --agent Agent-2 --priority urgent --tags bug critical

# Agent revival commands (NEW!)
python -m src.services.messaging_cli --revive-agent --agent Agent-1  # Revive specific agent
python -m src.services.messaging_cli --revive-all                    # Revive all agents

🐝 WE. ARE. SWARM - URGENT REVIVAL VIA CTRL+ENTER!
"""

REVIVAL_MESSAGE_TEMPLATE = """
🐝 AGENT REVIVAL SIGNAL - STALLED AGENT DETECTED
===============================================

**AGENT ID:** {agent_id}
**STATUS:** STALLED - REQUIRES IMMEDIATE ATTENTION
**TIMESTAMP:** {timestamp}

**REVIVAL PROTOCOL ACTIVATED:**
1. Focus on chat input coordinates
2. Clear any pending input
3. Send urgent revival message
4. Double-enter confirmation for activation

🐝 WE ARE SWARM - REVIVAL COMPLETE!
"""

BROADCAST_REVIVAL_TEMPLATE = """
🚨 SWARM REVIVAL ALERT - ALL AGENTS
===================================

**STATUS:** MULTIPLE AGENTS STALLED
**ACTION:** IMMEDIATE REVIVAL PROTOCOL

All agents receiving ctrl+enter urgent revival signals.

🐝 WE ARE SWARM - COORDINATED REVIVAL!
"""

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


class MessageCoordinator:
    """Unified message coordination system."""

    @staticmethod
    def send_to_agent(
        agent: str, message: str, priority=UnifiedMessagePriority.NORMAL, use_pyautogui=False
    ):
        try:
            return (
                send_message_pyautogui(agent_id=agent, message=message, timeout=30)
                if use_pyautogui
                else send_message(
                    content=message,
                    sender="CAPTAIN",
                    recipient=agent,
                    message_type=UnifiedMessageType.CAPTAIN_TO_AGENT,
                    priority=priority,
                    tags=[UnifiedMessageTag.SYSTEM],
                )
            )
        except:
            return False

    @staticmethod
    def broadcast_to_all(message: str, priority=UnifiedMessagePriority.NORMAL):
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
            for agent, assignment in AGENT_ASSIGNMENTS.items():
                msg = ASSIGNMENT_MESSAGE_TEMPLATE.format(agent=agent, assignment=assignment)
                send_message_pyautogui(agent_id=agent, message=msg, timeout=60)
        return success_count

    @staticmethod
    def coordinate_consolidation(batch: str, status: str):
        from datetime import datetime

        msg = CONSOLIDATION_MESSAGE_TEMPLATE.format(
            batch=batch, status=status, timestamp=datetime.now().isoformat()
        )
        return sum(
            1
            for agent in SWARM_AGENTS
            if send_message(
                content=msg,
                sender="CAPTAIN",
                recipient=agent,
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT,
                tags=[UnifiedMessageTag.SYSTEM, UnifiedMessageTag.COORDINATION],
            )
        )


class MessagingCLI:
    """Command-line interface for messaging operations."""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="🐝 SWARM Messaging CLI - Command the swarm through PyAutoGUI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=CLI_HELP_EPILOG,
        )

        # Core messaging arguments
        parser.add_argument("--message", "-m", type=str, help="Message content to send")

        parser.add_argument(
            "--agent", "-a", type=str, help="Target agent ID (e.g., Agent-1, Agent-2)"
        )

        parser.add_argument(
            "--broadcast", "-b", action="store_true", help="Broadcast message to all agents"
        )

        # Message options
        parser.add_argument(
            "--priority",
            "-p",
            choices=["normal", "urgent"],
            default="normal",
            help="Message priority (default: normal)",
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

        # Agent revival flags
        parser.add_argument(
            "--revive-agent", action="store_true", help="Send urgent revival message to agent"
        )

        parser.add_argument(
            "--revive-all", action="store_true", help="Send urgent revival messages to all agents"
        )

        # Automated monitoring and revival
        parser.add_argument(
            "--monitor-status", action="store_true", help="Monitor agent status and revive stalled agents"
        )

        parser.add_argument(
            "--revival-daemon", action="store_true", help="Start automated revival daemon (continuous monitoring)"
        )

        parser.add_argument(
            "--stall-threshold", type=int, default=300, help="Stall threshold in seconds (default: 300)"
        )

        parser.add_argument(
            "--consolidation-batch", type=str, help="Specify consolidation batch ID"
        )

        parser.add_argument(
            "--consolidation-status", type=str, help="Specify consolidation status update"
        )

        # Coordinate display
        parser.add_argument(
            "--coordinates", action="store_true", help="Display agent coordinates and configuration"
        )

        return parser

    def execute(self, args=None):
        if not MESSAGING_AVAILABLE:
            return 1
        parsed_args = self.parser.parse_args(args)
        try:
            if parsed_args.message or parsed_args.broadcast:
                return self._handle_message(parsed_args)
            elif parsed_args.revive_agent:
                return self._handle_agent_revival(parsed_args)
            elif parsed_args.revive_all:
                return self._handle_swarm_revival()
            elif parsed_args.monitor_status:
                return self._handle_status_monitoring(parsed_args)
            elif parsed_args.revival_daemon:
                return self._handle_revival_daemon(parsed_args)
            elif parsed_args.survey_coordination:
                return self._handle_survey()
            elif parsed_args.consolidation_coordination:
                return self._handle_consolidation(parsed_args)
            elif parsed_args.coordinates:
                return self._handle_coordinates()
            else:
                self.parser.print_help()
                return 0
        except:
            return 1

    def _handle_message(self, args):
        if not args.message and not args.broadcast:
            return 1
        priority = (
            UnifiedMessagePriority.URGENT
            if args.priority == "urgent"
            else UnifiedMessagePriority.NORMAL
        )
        if args.broadcast:
            success = MessageCoordinator.broadcast_to_all(args.message, priority)
            logger.info(
                f"📢 Broadcast successful to {success}/8 agents"
                if success > 0
                else "❌ Broadcast failed"
            )
            return 0 if success > 0 else 1
        elif args.agent:
            success = MessageCoordinator.send_to_agent(
                args.agent, args.message, priority, args.pyautogui
            )
            return 0 if success else 1
        return 1

    def _handle_survey(self):
        success = MessageCoordinator.coordinate_survey()
        return 0 if success > 0 else 1

    def _handle_consolidation(self, args):
        if not (args.consolidation_batch and args.consolidation_status):
            return 1
        success = MessageCoordinator.coordinate_consolidation(
            args.consolidation_batch, args.consolidation_status
        )
        return 0 if success > 0 else 1

    def _handle_agent_revival(self, args):
        """Handle individual agent revival."""
        if not args.agent:
            logger.error("❌ Agent ID required for revival. Use --agent <Agent-ID>")
            return 1

        from datetime import datetime

        revival_msg = REVIVAL_MESSAGE_TEMPLATE.format(
            agent_id=args.agent, timestamp=datetime.now().isoformat()
        )

        success = MessageCoordinator.send_to_agent(
            args.agent, revival_msg, UnifiedMessagePriority.URGENT, True
        )

        if success:
            logger.info(
                f"🚨 URGENT REVIVAL: Successfully sent ctrl+enter revival signal to {args.agent}"
            )
            return 0
        else:
            logger.error(f"❌ Failed to revive agent {args.agent}")
            return 1

    def _handle_swarm_revival(self):
        """Handle swarm-wide revival."""
        logger.info("🚨 INITIATING SWARM-WIDE REVIVAL PROTOCOL...")

        success_count = MessageCoordinator.broadcast_to_all(
            BROADCAST_REVIVAL_TEMPLATE, UnifiedMessagePriority.URGENT
        )

        if success_count > 0:
            logger.info(
                f"🚨 SWARM REVIVAL: Successfully sent ctrl+enter signals to {success_count}/8 agents"
            )
            return 0
        else:
            logger.error("❌ Swarm revival failed - no agents responded")
            return 1

    def _handle_coordinates(self):
        try:
            coord_loader = get_coordinate_loader()
            agents = coord_loader.get_all_agents()
            if not agents:
                return 1
            print("\n🐝 AGENT COORDINATES & CONFIGURATION\n" + "=" * 50)
            for agent_id in sorted(agents):
                try:
                    coords = coord_loader.get_chat_coordinates(agent_id)
                    desc = coord_loader.get_agent_description(agent_id) or "No description"
                    status = (
                        "✅ ACTIVE" if coord_loader.is_agent_active(agent_id) else "❌ INACTIVE"
                    )
                    print(
                        f"🤖 {agent_id}\n   📍 Coordinates: {coords}\n   📝 {desc}\n   🔄 {status}\n"
                    )
                except:
                    pass
            print("🎯 COORDINATE SYSTEM READY FOR SWARM COORDINATION!")
            return 0
        except:
            return 1


def main() -> int:
    """Main entry point."""
    cli = MessagingCLI()
    return cli.execute()


if __name__ == "__main__":
    exit_code = main()
    print()  # Add line break for agent coordination
    print("🐝 WE. ARE. SWARM. ⚡️🔥")  # Completion indicator
    sys.exit(exit_code)
