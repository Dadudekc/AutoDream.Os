#!/usr/bin/env python3
"""
FSM-Communication Integration Launcher - Agent Cellphone V2
=========================================================

Launches and manages the integrated FSM-Communication system.
Provides unified interface for FSM-driven agent coordination.
Follows V2 standards: ≤300 LOC, OOP design, SRP.

Author: FSM-Communication Integration Specialist
License: MIT
"""

import logging
import time
import json
import argparse
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import core components
from ..core.workspace_manager import WorkspaceManager
from ..core.inbox_manager import InboxManager
from ..core.fsm_core_v2 import FSMCoreV2
from ..core.agent_communication import AgentCommunicationProtocol
from ..core.fsm_communication_bridge import FSMCommunicationBridge

logger = logging.getLogger(__name__)


class FSMCommunicationIntegrationLauncher:
    """
    FSM-Communication Integration Launcher
    
    Single responsibility: Launch and manage integrated FSM-Communication system.
    Coordinates all components for seamless agent coordination.
    """
    
    def __init__(self, config_path: str = "config/fsm_communication_config.json"):
        """Initialize the integration launcher."""
        self.config_path = config_path
        self.config = self._load_config()
        
        # Core services
        self.workspace_manager = None
        self.inbox_manager = None
        self.fsm_core = None
        self.communication_protocol = None
        self.fsm_bridge = None
        
        # System state
        self.system_active = False
        self.services_status = {}
        self.startup_time = None
        
        # Initialize logging
        self._setup_logging()
        
        logger.info("FSM-Communication Integration Launcher initialized")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, 'r') as f:
                    return json.load(f)
            else:
                # Default configuration
                return {
                    "workspace_path": "agent_workspaces",
                    "inbox_path": "message_data",
                    "fsm_data_path": "fsm_data",
                    "communication": {
                        "heartbeat_interval": 30,
                        "message_timeout": 300,
                        "max_message_history": 10000
                    },
                    "fsm": {
                        "task_timeout": 3600,
                        "max_concurrent_tasks": 100,
                        "coordination_interval": 60
                    },
                    "bridge": {
                        "event_processing_interval": 0.1,
                        "coordination_check_interval": 60,
                        "cleanup_interval": 3600
                    }
                }
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('logs/fsm_communication_integration.log')
            ]
        )
    
    def launch_system(self) -> bool:
        """Launch the integrated FSM-Communication system."""
        try:
            logger.info("🚀 Launching FSM-Communication Integration System...")
            
            # Initialize core services
            if not self._initialize_core_services():
                logger.error("Failed to initialize core services")
                return False
            
            # Initialize FSM system
            if not self._initialize_fsm_system():
                logger.error("Failed to initialize FSM system")
                return False
            
            # Initialize communication system
            if not self._initialize_communication_system():
                logger.error("Failed to initialize communication system")
                return False
            
            # Initialize integration bridge
            if not self._initialize_integration_bridge():
                logger.error("Failed to initialize integration bridge")
                return False
            
            # Start system
            if not self._start_system():
                logger.error("Failed to start system")
                return False
            
            self.system_active = True
            self.startup_time = time.time()
            
            logger.info("✅ FSM-Communication Integration System launched successfully!")
            self._print_system_status()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch system: {e}")
            return False
    
    def _initialize_core_services(self) -> bool:
        """Initialize core workspace and inbox services."""
        try:
            logger.info("Initializing core services...")
            
            # Initialize workspace manager
            self.workspace_manager = WorkspaceManager(
                base_path=self.config.get("workspace_path", "agent_workspaces")
            )
            self.services_status["workspace_manager"] = "initialized"
            
            # Initialize inbox manager
            self.inbox_manager = InboxManager(self.workspace_manager)
            self.services_status["inbox_manager"] = "initialized"
            
            logger.info("✅ Core services initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize core services: {e}")
            return False
    
    def _initialize_fsm_system(self) -> bool:
        """Initialize FSM core system."""
        try:
            logger.info("Initializing FSM system...")
            
            self.fsm_core = FSMCoreV2(
                workspace_manager=self.workspace_manager,
                inbox_manager=self.inbox_manager,
                fsm_data_path=self.config.get("fsm_data_path", "fsm_data")
            )
            self.services_status["fsm_core"] = "initialized"
            
            logger.info("✅ FSM system initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize FSM system: {e}")
            return False
    
    def _initialize_communication_system(self) -> bool:
        """Initialize agent communication protocol."""
        try:
            logger.info("Initializing communication system...")
            
            comm_config = self.config.get("communication", {})
            self.communication_protocol = AgentCommunicationProtocol(comm_config)
            self.services_status["communication_protocol"] = "initialized"
            
            logger.info("✅ Communication system initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize communication system: {e}")
            return False
    
    def _initialize_integration_bridge(self) -> bool:
        """Initialize FSM-Communication integration bridge."""
        try:
            logger.info("Initializing integration bridge...")
            
            self.fsm_bridge = FSMCommunicationBridge(
                fsm_core=self.fsm_core,
                communication_protocol=self.communication_protocol,
                inbox_manager=self.inbox_manager
            )
            self.services_status["integration_bridge"] = "initialized"
            
            logger.info("✅ Integration bridge initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize integration bridge: {e}")
            return False
    
    def _start_system(self) -> bool:
        """Start all system components."""
        try:
            logger.info("Starting system components...")
            
            # Start communication protocol
            if hasattr(self.communication_protocol, 'start'):
                self.communication_protocol.start()
                self.services_status["communication_protocol"] = "running"
            
            # Start FSM bridge
            if hasattr(self.fsm_bridge, 'bridge_active'):
                self.services_status["integration_bridge"] = "running"
            
            # Start workspace manager
            if hasattr(self.workspace_manager, 'start'):
                self.workspace_manager.start()
                self.services_status["workspace_manager"] = "running"
            
            logger.info("✅ System components started")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start system components: {e}")
            return False
    
    def create_sample_tasks(self) -> List[str]:
        """Create sample FSM tasks for testing."""
        try:
            logger.info("Creating sample FSM tasks...")
            
            sample_tasks = [
                {
                    "title": "System Integration Test",
                    "description": "Test the FSM-Communication integration bridge",
                    "assigned_agent": "Agent-1",
                    "priority": "HIGH"
                },
                {
                    "title": "Communication Protocol Validation",
                    "description": "Validate message routing and delivery",
                    "assigned_agent": "Agent-2",
                    "priority": "NORMAL"
                },
                {
                    "title": "FSM State Transition Testing",
                    "description": "Test task state transitions and coordination",
                    "assigned_agent": "Agent-3",
                    "priority": "NORMAL"
                }
            ]
            
            created_tasks = []
            for task_data in sample_tasks:
                task_id = self.fsm_core.create_task(
                    title=task_data["title"],
                    description=task_data["description"],
                    assigned_agent=task_data["assigned_agent"],
                    priority=task_data["priority"]
                )
                if task_id:
                    created_tasks.append(task_id)
                    logger.info(f"Created sample task: {task_data['title']}")
            
            logger.info(f"✅ Created {len(created_tasks)} sample tasks")
            return created_tasks
            
        except Exception as e:
            logger.error(f"Failed to create sample tasks: {e}")
            return []
    
    def run_coordination_demo(self) -> bool:
        """Run a coordination demonstration."""
        try:
            logger.info("🎭 Running FSM-Communication coordination demo...")
            
            # Create sample tasks
            task_ids = self.create_sample_tasks()
            if not task_ids:
                logger.error("No sample tasks created for demo")
                return False
            
            # Simulate task progression
            for i, task_id in enumerate(task_ids):
                logger.info(f"Demo: Progressing task {i+1}/{len(task_ids)}")
                
                # Update task state
                if i == 0:
                    # First task: NEW -> IN_PROGRESS
                    self.fsm_core.update_task_state(
                        task_id, "IN_PROGRESS", "Agent-1", 
                        "Starting system integration test"
                    )
                    time.sleep(2)
                    
                    # IN_PROGRESS -> COMPLETED
                    self.fsm_core.update_task_state(
                        task_id, "COMPLETED", "Agent-1",
                        "System integration test completed successfully",
                        {"test_results": "PASS", "coverage": "95%"}
                    )
                
                elif i == 1:
                    # Second task: NEW -> IN_PROGRESS
                    self.fsm_core.update_task_state(
                        task_id, "IN_PROGRESS", "Agent-2",
                        "Validating communication protocol"
                    )
                    time.sleep(2)
                    
                    # IN_PROGRESS -> REVIEW
                    self.fsm_core.update_task_state(
                        task_id, "REVIEW", "Agent-2",
                        "Communication protocol validation ready for review"
                    )
                
                elif i == 2:
                    # Third task: NEW -> BLOCKED
                    self.fsm_core.update_task_state(
                        task_id, "BLOCKED", "Agent-3",
                        "Task blocked - waiting for dependency"
                    )
                    time.sleep(2)
                    
                    # BLOCKED -> IN_PROGRESS
                    self.fsm_core.update_task_state(
                        task_id, "IN_PROGRESS", "Agent-3",
                        "Dependency resolved - proceeding with testing"
                    )
                
                time.sleep(1)  # Brief pause between tasks
            
            logger.info("✅ Coordination demo completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to run coordination demo: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            status = {
                "system_active": self.system_active,
                "startup_time": self.startup_time,
                "services_status": self.services_status.copy(),
                "uptime": time.time() - self.startup_time if self.startup_time else 0
            }
            
            # Add FSM status
            if self.fsm_core:
                status["fsm_status"] = self.fsm_core.get_status()
            
            # Add bridge status
            if self.fsm_bridge:
                status["bridge_status"] = self.fsm_bridge.get_bridge_status()
            
            # Add communication status
            if self.communication_protocol:
                status["communication_status"] = {
                    "registered_agents": len(self.communication_protocol.registered_agents),
                    "message_queue_size": len(self.communication_protocol.message_queue),
                    "communication_active": self.communication_protocol.communication_active
                }
            
            return status
            
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {"error": str(e)}
    
    def _print_system_status(self):
        """Print system status to console."""
        try:
            status = self.get_system_status()
            
            print("\n" + "="*60)
            print("🤖 FSM-Communication Integration System Status")
            print("="*60)
            
            print(f"System Active: {'✅ YES' if status['system_active'] else '❌ NO'}")
            print(f"Uptime: {status.get('uptime', 0):.1f} seconds")
            
            print("\n📊 Services Status:")
            for service, state in status.get('services_status', {}).items():
                status_icon = "✅" if state == "running" else "🔄" if state == "initialized" else "❌"
                print(f"  {status_icon} {service}: {state}")
            
            if 'fsm_status' in status:
                fsm = status['fsm_status']
                print(f"\n🎯 FSM Status:")
                print(f"  Total Tasks: {fsm.get('total_tasks', 0)}")
                print(f"  Active Agents: {fsm.get('active_agents', 0)}")
                
                if 'state_counts' in fsm:
                    print("  Task States:")
                    for state, count in fsm['state_counts'].items():
                        if count > 0:
                            print(f"    {state}: {count}")
            
            if 'bridge_status' in status:
                bridge = status['bridge_status']
                print(f"\n🔗 Bridge Status:")
                print(f"  State: {bridge.get('bridge_state', 'unknown')}")
                print(f"  Coordinated Agents: {bridge.get('coordinated_agents', 0)}")
                print(f"  Active Tasks: {bridge.get('active_tasks', 0)}")
                print(f"  Messages Sent: {bridge.get('metrics', {}).get('messages_sent', 0)}")
            
            print("="*60 + "\n")
            
        except Exception as e:
            logger.error(f"Failed to print system status: {e}")
    
    def shutdown_system(self) -> bool:
        """Shutdown the integrated system gracefully."""
        try:
            logger.info("🛑 Shutting down FSM-Communication Integration System...")
            
            # Shutdown bridge
            if self.fsm_bridge:
                self.fsm_bridge.shutdown()
                self.services_status["integration_bridge"] = "shutdown"
            
            # Shutdown communication protocol
            if self.communication_protocol and hasattr(self.communication_protocol, 'shutdown'):
                self.communication_protocol.shutdown()
                self.services_status["communication_protocol"] = "shutdown"
            
            # Shutdown workspace manager
            if self.workspace_manager and hasattr(self.workspace_manager, 'shutdown'):
                self.workspace_manager.shutdown()
                self.services_status["workspace_manager"] = "shutdown"
            
            self.system_active = False
            logger.info("✅ System shutdown complete")
            return True
            
        except Exception as e:
            logger.error(f"Failed to shutdown system: {e}")
            return False


