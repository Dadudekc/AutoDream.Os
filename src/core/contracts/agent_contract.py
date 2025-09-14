"""
Agent contract system for the integrated onboarding coordination system.

This module provides the contract system for agent task commitments,
including contract types, contract management, and progress tracking.
"""

from datetime import datetime
from typing import List, Dict, Any
from enum import Enum


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
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert contract to dictionary representation."""
        return {
            "agent_id": self.agent_id,
            "contract_type": self.contract_type.value,
            "description": self.description,
            "estimated_cycles": self.estimated_cycles,
            "dependencies": self.dependencies,
            "status": self.status,
            "cycle_start": self.cycle_start.isoformat() if self.cycle_start else None,
            "cycle_end": self.cycle_end.isoformat() if self.cycle_end else None,
            "progress_percentage": self.progress_percentage,
            "created_at": self.created_at.isoformat()
        }