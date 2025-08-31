from pathlib import Path
from typing import Dict, List, Optional, Any
import asyncio
import json
import logging
import os
import sys
import time

# Import our FSM integration
try:
    from src.core.fsm_contract_integration import fsm_integration, get_fsm_integration, FSMContractIntegration
except ImportError:
    # Fallback if import fails
    FSMContractIntegration = None
    get_fsm_integration = lambda: None
    fsm_integration = None

"""
Unified Messaging Service with FSM Integration
Provides automated contract management and messaging capabilities
Integrates FSM, Contract, and Messaging systems into unified workflow
"""




logger = logging.getLogger(__name__)

class UnifiedMessagingService:
    """
    Unified messaging service that integrates FSM, Contract, and Messaging systems
    Provides automated contract workflow management
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = project_root
        self.messaging_mode = "pyautogui"  # Default mode
        # Use the global FSM integration instance
        try:
            self.fsm_integration = fsm_integration
        except ImportError:
            self.fsm_integration = get_fsm_integration()
        
        self.messaging_history = []
        self.auto_workflow_active = False
        
        if not self.fsm_integration:
            logger.warning("FSM integration not available, creating standalone service")
            self._create_standalone_fsm()
        
        logger.info("Unified Messaging Service initialized")
    
    def set_mode(self, mode):
        """Set the messaging mode"""
        self.messaging_mode = mode.value if hasattr(mode, 'value') else str(mode)
        logger.info(f"Messaging mode set to: {self.messaging_mode}")
    
    def _create_standalone_fsm(self):
        """Create standalone FSM integration if import fails"""
        try:
            # Try to create FSM integration directly
            fsm_path = Path(self.project_root) / "src" / "core" / "fsm_contract_integration.py"
            if fsm_path.exists():
                sys.path.insert(0, str(fsm_path.parent.parent))
                self.fsm_integration = FSMContractIntegration(self.project_root)
                logger.info("Standalone FSM integration created")
            else:
                logger.error("FSM integration file not found")
        except Exception as e:
            logger.error(f"Failed to create standalone FSM: {e}")
    
    def get_next_task(self, agent_id: str) -> Dict[str, Any]:
        """Get next available task for agent via FSM integration"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            # Check if agent needs next task
            agent = self.fsm_integration.agents.get(agent_id)
            if not agent:
                return {"error": f"Agent {agent_id} not found"}
            
            # Get available contracts
            available_contracts = self.fsm_integration.get_available_contracts()
            if not available_contracts:
                return {
                    "status": "no_tasks_available",
                    "message": "No contracts available at this time",
                    "agent_id": agent_id
                }
            
            # Select next contract (simple round-robin for now)
            next_contract = available_contracts[0]
            
            # Log the task retrieval
            self._log_messaging_action(
                action="get_next_task",
                agent_id=agent_id,
                contract_id=next_contract.contract_id,
                status="success"
            )
            
            return {
                "status": "task_found",
                "contract_id": next_contract.contract_id,
                "title": next_contract.title,
                "difficulty": next_contract.difficulty,
                "estimated_time": next_contract.estimated_time,
                "extra_credit": next_contract.extra_credit,
                "message": f"Next task found for {agent_id}: {next_contract.title}",
                "claim_command": f"python -m src.services.messaging --agent {agent_id} --claim-contract {next_contract.contract_id}"
            }
            
        except Exception as e:
            logger.error(f"Error getting next task for {agent_id}: {e}")
            return {"error": f"Failed to get next task: {str(e)}"}
    
    def claim_contract(self, agent_id: str, contract_id: str) -> Dict[str, Any]:
        """Claim contract for agent via FSM integration"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            # Claim contract through FSM
            success = self.fsm_integration.claim_contract_for_agent(agent_id, contract_id)
            
            if success:
                contract = self.fsm_integration.contracts[contract_id]
                
                # Log the contract claiming
                self._log_messaging_action(
                    action="claim_contract",
                    agent_id=agent_id,
                    contract_id=contract_id,
                    status="success"
                )
                
                return {
                    "status": "contract_claimed",
                    "message": f"Contract {contract_id} successfully claimed by {agent_id}",
                    "contract_details": {
                        "id": contract.contract_id,
                        "title": contract.title,
                        "difficulty": contract.difficulty,
                        "estimated_time": contract.estimated_time,
                        "extra_credit": contract.extra_credit
                    },
                    "next_action": "start_work",
                    "fsm_state": self.fsm_integration.fsm_states[agent_id].value
                }
            else:
                return {
                    "status": "claim_failed",
                    "message": f"Failed to claim contract {contract_id} for {agent_id}",
                    "error": "Contract not available or agent not in correct state"
                }
                
        except Exception as e:
            logger.error(f"Error claiming contract {contract_id} for {agent_id}: {e}")
            return {"error": f"Failed to claim contract: {str(e)}"}
    
    def start_contract_work(self, agent_id: str) -> Dict[str, Any]:
        """Start work on claimed contract via FSM integration"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            success = self.fsm_integration.start_contract_work(agent_id)
            
            if success:
                agent = self.fsm_integration.agents[agent_id]
                contract = agent.current_contract
                
                # Log the work start
                self._log_messaging_action(
                    action="start_contract_work",
                    agent_id=agent_id,
                    contract_id=contract.contract_id if contract else None,
                    status="success"
                )
                
                return {
                    "status": "work_started",
                    "message": f"Agent {agent_id} started work on contract {contract.contract_id if contract else 'unknown'}",
                    "fsm_state": self.fsm_integration.fsm_states[agent_id].value,
                    "estimated_completion": contract.estimated_time if contract else "unknown"
                }
            else:
                return {
                    "status": "work_start_failed",
                    "message": f"Failed to start work for {agent_id}",
                    "error": "Agent not in correct state or no contract claimed"
                }
                
        except Exception as e:
            logger.error(f"Error starting work for {agent_id}: {e}")
            return {"error": f"Failed to start work: {str(e)}"}
    
    def complete_contract(self, agent_id: str) -> Dict[str, Any]:
        """Complete current contract for agent via FSM integration"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            success = self.fsm_integration.complete_contract(agent_id)
            
            if success:
                agent = self.fsm_integration.agents[agent_id]
                contract = agent.current_contract
                
                # Log the contract completion
                self._log_messaging_action(
                    action="complete_contract",
                    agent_id=agent_id,
                    contract_id=contract.contract_id if contract else None,
                    status="success"
                )
                
                return {
                    "status": "contract_completed",
                    "message": f"Agent {agent_id} completed contract {contract.contract_id if contract else 'unknown'}",
                    "extra_credit_earned": contract.extra_credit if contract else 0,
                    "total_extra_credit": agent.extra_credit_earned,
                    "contracts_completed": agent.contracts_completed,
                    "next_action": "auto_claim_next",
                    "fsm_state": self.fsm_integration.fsm_states[agent_id].value
                }
            else:
                return {
                    "status": "completion_failed",
                    "message": f"Failed to complete contract for {agent_id}",
                    "error": "Agent not in correct state or no contract in progress"
                }
                
        except Exception as e:
            logger.error(f"Error completing contract for {agent_id}: {e}")
            return {"error": f"Failed to complete contract: {str(e)}"}
    
    def get_contract_status(self) -> Dict[str, Any]:
        """Get comprehensive contract status via FSM integration"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            summary = self.fsm_integration.get_agent_status_summary()
            
            return {
                "status": "success",
                "contract_system_status": summary,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "auto_workflow_active": self.auto_workflow_active
            }
            
        except Exception as e:
            logger.error(f"Error getting contract status: {e}")
            return {"error": f"Failed to get contract status: {str(e)}"}
    
    def start_auto_workflow(self) -> Dict[str, Any]:
        """Start automated workflow for all agents"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            if self.auto_workflow_active:
                return {
                    "status": "already_active",
                    "message": "Auto workflow already active"
                }
            
            # Start FSM continuous workflow
            self.fsm_integration.start_continuous_workflow()
            self.auto_workflow_active = True
            
            # Log the workflow start
            self._log_messaging_action(
                action="start_auto_workflow",
                agent_id="SYSTEM",
                contract_id=None,
                status="success"
            )
            
            return {
                "status": "workflow_started",
                "message": "🚀 Automated workflow started - agents will work continuously!",
                "workflow_type": "perpetual_motion",
                "agents_active": len(self.fsm_integration.agents),
                "contracts_available": len(self.fsm_integration.get_available_contracts())
            }
            
        except Exception as e:
            logger.error(f"Error starting auto workflow: {e}")
            return {"error": f"Failed to start auto workflow: {str(e)}"}
    
    def stop_auto_workflow(self) -> Dict[str, Any]:
        """Stop automated workflow"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            if not self.auto_workflow_active:
                return {
                    "status": "not_active",
                    "message": "Auto workflow not active"
                }
            
            # Stop FSM continuous workflow
            self.fsm_integration.stop_continuous_workflow()
            self.auto_workflow_active = False
            
            # Log the workflow stop
            self._log_messaging_action(
                action="stop_auto_workflow",
                agent_id="SYSTEM",
                contract_id=None,
                status="success"
            )
            
            return {
                "status": "workflow_stopped",
                "message": "🛑 Automated workflow stopped",
                "workflow_type": "perpetual_motion"
            }
            
        except Exception as e:
            logger.error(f"Error stopping auto workflow: {e}")
            return {"error": f"Failed to stop auto workflow: {str(e)}"}
    
    def _log_messaging_action(self, action: str, agent_id: str, contract_id: Optional[str], status: str):
        """Log messaging actions for tracking"""
        log_entry = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "action": action,
            "agent_id": agent_id,
            "contract_id": contract_id,
            "status": status
        }
        
        self.messaging_history.append(log_entry)
        logger.info(f"Messaging action: {action} by {agent_id} - {status}")
    
    def get_messaging_history(self, limit: int = 100) -> List[Dict]:
        """Get messaging action history"""
        return self.messaging_history[-limit:] if limit > 0 else self.messaging_history
    
    def get_agent_workflow_status(self, agent_id: str) -> Dict[str, Any]:
        """Get detailed workflow status for specific agent"""
        if not self.fsm_integration:
            return {"error": "FSM integration not available"}
        
        try:
            agent = self.fsm_integration.agents.get(agent_id)
            if not agent:
                return {"error": f"Agent {agent_id} not found"}
            
            contract = agent.current_contract
            
            return {
                "status": "success",
                "agent_id": agent_id,
                "role": agent.role,
                "fsm_state": agent.current_state.value,
                "current_contract": {
                    "id": contract.contract_id if contract else None,
                    "title": contract.title if contract else None,
                    "status": contract.status if contract else None
                } if contract else None,
                "contracts_completed": agent.contracts_completed,
                "extra_credit_earned": agent.extra_credit_earned,
                "last_activity": agent.last_activity,
                "next_actions": self._get_next_actions_for_agent(agent)
            }
            
        except Exception as e:
            logger.error(f"Error getting workflow status for {agent_id}: {e}")
            return {"error": f"Failed to get workflow status: {str(e)}"}
    
    def _get_next_actions_for_agent(self, agent) -> List[str]:
        """Get next actions for agent based on current state"""
        if agent.current_state.value == "idle":
            return ["get_next_task", "claim_contract"]
        elif agent.current_state.value == "contract_claimed":
            return ["start_contract_work"]
        elif agent.current_state.value == "in_progress":
            return ["complete_contract"]
        elif agent.current_state.value == "completed":
            return ["auto_claim_next"]
        else:
            return ["reset_to_idle"]

# Global instance for easy access
unified_messaging = UnifiedMessagingService()

def get_unified_messaging() -> UnifiedMessagingService:
    """Get the global unified messaging service instance"""
    return unified_messaging

if __name__ == "__main__":
    # Test the unified messaging service
    service = UnifiedMessagingService()
    
    print("🚀 Unified Messaging Service Test")
    print("=" * 50)
    
    # Test basic functionality
    print("\n1. Testing contract status:")
    status = service.get_contract_status()
    print(json.dumps(status, indent=2))
    
    print("\n2. Testing next task retrieval:")
    next_task = service.get_next_task("Agent-7")
    print(json.dumps(next_task, indent=2))
    
    print("\n3. Testing auto workflow start:")
    workflow_start = service.start_auto_workflow()
    print(json.dumps(workflow_start, indent=2))
    
    print("\n4. Testing agent workflow status:")
    agent_status = service.get_agent_workflow_status("Agent-7")
    print(json.dumps(agent_status, indent=2))
    
    print("\n✅ Unified messaging service test completed!")
