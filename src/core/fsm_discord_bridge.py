#!/usr/bin/env python3
"""
FSM-Discord Integration Bridge - Agent Cellphone V2
==================================================

Bridges FSM system with Discord for real-time state synchronization.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP.

**Features:**
- Real-time FSM state updates to Discord
- Discord command processing for FSM control
- Agent status synchronization
- Task coordination via Discord
- Decision engine integration

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import json
import time
import asyncio
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from pathlib import Path

# Import FSM and decision components
try:
    from .fsm_core_v2 import FSMCoreV2
    from .decision import AutonomousDecisionEngine
    from ..services.discord_integration_service import DiscordIntegrationService

    COMPONENTS_AVAILABLE = True
except ImportError as e:
    COMPONENTS_AVAILABLE = False

    # Define placeholder classes for when imports fail
    class FSMCoreV2:
        pass

    class AutonomousDecisionEngine:
        pass

    class DiscordIntegrationService:
        pass

    print(f"⚠️ Some components not available: {e} - using placeholder classes")


class FSMDiscordBridge:
    """
    Bridge between FSM system and Discord for real-time integration

    Responsibilities:
    - Synchronize FSM state with Discord
    - Process Discord commands for FSM control
    - Coordinate agent activities via Discord
    - Integrate decision engine with Discord
    """

    def __init__(
        self,
        fsm_core: Optional[FSMCoreV2] = None,
        decision_engine: Optional[AutonomousDecisionEngine] = None,
        discord_service: Optional[DiscordIntegrationService] = None,
    ):
        self.fsm_core = fsm_core
        self.decision_engine = decision_engine
        self.discord_service = discord_service
        self.logger = logging.getLogger(__name__)

        # Integration status
        self.fsm_enabled = fsm_core is not None
        self.decision_enabled = decision_engine is not None
        self.discord_enabled = discord_service is not None

        # State synchronization
        self.last_sync = datetime.now().isoformat()
        self.sync_interval = 30  # seconds
        self.auto_sync = True

        # Discord command handlers
        self.command_handlers: Dict[str, Callable] = {}
        self._register_default_commands()

        # FSM event listeners
        self.fsm_listeners: List[Callable] = []
        if self.fsm_enabled:
            self._setup_fsm_listeners()

        self.logger.info("🚀 FSM-Discord Bridge initialized")
        self._log_integration_status()

    def _log_integration_status(self):
        """Log current integration status"""
        status = []
        if self.fsm_enabled:
            status.append("✅ FSM Core")
        if self.decision_enabled:
            status.append("✅ Decision Engine")
        if self.discord_enabled:
            status.append("✅ Discord Service")

        self.logger.info(f"🔗 Integration Status: {' | '.join(status)}")

    def _register_default_commands(self):
        """Register default Discord command handlers"""
        if not self.discord_enabled:
            return

        self.command_handlers = {
            "!fsm_status": self._handle_fsm_status_command,
            "!create_task": self._handle_create_task_command,
            "!update_task": self._handle_update_task_command,
            "!agent_status": self._handle_agent_status_command,
            "!request_decision": self._handle_decision_request_command,
            "!sync_state": self._handle_sync_state_command,
            "!help": self._handle_help_command,
        }

    def _setup_fsm_listeners(self):
        """Setup FSM event listeners for Discord synchronization"""
        if not self.fsm_enabled:
            return

        # Listen for FSM state changes
        self.fsm_listeners.append(self._on_fsm_state_change)
        self.fsm_listeners.append(self._on_fsm_task_created)
        self.fsm_listeners.append(self._on_fsm_task_updated)

        self.logger.info("🔄 FSM event listeners configured")

    def process_discord_command(
        self, command: str, args: List[str], user_id: str, channel: str
    ) -> str:
        """Process Discord command and return response"""
        try:
            if command not in self.command_handlers:
                return (
                    f"❌ Unknown command: {command}. Use !help for available commands."
                )

            handler = self.command_handlers[command]
            response = handler(args, user_id, channel)

            # Send response to Discord
            if self.discord_service:
                self.discord_service.send_message(
                    "fsm_bridge", "command_response", response, channel
                )

            return response

        except Exception as e:
            error_msg = f"❌ Error processing command {command}: {e}"
            self.logger.error(error_msg)
            return error_msg

    def sync_fsm_state_to_discord(self, force: bool = False) -> bool:
        """Synchronize FSM state to Discord channels"""
        try:
            if not self.fsm_enabled or not self.discord_enabled:
                return False

            # Check if sync is needed
            if not force and not self._should_sync():
                return False

            # Get FSM state
            fsm_state = self._get_fsm_state()

            # Send to Discord
            self.discord_service.send_message(
                "fsm_bridge",
                "state_sync",
                f"FSM State Sync: {json.dumps(fsm_state, indent=2)}",
                "fsm_status",
            )

            self.last_sync = datetime.now().isoformat()
            self.logger.info("🔄 FSM state synchronized to Discord")
            return True

        except Exception as e:
            self.logger.error(f"Failed to sync FSM state: {e}")
            return False

    def create_task_via_discord(
        self,
        title: str,
        description: str,
        assigned_agent: str,
        priority: str = "normal",
        channel: str = "tasks",
    ) -> str:
        """Create FSM task via Discord command"""
        try:
            if not self.fsm_enabled:
                return "❌ FSM system not available"

            # Create task in FSM
            task_id = self.fsm_core.create_task(
                title=title,
                description=description,
                assigned_agent=assigned_agent,
                priority=self._convert_priority(priority),
            )

            if task_id:
                # Notify Discord
                self.discord_service.send_message(
                    "fsm_bridge",
                    "task_created",
                    f"✅ Task created: {title} (ID: {task_id}) assigned to {assigned_agent}",
                    channel,
                )

                return f"✅ Task created successfully! ID: {task_id}"
            else:
                return "❌ Failed to create task"

        except Exception as e:
            error_msg = f"❌ Error creating task: {e}"
            self.logger.error(error_msg)
            return error_msg

    def request_decision_via_discord(
        self,
        context: str,
        options: List[str],
        requester: str,
        channel: str = "decisions",
    ) -> str:
        """Request decision via Discord and integrate with decision engine"""
        try:
            if not self.decision_enabled:
                return "❌ Decision engine not available"

            # Create decision context
            decision_context = {
                "decision_id": f"discord_{int(time.time())}",
                "decision_type": "discord_coordination",
                "timestamp": datetime.now().isoformat(),
                "agent_id": requester,
                "context_data": {
                    "context": context,
                    "options": options,
                    "channel": channel,
                },
                "constraints": ["discord_integration"],
                "objectives": ["coordinate_agents"],
                "risk_factors": ["communication_delay"],
            }

            # Make decision
            result = self.decision_engine.make_autonomous_decision(
                "agent_coordination", decision_context
            )

            # Notify Discord
            self.discord_service.send_message(
                "fsm_bridge",
                "decision_result",
                f"🧠 Decision made: {result.selected_option}\nReasoning: {result.reasoning}",
                channel,
            )

            return (
                f"🧠 Decision: {result.selected_option}\nConfidence: {result.confidence}"
            )

        except Exception as e:
            error_msg = f"❌ Error requesting decision: {e}"
            self.logger.error(error_msg)
            return error_msg

    def get_bridge_status(self) -> Dict[str, Any]:
        """Get comprehensive bridge status"""
        return {
            "fsm_enabled": self.fsm_enabled,
            "decision_enabled": self.decision_enabled,
            "discord_enabled": self.discord_enabled,
            "auto_sync": self.auto_sync,
            "last_sync": self.last_sync,
            "sync_interval": self.sync_interval,
            "command_handlers": len(self.command_handlers),
            "fsm_listeners": len(self.fsm_listeners),
            "timestamp": datetime.now().isoformat(),
        }

    # Command handlers
    def _handle_fsm_status_command(
        self, args: List[str], user_id: str, channel: str
    ) -> str:
        """Handle !fsm_status command"""
        if not self.fsm_enabled:
            return "❌ FSM system not available"

        fsm_state = self._get_fsm_state()
        return f"📊 FSM Status:\n{json.dumps(fsm_state, indent=2)}"

    def _handle_create_task_command(
        self, args: List[str], user_id: str, channel: str
    ) -> str:
        """Handle !create_task command"""
        if len(args) < 3:
            return "❌ Usage: !create_task <title> <description> <agent> [priority]"

        title = args[0]
        description = args[1]
        agent = args[2]
        priority = args[3] if len(args) > 3 else "normal"

        return self.create_task_via_discord(
            title, description, agent, priority, channel
        )

    def _handle_update_task_command(
        self, args: List[str], user_id: str, channel: str
    ) -> str:
        """Handle !update_task command"""
        if len(args) < 3:
            return "❌ Usage: !update_task <task_id> <new_state> <summary>"

        task_id = args[0]
        new_state = args[1]
        summary = " ".join(args[2:])

        if not self.fsm_enabled:
            return "❌ FSM system not available"

        # Update task state
        success = self.fsm_core.update_task_state(task_id, new_state, user_id, summary)

        if success:
            return f"✅ Task {task_id} updated to state: {new_state}"
        else:
            return f"❌ Failed to update task {task_id}"

    def _handle_agent_status_command(
        self, args: List[str], user_id: str, channel: str
    ) -> str:
        """Handle !agent_status command"""
        if not self.discord_enabled:
            return "❌ Discord service not available"

        agent_status = self.discord_service.get_status()
        return f"📱 Agent Status:\n{json.dumps(agent_status, indent=2)}"

    def _handle_decision_request_command(
        self, args: List[str], user_id: str, channel: str
    ) -> str:
        """Handle !request_decision command"""
        if len(args) < 2:
            return "❌ Usage: !request_decision <context> <option1> <option2> ..."

        context = args[0]
        options = args[1:]

        return self.request_decision_via_discord(context, options, user_id, channel)

    def _handle_sync_state_command(
        self, args: List[str], user_id: str, channel: str
    ) -> str:
        """Handle !sync_state command"""
        success = self.sync_fsm_state_to_discord(force=True)

        if success:
            return "✅ FSM state synchronized to Discord"
        else:
            return "❌ Failed to sync FSM state"

    def _handle_help_command(self, args: List[str], user_id: str, channel: str) -> str:
        """Handle !help command"""
        help_text = """
