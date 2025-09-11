#!/usr/bin/env python3
"""
Agent Restart Protocol - V2 Compliant Module
============================================

Handles agent restarts and phase transitions using the onboarding system.
Supports automatic agent detection, restart coordination, and phase transitions.

Author: Captain Agent-4 (QA & Coordination)
License: MIT
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import pyautogui as pg
except ImportError:
    pg = None

logger = logging.getLogger(__name__)


class AgentRestartProtocol:
    """Handles agent restarts and phase transitions using onboarding system."""

    def __init__(self, status_file: str = "agent_status.json"):
        """Initialize agent restart protocol."""
        self.status_file = Path(status_file)
        self.coordinate_loader = self._load_coordinate_loader()
        self.onboarding_service = self._load_onboarding_service()
        self.agent_roles = self._load_agent_roles()
        
    def _load_coordinate_loader(self):
        """Load coordinate loader for agent positioning."""
        try:
            from src.core.coordinate_loader import get_coordinate_loader
            return get_coordinate_loader()
        except Exception as e:
            logger.error(f"Failed to load coordinate loader: {e}")
            return None

    def _load_onboarding_service(self):
        """Load onboarding service for message generation."""
        try:
            from src.services.onboarding_service import OnboardingService
            return OnboardingService()
        except Exception as e:
            logger.error(f"Failed to load onboarding service: {e}")
            return None

    def _load_agent_roles(self) -> Dict[str, str]:
        """Load agent role assignments."""
        return {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist", 
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }

    def detect_agent_restart(self, agent_id: str) -> bool:
        """Detect if an agent has restarted."""
        try:
            current_status = self._get_agent_status(agent_id)
            if not current_status:
                return True  # Agent not found, likely restarted
            
            # Check if agent is in restart state
            return current_status.get("status") == "RESTARTING"
        except Exception as e:
            logger.error(f"Error detecting agent restart for {agent_id}: {e}")
            return False

    def handle_agent_restart(self, agent_id: str, phase: str = "Cycle 1") -> Dict[str, Any]:
        """Handle agent restart with phase transition onboarding."""
        logger.info(f"🔄 Handling agent restart for {agent_id} in {phase}")
        
        try:
            # Generate phase transition message
            message = self._generate_phase_transition_message(agent_id, phase)
            
            # Send onboarding message via UI automation
            success = self._send_onboarding_message(agent_id, message)
            
            # Update agent status
            self._update_agent_status(agent_id, "ACTIVE", phase)
            
            return {
                "agent_id": agent_id,
                "success": success,
                "phase": phase,
                "message_sent": success,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error handling agent restart for {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _generate_phase_transition_message(self, agent_id: str, phase: str) -> str:
        """Generate phase transition onboarding message."""
        role = self.agent_roles.get(agent_id, "Specialist")
        
        if phase == "Cycle 1":
            phase_context = """
🎯 **CYCLE 1 FOUNDATION AUDIT - DEPENDENCY ANALYSIS PHASE**

**Current Phase Status:**
- Foundation backup complete (218 files secured)
- Dependency analysis in progress
- Consolidation opportunities identified (60%+ reduction)
- Cross-agent coordination protocols active

**Your Role in Cycle 1:**
- Execute dependency analysis tasks
- Coordinate with other agents for consolidation planning
- Maintain V2 compliance standards
- Support foundation audit completion
"""
        elif phase == "Phase 2":
            phase_context = """
🚀 **PHASE 2 CONSOLIDATION EXECUTION - ACTIVE CONSOLIDATION**

**Current Phase Status:**
- Dependency analysis complete
- Consolidation strategy finalized
- Phase 2 execution protocols activated
- Real-time consolidation coordination active

**Your Role in Phase 2:**
- Execute consolidation tasks according to assigned chunks
- Coordinate with swarm agents for parallel execution
- Maintain quality standards throughout consolidation
- Report progress and resolve blocking issues
"""
        else:
            phase_context = f"""
📋 **PHASE TRANSITION - {phase.upper()}**

**Current Phase Status:**
- Phase transition in progress
- Agent restart protocol activated
- Cross-agent coordination maintained
- System synchronization active

**Your Role in {phase}:**
- Execute assigned phase-specific tasks
- Maintain communication with swarm
- Follow established protocols and standards
- Contribute to phase objectives
"""

        return f"""
🤖 **AGENT RESTART PROTOCOL - PHASE TRANSITION ONBOARDING**

**Agent Identity:** {agent_id} - {role}
**Phase:** {phase}
**Restart Time:** {datetime.now().isoformat()}
**Status:** ACTIVE - READY FOR ASSIGNMENT

