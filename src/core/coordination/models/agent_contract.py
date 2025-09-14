"""
Agent Contract Models
====================

Models for agent contract management.

Author: Agent-2 (Architecture & Design Specialist)
Mission: Large File Modularization and V2 Compliance
Contract: CONTRACT_Agent-2_1757826687
License: MIT
"""

from typing import Dict, Any, Optional
from datetime import datetime
from .agent_state import ContractType


class AgentContract:
    """Agent contract model for task commitments."""
    
    def __init__(self, agent_id: str, contract_type: ContractType, 
                 task_description: str, priority: str = "NORMAL",
                 deadline: Optional[str] = None):
        """Initialize agent contract."""
        self.agent_id = agent_id
        self.contract_type = contract_type
        self.task_description = task_description
        self.priority = priority
        self.deadline = deadline
        self.created_at = datetime.now().isoformat()
        self.contract_id = f"CONTRACT_{agent_id}_{int(datetime.now().timestamp())}"
        self.status = "PENDING"
        self.progress = 0
        self.completed_at = None
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary."""
        return {
            "contract_id": self.contract_id,
            "agent_id": self.agent_id,
            "contract_type": self.contract_type.value,
            "task_description": self.task_description,
            "priority": self.priority,
            "deadline": self.deadline,
            "created_at": self.created_at,
            "status": self.status,
            "progress": self.progress,
            "completed_at": self.completed_at
        }

