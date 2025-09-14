#!/usr/bin/env python3
"""
Integrated Onboarding & Cycle Coordination System
================================================

This system integrates:
1. Contract system for agent task commitments
2. FSM (Finite State Machine) system for state management
3. Onboarding tool for agent initialization
4. Enhanced cycle coordination with role-specific prompts

Usage:
    python integrated_onboarding_coordination_system.py --onboard-all-agents
    python integrated_onboarding_coordination_system.py --start-enhanced-cycles
    python integrated_onboarding_coordination_system.py --contract-status

Author: Agent-8 (Operations & Support Specialist)
Mission: Integrated onboarding and cycle coordination with contracts and FSM
License: MIT
"""

import argparse
import json
import logging
import sys
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# PyAutoGUI imports
try:
    import pyautogui
    import pyperclip
    PYAUTOGUI_AVAILABLE = True
    pyautogui.PAUSE = 0.05
    pyautogui.FAILSAFE = True
except ImportError as e:
    PYAUTOGUI_AVAILABLE = False
    logger.error(f"❌ PyAutoGUI not available: {e}")

class AgentState(Enum):
    """Finite State Machine states for agents."""
    UNINITIALIZED = "uninitialized"
    ONBOARDING = "onboarding"
    IDLE = "idle"
    CONTRACT_NEGOTIATION = "contract_negotiation"
    TASK_EXECUTION = "task_execution"
    COLLABORATION = "collaboration"
    PROGRESS_REPORTING = "progress_reporting"
    CYCLE_COMPLETION = "cycle_completion"
    ERROR_RECOVERY = "error_recovery"

class ContractType(Enum):
    """Types of contracts agents can enter."""
    DEDUPLICATION = "deduplication"
    V2_COMPLIANCE = "v2_compliance"
    ARCHITECTURE = "architecture"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    COORDINATION = "coordination"
    ONBOARDING = "onboarding"

class AgentContract:
    """Contract system for agent task commitments."""
    
    def __init__(self, agent_id: str, contract_type: ContractType, 
                 description: str, estimated_cycles: int, dependencies: List[str] = None):
        self.agent_id = agent_id
        self.contract_type = contract_type
        self.description = description
        self.estimated_cycles = estimated_cycles
        self.dependencies = dependencies or []
        self.status = "pending"
        self.cycle_start = None
        self.cycle_end = None
        self.progress_percentage = 0
        self.created_at = datetime.now()
        
    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "contract_type": self.contract_type.value,
            "description": self.description,
            "estimated_cycles": self.estimated_cycles,
            "dependencies": self.dependencies,
            "status": self.status,
            "progress_percentage": self.progress_percentage,
            "created_at": self.created_at.isoformat()
        }

class AgentFSM:
    """Finite State Machine for agent state management."""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = AgentState.UNINITIALIZED
        self.previous_state = None
        self.state_history = []
        self.transition_count = 0
        
    def transition_to(self, new_state: AgentState):
        """Transition to a new state."""
        if new_state != self.current_state:
            self.previous_state = self.current_state
            self.current_state = new_state
            self.state_history.append({
                "timestamp": datetime.now(),
                "from": self.previous_state.value if self.previous_state else None,
                "to": new_state.value
            })
            self.transition_count += 1
            logger.info(f"🔄 {self.agent_id} FSM: {self.previous_state.value if self.previous_state else 'None'} → {new_state.value}")
    
    def get_state_info(self):
        """Get current state information."""
        return {
            "agent_id": self.agent_id,
            "current_state": self.current_state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "transition_count": self.transition_count,
            "state_history_count": len(self.state_history)
        }