def main():
    """Main CLI interface for the integration launcher."""
    parser = argparse.ArgumentParser(description="FSM-Communication Integration Launcher")
    parser.add_argument("--launch", action="store_true", help="Launch the integrated system")
    parser.add_argument("--demo", action="store_true", help="Run coordination demo")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument("--shutdown", action="store_true", help="Shutdown the system")
    parser.add_argument("--config", type=str, help="Configuration file path")
    
    args = parser.parse_args()
    
    print("🔗 FSM-Communication Integration Launcher - Agent Cellphone V2")
    
    # Initialize launcher
    config_path = args.config or "config/fsm_communication_config.json"
    launcher = FSMCommunicationIntegrationLauncher(config_path)
    
    try:
        if args.launch:
            if launcher.launch_system():
                print("✅ System launched successfully!")
                if args.demo:
                    launcher.run_coordination_demo()
            else:
                print("❌ Failed to launch system")
                return 1
        
        elif args.demo:
            if not launcher.system_active:
                print("⚠️  System not active, launching first...")
                if not launcher.launch_system():
                    print("❌ Failed to launch system")
                    return 1
            
            launcher.run_coordination_demo()
        
        elif args.status:
            launcher._print_system_status()
        
        elif args.shutdown:
            if launcher.system_active:
                launcher.shutdown_system()
                print("✅ System shutdown complete")
            else:
                print("⚠️  System not active")
        
        else:
            # Default: launch and show status
            if launcher.launch_system():
                print("✅ System launched successfully!")
                launcher._print_system_status()
                
                # Keep system running
                try:
                    print("\n🔄 System running... Press Ctrl+C to shutdown")
                    while True:
                        time.sleep(10)
                        launcher._print_system_status()
                except KeyboardInterrupt:
                    print("\n🛑 Shutdown requested...")
                    launcher.shutdown_system()
            else:
                print("❌ Failed to launch system")
                return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n🛑 Shutdown requested...")
        if launcher.system_active:
            launcher.shutdown_system()
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())

