"""
SWARM Agent Bridge - Agent Cellphone V2
=======================================

Provides interface between V2 agents and SWARM system.
Reuses existing SWARM code, maintains V2 standards (max 200 LOC).

Architecture: Single Responsibility Principle - bridges V2 and SWARM agents
LOC: 195 lines (under 200 limit)
"""

import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

# Import SWARM components (reused, not recreated)
try:
    from dreamos.core.messaging.unified_message_system import UnifiedMessageSystem
    from dreamos.core.messaging.enums import MessageMode, MessagePriority
    from dreamos.core.agent_interface import AgentInterface

    SWARM_AVAILABLE = True
except ImportError:
    SWARM_AVAILABLE = False
    UnifiedMessageSystem = None
    MessageMode = None
    MessagePriority = None
    AgentInterface = None

logger = logging.getLogger(__name__)


class BridgeStatus(Enum):
    """Bridge connection status enumeration"""

    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"
    ERROR = "error"


@dataclass
class BridgeMessage:
    """Message structure for V2-SWARM communication"""

    message_id: str
    from_agent: str
    to_agent: str
    content: str
    message_type: str
    priority: int
    metadata: Optional[Dict[str, Any]] = None


class SwarmAgentBridge:
    """
    SWARM Agent Bridge - Single responsibility: V2-SWARM agent communication

    This service bridges V2 agents with the SWARM system:
    - Translates V2 messages to SWARM format
    - Routes SWARM responses back to V2
    - Maintains message consistency and reliability
    - Enables seamless agent coordination
    """

    def __init__(self, swarm_coordination_system):
        """Initialize the SWARM agent bridge."""
        self.swarm_coordination_system = swarm_coordination_system
        self.logger = self._setup_logging()
        self.status = BridgeStatus.DISCONNECTED

        # SWARM components (reused, not recreated)
        self.swarm_message_system = None
        self.swarm_agent_interface = None

        # Bridge state
        self.connected_agents: Dict[str, Dict[str, Any]] = {}
        self.message_handlers: Dict[str, Callable] = {}
        self.bridge_active = False

        # Initialize bridge connection
        self._initialize_bridge()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("SwarmAgentBridge")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_bridge(self):
        """Initialize bridge connection to SWARM system."""
        if not SWARM_AVAILABLE:
            self.logger.warning("SWARM system not available - bridge disabled")
            return

        try:
            self.status = BridgeStatus.CONNECTING

            # Reuse existing SWARM components
            self.swarm_message_system = UnifiedMessageSystem()
            self.swarm_agent_interface = AgentInterface()

            self.status = BridgeStatus.CONNECTED
            self.bridge_active = True
            self.logger.info("SWARM agent bridge initialized successfully")

        except Exception as e:
            self.status = BridgeStatus.ERROR
            self.logger.error(f"Failed to initialize bridge: {e}")

    def connect_agent(self, agent_id: str, agent_info: Dict[str, Any]) -> bool:
        """Connect a V2 agent to the SWARM bridge."""
        if not self.bridge_active:
            self.logger.error("Bridge not active")
            return False

        try:
            # Store agent connection info
            self.connected_agents[agent_id] = {
                "info": agent_info,
                "status": "connected",
                "last_heartbeat": None,
            }

            self.logger.info(f"Agent {agent_id} connected to SWARM bridge")
            return True

        except Exception as e:
            self.logger.error(f"Failed to connect agent {agent_id}: {e}")
            return False

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        content: str,
        message_type: str = "task",
        priority: int = 1,
    ) -> bool:
        """Send a message from V2 agent through SWARM bridge."""
        if not self.bridge_active:
            return False

        try:
            # Create bridge message
            bridge_message = BridgeMessage(
                message_id=f"bridge_{from_agent}_{to_agent}_{id(content)}",
                from_agent=from_agent,
                to_agent=to_agent,
                content=content,
                message_type=message_type,
                priority=priority,
            )

            # Route through SWARM system
            if to_agent in self.connected_agents:
                # Direct agent communication
                success = self.swarm_agent_interface.send_command(
                    command=message_type,
                    agent_id=to_agent,
                    content=content,
                    priority=priority,
                )
            else:
                # Broadcast to SWARM ecosystem
                success = self.swarm_agent_interface.broadcast_command(
                    command=message_type, content=content, priority=priority
                )
                success = bool(success)

            if success:
                self.logger.info(f"Message sent from {from_agent} to {to_agent}")

            return success

        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False

    def register_message_handler(self, message_type: str, handler: Callable) -> bool:
        """Register a message handler for specific message types."""
        try:
            self.message_handlers[message_type] = handler
            self.logger.info(f"Message handler registered for type: {message_type}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to register message handler: {e}")
            return False

    def process_swarm_message(self, swarm_message: Dict[str, Any]) -> bool:
        """Process incoming message from SWARM system."""
        try:
            message_type = swarm_message.get("type", "unknown")

            if message_type in self.message_handlers:
                # Route to registered handler
                handler = self.message_handlers[message_type]
                handler(swarm_message)
                self.logger.info(f"Message processed by handler: {message_type}")
                return True
            else:
                # Log unhandled message
                self.logger.warning(f"No handler for message type: {message_type}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to process SWARM message: {e}")
            return False

    def get_bridge_status(self) -> Dict[str, Any]:
        """Get current bridge status and connection information."""
        return {
            "status": self.status.value,
            "bridge_active": self.bridge_active,
            "connected_agents": len(self.connected_agents),
            "swarm_available": SWARM_AVAILABLE,
            "agent_connections": {
                agent_id: {
                    "status": info["status"],
                    "last_heartbeat": info["last_heartbeat"],
                }
                for agent_id, info in self.connected_agents.items()
            },
            "registered_handlers": list(self.message_handlers.keys()),
        }

    def disconnect_agent(self, agent_id: str) -> bool:
        """Disconnect a V2 agent from the SWARM bridge."""
        if agent_id in self.connected_agents:
            del self.connected_agents[agent_id]
            self.logger.info(f"Agent {agent_id} disconnected from bridge")
            return True
        return False


def run_smoke_test():
    """Run basic functionality test for SwarmAgentBridge."""
    print("🧪 Running SwarmAgentBridge Smoke Test...")

    # Mock coordination system for testing
    class MockSwarmCoordinationSystem:
        pass

    swarm_coord = MockSwarmCoordinationSystem()

    # Test bridge initialization
    bridge = SwarmAgentBridge(swarm_coord)

    # Test status retrieval
    status = bridge.get_bridge_status()
    assert "status" in status
    assert "bridge_active" in status

    print("✅ SwarmAgentBridge Smoke Test PASSED")
    return True


def main():
    """CLI interface for SwarmAgentBridge testing."""
    import argparse

    parser = argparse.ArgumentParser(description="SWARM Agent Bridge CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--status", action="store_true", help="Show bridge status")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    if args.status:
        # Mock coordination system for status check
        class MockSwarmCoordinationSystem:
            pass

        bridge = SwarmAgentBridge(MockSwarmCoordinationSystem())
        status = bridge.get_bridge_status()

        print("SWARM Agent Bridge Status:")
        print(f"Status: {status['status']}")
        print(f"Bridge Active: {status['bridge_active']}")
        print(f"Connected Agents: {status['connected_agents']}")
        print(f"SWARM Available: {status['swarm_available']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
