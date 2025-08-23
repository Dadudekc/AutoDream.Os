#!/usr/bin/env python3
"""
V2 Onboarding Launcher - Agent Cellphone V2
===========================================

Launches and manages the V2 onboarding sequence integrated with real agent communication.
Follows V2 standards: ≤300 LOC, OOP design, SRP.

Author: V2 Onboarding & Launch Specialist
License: MIT
"""

import logging
import time
import json
import argparse
from typing import Dict, Any, List, Optional
from pathlib import Path

# Import V2 components
from ..core.v2_onboarding_sequence import V2OnboardingSequence
from ..core.v2_comprehensive_messaging_system import V2ComprehensiveMessagingSystem
from ..core.fsm_core_v2 import FSMCoreV2
from ..core.workspace_manager import WorkspaceManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class V2OnboardingLauncher:
    """
    V2 Onboarding Launcher - Single responsibility: Launch and manage V2 onboarding.

    Follows V2 standards: ≤300 LOC, OOP design, SRP.
    """

    def __init__(self, config_path: str = None):
        """Initialize the V2 onboarding launcher"""
        self.config_path = config_path or "config/agents/fsm_communication.json"
        self.config = self._load_config()

        # Core components
        self.onboarding_sequence: Optional[V2OnboardingSequence] = None
        self.messaging_system: Optional[V2ComprehensiveMessagingSystem] = None
        self.fsm_core: Optional[FSMCoreV2] = None
        self.workspace_manager: Optional[WorkspaceManager] = None

        # Onboarding state
        self.active_agents: List[str] = []
        self.onboarding_sessions: Dict[str, str] = {}  # agent_id -> session_id

        logger.info("V2OnboardingLauncher initialized")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {config_file}")
                return {}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def initialize_system(self) -> bool:
        """Initialize the V2 system components"""
        try:
            logger.info("Initializing V2 system components...")

            # Initialize workspace manager
            workspace_path = self.config.get("workspace_path", "agent_workspaces")
            self.workspace_manager = WorkspaceManager(workspace_path)
            logger.info("Workspace manager initialized")

            # Initialize FSM core
            fsm_data_path = self.config.get("fsm_data_path", "fsm_data")
            self.fsm_core = FSMCoreV2(fsm_data_path)
            logger.info("FSM core initialized")

            # Initialize messaging system
            comm_config = self.config.get("communication", {})
            self.messaging_system = V2ComprehensiveMessagingSystem(comm_config)
            logger.info("V2 messaging system initialized")

            # Initialize onboarding sequence
            onboarding_config = self.config.get("onboarding", {})
            self.onboarding_sequence = V2OnboardingSequence(onboarding_config)
            logger.info("Onboarding sequence initialized")

            logger.info("✅ V2 system components initialized successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to initialize V2 system: {e}")
            return False

    def start_agent_onboarding(self, agent_id: str) -> bool:
        """Start onboarding for a specific agent"""
        try:
            if not self.onboarding_sequence:
                logger.error("Onboarding sequence not initialized")
                return False

            if agent_id in self.onboarding_sessions:
                logger.warning(
                    f"Agent {agent_id} already has an active onboarding session"
                )
                return False

            logger.info(f"Starting onboarding for {agent_id}...")

            # Start onboarding session
            session_id = self.onboarding_sequence.start_onboarding(
                agent_id=agent_id,
                communication_protocol=self.communication_protocol,
                fsm_core=self.fsm_core,
                inbox_manager=self.inbox_manager,
            )

            if session_id:
                self.onboarding_sessions[agent_id] = session_id
                self.active_agents.append(agent_id)
                logger.info(
                    f"✅ Onboarding started for {agent_id} with session {session_id}"
                )
                return True
            else:
                logger.error(f"Failed to start onboarding for {agent_id}")
                return False

        except Exception as e:
            logger.error(f"Failed to start onboarding for {agent_id}: {e}")
            return False

    def start_bulk_onboarding(self, agent_ids: List[str]) -> Dict[str, bool]:
        """Start onboarding for multiple agents"""
        try:
            logger.info(f"Starting bulk onboarding for {len(agent_ids)} agents...")

            results = {}
            for agent_id in agent_ids:
                success = self.start_agent_onboarding(agent_id)
                results[agent_id] = success

                # Brief delay between starts
                time.sleep(0.5)

            successful_count = sum(results.values())
            logger.info(
                f"✅ Bulk onboarding completed: {successful_count}/{len(agent_ids)} successful"
            )

            return results

        except Exception as e:
            logger.error(f"Bulk onboarding failed: {e}")
            return {agent_id: False for agent_id in agent_ids}

    def start_all_agents_onboarding(self) -> Dict[str, bool]:
        """Start onboarding for all V2 agents"""
        try:
            all_agents = [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ]

            logger.info("Starting onboarding for all V2 agents...")
            return self.start_bulk_onboarding(all_agents)

        except Exception as e:
            logger.error(f"Failed to start all agents onboarding: {e}")
            return {}

    def monitor_onboarding_progress(self, timeout: int = 300) -> Dict[str, Any]:
        """Monitor onboarding progress for all active sessions"""
        try:
            logger.info(f"Monitoring onboarding progress (timeout: {timeout}s)...")

            start_time = time.time()
            progress_data = {}

            while time.time() - start_time < timeout:
                # Get status for all active sessions
                for agent_id, session_id in self.onboarding_sessions.items():
                    if self.onboarding_sequence:
                        status = self.onboarding_sequence.get_onboarding_status(
                            session_id
                        )
                        if status:
                            progress_data[agent_id] = status

                # Check if all onboarding is complete
                all_completed = all(
                    status.get("status") == "completed"
                    for status in progress_data.values()
                )

                if all_completed:
                    logger.info("✅ All onboarding sessions completed!")
                    break

                # Check for failed sessions
                failed_sessions = [
                    agent_id
                    for agent_id, status in progress_data.items()
                    if status.get("status") == "failed"
                ]

                if failed_sessions:
                    logger.warning(f"Failed onboarding sessions: {failed_sessions}")

                # Wait before next check
                time.sleep(5)

            return progress_data

        except Exception as e:
            logger.error(f"Failed to monitor onboarding progress: {e}")
            return {}

    def get_onboarding_status(self, agent_id: str = None) -> Dict[str, Any]:
        """Get onboarding status for specific agent or all agents"""
        try:
            if not self.onboarding_sequence:
                return {"error": "Onboarding sequence not initialized"}

            if agent_id:
                if agent_id not in self.onboarding_sessions:
                    return {"error": f"Agent {agent_id} not found in active sessions"}

                session_id = self.onboarding_sessions[agent_id]
                return self.onboarding_sequence.get_onboarding_status(session_id) or {}
            else:
                return self.onboarding_sequence.get_all_onboarding_status()

        except Exception as e:
            logger.error(f"Failed to get onboarding status: {e}")
            return {"error": str(e)}

    def cleanup_completed_sessions(self) -> int:
        """Clean up completed onboarding sessions"""
        try:
            if not self.onboarding_sequence:
                return 0

            # Clean up in onboarding sequence
            self.onboarding_sequence.cleanup_completed_sessions()

            # Clean up local tracking
            completed_agents = []
            for agent_id, session_id in self.onboarding_sessions.items():
                status = self.onboarding_sequence.get_onboarding_status(session_id)
                if status and status.get("status") == "completed":
                    completed_agents.append(agent_id)

            for agent_id in completed_agents:
                del self.onboarding_sessions[agent_id]
                if agent_id in self.active_agents:
                    self.active_agents.remove(agent_id)

            logger.info(f"Cleaned up {len(completed_agents)} completed sessions")
            return len(completed_agents)

        except Exception as e:
            logger.error(f"Failed to cleanup completed sessions: {e}")
            return 0

    def run_demo_onboarding(self) -> bool:
        """Run a demo onboarding sequence"""
        try:
            logger.info("🚀 Running V2 Onboarding Demo...")

            # Initialize system
            if not self.initialize_system():
                logger.error("Failed to initialize system for demo")
                return False

            # Start onboarding for demo agents
            demo_agents = ["Agent-1", "Agent-2"]
            results = self.start_bulk_onboarding(demo_agents)

            if any(results.values()):
                logger.info("Demo onboarding started successfully")

                # Monitor progress
                progress = self.monitor_onboarding_progress(timeout=60)
                logger.info(f"Demo progress: {progress}")

                # Cleanup
                self.cleanup_completed_sessions()

                return True
            else:
                logger.error("Demo onboarding failed to start")
                return False

        except Exception as e:
            logger.error(f"Demo onboarding failed: {e}")
            return False

    def run_full_onboarding(self) -> bool:
        """Run full onboarding for all V2 agents"""
        try:
            logger.info("🚀 Running Full V2 Onboarding Sequence...")

            # Initialize system
            if not self.initialize_system():
                logger.error("Failed to initialize system for full onboarding")
                return False

            # Start onboarding for all agents
            results = self.start_all_agents_onboarding()

            if any(results.values()):
                logger.info("Full onboarding started successfully")

                # Monitor progress
                progress = self.monitor_onboarding_progress(timeout=600)  # 10 minutes
                logger.info(f"Full onboarding progress: {progress}")

                # Cleanup
                self.cleanup_completed_sessions()

                return True
            else:
                logger.error("Full onboarding failed to start")
                return False

        except Exception as e:
            logger.error(f"Full onboarding failed: {e}")
            return False


