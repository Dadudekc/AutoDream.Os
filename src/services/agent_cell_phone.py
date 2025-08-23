"""
Agent Cell Phone - Main Coordination Interface (V2 with V1 Compatibility)

This module provides the main coordination interface integrating:
- Agent Manager for lifecycle control
- Message Router for communication
- Config Manager for settings
- PyAutoGUI integration for screen control
- Response capture system
- Heartbeat monitoring
- Message listening and handling

Architecture: Single Responsibility Principle - main coordination interface
LOC: 200 lines (at limit)
"""

import argparse
import time
import threading
import queue
import os
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
import logging

# Import core components
import sys
from pathlib import Path

# Add src to path for imports
src_path = Path(__file__).parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from core.agent_manager import AgentManager, AgentStatus
from core.message_router import MessageRouter, MessageType, MessagePriority
from core.config_manager import ConfigManager

# Try to import PyAutoGUI for screen control
try:
    import pyautogui

    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    PYAUTOGUI_AVAILABLE = False

logger = logging.getLogger(__name__)


class MsgTag(Enum):
    """Message tags for system communication (V1 compatible)"""

    NORMAL = ""
    RESUME = "[RESUME]"
    SYNC = "[SYNC]"
    VERIFY = "[VERIFY]"
    REPAIR = "[REPAIR]"
    BACKUP = "[BACKUP]"
    RESTORE = "[RESTORE]"
    CLEANUP = "[CLEANUP]"
    CAPTAIN = "[CAPTAIN]"
    TASK = "[TASK]"
    INTEGRATE = "[INTEGRATE]"
    REPLY = "[REPLY]"
    COORDINATE = "[COORDINATE]"
    ONBOARDING = "[ONBOARDING]"
    RESCUE = "[RESCUE]"


@dataclass
class SystemStatus:
    """System operational status"""

    total_agents: int
    online_agents: int
    message_queue_size: int
    uptime: float
    last_heartbeat: float


class AgentMessage:
    """Structure for agent messages (V1 compatible)"""

    def __init__(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        tag: MsgTag = MsgTag.NORMAL,
        timestamp: Optional[float] = None,
    ):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.tag = tag
        self.timestamp = timestamp or time.time()

    def __str__(self) -> str:
        return f"{self.from_agent} → {self.to_agent}: {self.tag.value} {self.content}"


