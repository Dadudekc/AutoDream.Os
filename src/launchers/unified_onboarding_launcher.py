#!/usr/bin/env python3
"""
Unified Onboarding Launcher - Agent Cellphone V2
===============================================

Single launcher for the unified onboarding system.
Eliminates duplication by consolidating all onboarding functionality.

Follows V2 standards: 400 LOC, OOP design, SRP.
"""

import logging
import time
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.utils.stability_improvements import stability_manager, safe_import
from ..core.unified_onboarding_system import UnifiedOnboardingSystem, create_onboarding_system
from ..core.fsm import FSMSystemManager
from ..core.workspace_manager import WorkspaceManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UnifiedOnboardingLauncher:
    """
    Unified Onboarding Launcher - Single responsibility: Launch unified onboarding system.
    
    Consolidates all onboarding launcher functionality to eliminate duplication.
    """

    def __init__(self, config_path: str = None):
        """Initialize the unified onboarding launcher."""
        self.config_path = config_path or "config/agents/onboarding.json"
        self.config = self._load_config()
        
        # Core components
        self.onboarding_system: Optional[UnifiedOnboardingSystem] = None
        self.fsm_system_manager: Optional[FSMSystemManager] = None
        self.workspace_manager: Optional[WorkspaceManager] = None
        
        # Onboarding state
        self.active_agents: List[str] = []
        self.onboarding_sessions: Dict[str, str] = {}  # agent_id -> session_id
        
        logger.info("UnifiedOnboardingLauncher initialized")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file."""
        try:
            config_file = Path(self.config_path)
            if config_file.exists():
                with open(config_file, "r") as f:
                    return json.load(f)
            else:
                logger.warning(f"Config file not found: {config_file}")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration if file not found."""
        return {
            "workspace_path": "agent_workspaces",
            "fsm_data_path": "fsm_data",
            "onboarding": {
                "phase_timeout": 30,
                "validation_retries": 3,
                "default_role": "default"
            },
            "communication": {
                "protocol": "v2",
                "timeout": 60
            }
        }

    def initialize_system(self) -> bool:
        """Initialize the unified system components."""
        try:
            logger.info("Initializing unified onboarding system...")
            
            # Initialize workspace manager
            workspace_path = self.config.get("workspace_path", "agent_workspaces")
            self.workspace_manager = WorkspaceManager(workspace_path)
            logger.info("Workspace manager initialized")
            
            # Initialize FSM core
            fsm_data_path = self.config.get("fsm_data_path", "fsm_data")
            self.fsm_system_manager = FSMSystemManager()
            logger.info("FSM core initialized")
            
            # Initialize unified onboarding system
            onboarding_config = self.config.get("onboarding", {})
            self.onboarding_system = create_onboarding_system(onboarding_config)
            
            # Connect FSM core to onboarding system
            self.onboarding_system.set_fsm_core(self.fsm_core)
            logger.info("Unified onboarding system initialized")
            
            logger.info("✅ Unified onboarding system initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize unified system: {e}")
            return False

    def start_agent_onboarding(self, agent_id: str, role: str = None) -> str:
        """Start onboarding for a specific agent."""
        try:
            if not self.onboarding_system:
                logger.error("Onboarding system not initialized")
                return ""
            
            # Use default role if none specified
            if not role:
                role = self.config.get("onboarding", {}).get("default_role", "default")
            
            # Start onboarding session
            session_id = self.onboarding_system.start_onboarding(agent_id, role)
            if not session_id:
                logger.error(f"Failed to start onboarding for {agent_id}")
                return ""
            
            # Track the session
            self.onboarding_sessions[agent_id] = session_id
            if agent_id not in self.active_agents:
                self.active_agents.append(agent_id)
            
            logger.info(f"Started onboarding session {session_id} for agent {agent_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to start agent onboarding for {agent_id}: {e}")
            return ""

    def get_onboarding_status(self, agent_id: str = None) -> Dict[str, Any]:
        """Get onboarding status for specific agent or all agents."""
        try:
            if not self.onboarding_system:
                return {"error": "Onboarding system not initialized"}
            
            if agent_id:
                # Get status for specific agent
                session_id = self.onboarding_sessions.get(agent_id)
                if not session_id:
                    return {"error": f"No onboarding session found for {agent_id}"}
                
                status = self.onboarding_system.get_onboarding_status(session_id)
                return {"agent_id": agent_id, "status": status}
            else:
                # Get status for all agents
                all_status = self.onboarding_system.get_all_onboarding_status()
                return {
                    "total_sessions": len(all_status),
                    "active_agents": self.active_agents,
                    "sessions": all_status
                }
                
        except Exception as e:
            logger.error(f"Failed to get onboarding status: {e}")
            return {"error": str(e)}

    def advance_agent_phase(self, agent_id: str, new_phase: str) -> bool:
        """Advance an agent to the next onboarding phase."""
        try:
            if not self.onboarding_system:
                logger.error("Onboarding system not initialized")
                return False
            
            session_id = self.onboarding_sessions.get(agent_id)
            if not session_id:
                logger.error(f"No onboarding session found for {agent_id}")
                return False
            
            # Convert string phase to enum
            from ..core.unified_onboarding_system import OnboardingPhase
            try:
                phase_enum = OnboardingPhase(new_phase)
            except ValueError:
                logger.error(f"Invalid phase: {new_phase}")
                return False
            
            # Advance the phase
            success = self.onboarding_system.advance_phase(session_id, phase_enum)
            if success:
                logger.info(f"Advanced {agent_id} to phase {new_phase}")
            else:
                logger.error(f"Failed to advance {agent_id} to phase {new_phase}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to advance agent phase for {agent_id}: {e}")
            return False

    def complete_agent_onboarding(self, agent_id: str) -> bool:
        """Complete onboarding for a specific agent."""
        try:
            if not self.onboarding_system:
                logger.error("Onboarding system not initialized")
                return False
            
            session_id = self.onboarding_sessions.get(agent_id)
            if not session_id:
                logger.error(f"No onboarding session found for {agent_id}")
                return False
            
            # Complete the onboarding
            success = self.onboarding_system.complete_onboarding(session_id)
            if success:
                # Remove from active tracking
                if agent_id in self.active_agents:
                    self.active_agents.remove(agent_id)
                if agent_id in self.onboarding_sessions:
                    del self.onboarding_sessions[agent_id]
                
                logger.info(f"Completed onboarding for {agent_id}")
            else:
                logger.error(f"Failed to complete onboarding for {agent_id}")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to complete agent onboarding for {agent_id}: {e}")
            return False

    def cleanup_completed_sessions(self) -> None:
        """Clean up completed onboarding sessions."""
        try:
            if self.onboarding_system:
                self.onboarding_system.cleanup_completed_sessions()
                logger.info("Cleaned up completed onboarding sessions")
        except Exception as e:
            logger.error(f"Failed to cleanup completed sessions: {e}")

    def run_interactive_onboarding(self, agent_id: str, role: str = None) -> bool:
        """Run interactive onboarding for an agent."""
        try:
            logger.info(f"Starting interactive onboarding for {agent_id}")
            
            # Start onboarding
            session_id = self.start_agent_onboarding(agent_id, role)
            if not session_id:
                return False
            
            # Get initial message
            status = self.get_onboarding_status(agent_id)
            if "error" in status:
                logger.error(f"Failed to get onboarding status: {status['error']}")
                return False
            
            current_phase = status["status"]["current_phase"]
            logger.info(f"Agent {agent_id} is in phase: {current_phase}")
            
            # Interactive phase progression
            phases = [
                "system_overview",
                "role_assignment", 
                "captain_coordination",
                "capability_training",
                "integration_testing",
                "performance_validation",
                "readiness_confirmation"
            ]
            
            current_index = phases.index(current_phase) if current_phase in phases else 0
            
            for i in range(current_index, len(phases)):
                phase = phases[i]
                logger.info(f"Advancing {agent_id} to phase: {phase}")
                
                if not self.advance_agent_phase(agent_id, phase):
                    logger.error(f"Failed to advance to phase {phase}")
                    return False
                
                # Simulate phase completion (in real system, this would be agent responses)
                time.sleep(1)
            
            # Complete onboarding
            if self.complete_agent_onboarding(agent_id):
                logger.info(f"✅ Successfully completed onboarding for {agent_id}")
                return True
            else:
                logger.error(f"❌ Failed to complete onboarding for {agent_id}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to run interactive onboarding for {agent_id}: {e}")
            return False

    def get_system_summary(self) -> Dict[str, Any]:
        """Get summary of the onboarding system."""
        try:
            return {
                "system_status": "initialized" if self.onboarding_system else "not_initialized",
                "active_agents": len(self.active_agents),
                "total_sessions": len(self.onboarding_sessions),
                "fsm_connected": self.fsm_core is not None,
                "workspace_connected": self.workspace_manager is not None
            }
        except Exception as e:
            logger.error(f"Failed to get system summary: {e}")
            return {"error": str(e)}


