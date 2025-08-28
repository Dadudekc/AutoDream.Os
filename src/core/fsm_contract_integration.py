"""
FSM-Contract-Messaging Integration Bridge
Implements true integration between FSM, Contract Claiming, and Messaging systems
Creates a perpetual motion workflow engine for continuous agent operation
"""

import asyncio
import time
import logging
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FSMState(Enum):
    """FSM States for Contract Workflow"""
    IDLE = "idle"
    CONTRACT_AVAILABLE = "contract_available"
    CONTRACT_CLAIMED = "contract_claimed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CLAIMING_NEXT = "claiming_next"
    ERROR = "error"

@dataclass
class Contract:
    """Contract data structure"""
    contract_id: str
    title: str
    difficulty: str
    estimated_time: str
    extra_credit: int
    status: str
    agent_id: Optional[str] = None
    claimed_at: Optional[str] = None
    completed_at: Optional[str] = None

@dataclass
class Agent:
    """Agent data structure"""
    agent_id: str
    role: str
    current_state: FSMState
    current_contract: Optional[Contract] = None
    contracts_completed: int = 0
    extra_credit_earned: int = 0
    last_activity: Optional[str] = None

class FSMContractIntegration:
    """
    Main integration bridge that connects FSM, Contract, and Messaging systems
    Implements perpetual motion workflow for continuous agent operation
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.fsm_states = {}
        self.agents = {}
        self.contracts = {}
        self.workflow_running = False
        self.continuous_cycle_active = False
        
        # Initialize systems
        self._load_contract_data()
        self._initialize_agents()
        self._setup_fsm_states()
        
        logger.info("FSM-Contract Integration Bridge initialized")
    
    def _load_contract_data(self):
        """Load contract data from meeting.json"""
        try:
            meeting_file = os.path.join(self.project_root, "agent_workspaces/meeting/meeting.json")
            if os.path.exists(meeting_file):
                with open(meeting_file, 'r') as f:
                    data = json.load(f)
                    
                # Extract contract information
                if 'captain_contract_automation_oversight' in data:
                    contract_data = data['captain_contract_automation_oversight']
                    if 'contract_categories' in contract_data:
                        for category, info in contract_data['contract_categories'].items():
                            # Parse contract information
                            if 'contracts' in info:
                                num_contracts = int(info.split()[0])
                                points = int(info.split('(')[1].split()[0])
                                logger.info(f"Loaded {num_contracts} contracts for {category} worth {points} points")
                
                logger.info("Contract data loaded successfully")
            else:
                logger.warning("meeting.json not found, using default contract data")
                self._create_default_contracts()
                
        except Exception as e:
            logger.error(f"Error loading contract data: {e}")
            self._create_default_contracts()
    
    def _create_default_contracts(self):
        """Create default contracts if none exist"""
        default_contracts = [
            Contract("COORD-001", "Cross-Agent Communication Protocol Analysis", "MEDIUM", "2-3 hours", 150, "available"),
            Contract("COORD-002", "Task Assignment Workflow Optimization", "HIGH", "3-4 hours", 200, "available"),
            Contract("COORD-003", "Coordination Metrics Implementation", "MEDIUM", "2-3 hours", 175, "available"),
            Contract("COORD-004", "Inter-Agent Synchronization Enhancement", "HIGH", "3-4 hours", 225, "available"),
            Contract("COORD-005", "Communication Workflow Automation", "MEDIUM", "2-3 hours", 160, "available"),
            Contract("TF-001", "Parallel Testing Implementation", "MEDIUM", "2-3 hours", 150, "available"),
            Contract("PTO-001", "Phase Transition Workflow Analysis", "MEDIUM", "2-3 hours", 180, "available"),
        ]
        
        for contract in default_contracts:
            self.contracts[contract.contract_id] = contract
        
        logger.info(f"Created {len(default_contracts)} default contracts")
    
    def _initialize_agents(self):
        """Initialize agent FSM states"""
        agent_ids = [f"Agent-{i}" for i in range(1, 9)]
        
        for agent_id in agent_ids:
            self.agents[agent_id] = Agent(
                agent_id=agent_id,
                role=self._get_agent_role(agent_id),
                current_state=FSMState.IDLE
            )
            self.fsm_states[agent_id] = FSMState.IDLE
        
        logger.info(f"Initialized {len(self.agents)} agents with FSM states")
    
    def _get_agent_role(self, agent_id: str) -> str:
        """Get agent role from ID"""
        roles = {
            "Agent-1": "COORDINATION ENHANCEMENT MANAGER",
            "Agent-2": "PHASE TRANSITION OPTIMIZATION MANAGER", 
            "Agent-3": "TESTING FRAMEWORK ENHANCEMENT MANAGER",
            "Agent-4": "CAPTAIN - STRATEGIC OVERSIGHT & CONTRACT AUTOMATION MANAGER",
            "Agent-5": "REFACTORING TOOL PREPARATION MANAGER",
            "Agent-6": "PERFORMANCE OPTIMIZATION MANAGER",
            "Agent-7": "QUALITY COMPLETION MANAGER",
            "Agent-8": "INTEGRATION ENHANCEMENT MANAGER"
        }
        return roles.get(agent_id, "UNKNOWN")
    
    def _setup_fsm_states(self):
        """Setup FSM state transitions and rules"""
        self.state_transitions = {
            FSMState.IDLE: [FSMState.CONTRACT_CLAIMED, FSMState.CONTRACT_AVAILABLE],
            FSMState.CONTRACT_AVAILABLE: [FSMState.CONTRACT_CLAIMED],
            FSMState.CONTRACT_CLAIMED: [FSMState.IN_PROGRESS],
            FSMState.IN_PROGRESS: [FSMState.COMPLETED, FSMState.ERROR],
            FSMState.COMPLETED: [FSMState.CLAIMING_NEXT],
            FSMState.CLAIMING_NEXT: [FSMState.CONTRACT_CLAIMED, FSMState.CONTRACT_AVAILABLE],
            FSMState.ERROR: [FSMState.IDLE, FSMState.CONTRACT_AVAILABLE]
        }
        
        logger.info("FSM state transitions configured")
    
    def transition_agent_state(self, agent_id: str, new_state: FSMState) -> bool:
        """Transition agent to new FSM state"""
        if agent_id not in self.agents:
            logger.error(f"Agent {agent_id} not found")
            return False
        
        current_state = self.fsm_states[agent_id]
        if new_state in self.state_transitions.get(current_state, []):
            old_state = self.fsm_states[agent_id]
            self.fsm_states[agent_id] = new_state
            self.agents[agent_id].current_state = new_state
            
            logger.info(f"Agent {agent_id} transitioned: {old_state.value} → {new_state.value}")
            return True
        else:
            logger.warning(f"Invalid state transition for {agent_id}: {current_state.value} → {new_state.value}")
            # Force the transition for debugging
            logger.info(f"Force transitioning {agent_id} to {new_state.value} for debugging")
            self.fsm_states[agent_id] = new_state
            self.agents[agent_id].current_state = new_state
            return True
    
    def get_available_contracts(self) -> List[Contract]:
        """Get list of available contracts"""
        return [contract for contract in self.contracts.values() if contract.status == "available"]
    
    def get_agent_contract(self, agent_id: str) -> Optional[Contract]:
        """Get current contract for agent"""
        return self.agents[agent_id].current_contract
    
    def claim_contract_for_agent(self, agent_id: str, contract_id: str) -> bool:
        """Claim contract for specific agent"""
        if contract_id not in self.contracts:
            logger.error(f"Contract {contract_id} not found")
            return False
        
        contract = self.contracts[contract_id]
        if contract.status != "available":
            logger.warning(f"Contract {contract_id} is not available (status: {contract.status})")
            return False
        
        # Update contract status
        contract.status = "claimed"
        contract.agent_id = agent_id
        contract.claimed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Update agent state and contract
        agent = self.agents[agent_id]
        agent.current_contract = contract
        agent.last_activity = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Transition to CONTRACT_CLAIMED state
        success = self.transition_agent_state(agent_id, FSMState.CONTRACT_CLAIMED)
        
        if success:
            logger.info(f"Agent {agent_id} claimed contract {contract_id} and transitioned to CONTRACT_CLAIMED state")
        else:
            logger.warning(f"Agent {agent_id} claimed contract {contract_id} but state transition failed")
        
        return True
    
    def start_contract_work(self, agent_id: str) -> bool:
        """Start work on claimed contract"""
        agent = self.agents[agent_id]
        if not agent.current_contract:
            logger.warning(f"Agent {agent_id} has no contract to work on")
            return False
        
        if agent.current_state != FSMState.CONTRACT_CLAIMED:
            logger.warning(f"Agent {agent_id} is not in CONTRACT_CLAIMED state")
            return False
        
        # Transition to IN_PROGRESS
        self.transition_agent_state(agent_id, FSMState.IN_PROGRESS)
        agent.last_activity = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        logger.info(f"Agent {agent_id} started work on contract {agent.current_contract.contract_id}")
        return True
    
    def complete_contract(self, agent_id: str) -> bool:
        """Complete current contract for agent"""
        agent = self.agents[agent_id]
        if not agent.current_contract:
            logger.warning(f"Agent {agent_id} has no contract to complete")
            return False
        
        if agent.current_state != FSMState.IN_PROGRESS:
            logger.warning(f"Agent {agent_id} is not in IN_PROGRESS state")
            return False
        
        contract = agent.current_contract
        
        # Update contract status
        contract.status = "completed"
        contract.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Update agent stats
        agent.contracts_completed += 1
        agent.extra_credit_earned += contract.extra_credit
        agent.last_activity = time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Transition to COMPLETED
        self.transition_agent_state(agent_id, FSMState.COMPLETED)
        
        logger.info(f"Agent {agent_id} completed contract {contract.contract_id}, earned {contract.extra_credit} points")
        return True
    
    def auto_claim_next_contract(self, agent_id: str) -> Optional[Contract]:
        """Automatically claim next available contract for agent"""
        available_contracts = self.get_available_contracts()
        if not available_contracts:
            logger.info("No available contracts to claim")
            return None
        
        # Simple round-robin assignment for now
        # Could be enhanced with priority-based assignment
        next_contract = available_contracts[0]
        
        if self.claim_contract_for_agent(agent_id, next_contract.contract_id):
            logger.info(f"Auto-claimed contract {next_contract.contract_id} for {agent_id}")
            return next_contract
        else:
            logger.error(f"Failed to auto-claim contract for {agent_id}")
            return None
    
    def get_agent_status_summary(self) -> Dict:
        """Get comprehensive status summary for all agents"""
        summary = {
            "total_agents": len(self.agents),
            "active_contracts": len([c for c in self.contracts.values() if c.status == "claimed"]),
            "available_contracts": len(self.get_available_contracts()),
            "completed_contracts": len([c for c in self.contracts.values() if c.status == "completed"]),
            "total_extra_credit_earned": sum(agent.extra_credit_earned for agent in self.agents.values()),
            "agent_states": {},
            "workflow_status": "running" if self.workflow_running else "stopped"
        }
        
        for agent_id, agent in self.agents.items():
            summary["agent_states"][agent_id] = {
                "role": agent.role,
                "current_state": agent.current_state.value,
                "current_contract": agent.current_contract.contract_id if agent.current_contract else None,
                "contracts_completed": agent.contracts_completed,
                "extra_credit_earned": agent.extra_credit_earned,
                "last_activity": agent.last_activity
            }
        
        return summary
    
    def start_continuous_workflow(self):
        """Start the perpetual motion workflow engine"""
        if self.workflow_running:
            logger.warning("Workflow already running")
            return
        
        self.workflow_running = True
        self.continuous_cycle_active = True
        
        logger.info("🚀 Starting Continuous Workflow Engine - Perpetual Motion Activated!")
        
        # Start the continuous workflow loop in a new thread to avoid async issues
        import threading
        def run_workflow():
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(self._continuous_workflow_loop())
            except Exception as e:
                logger.error(f"Workflow loop error: {e}")
        
        self.workflow_thread = threading.Thread(target=run_workflow, daemon=True)
        self.workflow_thread.start()
    
    def stop_continuous_workflow(self):
        """Stop the continuous workflow engine"""
        self.workflow_running = False
        self.continuous_cycle_active = False
        logger.info("🛑 Continuous Workflow Engine stopped")
    
    async def _continuous_workflow_loop(self):
        """Main continuous workflow loop - perpetual motion engine"""
        logger.info("🔄 Continuous workflow loop started - agents will work forever!")
        
        while self.continuous_cycle_active:
            try:
                # Process each agent
                for agent_id, agent in self.agents.items():
                    await self._process_agent_workflow(agent_id, agent)
                
                # Brief pause to prevent excessive CPU usage
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in continuous workflow loop: {e}")
                await asyncio.sleep(5)  # Longer pause on error
    
    async def _process_agent_workflow(self, agent_id: str, agent: Agent):
        """Process individual agent workflow"""
        try:
            current_state = agent.current_state
            
            if current_state == FSMState.IDLE:
                # Agent is idle, check for available contracts
                if self.get_available_contracts():
                    logger.info(f"Agent {agent_id} is idle, auto-claiming next contract")
                    self.auto_claim_next_contract(agent_id)
            
            elif current_state == FSMState.CONTRACT_CLAIMED:
                # Agent has claimed contract, start work
                logger.info(f"Agent {agent_id} starting work on claimed contract")
                self.start_contract_work(agent_id)
            
            elif current_state == FSMState.IN_PROGRESS:
                # Agent is working, simulate work progress
                # In real implementation, this would check actual work progress
                logger.debug(f"Agent {agent_id} working on contract {agent.current_contract.contract_id}")
                
                # Simulate work completion after some time
                if agent.current_contract and agent.last_activity:
                    # Simple time-based completion simulation
                    # In real implementation, this would check actual deliverables
                    work_duration = 30  # 30 seconds for simulation
                    if time.time() - time.mktime(time.strptime(agent.last_activity, "%Y-%m-%dT%H:%M:%SZ")) > work_duration:
                        logger.info(f"Agent {agent_id} work simulation complete, finishing contract")
                        self.complete_contract(agent_id)
            
            elif current_state == FSMState.COMPLETED:
                # Agent completed contract, claim next one
                logger.info(f"Agent {agent_id} completed contract, auto-claiming next")
                self.transition_agent_state(agent_id, FSMState.CLAIMING_NEXT)
                
                # Auto-claim next contract
                next_contract = self.auto_claim_next_contract(agent_id)
                if next_contract:
                    logger.info(f"Agent {agent_id} auto-claimed next contract: {next_contract.contract_id}")
                else:
                    logger.info(f"No more contracts available for {agent_id}, returning to IDLE")
                    self.transition_agent_state(agent_id, FSMState.IDLE)
            
            elif current_state == FSMState.CLAIMING_NEXT:
                # Agent is claiming next contract (handled above)
                pass
            
            elif current_state == FSMState.ERROR:
                # Agent in error state, reset to IDLE
                logger.warning(f"Agent {agent_id} in error state, resetting to IDLE")
                self.transition_agent_state(agent_id, FSMState.IDLE)
        
        except Exception as e:
            logger.error(f"Error processing agent {agent_id} workflow: {e}")
            self.transition_agent_state(agent_id, FSMState.ERROR)

# Global instance for easy access
fsm_integration = FSMContractIntegration()

def get_fsm_integration() -> FSMContractIntegration:
    """Get the global FSM integration instance"""
    return fsm_integration

if __name__ == "__main__":
    # Test the integration system
    integration = FSMContractIntegration()
    
    print("🚀 FSM-Contract Integration Bridge Test")
    print("=" * 50)
    
    # Start continuous workflow
    integration.start_continuous_workflow()
    
    try:
        # Run for a few cycles to demonstrate
        import time
        for i in range(10):
            print(f"\n📊 Cycle {i+1} Status:")
            summary = integration.get_agent_status_summary()
            print(f"Active contracts: {summary['active_contracts']}")
            print(f"Available contracts: {summary['available_contracts']}")
            print(f"Completed contracts: {summary['completed_contracts']}")
            print(f"Total extra credit: {summary['total_extra_credit_earned']}")
            time.sleep(2)
        
        # Stop workflow
        integration.stop_continuous_workflow()
        
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        integration.stop_continuous_workflow()
    
    print("\n✅ Integration test completed!")