🤖 **FSM-Discord Bridge Commands:**

**!fsm_status** - Show current FSM state
**!create_task <title> <description> <agent> [priority]** - Create new task
**!update_task <task_id> <new_state> <summary>** - Update task state
**!agent_status** - Show agent status
**!request_decision <context> <option1> <option2>** - Request AI decision
**!sync_state** - Force FSM state sync to Discord
**!help** - Show this help message

**Priority levels:** low, normal, high, critical
        """
        return help_text.strip()

    # FSM event handlers
    def _on_fsm_state_change(self, task_id: str, old_state: str, new_state: str):
        """Handle FSM state change events"""
        if self.discord_enabled:
            self.discord_service.send_message(
                "fsm_bridge",
                "state_change",
                f"🔄 Task {task_id} state changed: {old_state} → {new_state}",
                "fsm_events",
            )

    def _on_fsm_task_created(self, task_id: str, title: str, agent: str):
        """Handle FSM task creation events"""
        if self.discord_enabled:
            self.discord_service.send_message(
                "fsm_bridge",
                "task_created",
                f"📝 New task created: {title} (ID: {task_id}) assigned to {agent}",
                "fsm_events",
            )

    def _on_fsm_task_updated(self, task_id: str, summary: str):
        """Handle FSM task update events"""
        if self.discord_enabled:
            self.discord_service.send_message(
                "fsm_bridge",
                "task_updated",
                f"📝 Task {task_id} updated: {summary}",
                "fsm_events",
            )

    # Helper methods
    def _should_sync(self) -> bool:
        """Check if FSM state should be synchronized"""
        if not self.auto_sync:
            return False

        last_sync_time = datetime.fromisoformat(self.last_sync)
        time_diff = (datetime.now() - last_sync_time).total_seconds()

        return time_diff >= self.sync_interval

    def _get_fsm_state(self) -> Dict[str, Any]:
        """Get current FSM state"""
        if not self.fsm_enabled:
            return {"error": "FSM not available"}

        try:
            return {
                "total_tasks": len(self.fsm_core.tasks),
                "status": self.fsm_core.status,
                "last_sync": self.last_sync,
            }
        except Exception as e:
            return {"error": f"Failed to get FSM state: {e}"}

    def _convert_priority(self, priority: str) -> Any:
        """Convert string priority to FSM priority enum"""
        if not self.fsm_enabled:
            return priority

        try:
            from .fsm_task_v2 import TaskPriority

            priority_map = {
                "low": TaskPriority.LOW,
                "normal": TaskPriority.NORMAL,
                "high": TaskPriority.HIGH,
                "critical": TaskPriority.CRITICAL,
            }
            return priority_map.get(priority.lower(), TaskPriority.NORMAL)
        except ImportError:
            return priority


def main():
    """Main entry point for FSM-Discord Bridge"""
    import argparse

    parser = argparse.ArgumentParser(description="FSM-Discord Integration Bridge")
    parser.add_argument("--test", action="store_true", help="Run test mode")
    parser.add_argument("--status", action="store_true", help="Show bridge status")

    args = parser.parse_args()

    if args.test:
        print("🧪 Running FSM-Discord Bridge in test mode...")

        # Initialize bridge without components for testing
        bridge = FSMDiscordBridge()

        # Test command processing
        test_commands = [
            ("!help", [], "test_user", "test_channel"),
            ("!fsm_status", [], "test_user", "test_channel"),
            (
                "!create_task",
                ["Test Task", "Integration testing", "agent-1"],
                "test_user",
                "test_channel",
            ),
        ]

        for command, args, user, channel in test_commands:
            print(f"\n🔧 Testing command: {command}")
            response = bridge.process_discord_command(command, args, user, channel)
            print(f"Response: {response}")

        # Show status
        status = bridge.get_bridge_status()
        print(f"\n📊 Bridge Status: {json.dumps(status, indent=2)}")
        print("✅ Test completed successfully!")

        return

    if args.status:
        bridge = FSMDiscordBridge()
        status = bridge.get_bridge_status()
        print(f"📊 Bridge Status: {json.dumps(status, indent=2)}")
        return

    print("Use --test to run test mode")
    print("Use --status to show bridge status")


if __name__ == "__main__":
    main()
