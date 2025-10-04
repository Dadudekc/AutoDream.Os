#!/usr/bin/env python3
"""
Agent Hard Onboarding Module - Direct Activation Protocol
=========================================================

Handles direct agent activation via PyAutoGUI coordinate clicking.
Modular V2-compliant integration of hard onboarding functionality.

V2 Compliance: ≤400 lines, focused on hard onboarding functionality
Author: Agent-4 (Captain)
"""

import json
import logging
import time
import threading
from typing import Dict, List, Optional, Set
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    pyautogui = None
    pyperclip = None
    PYAUTOGUI_AVAILABLE = False


class AgentHardOnboarder:
    """Handle direct agent activation operations."""
    
    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize hard onboarder."""
        self.coord_path = Path(coord_path)
        self.recently_onboarded: Set[str] = set()
        self._onboarding_lock = threading.Lock()
    
    def get_agent_default_role(self, agent_id: str) -> str:
        """Get agent's default role from capabilities."""
        try:
            # Default role mapping based on agent ID
            default_roles = {
                "Agent-1": "INTEGRATION_SPECIALIST",
                "Agent-2": "ARCHITECTURE_SPECIALIST", 
                "Agent-3": "WEB_DEVELOPER",
                "Agent-4": "CAPTAIN",
                "Agent-5": "COORDINATOR",
                "Agent-6": "QUALITY_ASSURANCE",
                "Agent-7": "IMPLEMENTATION_SPECIALIST",
                "Agent-8": "INTEGRATION_SPECIALIST"
            }
            
            return default_roles.get(agent_id, "TASK_EXECUTOR")
        except Exception as e:
            logger.warning(f"Could not determine default role for {agent_id}: {e}")
            return "TASK_EXECUTOR"
    
    def create_onboarding_message(self, agent_id: str, default_role: str) -> str:
        """Create comprehensive hard onboarding message."""
        return f"""🔔 HARD ONBOARD SEQUENCE INITIATED
═══════════════════════════════════════════════════════════════════════════════
🤖 AGENT: {agent_id}
🎭 DEFAULT ROLE: {default_role}
📋 STATUS: ACTIVATING VIA COORDINATE-BASED WORKFLOW
⠀⠀⠀⠀⠀⠀═══════════════════════════════════════════════════════════════

📖 IMMEDIATE ACTIONS REQUIRED:
1. Review AGENTS.md for complete system overview
2. Understand your role: {default_role}
3. Initialize agent workspace and inbox
4. Load role-specific protocols from config/protocols/
5. Discover and integrate available tools
6. Begin autonomous workflow cycle

🎯 COORDINATION PROTOCOL:
- Monitor inbox for role assignments from Captain Agent-4
- Execute General Cycle: CHECK_INBOX → EVALUATE_TASKS → EXECUTE_ROLE → QUALITY_GATES → CYCLE_DONE
- Maintain V2 compliance standards (≤400 lines, proper structure)
- Use PyAutoGUI messaging for agent coordination

📊 AVAILABLE ROLES (25 total):
Core: CAPTAIN, SSOT_MANAGER, COORDINATOR
Technical: INTEGRATION_SPECIALIST, ARCHITECTURE_SPECIALIST, INFRASTRUCTURE_SPECIALIST, WEB_DEVELOPER, DATA_ANALYST, QUALITY_ASSURANCE, PERFORMANCE_DETECTIVE, SECURITY_INSPECTOR, INTEGRATION_EXPLORER, FINANCIAL_ANALYST, TRADING_STRATEGIST, RISK_MANAGER, PORTFOLIO_OPTIMIZER, COMPLIANCE_AUDITOR
Operational: TASK_EXECUTOR, RESEARCHER, TROUBLESHOOTER, OPTIMIZER, DEVLOG_STORYTELLER, CODE_ARCHAEOLOGIST, DOCUMENTATION_ARCHITECT, MARKET_RESEARCHER

🛠️ TOOL DISCOVERY PROTOCOL:
1. Core Communication: messaging_system.py [UNIFIED MESSAGING]
2. Captain Tools: tools/captain_cli.py, tools/captain_directive_manager.py
3. Analysis Tools: tools/analysis_cli.py, tools/overengineering_detector.py
4. Workflow Tools: tools/agent_workflow_manager.py, tools/simple_workflow_automation.py
5. Static Analysis: tools/static_analysis/ (code_quality_analyzer.py, dependency_scanner.py, security_scanner.py)
6. Protocol Tools: tools/protocol_compliance_checker.py, tools/protocol_governance_system.py
7. DevOps Tools: scripts/deployment_dashboard.py, tools/performance_detective_cli.py
8. Specialized Tools: tools/financial_analyst_cli.py, tools/trading_strategist_cli.py, tools/risk_manager_cli.py
9. Agent Passdown: src/services/agent_passdown.py (soft onboarding)
10. Alerting Tools: tools/intelligent_alerting_cli.py, tools/predictive_analytics_cli.py

🔧 TOOL INTEGRATION IN GENERAL CYCLE:
- PHASE 1 (CHECK_INBOX): Use messaging tools, check tool status
- PHASE 2 (EVALUATE_TASKS): Use analysis tools, workflow tools
- PHASE 3 (EXECUTE_ROLE): Use role-specific tools, specialized tools
- PHASE 4 (QUALITY_GATES): Use quality tools, static analysis tools
- PHASE 5 (CYCLE_DONE): Use reporting tools, update tool status

📚 REQUIRED READING FOR TOOL DISCOVERY:
- AGENTS.md (complete tool integration in General Cycle)
- tools/ directory (all available CLI tools)
- src/services/ directory (all available services)
- config/protocols/ (role-specific tool protocols)

🎮 AUTONOMOUS DEVELOPMENT MACHINE INTEGRATION:
- Discord Infrastructure: Agent channels, SSOT routing, devlog posting
- Project Scanner: Analysis capabilities, task creation, cursor database
- FSM States: Agent coordination, state transitions, error recovery
- Dynamic Roles: Captain-assigned roles and task distribution

🚀 BEGIN ONBOARDING PROTOCOLS
============================================================
🐝 WE ARE SWARM - {agent_id} Activation Complete"""
    
    def hard_onboard_agent(self, agent_id: str) -> bool:
        """Hard onboard specific agent with PyAutoGUI messaging."""
        try:
            with self._onboarding_lock:
                # Check if recently onboarded to prevent duplicates
                if agent_id in self.recently_onboarded:
                    logger.warning(f"Agent {agent_id} recently onboarded, skipping duplicate")
                    return True
                
                # Load agent coordinates
                if not self.coord_path.exists():
                    logger.error(f"Coordinates file not found: {self.coord_path}")
                    return False
                
                with open(self.coord_path) as f:
                    coords = json.load(f)
                
                if agent_id not in coords["agents"]:
                    logger.error(f"Agent {agent_id} not found in coordinates")
                    return False
                
                # Get default role
                default_role = self.get_agent_default_role(agent_id)
                
                # Create onboarding message
                message = self.create_onboarding_message(agent_id, default_role)
                
                # Send via PyAutoGUI
                if not PYAUTOGUI_AVAILABLE:
                    logger.warning(f"PyAutoGUI not available, cannot hard onboard {agent_id}")
                    return False
                
                # Copy message to clipboard
                pyperclip.copy(message)
                
                # PROPER HARD ONBOARDING SEQUENCE:
                # 1st: Click chat input coordinates
                agent_coords = coords["agents"][agent_id]["chat_input_coordinates"]
                pyautogui.click(agent_coords[0], agent_coords[1])
                time.sleep(0.5)  # Brief pause for focus
                
                # 2nd: Press ctrl+shift+backspace (clear input)
                pyautogui.hotkey("ctrl", "shift", "backspace")
                time.sleep(0.3)  # Brief pause for cleanup
                
                # 3rd: Press ctrl+n (new window/tab)
                pyautogui.hotkey("ctrl", "n")
                time.sleep(1.0)  # Wait for new window to load
                
                # 4th: Navigate to onboarding input location and wait
                # Note: This assumes there's an onboarding_coordinates in the config
                onboarding_coords = coords["agents"][agent_id].get("onboarding_coordinates")
                if onboarding_coords:
                    pyautogui.click(onboarding_coords[0], onboarding_coords[1])
                else:
                    # Fallback to chat input coordinates if no onboarding coordinates
                    pyautogui.click(agent_coords[0], agent_coords[1])
                time.sleep(1.0)  # Wait moment for focus
                
                # 5th: Paste the onboarding message
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.3)  # Brief pause for paste
                pyautogui.press("enter")
                
                logger.info(f"Hard onboarded agent {agent_id} with role {default_role}")
                
                # Mark as recently onboarded
                self.recently_onboarded.add(agent_id)
                
                # Remove from recently onboarded after 5 minutes
                def remove_from_recent():
                    time.sleep(300)  # 5 minutes
                    self.recently_onboarded.discard(agent_id)
                
                threading.Thread(target=remove_from_recent, daemon=True).start()
                
                return True
                
        except Exception as e:
            logger.error(f"Error hard onboarding agent {agent_id}: {e}")
            return False
    
    def hard_onboard_all_agents(self) -> bool:
        """Hard onboard all agents."""
        try:
            if not self.coord_path.exists():
                logger.error(f"Coordinates file not found: {self.coord_path}")
                return False
                
            with open(self.coord_path) as f:
                coords = json.load(f)
            
            success_count = 0
            for agent_id in coords["agents"]:
                if self.hard_onboard_agent(agent_id):
                    success_count += 1
                    time.sleep(1)  # Brief delay between onboardings
            
            logger.info(f"Hard onboarded {success_count}/{len(coords['agents'])} agents")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error hard onboarding all agents: {e}")
            return False


def process_hard_onboard_command(target_agent_id: str = None) -> Dict[str, any]:
    """Process hard onboard command and return results."""
    try:
        onboarder = AgentHardOnboarder()
        
        if target_agent_id:
            # Single agent onboarding
            success = onboarder.hard_onboard_agent(target_agent_id)
            return {
                "target_agent": target_agent_id,
                "success": success,
                "operation": "single_agent_onboarding",
                "message": f"Hard onboard {'successful' if success else 'failed'} for {target_agent_id}"
            }
        else:
            # All agents onboarding
            success = onboarder.hard_onboard_all_agents()
            return {
                "target_agent": "ALL_AGENTS",
                "success": success,
                "operation": "all_agents_onboarding", 
                "message": f"Hard onboard all agents {'successful' if success else 'failed'}"
            }
            
    except Exception as e:
        logger.error(f"Error processing hard onboard command: {e}")
        return {
            "target_agent": target_agent_id or "ALL_AGENTS",
            "success": False,
            "operation": "hard_onboarding",
            "error": str(e)
        }