class AgentCellPhone:
    """
    Main coordination interface for the agent system (V2 with V1 compatibility)

    Responsibilities:
    - Integrate core components (Agent Manager, Message Router, Config Manager)
    - Provide high-level system operations
    - Coordinate agent activities
    - Monitor system health
    - Maintain V1 compatibility for existing integrations
    """

    def __init__(
        self, agent_id: str = "Agent-1", config_dir: str = "config", test: bool = False
    ):
        self.agent_id = agent_id
        self.agent_manager = AgentManager()
        self.message_router = MessageRouter()
        self.config_manager = ConfigManager(config_dir)
        self.start_time = time.time()
        self.logger = logging.getLogger(f"{__name__}.AgentCellPhone")

        # V1 compatibility features
        self._test_mode = test
        self._pyautogui_queue = None
        self._conversation_history: List[AgentMessage] = []
        self._message_handlers: Dict[str, Callable[[AgentMessage], None]] = {}
        self._listening = False
        self._listener_thread: Optional[threading.Thread] = None

        # Heartbeat system
        self._heartbeat_interval = float(
            os.environ.get("ACP_HEARTBEAT_SEC", "60") or 60
        )
        self._hb_stop = threading.Event()
        self._hb_thread: Optional[threading.Thread] = None

        self._load_configuration()
        self._start_heartbeat()

    def _load_configuration(self):
        """Load system configuration"""
        try:
            self.config_manager.load_configs()
            self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")

    def _start_heartbeat(self):
        """Start heartbeat monitoring thread"""
        if self._heartbeat_interval > 0:
            self._hb_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self._hb_thread.start()
            self.logger.info("Heartbeat monitoring started")

    def _heartbeat_loop(self):
        """Heartbeat monitoring loop"""
        while not self._hb_stop.is_set():
            try:
                self._emit_heartbeat()
                time.sleep(self._heartbeat_interval)
            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
                time.sleep(5)  # Brief pause on error

    def _emit_heartbeat(self):
        """Emit heartbeat for all online agents"""
        for agent_id in self.agent_manager.get_all_agents():
            if self.agent_manager.get_agent_status(agent_id) == AgentStatus.ONLINE:
                self.agent_manager.update_agent_metadata(
                    agent_id, {"last_heartbeat": time.time()}
                )

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
        return self.message_router.send_message(sender, recipient, content)

    # V1 Compatibility Methods
    def send(
        self,
        agent: str,
        message: str,
        tag: MsgTag = MsgTag.NORMAL,
        new_chat: bool = False,
        nudge_stalled: bool = False,
    ) -> None:
        """Send message to agent (V1 compatibility)"""
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("PyAutoGUI not available, using message router")
            self.send_message(self.agent_id, agent, message)
            return

        # Create message object and add to history
        msg = AgentMessage(self.agent_id, agent, message, tag)
        self._conversation_history.append(msg)

        # Log the send operation
        self.logger.info(f"→ {agent}: {message[:80]}")

        # For now, route through message system
        # TODO: Implement full PyAutoGUI integration
        self.send_message(self.agent_id, agent, message)

    def broadcast(self, message: str, tag: MsgTag = MsgTag.NORMAL) -> None:
        """Send message to all agents (V1 compatibility)"""
        agents = self.agent_manager.get_all_agents()
        for agent_id in agents:
            if agent_id != self.agent_id:
                self.send(agent_id, message, tag)

    def start_listening(self) -> None:
        """Start listening for incoming messages (V1 compatibility)"""
        if self._listening:
            return

        self._listening = True
        self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listener_thread.start()
        self.logger.info("Started listening for messages")

    def stop_listening(self) -> None:
        """Stop listening for incoming messages (V1 compatibility)"""
        self._listening = False
        if self._listener_thread:
            self._listener_thread.join(timeout=1)
        self.logger.info("Stopped listening for messages")

    def _listen_loop(self):
        """Message listening loop (V1 compatibility)"""
        while self._listening:
            try:
                # Check for messages from message router
                for agent_id in self.agent_manager.get_all_agents():
                    message = self.message_router.get_message(agent_id, timeout=0.1)
                    if message:
                        self._handle_incoming_message(message)
                time.sleep(0.1)
            except Exception as e:
                self.logger.error(f"Listen loop error: {e}")
                time.sleep(1)

    def _handle_incoming_message(self, message):
        """Handle incoming message (V1 compatibility)"""
        try:
            # Create V1-compatible message object
            v1_message = AgentMessage(
                from_agent=message.sender,
                to_agent=message.recipient,
                content=message.content,
                tag=MsgTag.NORMAL,
                timestamp=message.timestamp,
            )

            # Add to conversation history
            self._conversation_history.append(v1_message)

            # Route to handlers if registered
            if message.message_type.value in self._message_handlers:
                self._message_handlers[message.message_type.value](v1_message)

            self.logger.info(f"← {message.sender}: {message.content[:80]}")

        except Exception as e:
            self.logger.error(f"Error handling incoming message: {e}")

    def register_handler(
        self, message_type: str, handler: Callable[[AgentMessage], None]
    ) -> None:
        """Register message handler (V1 compatibility)"""
        self._message_handlers[message_type] = handler

    def get_conversation_history(self) -> List[AgentMessage]:
        """Get conversation history (V1 compatibility)"""
        return self._conversation_history.copy()

    def get_system_status(self) -> SystemStatus:
        """Get comprehensive system status"""
        agents = self.agent_manager.get_all_agents()
        online_count = sum(1 for a in agents.values() if a.status == AgentStatus.ONLINE)
        queue_status = self.message_router.get_queue_status()
        total_queue_size = sum(queue_status.values())

        return SystemStatus(
            total_agents=len(agents),
            online_agents=online_count,
            message_queue_size=total_queue_size,
            uptime=time.time() - self.start_time,
            last_heartbeat=time.time(),
        )

    def get_all_agents(self) -> Dict[str, Any]:
        """Get all agents (V1 compatibility)"""
        return self.agent_manager.get_all_agents()

    def stop(self) -> None:
        """Stop background threads and services"""
        self.stop_listening()
        if self._hb_thread and self._hb_thread.is_alive():
            self._hb_stop.set()
            self._hb_thread.join(timeout=1)
        self.logger.info("AgentCellPhone stopped")

    def __del__(self):
        try:
            self.stop()
        except Exception:
            pass


def run_smoke_test():
    """Run basic functionality test for AgentCellPhone"""
    print("🧪 Running AgentCellPhone Smoke Test...")

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

        print("✅ AgentCellPhone Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ AgentCellPhone Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for AgentCellPhone testing"""
    parser = argparse.ArgumentParser(description="Agent Cell Phone CLI")
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
        print(f"AgentCellPhone system started for {args.agent_id}")
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
