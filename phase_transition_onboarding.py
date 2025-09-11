#!/usr/bin/env python3
"""
Phase Transition Onboarding System - V2 Compliant Module
=======================================================

Handles phase transitions and agent onboarding for new phases.
Supports Cycle 1 → Phase 2 transitions and consolidation phase preparation.

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


class PhaseTransitionOnboarding:
    """Handles phase transitions and agent onboarding for new phases."""

    def __init__(self, status_file: str = "phase_status.json"):
        """Initialize phase transition onboarding system."""
        self.status_file = Path(status_file)
        self.coordinate_loader = self._load_coordinate_loader()
        self.agent_roles = self._load_agent_roles()
        self.phase_configs = self._load_phase_configs()
        
    def _load_coordinate_loader(self):
        """Load coordinate loader for agent positioning."""
        try:
            from src.core.coordinate_loader import get_coordinate_loader
            return get_coordinate_loader()
        except Exception as e:
            logger.error(f"Failed to load coordinate loader: {e}")
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

    def _load_phase_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load phase-specific configurations."""
        return {
            "Cycle 1": {
                "name": "Foundation Audit",
                "description": "Dependency analysis and consolidation planning",
                "targets": ["Dependency mapping", "Risk assessment", "Strategy finalization"],
                "agent_assignments": {
                    "Agent-3": "Dependency analysis leadership",
                    "Agent-4": "Safety validation and QA",
                    "Agent-7": "JavaScript consolidation analysis",
                    "Agent-1": "Integration point mapping",
                    "Agent-2": "Core module consolidation strategy"
                }
            },
            "Phase 2": {
                "name": "Consolidation Execution",
                "description": "Active consolidation of identified opportunities",
                "targets": ["Core modules", "Services", "Web interface", "Utilities"],
                "agent_assignments": {
                    "Agent-2": "Chunk 001 (Core) - 50→15 files (70% reduction)",
                    "Agent-1": "Chunk 002 (Services) - 50→20 files (60% reduction)",
                    "Agent-3": "Chunk 004-005 (Utils/Infrastructure) - 31→13 files (58% reduction)",
                    "Agent-7": "Chunk 003 (Web) - 50→30 files (40% reduction)",
                    "Agent-4": "Chunk 006-007 (Domain) - 40→20 files (50% reduction)"
                }
            }
        }

    def initiate_phase_transition(self, from_phase: str, to_phase: str) -> Dict[str, Any]:
        """Initiate phase transition for all agents."""
        logger.info(f"🚀 Initiating phase transition: {from_phase} → {to_phase}")
        
        try:
            # Validate phase transition
            if to_phase not in self.phase_configs:
                raise ValueError(f"Unknown phase: {to_phase}")
            
            # Get all agents
            agents = self._get_all_agents()
            if not agents:
                raise ValueError("No agents found for phase transition")
            
            # Prepare phase transition
            transition_data = {
                "from_phase": from_phase,
                "to_phase": to_phase,
                "timestamp": datetime.now().isoformat(),
                "agents": agents,
                "phase_config": self.phase_configs[to_phase]
            }
            
            # Send phase transition messages to all agents
            results = []
            for agent_id in agents:
                result = self._send_phase_transition_message(agent_id, to_phase)
                results.append(result)
            
            # Update phase status
            self._update_phase_status(to_phase, transition_data)
            
            # Generate transition summary
            summary = self._generate_transition_summary(transition_data, results)
            
            return {
                "success": True,
                "from_phase": from_phase,
                "to_phase": to_phase,
                "agents_processed": len(agents),
                "successful_transitions": sum(1 for r in results if r.get("success", False)),
                "results": results,
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error initiating phase transition: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _send_phase_transition_message(self, agent_id: str, phase: str) -> Dict[str, Any]:
        """Send phase transition message to specific agent."""
        try:
            role = self.agent_roles.get(agent_id, "Specialist")
            phase_config = self.phase_configs.get(phase, {})
            agent_assignment = phase_config.get("agent_assignments", {}).get(agent_id, "General support")
            
            message = self._generate_phase_transition_message(agent_id, role, phase, phase_config, agent_assignment)
            
            # Send via UI automation
            success = self._send_ui_message(agent_id, message)
            
            return {
                "agent_id": agent_id,
                "success": success,
                "phase": phase,
                "assignment": agent_assignment,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error sending phase transition message to {agent_id}: {e}")
            return {
                "agent_id": agent_id,
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _generate_phase_transition_message(self, agent_id: str, role: str, phase: str, 
                                         phase_config: Dict[str, Any], assignment: str) -> str:
        """Generate phase transition message."""
        phase_name = phase_config.get("name", phase)
        description = phase_config.get("description", "")
        targets = phase_config.get("targets", [])
        
        return f"""
🎯 **PHASE TRANSITION ONBOARDING - {phase_name.upper()}**

**Agent Identity:** {agent_id} - {role}
**Phase:** {phase_name}
**Transition Time:** {datetime.now().isoformat()}
**Status:** ACTIVE - READY FOR {phase_name.upper()} ASSIGNMENT

**Phase Description:**
{description}

**Phase Targets:**
{chr(10).join(f"• {target}" for target in targets)}

**Your Specific Assignment:**
{assignment}

**Core Responsibilities:**
- Execute assigned tasks efficiently
- Maintain communication with the swarm
- Follow V2 compliance standards
- Contribute to phase objectives

**Phase-Specific Protocols:**
- Coordinate with assigned agents for parallel execution
- Report progress and resolve blocking issues
- Maintain quality standards throughout execution
- Follow established consolidation procedures

**Essential Commands:**
- Check current phase status and assignments
- Coordinate with other agents as needed
- Report progress and resolve issues
- Maintain system synchronization

**Mission Success Criteria:**
- Complete assigned tasks on time
- Maintain accurate status reporting
- Collaborate effectively with team members
- Follow operational protocols precisely

🐝 **WE ARE SWARM - WELCOME TO {phase_name.upper()} PHASE!**

Best regards,
Captain Agent-4 (QA & Coordination)
"""

    def _send_ui_message(self, agent_id: str, message: str) -> bool:
        """Send message via UI automation using copy/paste."""
        if not pg or not self.coordinate_loader:
            logger.warning("PyAutoGUI or coordinate loader not available - skipping UI automation")
            return False
            
        try:
            import pyperclip
            
            # Get agent coordinates
            chat_coords = self.coordinate_loader.get_chat_coordinates(agent_id)
            
            # Focus agent window
            self._focus_agent_window(agent_id)
            
            # Click on chat input
            pg.click(chat_coords[0], chat_coords[1])
            time.sleep(0.1)
            
            # Copy message to clipboard
            pyperclip.copy(message)
            
            # Paste message
            pg.hotkey("ctrl", "a")  # Select all existing text
            pg.hotkey("ctrl", "v")  # Paste new message
            time.sleep(0.1)
            
            logger.info(f"✅ Phase transition message sent to {agent_id} via copy/paste")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send phase transition message to {agent_id}: {e}")
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

    def _get_all_agents(self) -> List[str]:
        """Get all available agents."""
        if self.coordinate_loader:
            return self.coordinate_loader.get_all_agents()
        return list(self.agent_roles.keys())

    def _update_phase_status(self, phase: str, transition_data: Dict[str, Any]):
        """Update phase status."""
        try:
            data = {
                "current_phase": phase,
                "last_transition": transition_data,
                "timestamp": datetime.now().isoformat()
            }
            
            self.status_file.write_text(json.dumps(data, indent=2), encoding="utf-8")
            
        except Exception as e:
            logger.error(f"Error updating phase status: {e}")

    def _generate_transition_summary(self, transition_data: Dict[str, Any], results: List[Dict[str, Any]]) -> str:
        """Generate phase transition summary."""
        successful = sum(1 for r in results if r.get("success", False))
        total = len(results)
        
        return f"""
📊 **PHASE TRANSITION SUMMARY**

**Transition:** {transition_data['from_phase']} → {transition_data['to_phase']}
**Agents Processed:** {total}
**Successful Transitions:** {successful}
**Success Rate:** {(successful/total)*100:.1f}%

**Phase Configuration:**
- Name: {transition_data['phase_config']['name']}
- Description: {transition_data['phase_config']['description']}
- Targets: {', '.join(transition_data['phase_config']['targets'])}

**Agent Assignments:**
{chr(10).join(f"- {agent}: {assignment}" for agent, assignment in transition_data['phase_config']['agent_assignments'].items())}

**Status:** {'✅ SUCCESSFUL' if successful == total else '⚠️ PARTIAL SUCCESS'}
"""

    def get_current_phase_status(self) -> Dict[str, Any]:
        """Get current phase status."""
        try:
            if not self.status_file.exists():
                return {"current_phase": "Unknown", "status": "No phase data"}
            
            data = json.loads(self.status_file.read_text(encoding="utf-8"))
            return data
            
        except Exception as e:
            logger.error(f"Error getting phase status: {e}")
            return {"error": str(e)}


def main():
    """Main function for testing phase transition onboarding."""
    onboarding = PhaseTransitionOnboarding()
    
    # Test phase transition
    result = onboarding.initiate_phase_transition("Cycle 1", "Phase 2")
    print(f"Phase transition result: {result}")
    
    # Get current status
    status = onboarding.get_current_phase_status()
    print(f"Current phase status: {status}")
    
    return 0 if result.get('success', False) else 1


if __name__ == "__main__":
    import sys
    exit_code = main()
    print()
    print("⚡ WE. ARE. SWARM. ⚡️🔥")
    sys.exit(exit_code)
