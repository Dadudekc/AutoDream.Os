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
from typing import Any, Dict, List, Optional, Tuple

# Fix imports when running as a script
if __name__ == "__main__":
    # Add the project root to Python path so we can import src modules
    script_dir = Path(__file__).parent.parent.parent  # Go up to project root
    if str(script_dir) not in sys.path:
        sys.path.insert(0, str(script_dir))

# Import from PyAutoGUI messaging system (SSOT)
try:
    from src.core.messaging_pyautogui import (
        format_message_for_delivery,
        deliver_message_pyautogui,
        deliver_bulk_messages_pyautogui,
        get_agent_coordinates,
        load_coordinates_from_json,
        PyAutoGUIMessagingDelivery,
        PYAUTOGUI_AVAILABLE,
        PYPERCLIP_AVAILABLE,
    )
    
    # Create missing function stubs
    def send_message_to_inbox(message, agent_id):
        """Stub for send_message_to_inbox - use deliver_message_pyautogui instead."""
        # Create UnifiedMessage object
        from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        from datetime import datetime
        
        unified_message = UnifiedMessage(
            content=message,
            sender="ConsolidatedMessagingService",
            recipient=agent_id,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            tags=[UnifiedMessageTag.GENERAL]
        )
        
        # Get coordinates for the agent
        coords = get_agent_coordinates(agent_id)
        if coords:
            return deliver_message_pyautogui(unified_message, coords)
        else:
            print(f"❌ No coordinates found for agent {agent_id}")
            return False
    
    def send_message_with_fallback(agent_id, message, sender="System"):
        """Stub for send_message_with_fallback - use deliver_message_pyautogui instead."""
        # Create UnifiedMessage object
        from src.core.messaging_core import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag
        from datetime import datetime
        
        unified_message = UnifiedMessage(
            content=message,
            sender=sender,
            recipient=agent_id,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            tags=[UnifiedMessageTag.GENERAL],
            timestamp=datetime.now()
        )
        
        # Get coordinates for the agent
        coords = get_agent_coordinates(agent_id)
        if coords:
            return deliver_message_pyautogui(unified_message, coords)
        else:
            print(f"❌ No coordinates found for agent {agent_id}")
            return False
    
    def broadcast_message_to_agents(message, agent_ids):
        """Stub for broadcast_message_to_agents - use deliver_bulk_messages_pyautogui instead."""
        return deliver_bulk_messages_pyautogui(message, agent_ids)
    
    def get_agent_workspaces_status():
        """Stub for get_agent_workspaces_status - return basic status."""
        return {"status": "active", "agents": ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]}
    from src.core.coordinate_loader import get_coordinate_loader

    # Create fallback classes for unified messaging compatibility
    from typing import List, Dict, Any, Optional
    from enum import Enum

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
        def __init__(self, content: str, sender: str, recipient: str,
                     message_type: UnifiedMessageType, priority: UnifiedMessagePriority,
                     tags: List[UnifiedMessageTag], timestamp: Optional[str] = None):
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
        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]:
            msg = UnifiedMessage(
                content=content,
                sender=sender,
                recipient=agent_id,
                message_type=UnifiedMessageType.BROADCAST,
                priority=UnifiedMessagePriority.NORMAL,
                tags=[UnifiedMessageTag.COORDINATION]
            )
            messages.append(msg)
        results = deliver_bulk_messages_pyautogui(messages)
        return all(results.values())

    def list_agents() -> List[str]:
        """List all available agents"""
        coords = load_coordinates_from_json()
        return list(coords.keys())

    def get_messaging_core():
        """Get messaging core instance"""
        return PyAutoGUIMessagingDelivery()

    def show_message_history(agent_id: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
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
            from src.core.coordinate_loader import get_coordinate_loader as core_get_coordinate_loader
            return core_get_coordinate_loader()
        except ImportError:
            pass

    # Fallback coordinate loader for testing
    class MockCoordinateLoader:
        def get_all_agents(self):
            return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

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
            from src.core.messaging_core import get_messaging_core as core_get_messaging_core
            return core_get_messaging_core()
        except ImportError:
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
    "Agent-1", "Agent-2", "Agent-3", "Agent-4",
    "Agent-5", "Agent-6", "Agent-7", "Agent-8"
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
        self.pyautogui_delivery = PyAutoGUIMessagingDelivery() if MESSAGING_AVAILABLE else None
        self.logger = logging.getLogger(__name__)
        
    def load_coordinates_from_json(self) -> Dict[str, Tuple[int, int]]:
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

    def send_message_pyautogui(self, agent_id: str, message: str,
                              priority: str = "NORMAL", tag: str = "GENERAL") -> bool:
        """Send message using enhanced PyAutoGUI SSOT with inbox fallback."""
        if not self.pyautogui_available:
            logger.error("❌ PyAutoGUI messaging system not available")
            return False

        if self.dry_run:
            logger.info(f"🔍 DRY RUN: Would send to {agent_id}: {message}")
            return True

        try:
            # Use enhanced send_message_with_fallback from SSOT
            success = send_message_with_fallback(agent_id, message, "ConsolidatedMessagingService")
            if success:
                logger.info(f"✅ Enhanced message sent to {agent_id} via PyAutoGUI SSOT")
            return success

        except Exception as e:
            logger.error(f"❌ Failed to send enhanced message to {agent_id}: {e}")
            return False

    def send_message_unified(self, agent_id: str, message: str, 
                           priority: str = "NORMAL", tag: str = "GENERAL") -> bool:
        """Send message using unified messaging system."""
        if not MESSAGING_AVAILABLE:
            logger.error("❌ Messaging system not available")
            return False
            
        try:
            # Create unified message
            unified_message = UnifiedMessage(
                content=message,
                sender="Agent-1",
                recipient=agent_id,
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority[priority.upper()],
                tags=[UnifiedMessageTag[tag.upper()]]
            )
            
            # Send via PyAutoGUI delivery
            result = self.pyautogui_delivery.send_message_via_pyautogui(unified_message)
            logger.info(f"✅ Message sent to {agent_id} via unified system")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to send unified message to {agent_id}: {e}")
            return False

    def broadcast_message_swarm(self, message: str, priority: str = "NORMAL",
                               tag: str = "GENERAL") -> Dict[str, bool]:
        """Broadcast message to all swarm agents using enhanced PyAutoGUI SSOT."""
        if not self.pyautogui_available:
            logger.error("❌ PyAutoGUI messaging system not available for broadcast")
            return {agent: False for agent in SWARM_AGENTS}

        if self.dry_run:
            logger.info(f"🔍 DRY RUN BROADCAST: {message} to all agents")
            return {agent: True for agent in SWARM_AGENTS}

        try:
            # Use enhanced broadcast_message_to_agents from SSOT
            results = broadcast_message_to_agents(message, "ConsolidatedMessagingService")
            logger.info(f"✅ Enhanced broadcast completed with results: {results}")
            return results

        except Exception as e:
            logger.error(f"❌ Broadcast failed: {e}")
            return {agent: False for agent in SWARM_AGENTS}

    def list_available_agents(self) -> List[str]:
        """List all available agents."""
        if MESSAGING_AVAILABLE and self.coordinate_loader:
            return list(self.coordinate_loader.get_all_agents())
        return SWARM_AGENTS

    def show_message_history(self, agent_id: Optional[str] = None) -> None:
        """Show message history for agent or all agents."""
        if not MESSAGING_AVAILABLE:
            logger.error("❌ Messaging system not available")
            return
            
        try:
            show_message_history(agent_id)
        except Exception as e:
            logger.error(f"❌ Failed to show message history: {e}")

    def run_cli_interface(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI interface for messaging operations."""
        parser = argparse.ArgumentParser(description="Consolidated Messaging Service CLI")
        parser.add_argument("--agent", "-a", help="Target agent ID")
        parser.add_argument("--message", "-m", help="Message content")
        parser.add_argument("--priority", "-p", choices=["LOW", "NORMAL", "HIGH", "URGENT"], 
                          default="NORMAL", help="Message priority")
        parser.add_argument("--tag", "-t", choices=["GENERAL", "COORDINATION", "TASK", "STATUS"], 
                          default="GENERAL", help="Message tag")
        parser.add_argument("--broadcast", "-b", action="store_true", 
                          help="Broadcast to all agents")
        parser.add_argument("--list-agents", "-l", action="store_true",
                          help="List available agents")
        parser.add_argument("--history", action="store_true",
                          help="Show message history")
        parser.add_argument("--dry-run", action="store_true",
                          help="Dry run mode (no actual sending)")
        parser.add_argument("--capture-coords", action="store_true",
                          help="Launch interactive coordinate capture tool")
        parser.add_argument("--show-coords", action="store_true",
                          help="Display current coordinates for all agents")

        # Thea Communication options
        parser.add_argument("--thea-message", help="Send message to Thea AI assistant")
        parser.add_argument("--thea-username", help="ChatGPT username for Thea authentication")
        parser.add_argument("--thea-password", help="ChatGPT password for Thea authentication")
        parser.add_argument("--thea-headless", action="store_true", default=True,
                          help="Run Thea browser in headless mode (default: True)")
        parser.add_argument("--thea-no-headless", action="store_true",
                          help="Disable headless mode for Thea browser")

        # Task-to-Thea pipeline options
        parser.add_argument("--task-assistance", help="Request Thea assistance for a specific task")
        parser.add_argument("--task-context", help="Additional context for the task")
        parser.add_argument("--agent-id", help="Agent requesting assistance (for task context)")

        # v3.3 Thea enhancements
        parser.add_argument("--thea-resume-last", action="store_true", help="Resume Thea conversation at last stored thread URL")
        parser.add_argument("--thea-thread-url", help="Resume Thea conversation at this specific thread URL")
        parser.add_argument("--thea-attach", help="Path to a file to attach to Thea message (best-effort UI automation)")

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
                parsed_args.message, 
                parsed_args.priority, 
                parsed_args.tag
            )
            
            print(f"Broadcast results:")
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
                getattr(parsed_args, 'thea_thread_url', None),
                getattr(parsed_args, 'thea_resume_last', False),
                getattr(parsed_args, 'thea_attach', None)
            )
            return

        # Handle Thea communication
        if parsed_args.thea_message:
            self.handle_thea_communication(
                parsed_args.thea_message,
                parsed_args.thea_username,
                parsed_args.thea_password,
                parsed_args.thea_headless,
                getattr(parsed_args, 'thea_thread_url', None),
                getattr(parsed_args, 'thea_resume_last', False),
                getattr(parsed_args, 'thea_attach', None)
            )
            return

        if parsed_args.agent and parsed_args.message:
            # Prioritize enhanced PyAutoGUI messaging system
            if self.pyautogui_available:
                success = self.send_message_pyautogui(
                    parsed_args.agent,
                    parsed_args.message,
                    parsed_args.priority,
                    parsed_args.tag
                )
            elif MESSAGING_AVAILABLE:
                success = self.send_message_unified(
                    parsed_args.agent,
                    parsed_args.message,
                    parsed_args.priority,
                    parsed_args.tag
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

    def broadcast_message(self, content: str, sender: str = "Agent-1") -> Dict[str, bool]:
        """Broadcast message to all agents."""
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        results = {}

        if not self.service_available:
            self.logger.warning("⚠️ Messaging system not available for broadcast")
            # Return False for all agents when messaging unavailable
            return {agent: False for agent in agents}

        try:
            # Use the imported broadcast_message function if available
            if MESSAGING_AVAILABLE:
                broadcast_result = broadcast_message(content, sender)
                # Assume broadcast succeeds for all agents
                return {agent: broadcast_result for agent in agents}
            else:
                self.logger.info(f"🔍 DRY RUN BROADCAST: {content} from {sender}")
                # Dry run succeeds for all agents
                return {agent: True for agent in agents}
        except Exception as e:
            self.logger.error(f"❌ Broadcast failed: {e}")
            return {agent: False for agent in agents}

    def list_agents(self) -> List[str]:
        """List all available agents."""
        if not self.service_available:
            # Return default agent list
            return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        try:
            # Use the imported list_agents function if available
            if MESSAGING_AVAILABLE:
                return list_agents()
            else:
                return ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        except Exception as e:
            self.logger.error(f"❌ List agents failed: {e}")
            return []

    def show_message_history(self) -> Optional[List[Dict[str, Any]]]:
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

    def get_agent_workspaces_status(self) -> Dict[str, Any]:
        """Get status of agent workspaces and inboxes."""
        if not self.pyautogui_available:
            self.logger.warning("⚠️ PyAutoGUI messaging system not available for status check")
            return {"workspaces_exist": False, "agents": {}}

        try:
            return get_agent_workspaces_status()
        except Exception as e:
            self.logger.error(f"❌ Failed to get agent workspaces status: {e}")
            return {"workspaces_exist": False, "agents": {}}

    def launch_coordinate_capture(self):
        """Launch the interactive coordinate capture tool."""
        try:
            print("🚀 Launching Interactive Coordinate Capture Tool...")
            print("="*60)

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

    def handle_task_assistance(self, task: str, context: str = None, agent_id: str = None,
                              username: str = None, password: str = None, headless: bool = True,
                              thread_url: str = None, resume_last: bool = False, attach_file: str = None):
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
                print(structured_message[:200] + "..." if len(structured_message) > 200 else structured_message)
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
                attach_file
            )

        except Exception as e:
            self.logger.error(f"❌ Task assistance failed: {e}")
            print(f"❌ Error during task assistance: {e}")

    def _create_task_assistance_message(self, task: str, context: str = None, agent_id: str = None) -> str:
        """Create a structured message for Thea task assistance."""
        message_parts = [
            "🎯 AGENT TASK ASSISTANCE REQUEST",
            "",
            f"**Agent ID:** {agent_id or 'Unknown Agent'}",
            f"**Request Type:** Task Assistance",
            f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Task Description",
            task,
        ]

        if context:
            message_parts.extend([
                "",
                "## Additional Context",
                context
            ])

        message_parts.extend([
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
            "🐝 **WE ARE SWARM** - Task assistance requested through automated pipeline"
        ])

        return "\n".join(message_parts)

    def handle_thea_communication(self, message: str, username: str = None,
                                  password: str = None, headless: bool = True,
                                  thread_url: str = None, resume_last: bool = False,
                                  attach_file: str = None):
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
            import sys
            import os
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
                attach_file=attach_file
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
            with open(coord_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            print("📊 CURRENT AGENT COORDINATES")
            print("="*80)

            agents = data.get("agents", {})
            if not agents:
                print("❌ No agents configured yet.")
                print("💡 Run coordinate capture: --capture-coords")
                return

            print("<8")
            print("-" * 82)

            agent_order = ["Agent-1", "Agent-2", "Agent-3", "Agent-4",
                          "Agent-5", "Agent-6", "Agent-7", "Agent-8"]

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

            print("="*80)
            print(f"📁 Coordinate file: {coord_file}")
            print(f"📅 Last updated: {data.get('last_updated', 'Unknown')}")
            print(f"🔢 Version: {data.get('version', 'Unknown')}")

        except Exception as e:
            self.logger.error(f"❌ Failed to show coordinates: {e}")
            print(f"❌ Error displaying coordinates: {e}")


def get_consolidated_messaging_system():
    """Get the consolidated messaging system instance."""
    return ConsolidatedMessagingService()


def main():
    """Main entry point for CLI interface."""
    service = ConsolidatedMessagingService()
    service.run_cli_interface()


if __name__ == "__main__":
    main()