class IntegratedOnboardingCoordinationSystem:
    """Integrated system combining onboarding, contracts, FSM, and cycle coordination."""
    
    def __init__(self):
        """Initialize the integrated system."""
        self.coordinates_file = Path("cursor_agent_coords.json")
        self.agent_coordinates = self.load_coordinates()
        self.swarm_agents = [
            "Agent-1", "Agent-2", "Agent-3", "Agent-4",
            "Agent-5", "Agent-6", "Agent-7", "Agent-8"
        ]
        
        # Agent role specializations
        self.agent_roles = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist", 
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "Operations & Support Specialist"
        }
        
        # Initialize FSM for each agent
        self.agent_fsms = {agent_id: AgentFSM(agent_id) for agent_id in self.swarm_agents}
        
        # Initialize contract system
        self.active_contracts = {}
        self.contract_history = []
        
        # Onboarding status
        self.onboarding_status = {agent_id: False for agent_id in self.swarm_agents}
        
        # Load persistent state
        self.load_persistent_state()
        
        # Cycle management
        self.scheduler_active = False
        self.scheduler_thread = None
        self.cycle_count = 0
        self.start_time = None
        
    def load_persistent_state(self):
        """Load persistent state from agent status files."""
        try:
            for agent_id in self.swarm_agents:
                status_file = Path(f"agent_workspaces/{agent_id}/status.json")
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                        
                    # Update onboarding status based on actual status files
                    if (status_data.get('onboarding_status') == 'COMPLETED' or 
                        status_data.get('status') == 'onboarded' or
                        status_data.get('status') == 'OPERATIONAL'):
                        self.onboarding_status[agent_id] = True
                        
                    # Update FSM state based on actual status files
                    fsm_data = status_data.get('fsm_state', {})
                    if isinstance(fsm_data, dict):
                        fsm_state = fsm_data.get('current_state', 'uninitialized')
                    else:
                        fsm_state = fsm_data
                    if agent_id in self.agent_fsms:
                        # Convert string state to AgentState enum
                        try:
                            if isinstance(fsm_state, str):
                                # Map uppercase states to enum values
                                state_mapping = {
                                    'ONBOARDED': 'idle',  # Map onboarded to idle since mission is complete
                                    'UNINITIALIZED': 'uninitialized',
                                    'IDLE': 'idle',
                                    'TASK_EXECUTION': 'task_execution',
                                    'CYCLE_COMPLETION': 'cycle_completion',
                                    'ERROR_RECOVERY': 'error_recovery'
                                }
                                mapped_state = state_mapping.get(fsm_state, fsm_state.lower())
                                self.agent_fsms[agent_id].current_state = AgentState(mapped_state)
                            else:
                                self.agent_fsms[agent_id].current_state = fsm_state
                        except ValueError:
                            # If state doesn't match enum, keep default
                            pass
                        
            logger.info("✅ Loaded persistent state from agent status files")
        except Exception as e:
            logger.error(f"❌ Failed to load persistent state: {e}")
    
    def save_persistent_state(self):
        """Save persistent state to coordination system state file."""
        try:
            state_data = {
                'onboarding_status': self.onboarding_status,
                'contract_history': self.contract_history,
                'agent_fsm_states': {
                    agent_id: fsm.current_state for agent_id, fsm in self.agent_fsms.items()
                },
                'last_updated': datetime.now().isoformat()
            }
            
            state_file = Path("coordination_system_state.json")
            with open(state_file, 'w') as f:
                json.dump(state_data, f, indent=2)
                
            logger.info("✅ Saved persistent state to coordination system state file")
        except Exception as e:
            logger.error(f"❌ Failed to save persistent state: {e}")

    def load_coordinates(self) -> Dict[str, Dict]:
        """Load agent coordinates from JSON file."""
        if not self.coordinates_file.exists():
            logger.error(f"❌ Coordinates file not found: {self.coordinates_file}")
            return {}
            
        try:
            with open(self.coordinates_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("agents", {})
        except Exception as e:
            logger.error(f"❌ Failed to load coordinates: {e}")
            return {}
    
    def get_chat_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get chat input coordinates for a specific agent."""
        if agent_id not in self.agent_coordinates:
            logger.error(f"❌ No coordinates found for {agent_id}")
            return None
            
        coords = self.agent_coordinates[agent_id].get("chat_input_coordinates")
        if not coords or len(coords) != 2:
            logger.error(f"❌ Invalid coordinates for {agent_id}: {coords}")
            return None
            
        return tuple(coords)
    
    def get_onboarding_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get onboarding input coordinates for a specific agent."""
        if agent_id not in self.agent_coordinates:
            logger.error(f"❌ No coordinates found for {agent_id}")
            return None
            
        coords = self.agent_coordinates[agent_id].get("onboarding_input_coords")
        if not coords or len(coords) != 2:
            logger.error(f"❌ Invalid coordinates for {agent_id}: {coords}")
            return None
            
        return tuple(coords)
    
    def create_onboarding_contract(self, agent_id: str) -> AgentContract:
        """Create an onboarding contract for an agent."""
        role = self.agent_roles.get(agent_id, "Swarm Agent")
        contract = AgentContract(
            agent_id=agent_id,
            contract_type=ContractType.ONBOARDING,
            description=f"Complete onboarding process for {role}",
            estimated_cycles=1
        )
        self.active_contracts[agent_id] = contract
        logger.info(f"📋 Onboarding contract created for {agent_id}: {role}")
        return contract
    
    def create_contract(self, agent_id: str, contract_type: ContractType, 
                       description: str, estimated_cycles: int, dependencies: List[str] = None):
        """Create a new contract for an agent."""
        contract = AgentContract(agent_id, contract_type, description, estimated_cycles, dependencies)
        self.active_contracts[agent_id] = contract
        self.contract_history.append(contract)
        self.save_persistent_state()  # Save state after contract creation
        logger.info(f"📋 Contract created for {agent_id}: {contract_type.value} - {description}")
        return contract
    
    def perform_agent_onboarding(self, agent_id: str, role: str) -> bool:
        """Perform onboarding sequence for a specific agent."""
        if not PYAUTOGUI_AVAILABLE:
            logger.error("❌ PyAutoGUI not available for onboarding")
            return False
        
        # Get coordinates
        chat_coords = self.get_chat_coordinates(agent_id)
        onboarding_coords = self.get_onboarding_coordinates(agent_id)
        
        if not chat_coords or not onboarding_coords:
            logger.error(f"❌ Missing coordinates for {agent_id}")
            return False
        
        try:
            # Create onboarding contract
            self.create_onboarding_contract(agent_id)
            fsm = self.agent_fsms[agent_id]
            fsm.transition_to(AgentState.ONBOARDING)
            
            logger.info(f"🎯 Starting onboarding for {agent_id} ({role})")
            
            # Step 1: Click chat input coordinates
            pyautogui.moveTo(chat_coords[0], chat_coords[1], duration=0.4)
            pyautogui.click()
            time.sleep(0.1)
            
            # Step 2: Press Ctrl+N (new chat)
            pyautogui.hotkey('ctrl', 'n')
            time.sleep(0.2)
            
            # Step 3: Click onboarding input coordinates
            pyautogui.moveTo(onboarding_coords[0], onboarding_coords[1], duration=0.4)
            pyautogui.click()
            time.sleep(0.1)
            
            # Step 4: Create and send onboarding message
            onboarding_message = self.create_onboarding_message(agent_id, role)
            pyperclip.copy(onboarding_message)
            time.sleep(0.05)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            
            # Step 5: Press Enter to send
            pyautogui.press('enter')
            time.sleep(0.2)
            
            # Update status
            self.onboarding_status[agent_id] = True
            fsm.transition_to(AgentState.IDLE)
            self.save_persistent_state()  # Save state after onboarding
            
            logger.info(f"✅ Onboarding completed for {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Onboarding failed for {agent_id}: {e}")
            fsm.transition_to(AgentState.ERROR_RECOVERY)
            return False
    
    def create_onboarding_message(self, agent_id: str, role: str) -> str:
        """Create onboarding message for agent."""
        return f"""🚀 AGENT ONBOARDING - {agent_id.upper()}
Role: {role}

Priority: HIGH
Tags: ONBOARDING, INITIALIZATION

🎯 ONBOARDING DIRECTIVE FOR {agent_id.upper()}:

Welcome to the enhanced swarm coordination system! You are being onboarded as {role}.

📋 ONBOARDING REQUIREMENTS:
1. ✅ Confirm your agent identity and role
2. ✅ Initialize your workspace and status tracking
3. ✅ Complete SSOT compliance training
4. ✅ Establish communication with Captain Agent-4
5. ✅ Claim your first contract assignment

🛠️ IMMEDIATE ONBOARDING ACTIONS:
• Check workspace: agent_workspaces/{agent_id}/
• Update status: agent_workspaces/{agent_id}/status.json
• Message Captain: python src/services/consolidated_messaging_service.py --agent Agent-4 --message "Onboarding: {agent_id} ready for assignment"
• Get first task: python src/services/consolidated_messaging_service.py --agent {agent_id} --get-next-task

🎯 ROLE-SPECIFIC ONBOARDING:
{self._get_role_onboarding_guidance(agent_id)}

📊 CONTRACT & FSM SYSTEM:
• Contract System: Task commitments and progress tracking
• FSM System: State management and workflow coordination
• Cycle Coordination: 10-minute collaborative cycles
• Onboarding Status: Active and ready for integration

🔧 ONBOARDING COMMANDS:
• Status Check: python src/services/consolidated_messaging_service.py --check-status
• Agent Check-in: python tools/agent_checkin.py examples/agent_checkins/{agent_id}_checkin.json
• Captain Communication: python src/services/consolidated_messaging_service.py --agent Agent-4 --message "Status: Onboarding complete"

🐝 WE ARE SWARM - Enhanced onboarding with contracts and FSM active!

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory

You are {agent_id}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    def _get_role_onboarding_guidance(self, agent_id: str) -> str:
        """Get role-specific onboarding guidance."""
        guidance_map = {
            "Agent-1": """• Initialize core system integration workspace
• Review messaging systems and coordinate loading
• Prepare for V2 compliance work in core modules
• Establish integration patterns with Agent-2""",
            
            "Agent-2": """• Initialize architectural design workspace
• Review large files requiring modularization
• Prepare architectural consolidation strategies
• Establish design patterns with Agent-1""",
            
            "Agent-3": """• Initialize infrastructure and DevOps workspace
• Review deployment scripts and CI/CD pipelines
• Prepare infrastructure optimization work
• Establish quality gates with Agent-4""",
            
            "Agent-4": """• Initialize Captain coordination workspace
• Review agent status monitoring systems
• Prepare task assignment and tracking
• Establish quality oversight across all agents""",
            
            "Agent-5": """• Initialize business intelligence workspace
• Review analytics and reporting modules
• Prepare data flow optimization work
• Establish communication strategies with Agent-6""",
            
            "Agent-6": """• Initialize coordination and communication workspace
• Review messaging protocols and workflows
• Prepare inter-agent coordination systems
• Establish communication leadership""",
            
            "Agent-7": """• Initialize web development workspace
• Review UI components and frontend architecture
• Prepare web performance optimization work
• Establish deployment coordination with Agent-8""",
            
            "Agent-8": """• Initialize operations and support workspace
• Review coordination tools and operational scripts
• Prepare tool development and maintenance
• Establish operational coordination with all agents"""
        }
        
        return guidance_map.get(agent_id, "• Initialize general workspace and prepare for swarm coordination")
    
    def onboard_all_agents(self) -> Dict[str, bool]:
        """Onboard all agents with their specific roles."""
        results = {}
        logger.info("🚀 Starting comprehensive agent onboarding sequence...")
        
        for agent_id in self.swarm_agents:
            role = self.agent_roles.get(agent_id, "Swarm Agent")
            logger.info(f"📡 Onboarding {agent_id} as {role}...")
            
            success = self.perform_agent_onboarding(agent_id, role)
            results[agent_id] = success
            
            if success:
                logger.info(f"✅ {agent_id} onboarding completed successfully")
            else:
                logger.error(f"❌ Failed to onboard {agent_id}")
                
            # Small delay between agents
            time.sleep(3.0)
            
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        
        logger.info(f"📊 Onboarding complete: {successful}/{total} agents onboarded successfully")
        return results
    
    def get_agent_specific_prompt(self, agent_id: str) -> str:
        """Generate agent-specific cycle prompt based on role, state, and contracts."""
        agent_role = self.agent_roles.get(agent_id, "Swarm Agent")
        fsm = self.agent_fsms[agent_id]
        current_state = fsm.current_state
        contract = self.active_contracts.get(agent_id)
        is_onboarded = self.onboarding_status.get(agent_id, False)
        
        # Base prompt structure
        base_prompt = f"""🚀 ENHANCED CYCLE COORDINATION - {agent_id.upper()}
Role: {agent_role}
FSM State: {current_state.value.upper()}
Onboarding Status: {'✅ ONBOARDED' if is_onboarded else '❌ PENDING'}
Cycle: #{self.cycle_count + 1}

📋 CURRENT STATUS:
• State: {current_state.value}
• Onboarded: {is_onboarded}
• Transitions: {fsm.transition_count}
• Previous State: {fsm.previous_state.value if fsm.previous_state else 'None'}

"""
        
        # Add contract information if exists
        if contract:
            base_prompt += f"""📋 ACTIVE CONTRACT:
• Type: {contract.contract_type.value}
• Description: {contract.description}
• Estimated Cycles: {contract.estimated_cycles}
• Progress: {contract.progress_percentage}%
• Dependencies: {', '.join(contract.dependencies) if contract.dependencies else 'None'}

"""
        
        # Add onboarding-specific instructions if not onboarded
        if not is_onboarded:
            base_prompt += f"""🚨 ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize workspace and status tracking
• Establish communication with Captain
• Claim first contract assignment

"""
        
        # Agent-specific instructions based on role and state
        if agent_id == "Agent-1":  # Integration & Core Systems Specialist
            base_prompt += self._get_agent1_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-2":  # Architecture & Design Specialist
            base_prompt += self._get_agent2_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-3":  # Infrastructure & DevOps Specialist
            base_prompt += self._get_agent3_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-4":  # Captain
            base_prompt += self._get_agent4_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-5":  # Business Intelligence Specialist
            base_prompt += self._get_agent5_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-6":  # Coordination & Communication Specialist
            base_prompt += self._get_agent6_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-7":  # Web Development Specialist
            base_prompt += self._get_agent7_instructions(current_state, contract, is_onboarded)
        elif agent_id == "Agent-8":  # Operations & Support Specialist
            base_prompt += self._get_agent8_instructions(current_state, contract, is_onboarded)
        
        # Add common tools and coordination
        base_prompt += f"""
🛠️ INTEGRATED SYSTEM TOOLS:
• Onboarding Status: Check agent initialization
• Contract System: Task commitments and progress tracking
• FSM Transitions: State management and workflow coordination
• Cycle Coordination: 10-minute collaborative cycles
• Messaging System: Inter-agent communication

🔧 COORDINATION COMMANDS:
• Message Captain: python src/services/consolidated_messaging_service.py --agent Agent-4 --message "Status: [status]"
• Update FSM: Report state transitions to coordination system
• Broadcast Progress: python src/services/consolidated_messaging_service.py --broadcast --message "Progress: [update]"
• Check Status: python src/services/consolidated_messaging_service.py --check-status

🐝 WE ARE SWARM - Integrated onboarding, contracts, and FSM coordination active!

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory

You are {agent_id}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        return base_prompt.strip()
    
    def _get_agent1_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-1 specific instructions."""
        if not is_onboarded:
            return """🎯 INTEGRATION SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize core system integration workspace
• Review messaging systems and coordinate loading
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-1/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-1 ready for assignment"
4. Complete SSOT compliance training
"""
        elif state == AgentState.IDLE:
            return """🎯 INTEGRATION SPECIALIST - IDLE STATE:
• Analyze core system integration opportunities
• Review messaging systems for consolidation
• Identify V2 compliance violations in core modules
• Prepare contract for integration work

📋 IMMEDIATE ACTIONS:
1. Scan core systems: python tools/run_project_scan.py --focus core
2. Identify integration patterns
3. Create contract for integration work
4. Coordinate with Agent-2 on architecture decisions
"""
        else:
            return """🎯 INTEGRATION SPECIALIST - GENERAL:
• Focus on core system integration and service consolidation
• Analyze messaging systems, coordinate loading, and unified configs
• Prioritize V2 compliance in core modules and shared utilities
• Coordinate with Agent-2 on architecture decisions
"""
    
    def _get_agent2_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-2 specific instructions."""
        if not is_onboarded:
            return """🎯 ARCHITECTURE SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize architectural design workspace
• Review large files requiring modularization
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-2/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-2 ready for assignment"
4. Complete SSOT compliance training
"""
        elif state == AgentState.IDLE:
            return """🎯 ARCHITECTURE SPECIALIST - IDLE STATE:
• Review architectural patterns and large file violations
• Analyze modularization opportunities
• Design consolidation strategies
• Prepare contract for architecture work

📋 IMMEDIATE ACTIONS:
1. Scan for large files: python tools/run_project_scan.py --focus large-files
2. Analyze architectural patterns
3. Create modularization strategy
4. Coordinate with Agent-1 on integration patterns
"""
        else:
            return """🎯 ARCHITECTURE SPECIALIST - GENERAL:
• Lead architectural design and system consolidation
• Review and optimize large files requiring modularization
• Coordinate with Agent-1 on integration patterns
• Ensure architectural consistency across the project
"""
    
    def _get_agent3_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-3 specific instructions."""
        if not is_onboarded:
            return """🎯 DEVOPS SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize infrastructure and DevOps workspace
• Review deployment scripts and CI/CD pipelines
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-3/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-3 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 DEVOPS SPECIALIST - GENERAL:
• Focus on infrastructure, deployment, and DevOps automation
• Review deployment scripts, container configs, and CI/CD pipelines
• Optimize build processes and environment configurations
• Coordinate with Agent-4 on quality gates
"""
    
    def _get_agent4_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-4 (Captain) specific instructions."""
        if not is_onboarded:
            return """🎯 CAPTAIN - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize Captain coordination workspace
• Review agent status monitoring systems
• Establish quality oversight across all agents

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-4/
2. Update status file with Captain role information
3. Review agent status monitoring systems
4. Complete SSOT compliance training
"""
        elif state == AgentState.IDLE:
            return """🎯 CAPTAIN - IDLE STATE:
• Monitor overall project quality and progress
• Review contract proposals from other agents
• Assign tasks and track completion
• Make strategic decisions about project direction

📋 IMMEDIATE ACTIONS:
1. Review agent contract proposals
2. Monitor V2 compliance across all agents
3. Assign new tasks based on project priorities
4. Coordinate strategic project decisions
"""
        else:
            return """🎯 CAPTAIN - GENERAL:
• CAPTAIN: Coordinate overall project quality and progress
• Monitor V2 compliance across all agents
• Assign tasks and track completion
• Make strategic decisions about project direction
"""
    
    def _get_agent5_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-5 specific instructions."""
        if not is_onboarded:
            return """🎯 BUSINESS INTELLIGENCE SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize business intelligence workspace
• Review analytics and reporting modules
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-5/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-5 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 BUSINESS INTELLIGENCE SPECIALIST - GENERAL:
• Focus on business intelligence and data analysis
• Review analytics, reporting, and data processing modules
• Optimize data flows and business logic
• Coordinate with Agent-6 on communication strategies
"""
    
    def _get_agent6_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-6 specific instructions."""
        if not is_onboarded:
            return """🎯 COORDINATION SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize coordination and communication workspace
• Review messaging protocols and workflows
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-6/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-6 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 COORDINATION SPECIALIST - GENERAL:
• Lead coordination and communication protocols
• Manage agent messaging and workflow coordination
• Review communication systems and protocols
• Facilitate inter-agent coordination and task distribution
"""
    
    def _get_agent7_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-7 specific instructions."""
        if not is_onboarded:
            return """🎯 WEB DEVELOPMENT SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize web development workspace
• Review UI components and frontend architecture
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-7/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-7 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 WEB DEVELOPMENT SPECIALIST - GENERAL:
• Focus on web development and frontend systems
• Review UI components, web services, and frontend architecture
• Optimize web performance and user experience
• Coordinate with Agent-8 on deployment and operations
"""
    
    def _get_agent8_instructions(self, state: AgentState, contract: Optional[AgentContract], is_onboarded: bool) -> str:
        """Agent-8 specific instructions."""
        if not is_onboarded:
            return """🎯 OPERATIONS SPECIALIST - ONBOARDING REQUIRED:
• Complete onboarding process first
• Initialize operations and support workspace
• Review coordination tools and operational scripts
• Establish communication with Captain Agent-4

📋 ONBOARDING ACTIONS:
1. Initialize workspace: agent_workspaces/Agent-8/
2. Update status file with role information
3. Message Captain: "Onboarding: Agent-8 ready for assignment"
4. Complete SSOT compliance training
"""
        else:
            return """🎯 OPERATIONS SPECIALIST - GENERAL:
• Focus on operations, support, and tool development
• Develop and maintain coordination tools
• Review operational scripts and support systems
• Coordinate with all agents on tool usage and workflows
"""
    
    def send_enhanced_cycle_message(self, agent_id: str) -> bool:
        """Send enhanced cycle message to specific agent."""
        if not PYAUTOGUI_AVAILABLE:
            logger.error("❌ PyAutoGUI not available for cycle coordination")
            return False
            
        coords = self.get_chat_coordinates(agent_id)
        if not coords:
            return False
            
        x, y = coords
        logger.info(f"🎯 Sending enhanced cycle message to {agent_id} at coordinates ({x}, {y})")
        
        try:
            # Generate agent-specific prompt
            cycle_message = self.get_agent_specific_prompt(agent_id)
            
            # Move to chat input area and click
            pyautogui.moveTo(x, y, duration=0.4)
            pyautogui.click()
            time.sleep(0.1)
            
            # Clear any existing content
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.05)
            pyautogui.press('backspace')
            time.sleep(0.05)
            
            # Copy cycle message to clipboard and paste
            pyperclip.copy(cycle_message)
            time.sleep(0.05)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(0.1)
            
            # Send message using Ctrl+Enter
            pyautogui.hotkey('ctrl', 'enter')
            time.sleep(0.2)
            
            logger.info(f"✅ Enhanced cycle message sent to {agent_id} via Ctrl+Enter")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send enhanced cycle message to {agent_id}: {e}")
            return False
    
    def run_enhanced_cycle(self) -> Dict[str, bool]:
        """Run enhanced cycle with contracts and FSM."""
        results = {}
        cycle_start = datetime.now()
        logger.info(f"🔄 Starting enhanced cycle #{self.cycle_count + 1} at {cycle_start.strftime('%H:%M:%S')}")
        
        for agent_id in self.swarm_agents:
            logger.info(f"📡 Sending enhanced cycle message to {agent_id}...")
            success = self.send_enhanced_cycle_message(agent_id)
            results[agent_id] = success
            
            if success:
                logger.info(f"✅ {agent_id} enhanced cycle message sent successfully")
            else:
                logger.error(f"❌ Failed to send enhanced cycle message to {agent_id}")
                
            # Small delay between agents
            time.sleep(2.0)
            
        successful = sum(1 for success in results.values() if success)
        total = len(results)
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        
        logger.info(f"📊 Enhanced cycle #{self.cycle_count + 1} completed: {successful}/{total} agents in {cycle_duration:.1f}s")
        self.cycle_count += 1
        
        return results
    
    def run_cli(self, args: Optional[List[str]] = None) -> None:
        """Run the CLI interface."""
        parser = argparse.ArgumentParser(
            description="Integrated Onboarding & Cycle Coordination System"
        )
        parser.add_argument(
            "--onboard-all-agents", "-o",
            action="store_true",
            help="Onboard all agents with their specific roles"
        )
        parser.add_argument(
            "--start-enhanced-cycles", "-s",
            action="store_true",
            help="Start enhanced cycle coordination (every 10 minutes)"
        )
        parser.add_argument(
            "--agent", "-a",
            help="Target specific agent for cycle message or onboarding"
        )
        parser.add_argument(
            "--onboard-agent",
            help="Onboard specific agent with role"
        )
        parser.add_argument(
            "--contract-status", "-c",
            action="store_true",
            help="Show contract status for all agents"
        )
        parser.add_argument(
            "--fsm-status", "-f",
            action="store_true",
            help="Show FSM status for all agents"
        )
        parser.add_argument(
            "--onboarding-status",
            action="store_true",
            help="Show onboarding status for all agents"
        )
        parser.add_argument(
            "--create-contract",
            help="Create contract for agent (format: agent_id:type:description:cycles)"
        )
        
        if args is None:
            args = sys.argv[1:]
            
        parsed_args = parser.parse_args(args)
        
        if parsed_args.onboarding_status:
            logger.info("🚀 ONBOARDING STATUS FOR ALL AGENTS:")
            logger.info("=" * 60)
            for agent_id in self.swarm_agents:
                status = "✅ ONBOARDED" if self.onboarding_status.get(agent_id, False) else "❌ PENDING"
                role = self.agent_roles.get(agent_id, "Unknown Role")
                logger.info(f"{agent_id}: {status} - {role}")
            return
            
        if parsed_args.contract_status:
            logger.info("📋 ACTIVE CONTRACTS STATUS:")
            logger.info("=" * 50)
            if self.active_contracts:
                for agent_id, contract in self.active_contracts.items():
                    logger.info(f"{agent_id}: {contract.contract_type.value} - {contract.description}")
                    logger.info(f"  Progress: {contract.progress_percentage}% | Status: {contract.status} | Cycles: {contract.estimated_cycles}")
            else:
                logger.info("No active contracts")
                logger.info(f"Contract history count: {len(self.contract_history)}")
                if self.contract_history:
                    logger.info("Recent contracts:")
                    for contract in self.contract_history[-5:]:  # Show last 5
                        logger.info(f"  {contract.agent_id}: {contract.contract_type.value} - {contract.description}")
            return
            
        if parsed_args.fsm_status:
            logger.info("🔄 FSM STATUS FOR ALL AGENTS:")
            logger.info("=" * 50)
            for agent_id, fsm in self.agent_fsms.items():
                state_info = fsm.get_state_info()
                logger.info(f"{agent_id}: {state_info['current_state']} (transitions: {state_info['transition_count']})")
            return
            
        if parsed_args.create_contract:
            # Parse contract creation: agent_id:type:description:cycles
            try:
                parts = parsed_args.create_contract.split(':', 3)
                if len(parts) == 4:
                    agent_id, contract_type, description, cycles = parts
                    contract_type_enum = ContractType(contract_type)
                    cycles_int = int(cycles)
                    self.create_contract(agent_id, contract_type_enum, description, cycles_int)
                    logger.info(f"✅ Contract created for {agent_id}")
                else:
                    logger.error("❌ Invalid contract format. Use: agent_id:type:description:cycles")
            except Exception as e:
                logger.error(f"❌ Failed to create contract: {e}")
            return
            
        if parsed_args.onboard_agent:
            # Parse agent:role format
            try:
                if ':' in parsed_args.onboard_agent:
                    agent_id, role = parsed_args.onboard_agent.split(':', 1)
                else:
                    agent_id = parsed_args.onboard_agent
                    role = self.agent_roles.get(agent_id, "Swarm Agent")
                
                success = self.perform_agent_onboarding(agent_id, role)
                if success:
                    logger.info(f"✅ Agent {agent_id} onboarded successfully as {role}")
                else:
                    logger.error(f"❌ Failed to onboard agent {agent_id}")
            except Exception as e:
                logger.error(f"❌ Failed to onboard agent: {e}")
            return
            
        if parsed_args.agent:
            success = self.send_enhanced_cycle_message(parsed_args.agent)
            if success:
                logger.info(f"✅ Enhanced cycle message sent to {parsed_args.agent}")
            else:
                logger.error(f"❌ Failed to send enhanced cycle message to {parsed_args.agent}")
            return
            
        if parsed_args.onboard_all_agents:
            results = self.onboard_all_agents()
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            logger.info(f"📊 Onboarding complete: {successful}/{total} agents")
            return
            
        if parsed_args.start_enhanced_cycles:
            logger.info("🚀 Starting enhanced cycle coordination system...")
            logger.info("💡 Use --onboarding-status to view onboarding status")
            logger.info("💡 Use --contract-status to view contracts")
            logger.info("💡 Use --fsm-status to view FSM states")
            # For now, just run a single cycle
            results = self.run_enhanced_cycle()
            successful = sum(1 for success in results.values() if success)
            total = len(results)
            logger.info(f"📊 Enhanced cycle completed: {successful}/{total} agents")
            return
            
        # If no valid combination of arguments, show help
        parser.print_help()


def main():
    """Main entry point."""
    system = IntegratedOnboardingCoordinationSystem()
    system.run_cli()


if __name__ == "__main__":
    main()

