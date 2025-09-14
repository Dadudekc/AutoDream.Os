"""
Agent Factory
=============

Factory for creating agent-related objects using Factory pattern.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Large File Modularization and V2 Compliance
Contract: CONTRACT_Agent-2_1757826687
License: MIT
"""

from typing import Dict, List
from ..models.agent_fsm import AgentFSM
from ..models.agent_contract import AgentContract
from ..models.agent_state import ContractType, AgentState


class AgentFactory:
    """Factory for creating agent-related objects."""
    
    # Agent role specializations
    AGENT_ROLES = {
        "Agent-1": "Integration & Core Systems Specialist",
        "Agent-2": "Architecture & Design Specialist", 
        "Agent-3": "Infrastructure & DevOps Specialist",
        "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
        "Agent-5": "Business Intelligence Specialist",
        "Agent-6": "Coordination & Communication Specialist",
        "Agent-7": "Web Development Specialist",
        "Agent-8": "Operations & Support Specialist"
    }
    
    SWARM_AGENTS = [
        "Agent-1", "Agent-2", "Agent-3", "Agent-4",
        "Agent-5", "Agent-6", "Agent-7", "Agent-8"
    ]
    
    @classmethod
    def create_agent_fsm(cls, agent_id: str) -> AgentFSM:
        """Create agent FSM instance."""
        return AgentFSM(agent_id)
        
    @classmethod
    def create_agent_contract(cls, agent_id: str, contract_type: ContractType,
                            task_description: str, priority: str = "NORMAL",
                            deadline: str = None) -> AgentContract:
        """Create agent contract instance."""
        return AgentContract(
            agent_id=agent_id,
            contract_type=contract_type,
            task_description=task_description,
            priority=priority,
            deadline=deadline
        )
        
    @classmethod
    def create_all_agent_fsms(cls) -> Dict[str, AgentFSM]:
        """Create FSM instances for all agents."""
        return {agent_id: cls.create_agent_fsm(agent_id) 
                for agent_id in cls.SWARM_AGENTS}
                
    @classmethod
    def get_agent_role(cls, agent_id: str) -> str:
        """Get agent role specialization."""
        return cls.AGENT_ROLES.get(agent_id, "Unknown Specialist")
        
    @classmethod
    def get_all_agent_roles(cls) -> Dict[str, str]:
        """Get all agent role specializations."""
        return cls.AGENT_ROLES.copy()
        
    @classmethod
    def get_swarm_agents(cls) -> List[str]:
        """Get list of all swarm agents."""
        return cls.SWARM_AGENTS.copy()

