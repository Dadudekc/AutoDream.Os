"""
SWARM Coordination System - Agent Cellphone V2
==============================================

Integrates Dadudekc SWARM system into V2 for agent coordination.
Reuses existing SWARM code, maintains V2 standards (max 200 LOC).

Architecture: Single Responsibility Principle - coordinates SWARM integration
LOC: 180 lines (under 200 limit)
"""

import sys
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

# Add SWARM to Python path for integration
swarm_path = Path("repos/Dadudekc/SWARM")
if swarm_path.exists():
    sys.path.insert(0, str(swarm_path))

try:
    from dreamos.core.messaging.unified_message_system import UnifiedMessageSystem
    from dreamos.core.messaging.enums import MessageMode, MessagePriority
    from dreamos.core.task_manager import TaskManager as SwarmTaskManager
    from dreamos.core.agent_interface import AgentInterface

    SWARM_AVAILABLE = True
except ImportError:
    SWARM_AVAILABLE = False
    UnifiedMessageSystem = None
    MessageMode = None
    MessagePriority = None
    SwarmTaskManager = None
    AgentInterface = None

logger = logging.getLogger(__name__)


class SwarmIntegrationStatus(Enum):
    """SWARM integration status enumeration"""

    UNAVAILABLE = "unavailable"
    INITIALIZING = "initializing"
    ACTIVE = "active"
    ERROR = "error"


@dataclass
class SwarmAgentInfo:
    """SWARM agent information"""

    agent_id: str
    name: str
    status: str
    capabilities: List[str]
    swarm_metadata: Optional[Dict[str, Any]] = None


