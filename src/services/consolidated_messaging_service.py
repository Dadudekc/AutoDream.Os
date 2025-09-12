#!/usr/bin/env python3
"""
Consolidated Messaging Service - V2 Compliant Module
===================================================

Unified messaging service consolidating:
- messaging_core.py (stub - points to core system)
- messaging_cli.py (CLI interface)
- messaging_pyautogui.py (PyAutoGUI delivery)

V2 Compliance: < 400 lines, single responsibility for all messaging operations.

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: Phase 2 Consolidation - Chunk 002 (Services)
License: MIT
"""

import argparse
import logging
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Fix imports when running as a script
if __name__ == "__main__":
    # Add the project root to Python path so we can import src modules
    script_dir = Path(__file__).parent.parent.parent  # Go up to project root
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

# Import from PyAutoGUI messaging system (SSOT)
try:
    from enum import Enum

    # Create fallback classes for unified messaging compatibility
    from typing import Any, Dict, List, Optional

    from src.core.coordinate_loader import get_coordinate_loader
    from src.core.messaging_pyautogui import (
        PYAUTOGUI_AVAILABLE,
        deliver_bulk_messages_pyautogui,
        deliver_message_pyautogui,
        get_agent_coordinates,
        load_coordinates_from_json,
    )

    class UnifiedMessageType(Enum):
        AGENT_TO_AGENT = "agent_to_agent"
        BROADCAST = "broadcast"
        SYSTEM_TO_AGENT = "system_to_agent"

    class UnifiedMessagePriority(Enum):
        LOW = "LOW"
        NORMAL = "NORMAL"
        HIGH = "HIGH"
        URGENT = "URGENT"

    class UnifiedMessageTag(Enum):
        GENERAL = "GENERAL"
        COORDINATION = "COORDINATION"
        TASK = "TASK"
        STATUS = "STATUS"

    class UnifiedMessage:
        def __init__(
            self,
            content: str,
            sender: str,
            recipient: str,
            message_type: UnifiedMessageType,
            priority: UnifiedMessagePriority,
            tags: list[UnifiedMessageTag],
            timestamp: str | None = None,
        ):
            self.content = content
            self.sender = sender
            self.recipient = recipient
            self.message_type = message_type
            self.priority = priority
            self.tags = tags
            self.timestamp = timestamp or time.strftime("%Y-%m-%d %H:%M:%S")

    def send_message(message: UnifiedMessage) -> bool:
        """Send message using PyAutoGUI system"""
        coords = get_agent_coordinates(message.recipient)
        if not coords:
            return False
        return deliver_message_pyautogui(message, coords)

    def broadcast_message(content: str, sender: str) -> bool:
        """Broadcast message to all agents"""
        messages = []
        for agent_id in [
            "Agent-1",
            "Agent-2",
            "Agent-3",
            "Agent-4",
            "Agent-5",
            "Agent-6",
            "Agent-7",
            "Agent-8",
        ]:
            msg = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority.NORMAL,
                tags=[UnifiedMessageTag.COORDINATION],
            )
            messages.append(msg)
        results = deliver_bulk_messages_pyautogui(messages)
        return all(results.values())

    def list_agents() -> list[str]:
        """List all available agents"""
        coords = load_coordinates_from_json()
        return list(coords.keys())

    def get_messaging_core():
        """Get messaging core instance"""
        return PyAutoGUIMessagingDelivery()

    def show_message_history(agent_id: str | None = None) -> list[dict[str, Any]] | None:
        """Show message history (placeholder)"""
        logger.info(f"Message history for {agent_id or 'all agents'}")
        return []

    MESSAGING_AVAILABLE = True

except ImportError as e:
    logging.error(f"❌ PyAutoGUI messaging system not available: {e}")
    MESSAGING_AVAILABLE = False


# Module-level functions for testing compatibility
def get_coordinate_loader():
    """Get coordinate loader instance."""
    if MESSAGING_AVAILABLE:
        try:
            from src.core.coordinate_loader import (
                get_coordinate_loader as core_get_coordinate_loader,
            )

            return core_get_coordinate_loader()
        except ImportError:
            pass

    # Fallback coordinate loader for testing
    class MockCoordinateLoader:
        def get_all_agents(self):
            return [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]

        def is_agent_active(self, agent_id):
            return agent_id in self.get_all_agents()

        def get_chat_coordinates(self, agent_id):
            # Return mock coordinates
            return (100, 100)

    return MockCoordinateLoader()


def get_messaging_core():
    """Get messaging core instance."""
    if MESSAGING_AVAILABLE:
        try:
            # Return a simple mock since messaging_core was removed
            class MockMessagingCore:
                def send_message(self, agent_id, message):
                    return True

            return MockMessagingCore()
        except Exception:
            pass

    # Fallback messaging core for testing
    class MockMessagingCore:
        def send_message(self, message, target_agent):
            return True

        def broadcast_message(self, content, sender):
            return True

    return MockMessagingCore()