def main():
    """Main entry point for V2 onboarding launcher"""
    parser = argparse.ArgumentParser(description="V2 Onboarding Launcher")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--demo", action="store_true", help="Run demo onboarding")
    parser.add_argument(
        "--full", action="store_true", help="Run full onboarding for all agents"
    )
    parser.add_argument("--agent", help="Start onboarding for specific agent")
    parser.add_argument("--status", help="Get status for specific agent")
    parser.add_argument(
        "--all-status", action="store_true", help="Get status for all agents"
    )
    parser.add_argument(
        "--cleanup", action="store_true", help="Clean up completed sessions"
    )

    args = parser.parse_args()

    # Initialize launcher
    launcher = V2OnboardingLauncher(args.config)

    try:
        if args.demo:
            success = launcher.run_demo_onboarding()
            exit(0 if success else 1)

        elif args.full:
            success = launcher.run_full_onboarding()
            exit(0 if success else 1)

        elif args.agent:
            success = launcher.start_agent_onboarding(args.agent)
            exit(0 if success else 1)

        elif args.status:
            status = launcher.get_onboarding_status(args.status)
            print(json.dumps(status, indent=2))

        elif args.all_status:
            status = launcher.get_onboarding_status()
            print(json.dumps(status, indent=2))

        elif args.cleanup:
            count = launcher.cleanup_completed_sessions()
            print(f"Cleaned up {count} completed sessions")

        else:
            # Default: initialize system and show status
            if launcher.initialize_system():
                print("✅ V2 Onboarding System initialized")
                print("Use --help for available commands")
            else:
                print("❌ Failed to initialize V2 Onboarding System")
                exit(1)

    except KeyboardInterrupt:
        print("\n🛑 Onboarding interrupted by user")
        exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