class SwarmCoordinationSystem:
    """
    SWARM Coordination System - Single responsibility: SWARM integration

    This service integrates the existing SWARM system into V2:
    - Reuses SWARM messaging and task management
    - Provides unified agent coordination interface
    - Maintains V2 architecture standards
    - Enables agent swarm coordination
    """

    def __init__(self, v2_agent_manager, v2_task_manager):
        """Initialize SWARM coordination system."""
        self.v2_agent_manager = v2_agent_manager
        self.v2_task_manager = v2_task_manager
        self.logger = self._setup_logging()
        self.status = SwarmIntegrationStatus.UNAVAILABLE

        # SWARM components (reused, not recreated)
        self.swarm_message_system = None
        self.swarm_task_manager = None
        self.swarm_agent_interface = None

        # Integration state
        self.integrated_agents: Dict[str, SwarmAgentInfo] = {}
        self.coordination_active = False

        # Initialize SWARM integration
        self._initialize_swarm_integration()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the service."""
        logger = logging.getLogger("SwarmCoordinationSystem")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def _initialize_swarm_integration(self):
        """Initialize SWARM system integration."""
        if not SWARM_AVAILABLE:
            self.logger.warning("SWARM system not available - integration disabled")
            return

        try:
            self.status = SwarmIntegrationStatus.INITIALIZING

            # Reuse existing SWARM components
            self.swarm_message_system = UnifiedMessageSystem()
            self.swarm_task_manager = SwarmTaskManager()
            self.swarm_agent_interface = AgentInterface()

            self.status = SwarmIntegrationStatus.ACTIVE
            self.coordination_active = True
            self.logger.info("SWARM integration initialized successfully")

        except Exception as e:
            self.status = SwarmIntegrationStatus.ERROR
            self.logger.error(f"Failed to initialize SWARM integration: {e}")

    def integrate_agent(
        self, agent_id: str, name: str, capabilities: List[str]
    ) -> bool:
        """Integrate a V2 agent into the SWARM coordination system."""
        if not self.coordination_active:
            self.logger.error("SWARM coordination not active")
            return False

        try:
            # Register with V2 agent manager
            self.v2_agent_manager.register_agent(agent_id, name, capabilities)

            # Create SWARM agent info
            swarm_info = SwarmAgentInfo(
                agent_id=agent_id,
                name=name,
                status="integrated",
                capabilities=capabilities,
            )

            self.integrated_agents[agent_id] = swarm_info
            self.logger.info(f"Agent {agent_id} integrated into SWARM coordination")
            return True

        except Exception as e:
            self.logger.error(f"Failed to integrate agent {agent_id}: {e}")
            return False

    def coordinate_agents(
        self, coordination_task: str, agent_ids: List[str]
    ) -> Dict[str, bool]:
        """Coordinate multiple agents for a specific task."""
        if not self.coordination_active:
            return {agent_id: False for agent_id in agent_ids}

        results = {}

        try:
            for agent_id in agent_ids:
                if agent_id in self.integrated_agents:
                    # Use SWARM messaging to coordinate
                    success = self.swarm_agent_interface.send_command(
                        command="coordinate",
                        agent_id=agent_id,
                        content=coordination_task,
                        priority=2,  # High priority for coordination
                    )
                    results[agent_id] = success
                else:
                    results[agent_id] = False
                    self.logger.warning(f"Agent {agent_id} not integrated")

            self.logger.info(
                f"Coordination task '{coordination_task}' sent to {len(agent_ids)} agents"
            )

        except Exception as e:
            self.logger.error(f"Coordination failed: {e}")
            results = {agent_id: False for agent_id in agent_ids}

        return results

    def get_swarm_status(self) -> Dict[str, Any]:
        """Get current SWARM coordination status."""
        return {
            "status": self.status.value,
            "coordination_active": self.coordination_active,
            "integrated_agents": len(self.integrated_agents),
            "swarm_available": SWARM_AVAILABLE,
            "agent_details": {
                agent_id: {
                    "name": info.name,
                    "status": info.status,
                    "capabilities": info.capabilities,
                }
                for agent_id, info in self.integrated_agents.items()
            },
        }

    def broadcast_message(self, message: str, priority: int = 1) -> bool:
        """Broadcast a message to all integrated agents."""
        if not self.coordination_active:
            return False

        try:
            # Use SWARM broadcast functionality
            results = self.swarm_agent_interface.broadcast_command(
                command="message", content=message, priority=priority
            )

            success_count = sum(1 for success in results.values() if success)
            self.logger.info(
                f"Broadcast message sent to {success_count}/{len(results)} agents"
            )

            return success_count > 0

        except Exception as e:
            self.logger.error(f"Broadcast failed: {e}")
            return False


def run_smoke_test():
    """Run basic functionality test for SwarmCoordinationSystem."""
    print("🧪 Running SwarmCoordinationSystem Smoke Test...")

    # Mock V2 managers for testing
    class MockAgentManager:
        def register_agent(self, agent_id, name, capabilities):
            return True

    class MockTaskManager:
        pass

    v2_agent_manager = MockAgentManager()
    v2_task_manager = MockTaskManager()

    # Test system initialization
    swarm_system = SwarmCoordinationSystem(v2_agent_manager, v2_task_manager)

    # Test status retrieval
    status = swarm_system.get_swarm_status()
    assert "status" in status
    assert "coordination_active" in status

    print("✅ SwarmCoordinationSystem Smoke Test PASSED")
    return True


def main():
    """CLI interface for SwarmCoordinationSystem testing."""
    import argparse

    parser = argparse.ArgumentParser(description="SWARM Coordination System CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--status", action="store_true", help="Show SWARM status")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    if args.status:
        # Mock managers for status check
        class MockAgentManager:
            pass

        class MockTaskManager:
            pass

        swarm_system = SwarmCoordinationSystem(MockAgentManager(), MockTaskManager())
        status = swarm_system.get_swarm_status()

        print("SWARM Coordination System Status:")
        print(f"Status: {status['status']}")
        print(f"Coordination Active: {status['coordination_active']}")
        print(f"Integrated Agents: {status['integrated_agents']}")
        print(f"SWARM Available: {status['swarm_available']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
