#!/usr/bin/env python3
"""
Agent Cell Phone - Refactored (V2 with V1 Compatibility)
========================================================
Main coordination interface using extracted services.
Follows 200 LOC limit and single responsibility principle.
"""

import argparse
import time
import logging
from typing import Dict, List, Any, Optional

# Import core components
from ..core.agent_manager import AgentManager, AgentStatus
from ..core.message_router import MessageRouter
from ..core.config_manager import ConfigManager

# Import extracted services
from .message_handler_v2 import MessageHandlerV2, MsgTag
from .heartbeat_monitor import HeartbeatMonitor
from .v1_compatibility_layer import V1CompatibilityLayer

logger = logging.getLogger(__name__)


class AgentCellPhone:
    """
    Main coordination interface for the agent system (V2 with V1 compatibility)

    Responsibilities:
    - Integrate core components (Agent Manager, Message Router, Config Manager)
    - Provide high-level system operations
    - Coordinate agent activities
    - Maintain V1 compatibility for existing integrations
    """

    def __init__(
        self, agent_id: str = "Agent-1", config_dir: str = "config", test: bool = False
    ):
        self.agent_id = agent_id
        self.agent_manager = AgentManager()
        self.message_router = MessageRouter()
        self.config_manager = ConfigManager(config_dir)

        # Initialize extracted services
        self.message_handler = MessageHandlerV2(self.message_router)
        self.heartbeat_monitor = HeartbeatMonitor(self.agent_manager)
        self.v1_compatibility = V1CompatibilityLayer(self.message_handler, agent_id)

        # V1 compatibility features
        self._test_mode = test
        self.logger = logging.getLogger(f"{__name__}.AgentCellPhone")

        self._load_configuration()

    def _load_configuration(self):
        """Load system configuration"""
        try:
            self.config_manager.load_configs()
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")

    def register_agent(self, agent_id: str, name: str, capabilities: List[str]) -> bool:
        """Register a new agent with the system"""
        try:
            if not self.agent_manager.register_agent(agent_id, name, capabilities):
                return False
            if not self.message_router.register_agent(agent_id):
                self.agent_manager.stop_agent(agent_id)
                return False
            self.logger.info(f"Agent {agent_id} registered successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to register agent {agent_id}: {e}")
            return False

    def start_agent(self, agent_id: str) -> bool:
        """Start an agent"""
        return self.agent_manager.start_agent(agent_id)

    def stop_agent(self, agent_id: str) -> bool:
        """Stop an agent"""
        return self.agent_manager.stop_agent(agent_id)

    def send_message(
        self,
        sender: str,
        recipient: str,
        content: Any,
        msg_tag: MsgTag = MsgTag.COORDINATE,
    ) -> bool:
        """Send a message between agents"""
        return self.message_handler.send_message(sender, recipient, content, msg_tag)

    # V1 Compatibility Methods (delegated to V1CompatibilityLayer)
    def send(
        self,
        agent: str,
        message: str,
        tag: MsgTag = MsgTag.NORMAL,
        new_chat: bool = False,
        nudge_stalled: bool = False,
    ) -> None:
        """Send message to agent (V1 compatibility)"""
        self.v1_compatibility.send(agent, message, tag, new_chat, nudge_stalled)

    def broadcast(self, message: str, tag: MsgTag = MsgTag.NORMAL) -> None:
        """Send message to all agents (V1 compatibility)"""
        self.v1_compatibility.broadcast(message, tag)

    def start_listening(self) -> None:
        """Start listening for incoming messages (V1 compatibility)"""
        self.v1_compatibility.start_listening()

    def stop_listening(self) -> None:
        """Stop listening for incoming messages (V1 compatibility)"""
        self.v1_compatibility.stop_listening()

    def register_handler(self, message_type: str, handler) -> None:
        """Register message handler (V1 compatibility)"""
        self.v1_compatibility.register_handler(message_type, handler)

    def get_conversation_history(self):
        """Get conversation history (V1 compatibility)"""
        return self.v1_compatibility.get_conversation_history()

    def get_system_status(self):
        """Get comprehensive system status"""
        return self.heartbeat_monitor.get_system_status()

    def get_all_agents(self) -> Dict[str, Any]:
        """Get all agents (V1 compatibility)"""
        return self.agent_manager.get_all_agents()

    def stop(self) -> None:
        """Stop background threads and services"""
        self.v1_compatibility.stop_listening()
        self.heartbeat_monitor.stop()
        self.logger.info("AgentCellPhone stopped")

    def __del__(self):
        try:
            self.stop()
        except Exception:
            pass


def run_smoke_test():
    """Run basic functionality test for AgentCellPhone"""
    print("🧪 Running AgentCellPhone Refactored Smoke Test...")

    try:
        system = AgentCellPhone(test=True)

        # Test agent registration
        assert system.register_agent("test-1", "Test Agent 1", ["test"])
        assert system.register_agent("test-2", "Test Agent 2", ["test", "demo"])

        # Test agent start
        assert system.start_agent("test-1")
        assert system.agent_manager.get_agent_status("test-1") == AgentStatus.ONLINE

        # Test message sending
        assert system.send_message("test-1", "test-2", "Hello!")

        # Test system status
        status = system.get_system_status()
        assert status.total_agents == 2
        assert status.online_agents == 1

        # Test V1 compatibility methods
        system.send("test-2", "Test message", MsgTag.NORMAL)
        system.broadcast("Broadcast message", MsgTag.COORDINATE)

        # Cleanup
        system.stop()

        print("✅ AgentCellPhone Refactored Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ AgentCellPhone Refactored Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for AgentCellPhone testing"""
    parser = argparse.ArgumentParser(description="Agent Cell Phone Refactored CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--agent-id", default="Agent-1", help="Agent ID")
    parser.add_argument(
        "--config-dir", default="config", help="Configuration directory"
    )

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    # Create system instance
    system = AgentCellPhone(agent_id=args.agent_id, config_dir=args.config_dir)

    try:
        print(f"AgentCellPhone Refactored system started for {args.agent_id}")
        print("Press Ctrl+C to stop")

        # Start listening
        system.start_listening()

        # Keep running
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        system.stop()


if __name__ == "__main__":
    main()