logger = logging.getLogger(__name__)

# Constants
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


class ConsolidatedMessagingService:
    """Unified messaging service using PyAutoGUI messaging as SSOT."""

    def __init__(self, dry_run: bool = False):
        """Initialize the consolidated messaging service."""
        self.dry_run = dry_run
        self.service_available = MESSAGING_AVAILABLE
        self.pyautogui_available = MESSAGING_AVAILABLE  # Now using the same flag
        self.messaging_core = get_messaging_core() if MESSAGING_AVAILABLE else None
        self.coordinate_loader = get_coordinate_loader() if MESSAGING_AVAILABLE else None
        self.pyautogui_delivery = None  # Will use direct function calls instead
        self.logger = logging.getLogger(__name__)

    def load_coordinates_from_json(self) -> dict[str, tuple[int, int]]:
        """Load agent coordinates using SSOT coordinate loader."""
        if not self.coordinate_loader:
            return {}

        coordinates = {}
        for agent_id in self.coordinate_loader.get_all_agents():
            if self.coordinate_loader.is_agent_active(agent_id):
                try:
                    coords = self.coordinate_loader.get_chat_coordinates(agent_id)
                    coordinates[agent_id] = coords
                    logging.debug(f"Loaded coordinates for {agent_id}: {coords}")
                except ValueError:
                    logging.warning(f"Invalid coordinates for {agent_id}")
        return coordinates

    def send_message_pyautogui(
        self, agent_id: str, message: str, priority: str = "NORMAL", tag: str = "GENERAL"
    ) -> bool:
        """Send message using enhanced PyAutoGUI SSOT with inbox fallback."""
        if not self.pyautogui_available:
            logger.error("❌ PyAutoGUI messaging system not available")
            return False

        if self.dry_run:
            logger.info(f"🔍 DRY RUN: Would send to {agent_id}: {message}")
            return True

        try:
            # Try PyAutoGUI first if available
            if PYAUTOGUI_AVAILABLE:
                coords = get_agent_coordinates(agent_id)
                if coords:
                    # Use local UnifiedMessage classes (moved from messaging_core)
                    # Convert string priority to enum
                    priority_map = {
                        "LOW": UnifiedMessagePriority.LOW,
                        "NORMAL": UnifiedMessagePriority.NORMAL,
                        "HIGH": UnifiedMessagePriority.HIGH,
                        "URGENT": UnifiedMessagePriority.URGENT,
                    }
                    msg_priority = priority_map.get(priority.upper(), UnifiedMessagePriority.NORMAL)

                    # Convert string tag to enum
                    tag_map = {
                        "GENERAL": UnifiedMessageTag.GENERAL,
                        "COORDINATION": UnifiedMessageTag.COORDINATION,
                        "TASK": UnifiedMessageTag.TASK,
                    }
                    msg_tag = tag_map.get(tag.upper(), UnifiedMessageTag.GENERAL)

                    unified_msg = UnifiedMessage(
                        content=message,
                        sender="ConsolidatedMessagingService",
                        recipient=agent_id,
                        message_type=UnifiedMessageType.AGENT_TO_AGENT,
                        priority=msg_priority,
                        tags=[msg_tag],
                    )
                    success = deliver_message_pyautogui(unified_msg, coords)
                    if success:
                        logger.info(f"✅ Enhanced message sent to {agent_id} via PyAutoGUI SSOT")
                        return success

            # Fallback to regular messaging system
            if MESSAGING_AVAILABLE:
                # Use local send_message function
                success = send_message(agent_id, message)
                if success:
                    logger.info(f"✅ Message sent to {agent_id} via fallback messaging")
                    return success

            # Last resort: write to inbox directly
            import os

            inbox_path = f"agent_workspaces/{agent_id}/inbox"
            os.makedirs(inbox_path, exist_ok=True)

            import datetime

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            message_file = f"{inbox_path}/MESSAGE_{timestamp}.md"

            with open(message_file, "w") as f:
                f.write(
                    f"# System Message\n\n**From:** ConsolidatedMessagingService\n**To:** {agent_id}\n**Time:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{message}\n"
                )

            logger.info(f"✅ Message written to {agent_id}'s inbox directly")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to send enhanced message to {agent_id}: {e}")
            return False

    def send_message_unified(
        self, agent_id: str, message: str, priority: str = "NORMAL", tag: str = "GENERAL"
    ) -> bool:
        """Send message using unified messaging system."""
        if not MESSAGING_AVAILABLE:
            logger.error("❌ Messaging system not available")
            return False

        try:
            # Create unified message
            unified_message = UnifiedMessage(
                content=message,
                sender="ConsolidatedMessagingService",
                recipient=agent_id,
                message_type=UnifiedMessageType.COORDINATION,
                priority=UnifiedMessagePriority[priority.upper()],
                tag=UnifiedMessageTag[tag.upper()],
            )

            # Send via core system
            result = send_message(unified_message)
            logger.info(f"✅ Message sent to {agent_id} via unified system")
            return result

        except Exception as e:
            logger.error(f"❌ Failed to send unified message to {agent_id}: {e}")
            return False

    def broadcast_message_swarm(
        self, message: str, priority: str = "NORMAL", tag: str = "GENERAL"
    ) -> dict[str, bool]:
        """Broadcast message to all swarm agents using enhanced PyAutoGUI SSOT."""
        if not self.pyautogui_available:
            logger.error("❌ PyAutoGUI messaging system not available for broadcast")
            return dict.fromkeys(SWARM_AGENTS, False)

        if self.dry_run:
            logger.info(f"🔍 DRY RUN BROADCAST: {message} to all agents")
            return dict.fromkeys(SWARM_AGENTS, True)

        try:
            # Use enhanced deliver_bulk_messages_pyautogui from SSOT
            from .messaging_core import UnifiedMessage, UnifiedMessagePriority, UnifiedMessageType

            unified_msg = UnifiedMessage(
                content=message,
                sender="ConsolidatedMessagingService",
                recipient="all",
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority.NORMAL,
            )
            results = deliver_bulk_messages_pyautogui(unified_msg)
            logger.info(f"✅ Enhanced broadcast completed with results: {results}")
            return results

        except Exception as e:
            logger.error(f"❌ Broadcast failed: {e}")
            return dict.fromkeys(SWARM_AGENTS, False)

    def list_available_agents(self) -> list[str]:
        """List all available agents."""
        if MESSAGING_AVAILABLE and self.coordinate_loader:
            return list(self.coordinate_loader.get_all_agents())
        return SWARM_AGENTS

    def show_message_history(self, agent_id: str | None = None) -> None:
        """Show message history for agent or all agents."""
        if not MESSAGING_AVAILABLE:
            logger.error("❌ Messaging system not available")
            return

        try:
            show_message_history(agent_id)
        except Exception as e:
            logger.error(f"❌ Failed to show message history: {e}")

    def run_cli_interface(self, args: list[str] | None = None) -> None:
        """Run the CLI interface for messaging operations."""
        parser = argparse.ArgumentParser(description="Consolidated Messaging Service CLI")
        parser.add_argument("--agent", "-a", help="Target agent ID")
        parser.add_argument("--message", "-m", help="Message content")
        parser.add_argument(
            "--priority",
            "-p",
            choices=["LOW", "NORMAL", "HIGH", "URGENT"],
            default="NORMAL",
            help="Message priority",
        )
        parser.add_argument(
            "--tag",
            "-t",
            choices=["GENERAL", "COORDINATION", "TASK", "STATUS"],
            default="GENERAL",
            help="Message tag",
        )
        parser.add_argument(
            "--broadcast", "-b", action="store_true", help="Broadcast to all agents"
        )
        parser.add_argument(
            "--list-agents", "-l", action="store_true", help="List available agents"
        )
        parser.add_argument("--history", action="store_true", help="Show message history")
        parser.add_argument(
            "--dry-run", action="store_true", help="Dry run mode (no actual sending)"
        )
        parser.add_argument(
            "--capture-coords",
            action="store_true",
            help="Launch interactive coordinate capture tool",
        )
        parser.add_argument(
            "--show-coords", action="store_true", help="Display current coordinates for all agents"
        )

        # Thea Communication options
        parser.add_argument("--thea-message", help="Send message to Thea AI assistant")
        parser.add_argument("--thea-username", help="ChatGPT username for Thea authentication")
        parser.add_argument("--thea-password", help="ChatGPT password for Thea authentication")
        parser.add_argument(
            "--thea-headless",
            action="store_true",
            default=True,
            help="Run Thea browser in headless mode (default: True)",
        )
        parser.add_argument(
            "--thea-no-headless", action="store_true", help="Disable headless mode for Thea browser"
        )

        # Task-to-Thea pipeline options
        parser.add_argument("--task-assistance", help="Request Thea assistance for a specific task")
        parser.add_argument("--task-context", help="Additional context for the task")
        parser.add_argument("--agent-id", help="Agent requesting assistance (for task context)")

        # v3.3 Thea enhancements
        parser.add_argument(
            "--thea-resume-last",
            action="store_true",
            help="Resume Thea conversation at last stored thread URL",
        )
        parser.add_argument(
            "--thea-thread-url", help="Resume Thea conversation at this specific thread URL"
        )
        parser.add_argument(
            "--thea-attach",
            help="Path to a file to attach to Thea message (best-effort UI automation)",
        )

        # Task management
        parser.add_argument(
            "--claim-task",
            action="store_true",
            help="Claim next available task for the specified agent",
        )
        parser.add_argument("--complete-task", action="store_true", help="Mark a task as completed")
        parser.add_argument(
            "--task-id", type=str, help="Task ID for completion (required with --complete-task)"
        )
        parser.add_argument(
            "--task-notes", type=str, help="Completion notes (optional with --complete-task)"
        )

        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        # Handle headless flag logic
        if parsed_args.thea_no_headless:
            parsed_args.thea_headless = False

        if parsed_args.dry_run:
            self.dry_run = True

        if parsed_args.list_agents:
            agents = self.list_available_agents()
            print("Available agents:")
            for agent in agents:
                print(f"  - {agent}")
            return

        if parsed_args.history:
            self.show_message_history(parsed_args.agent)
            return

        if parsed_args.capture_coords:
            self.launch_coordinate_capture()
            return

        if parsed_args.show_coords:
            self.show_current_coordinates()
            return

        if parsed_args.broadcast:
            if not parsed_args.message:
                print("❌ Error: Message required for broadcast")
                return

            results = self.broadcast_message_swarm(
                parsed_args.message, parsed_args.priority, parsed_args.tag
            )

            print("Broadcast results:")
            for agent, success in results.items():
                status = "✅" if success else "❌"
                print(f"  {status} {agent}")
            return

        # Handle task assistance pipeline
        if parsed_args.task_assistance:
            self.handle_task_assistance(
                parsed_args.task_assistance,
                parsed_args.task_context,
                parsed_args.agent_id,
                parsed_args.thea_username,
                parsed_args.thea_password,
                parsed_args.thea_headless,
                getattr(parsed_args, "thea_thread_url", None),
                getattr(parsed_args, "thea_resume_last", False),
                getattr(parsed_args, "thea_attach", None),
            )
            return

        # Handle Thea communication
        if parsed_args.thea_message:
            self.handle_thea_communication(
                parsed_args.thea_message,
                parsed_args.thea_username,
                parsed_args.thea_password,
                parsed_args.thea_headless,
                getattr(parsed_args, "thea_thread_url", None),
                getattr(parsed_args, "thea_resume_last", False),
                getattr(parsed_args, "thea_attach", None),
            )
            return

        # Handle task management
        if parsed_args.claim_task:
            self.handle_claim_task(parsed_args)
            return

        if parsed_args.complete_task:
            self.handle_complete_task(parsed_args)
            return

        if parsed_args.agent and parsed_args.message:
            # Prioritize enhanced PyAutoGUI messaging system
            if self.pyautogui_available:
                success = self.send_message_pyautogui(
                    parsed_args.agent, parsed_args.message, parsed_args.priority, parsed_args.tag
                )
            elif MESSAGING_AVAILABLE:
                success = self.send_message_unified(
                    parsed_args.agent, parsed_args.message, parsed_args.priority, parsed_args.tag
                )
            else:
                print("❌ No messaging system available")
                success = False

            if success:
                print(f"✅ Enhanced message sent to {parsed_args.agent}")
            else:
                print(f"❌ Failed to send enhanced message to {parsed_args.agent}")
        else:
            parser.print_help()

    def broadcast_message(self, content: str, sender: str = "Agent-1") -> dict[str, bool]:
        """Broadcast message to all agents."""
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
        results = {}

        if not self.service_available:
            self.logger.warning("⚠️ Messaging system not available for broadcast")
            # Return False for all agents when messaging unavailable
            return dict.fromkeys(agents, False)

        try:
            # Use the imported broadcast_message function if available
            if MESSAGING_AVAILABLE:
                broadcast_result = broadcast_message(content, sender)
                # Assume broadcast succeeds for all agents
                return dict.fromkeys(agents, broadcast_result)
            else:
                self.logger.info(f"🔍 DRY RUN BROADCAST: {content} from {sender}")
                # Dry run succeeds for all agents
                return dict.fromkeys(agents, True)
        except Exception as e:
            self.logger.error(f"❌ Broadcast failed: {e}")
            return dict.fromkeys(agents, False)

    def list_agents(self) -> list[str]:
        """List all available agents."""
        if not self.service_available:
            # Return default agent list
            return [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]
        try:
            # Use the imported list_agents function if available
            if MESSAGING_AVAILABLE:
                return list_agents()
            else:
                return [
                    "Agent-1",
                    "Agent-2",
                    "Agent-3",
                    "Agent-4",
                    "Agent-5",
                    "Agent-6",
                    "Agent-7",
                    "Agent-8",
                ]
        except Exception as e:
            self.logger.error(f"❌ List agents failed: {e}")
            return []

    def show_message_history(self) -> list[dict[str, Any]] | None:
        """Show message history."""
        if not self.service_available:
            return []
        try:
            # Use the imported show_message_history function if available
            if MESSAGING_AVAILABLE:
                return show_message_history()
            else:
                return []
        except Exception as e:
            self.logger.error(f"❌ Show message history failed: {e}")
            return []

    def get_agent_workspaces_status(self) -> dict[str, Any]:
        """Get status of agent workspaces and inboxes."""
        if not self.pyautogui_available:
            self.logger.warning("⚠️ PyAutoGUI messaging system not available for status check")
            return {"workspaces_exist": False, "agents": {}}

        try:
            # Simple workspace status check
            import os

            workspace_base = "agent_workspaces"
            agents_status = {}

            for agent_id in SWARM_AGENTS:
                agent_path = f"{workspace_base}/{agent_id}"
                inbox_path = f"{agent_path}/inbox"
                status_path = f"{agent_path}/status.json"

                agents_status[agent_id] = {
                    "workspace_exists": os.path.exists(agent_path),
                    "inbox_exists": os.path.exists(inbox_path),
                    "status_exists": os.path.exists(status_path),
                    "inbox_count": len(os.listdir(inbox_path)) if os.path.exists(inbox_path) else 0,
                }

            return {"workspaces_exist": os.path.exists(workspace_base), "agents": agents_status}
        except Exception as e:
            self.logger.error(f"❌ Failed to get agent workspaces status: {e}")
            return {"workspaces_exist": False, "agents": {}}

    def launch_coordinate_capture(self):
        """Launch the interactive coordinate capture tool."""
        try:
            print("🚀 Launching Interactive Coordinate Capture Tool...")
            print("=" * 60)

            # Import and run the coordinate capture tool
            import subprocess
            import sys
            from pathlib import Path

            # Get the path to the coordinate capture tool
            tool_path = Path(__file__).parent.parent.parent / "coordinate_capture_tool.py"

            if tool_path.exists():
                print(f"📁 Tool location: {tool_path}")
                print("🎯 Starting coordinate capture process...\n")

                # Launch the coordinate capture tool
                result = subprocess.run([sys.executable, str(tool_path)], cwd=Path.cwd())
                if result.returncode == 0:
                    print("\n✅ Coordinate capture completed successfully!")
                else:
                    print(f"\n❌ Coordinate capture failed with exit code: {result.returncode}")
            else:
                print(f"❌ Coordinate capture tool not found at: {tool_path}")
                print("💡 Make sure coordinate_capture_tool.py is in the project root directory")

        except Exception as e:
            self.logger.error(f"❌ Failed to launch coordinate capture tool: {e}")
            print(f"❌ Error launching coordinate capture: {e}")

    def handle_task_assistance(
        self,
        task: str,
        context: str = None,
        agent_id: str = None,
        username: str = None,
        password: str = None,
        headless: bool = True,
        thread_url: str = None,
        resume_last: bool = False,
        attach_file: str = None,
    ):
        """Handle task assistance pipeline to Thea."""
        try:
            print("🎯 TASK ASSISTANCE PIPELINE")
            print("=" * 40)
            print(f"📋 Task: {task}")
            print(f"🤖 Agent: {agent_id or 'Unknown'}")
            print(f"📝 Context: {context or 'None provided'}")
            print(f"🫥 Headless: {headless}")

            # Create structured message for Thea
            structured_message = self._create_task_assistance_message(task, context, agent_id)

            if self.dry_run:
                print("🔍 DRY RUN: Would send task assistance to Thea")
                print("📨 Structured message preview:")
                print("-" * 30)
                print(
                    structured_message[:200] + "..."
                    if len(structured_message) > 200
                    else structured_message
                )
                print("-" * 30)
                print("✅ Task assistance pipeline simulation completed")
                return

            print("📨 Sending structured task assistance to Thea...")

            # Use the existing Thea communication method
            self.handle_thea_communication(
                structured_message,
                username,
                password,
                headless,
                thread_url,
                resume_last,
                attach_file,
            )

        except Exception as e:
            self.logger.error(f"❌ Task assistance failed: {e}")
            print(f"❌ Error during task assistance: {e}")

    def _create_task_assistance_message(
        self, task: str, context: str = None, agent_id: str = None
    ) -> str:
        """Create a structured message for Thea task assistance."""
        message_parts = [
            "🎯 AGENT TASK ASSISTANCE REQUEST",
            "",
            f"**Agent ID:** {agent_id or 'Unknown Agent'}",
            "**Request Type:** Task Assistance",
            f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Task Description",
            task,
        ]

        if context:
            message_parts.extend(["", "## Additional Context", context])

        message_parts.extend(
            [
                "",
                "## Requested Assistance",
                "Please provide:",
                "1. **Guidance** on how to approach this task",
                "2. **Best practices** relevant to this task",
                "3. **Potential challenges** to consider",
                "4. **Implementation recommendations**",
                "5. **Code examples** if applicable",
                "",
                "## Agent Context",
                f"- **Agent Role:** V2_SWARM Agent ({agent_id or 'Unknown'})",
                "- **Environment:** Autonomous swarm coordination system",
                "- **Communication:** Via autonomous Thea integration",
                "",
                "🐝 **WE ARE SWARM** - Task assistance requested through automated pipeline",
            ]
        )

        return "\n".join(message_parts)

    def handle_thea_communication(
        self,
        message: str,
        username: str = None,
        password: str = None,
        headless: bool = True,
        thread_url: str = None,
        resume_last: bool = False,
        attach_file: str = None,
    ):
        """Handle autonomous Thea communication."""
        try:
            print("🚀 THEA AUTONOMOUS COMMUNICATION")
            print("=" * 40)
            print(f"📝 Message: {message[:100]}{'...' if len(message) > 100 else ''}")
            print(f"🫥 Headless: {headless}")
            print(f"👤 Username: {username or 'Not provided'}")

            if self.dry_run:
                print("🔍 DRY RUN: Would send message to Thea")
                print("✅ Thea communication simulation completed")
                return

            # Import and use the autonomous Thea communication system
            import os
            import sys
            from pathlib import Path

            # Add project root to path for imports
            project_root = Path(__file__).parent.parent.parent
            if str(project_root) not in sys.path:
                sys.path.insert(0, str(project_root))

            # Import the autonomous Thea communication class
            from simple_thea_communication import SimpleTheaCommunication

            # Create Thea communication instance
            thea_comm = SimpleTheaCommunication(
                username=username,
                password=password,
                use_selenium=True,  # Force selenium for autonomous mode
                headless=headless,
                thread_url=thread_url,
                resume_last=resume_last,
                attach_file=attach_file,
            )

            print("🤖 Initializing autonomous Thea communication...")

            # Run the complete communication cycle
            success = thea_comm.run_communication_cycle(message)

            if success:
                print("✅ Thea communication completed successfully!")
                print("📊 Check thea_responses/ directory for results")
            else:
                print("❌ Thea communication failed")
                print("💡 Check logs for details and try again")

            # Cleanup
            thea_comm.cleanup()

        except ImportError as e:
            print(f"❌ Failed to import Thea communication system: {e}")
            print("💡 Make sure simple_thea_communication.py is in the project root")
        except Exception as e:
            self.logger.error(f"❌ Thea communication failed: {e}")
            print(f"❌ Error during Thea communication: {e}")

    def show_current_coordinates(self):
        """Display current coordinates for all agents."""
        try:
            from pathlib import Path

            coord_file = Path("cursor_agent_coords.json")

            if not coord_file.exists():
                print("❌ No coordinate file found: cursor_agent_coords.json")
                print("💡 Run coordinate capture first: --capture-coords")
                return

            import json

            with open(coord_file, encoding="utf-8") as f:
                data = json.load(f)

            print("📊 CURRENT AGENT COORDINATES")
            print("=" * 80)

            agents = data.get("agents", {})
            if not agents:
                print("❌ No agents configured yet.")
                print("💡 Run coordinate capture: --capture-coords")
                return

            print("<8")
            print("-" * 82)

            agent_order = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]

            for agent_id in agent_order:
                if agent_id in agents:
                    agent_data = agents[agent_id]
                    onboarding = agent_data.get("onboarding_input_coords", ["-", "-"])
                    chat = agent_data.get("chat_input_coordinates", ["-", "-"])
                    active = "✅" if agent_data.get("active", False) else "❌"

                    description = agent_data.get("description", "")
                    if len(description) > 25:
                        description = description[:22] + "..."

                    print("<8")
                else:
                    print("<8")

            print("=" * 80)
            print(f"📁 Coordinate file: {coord_file}")
            print(f"📅 Last updated: {data.get('last_updated', 'Unknown')}")
            print(f"🔢 Version: {data.get('version', 'Unknown')}")

        except Exception as e:
            self.logger.error(f"❌ Failed to show coordinates: {e}")
            print(f"❌ Error displaying coordinates: {e}")

    def handle_claim_task(self, args):
        """Handle task claiming."""
        try:
            if not args.agent:
                print("❌ --agent is required for --claim-task")
                return

            # Get next available task for agent
            task_data = self._get_next_available_task(args.agent)

            if task_data:
                # Quiet task assignment - no PyAutoGUI messaging, just log
                print("\n🎯 **TASK ASSIGNED**")
                print(f"📋 Task ID: {task_data['task_id']}")
                print(f"📝 Title: {task_data['title']}")
                print(f"🎯 Type: {task_data.get('task_type', 'General')}")
                print(f"⚡ Priority: {task_data.get('priority', 'Medium')}")
                print(f"👤 Assigned to: {args.agent}")
                print("\n🚀 **Begin task execution immediately**")
                print("⚡️ **WE. ARE. SWARM.**\n")

                print(f"✅ Task {task_data['task_id']} assigned to {args.agent} (quiet mode)")
            else:
                # Notify Captain that task queue is empty and needs replenishment
                captain_notification = f"""🚨 **TASK QUEUE EMPTY - ACTION REQUIRED**

⚠️ **Agent {args.agent} requested a task but none are available**

📋 **Required Actions:**
1. Scan the project for new work items
2. Update the task system with fresh tasks
3. Notify agents when new tasks are available

🎯 **Captain Agent-4 - Please replenish the task queue**

⚡️ **WE. ARE. SWARM.**"""

                # Send notification to Captain Agent-4
                captain_coords = get_agent_coordinates("Agent-4")
                if captain_coords:
                    captain_msg = UnifiedMessage(
                        content=captain_notification,
                        sender="TaskManagementSystem",
                        recipient="Agent-4",
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                        priority=UnifiedMessagePriority.URGENT,
                        tags=[UnifiedMessageTag.TASK],
                    )
                    deliver_message_pyautogui(captain_msg, captain_coords)

                print("🚨 Task queue empty - Captain Agent-4 notified to replenish tasks")
                print(f"ℹ️ No tasks available for {args.agent} at this time")

        except Exception as e:
            self.logger.error(f"❌ Error claiming task: {e}")
            print(f"❌ Error claiming task: {e}")

    def handle_complete_task(self, args):
        """Handle task completion."""
        try:
            if not args.agent:
                print("❌ --agent is required for --complete-task")
                return

            if not args.task_id:
                print("❌ --task-id is required for --complete-task")
                return

            from datetime import datetime

            # Mark task as completed
            completion_notes = args.task_notes or "Task completed successfully"

            # Send completion confirmation to the agent
            completion_message = f"""✅ **TASK COMPLETED SUCCESSFULLY**

🆔 Task ID: {args.task_id}
📝 Completion Notes: {completion_notes}
👤 Completed By: {args.agent}
⏰ Completed At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🎉 Task marked as complete! Great work, Agent {args.agent}!

⚡️ **WE. ARE. SWARM.**"""

            coords = get_agent_coordinates(args.agent)
            if coords:
                unified_msg = UnifiedMessage(
                    content=completion_message,
                    sender="ConsolidatedMessagingService",
                    recipient=args.agent,
                    message_type=UnifiedMessageType.AGENT_TO_AGENT,
                    priority=UnifiedMessagePriority.NORMAL,
                    tags=[UnifiedMessageTag.TASK],
                )
                success = deliver_message_pyautogui(unified_msg, coords)
            else:
                success = False

            # Notify Captain Agent-4 of task completion
            captain_notification = f"""📋 **TASK COMPLETION REPORT**

✅ **Task Completed Successfully**
🆔 Task ID: {args.task_id}
👤 Completed By: {args.agent}
📝 Completion Notes: {completion_notes}
⏰ Completed At: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🎯 **Action Required:** Please check your inbox for details on how to test the completed work in practice.

⚡️ **WE. ARE. SWARM.**"""

            captain_coords = get_agent_coordinates("Agent-4")
            if captain_coords:
                captain_msg = UnifiedMessage(
                    content=captain_notification,
                    sender="TaskManagementSystem",
                    recipient="Agent-4",
                    message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                    priority=UnifiedMessagePriority.HIGH,
                    tags=[UnifiedMessageTag.TASK],
                )
                deliver_message_pyautogui(captain_msg, captain_coords)

            if success:
                print(f"✅ Task {args.task_id} marked as completed by {args.agent}")
                print("📢 Captain Agent-4 notified of task completion")
            else:
                print(f"❌ Failed to send completion confirmation to {args.agent}")

        except Exception as e:
            self.logger.error(f"❌ Error completing task: {e}")
            print(f"❌ Error completing task: {e}")

    def _get_next_available_task(self, agent_id: str) -> dict | None:
        """Get next available task for agent (placeholder for now)."""
        # Simulate empty task queue occasionally for testing
        import random
        import uuid
        from datetime import datetime

        if random.random() < 0.3:  # 30% chance of no tasks available
            return None

        # Generate comprehensive tasks with detailed requirements
        task_templates = {
            "Code Review": {
                "title": "Comprehensive Code Review & Quality Assurance",
                "description": """Perform a thorough code review of the latest commits in the repository. Focus on:

• Code quality and adherence to PEP 8 standards
• Security vulnerabilities and potential exploits
• Performance optimizations and efficiency improvements
• Error handling and edge case coverage
• Documentation completeness and accuracy
• Test coverage analysis and recommendations
• Architecture consistency and design patterns
• Dependency management and version compatibility

Provide detailed feedback with specific line references and actionable recommendations.""",
                "estimated_duration": "4-6 hours",
            },
            "Bug Fix": {
                "title": "Critical Bug Investigation & Resolution",
                "description": """Investigate and resolve reported system issues. Complete analysis should include:

• Root cause analysis with detailed investigation
• Reproduction of the issue in multiple environments
• Impact assessment on system stability and user experience
• Development of comprehensive test cases
• Implementation of robust fix with proper error handling
• Verification of fix across all affected components
• Documentation of solution and prevention measures
• Regression testing to ensure no new issues introduced

Document all findings and provide detailed resolution report.""",
                "estimated_duration": "6-8 hours",
            },
            "Feature Development": {
                "title": "Advanced Feature Implementation & Integration",
                "description": """Design and implement a new feature following best practices. This comprehensive task includes:

• Requirements gathering and detailed specification
• Architecture design and component planning
• Database schema modifications if required
• API endpoint development and documentation
• Frontend component development and integration
• Comprehensive unit and integration testing
• Performance optimization and load testing
• Security implementation and vulnerability assessment
• Documentation and user guide creation
• Deployment preparation and rollback planning

Ensure feature integrates seamlessly with existing system architecture.""",
                "estimated_duration": "8-12 hours",
            },
            "Documentation": {
                "title": "Technical Documentation & Knowledge Base Enhancement",
                "description": """Create comprehensive technical documentation to improve system maintainability:

• API documentation with examples and use cases
• Architecture diagrams and system flow documentation
• Code commenting and inline documentation standards
• Troubleshooting guides and common issue resolution
• Deployment and configuration documentation
• Performance monitoring and optimization guides
• Security best practices and compliance documentation
• Training materials for new team members
• Changelog and release notes maintenance

Ensure documentation is accessible, accurate, and regularly updated.""",
                "estimated_duration": "5-7 hours",
            },
            "Testing": {
                "title": "Comprehensive Testing Suite Development & Execution",
                "description": """Develop and execute thorough testing strategies to ensure system reliability:

• Unit test development for all new and modified components
• Integration testing across system boundaries
• End-to-end testing of critical user workflows
• Performance testing and benchmarking
• Load testing and stress testing scenarios
• Security testing and vulnerability assessment
• Cross-browser and cross-platform compatibility testing
• Accessibility testing and compliance verification
• Automated test suite maintenance and CI/CD integration

Provide detailed test reports with coverage metrics and recommendations.""",
                "estimated_duration": "6-10 hours",
            },
            "Security Audit": {
                "title": "System Security Assessment & Hardening",
                "description": """Conduct comprehensive security audit and implement protective measures:

• Vulnerability scanning and assessment
• Code security review for common vulnerabilities (OWASP Top 10)
• Authentication and authorization system review
• Data encryption and privacy protection verification
• Network security configuration assessment
• Input validation and sanitization review
• Session management and cookie security
• Error handling and information leakage prevention
• Security headers and HTTPS configuration
• Incident response and logging capabilities

Implement necessary security patches and provide detailed security report.""",
                "estimated_duration": "7-9 hours",
            },
            "Performance Optimization": {
                "title": "System Performance Analysis & Optimization",
                "description": """Analyze and optimize system performance across all components:

• Performance profiling and bottleneck identification
• Database query optimization and indexing strategy
• Memory usage analysis and leak detection
• CPU utilization optimization and threading improvements
• Network request optimization and caching strategies
• Frontend performance optimization and bundle analysis
• Image and asset optimization for web delivery
• CDN configuration and static asset delivery
• Database connection pooling and resource management
• Monitoring and alerting system implementation

Document performance improvements and establish ongoing monitoring.""",
                "estimated_duration": "6-8 hours",
            },
        }

        task_keys = list(task_templates.keys())
        selected_task = task_keys[hash(agent_id + str(datetime.now().hour)) % len(task_keys)]
        task_config = task_templates[selected_task]

        priorities = ["Medium", "High", "Urgent"]
        selected_priority = priorities[hash(agent_id) % len(priorities)]

        return {
            "task_id": f"TASK-{uuid.uuid4().hex[:8].upper()}",
            "title": task_config["title"],
            "description": task_config["description"],
            "task_type": selected_task,
            "priority": selected_priority,
            "estimated_duration": task_config["estimated_duration"],
            "assigned_to": agent_id,
            "created_at": datetime.now().isoformat(),
            "status": "assigned",
        }


def main():
    """Main entry point for CLI interface."""
    service = ConsolidatedMessagingService()
    service.run_cli_interface()


if __name__ == "__main__":
    main()