{phase_context}

**Core Responsibilities:**
- Execute assigned tasks efficiently
- Maintain communication with the swarm
- Follow V2 compliance standards
- Contribute to phase objectives

**Essential Commands:**
- Check agent status and current assignments
- Coordinate with other agents as needed
- Report progress and resolve issues
- Maintain system synchronization

**Mission Success Criteria:**
- Complete assigned tasks on time
- Maintain accurate status reporting
- Collaborate effectively with team members
- Follow operational protocols precisely

🐝 **WE ARE SWARM - WELCOME BACK TO THE COLLABORATIVE TEAM!**

Best regards,
Captain Agent-4 (QA & Coordination)
"""

    def _send_onboarding_message(self, agent_id: str, message: str) -> bool:
        """Send onboarding message via UI automation."""
        if not pg or not self.coordinate_loader:
            logger.warning("PyAutoGUI or coordinate loader not available - skipping UI automation")
            return False
            
        try:
            # Get agent coordinates
            chat_coords = self.coordinate_loader.get_chat_coordinates(agent_id)
            
            # Focus agent window
            self._focus_agent_window(agent_id)
            
            # Click on chat input
            pg.click(chat_coords[0], chat_coords[1])
            time.sleep(0.1)
            
            # Copy message to clipboard and paste
            import pyperclip
            pyperclip.copy(message)
            pg.hotkey("ctrl", "a")  # Select all existing text
            pg.hotkey("ctrl", "v")  # Paste new message
            time.sleep(0.1)
            
            logger.info(f"✅ Onboarding message sent to {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send onboarding message to {agent_id}: {e}")
            return False

    def _focus_agent_window(self, agent_id: str):
        """Focus the agent window."""
        try:
            import pygetwindow as gw
            windows = gw.getWindowsWithTitle(agent_id)
            if windows:
                windows[0].activate()
            else:
                pg.hotkey("alt", "tab")
        except Exception:
            pg.hotkey("alt", "tab")
        time.sleep(0.1)

    def _get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current agent status."""
        try:
            if self.status_file.exists():
                data = json.loads(self.status_file.read_text(encoding="utf-8"))
                return data.get("agents", {}).get(agent_id)
        except Exception as e:
            logger.error(f"Error reading agent status: {e}")
        return None

    def _update_agent_status(self, agent_id: str, status: str, phase: str):
        """Update agent status."""
        try:
            data = {}
            if self.status_file.exists():
                data = json.loads(self.status_file.read_text(encoding="utf-8"))
            
            if "agents" not in data:
                data["agents"] = {}
            
            data["agents"][agent_id] = {
                "status": status,
                "phase": phase,
                "last_updated": datetime.now().isoformat(),
                "restart_count": data["agents"].get(agent_id, {}).get("restart_count", 0) + 1
            }
            
            self.status_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            
        except Exception as e:
            logger.error(f"Error updating agent status: {e}")

    def get_restart_summary(self) -> Dict[str, Any]:
        """Get summary of agent restart activity."""
        try:
            if not self.status_file.exists():
                return {"total_agents": 0, "active_agents": 0, "restart_activity": []}
            
            data = json.loads(self.status_file.read_text(encoding="utf-8"))
            agents = data.get("agents", {})
            
            active_count = sum(1 for agent in agents.values() if agent.get("status") == "ACTIVE")
            restart_activity = [
                {
                    "agent_id": agent_id,
                    "status": agent_data.get("status"),
                    "phase": agent_data.get("phase"),
                    "restart_count": agent_data.get("restart_count", 0),
                    "last_updated": agent_data.get("last_updated")
                }
                for agent_id, agent_data in agents.items()
            ]
            
            return {
                "total_agents": len(agents),
                "active_agents": active_count,
                "restart_activity": restart_activity,
                "last_updated": data.get("last_updated", datetime.now().isoformat())
            }
            
        except Exception as e:
            logger.error(f"Error getting restart summary: {e}")
            return {"error": str(e)}


def main():
    """Main function for testing agent restart protocol."""
    protocol = AgentRestartProtocol()
    
    # Test agent restart detection and handling
    for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
        if protocol.detect_agent_restart(agent_id):
            result = protocol.handle_agent_restart(agent_id, "Cycle 1")
            print(f"Agent restart handled: {result}")
    
    # Get restart summary
    summary = protocol.get_restart_summary()
    print(f"Restart summary: {summary}")


if __name__ == "__main__":
    main()