def main():
    """Main entry point for the unified onboarding launcher."""
    parser = argparse.ArgumentParser(description="Unified Onboarding Launcher")
    parser.add_argument("--config", help="Configuration file path")
    parser.add_argument("--agent", help="Agent ID to onboard")
    parser.add_argument("--role", help="Role for the agent")
    parser.add_argument("--interactive", action="store_true", help="Run interactive onboarding")
    parser.add_argument("--status", help="Get status for specific agent")
    parser.add_argument("--summary", action="store_true", help="Get system summary")
    
    args = parser.parse_args()
    
    # Create launcher
    launcher = UnifiedOnboardingLauncher(args.config)
    
    # Initialize system
    if not launcher.initialize_system():
        logger.error("Failed to initialize system")
        return 1
    
    try:
        if args.summary:
            # Get system summary
            summary = launcher.get_system_summary()
            print(json.dumps(summary, indent=2))
            
        elif args.status:
            # Get status for specific agent
            status = launcher.get_onboarding_status(args.status)
            print(json.dumps(status, indent=2))
            
        elif args.agent:
            # Start onboarding for specific agent
            if args.interactive:
                success = launcher.run_interactive_onboarding(args.agent, args.role)
                return 0 if success else 1
            else:
                session_id = launcher.start_agent_onboarding(args.agent, args.role)
                if session_id:
                    print(f"Started onboarding session: {session_id}")
                    return 0
                else:
                    print("Failed to start onboarding")
                    return 1
        else:
            # Show help
            parser.print_help()
            
    except KeyboardInterrupt:
        logger.info("Onboarding interrupted by user")
        return 0
    except Exception as e:
        logger.error(f"Onboarding failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
