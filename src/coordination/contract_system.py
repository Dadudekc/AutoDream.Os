#!/usr/bin/env python3
"""
Contract System - Agent Task Commitments
=======================================

Contract system for agent task commitments and tracking.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from enum import Enum

logger = logging.getLogger(__name__)

class ContractStatus(Enum):
    """Contract status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class Contract:
    """Contract for agent task commitments."""
    
    def __init__(self, contract_id: str, agent_id: str, task: str, 
                 priority: str = "NORMAL", deadline: Optional[datetime] = None):
        self.contract_id = contract_id
        self.agent_id = agent_id
        self.task = task
        self.priority = priority
        self.status = ContractStatus.PENDING
        self.created_at = datetime.now()
        self.deadline = deadline
        self.completed_at = None
        self.progress = 0.0
        self.notes = []
    
    def to_dict(self) -> Dict:
        """Convert contract to dictionary."""
        return {
            "contract_id": self.contract_id,
            "agent_id": self.agent_id,
            "task": self.task,
            "priority": self.priority,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "progress": self.progress,
            "notes": self.notes
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Contract':
        """Create contract from dictionary."""
        contract = cls(
            data["contract_id"],
            data["agent_id"],
            data["task"],
            data.get("priority", "NORMAL")
        )
        contract.status = ContractStatus(data["status"])
        contract.created_at = datetime.fromisoformat(data["created_at"])
        if data.get("deadline"):
            contract.deadline = datetime.fromisoformat(data["deadline"])
        if data.get("completed_at"):
            contract.completed_at = datetime.fromisoformat(data["completed_at"])
        contract.progress = data.get("progress", 0.0)
        contract.notes = data.get("notes", [])
        return contract

class ContractManager:
    """Manager for agent contracts."""
    
    def __init__(self, contracts_file: str = "agent_contracts.json"):
        self.contracts_file = Path(contracts_file)
        self.contracts: Dict[str, Contract] = {}
        self._load_contracts()
    
    def _load_contracts(self) -> None:
        """Load contracts from file."""
        try:
            if self.contracts_file.exists():
                with open(self.contracts_file, encoding="utf-8") as f:
                    data = json.load(f)
                    for contract_data in data.get("contracts", []):
                        contract = Contract.from_dict(contract_data)
                        self.contracts[contract.contract_id] = contract
                logger.info(f"Loaded {len(self.contracts)} contracts")
        except Exception as e:
            logger.error(f"Error loading contracts: {e}")
    
    def _save_contracts(self) -> None:
        """Save contracts to file."""
        try:
            data = {
                "contracts": [contract.to_dict() for contract in self.contracts.values()],
                "last_updated": datetime.now().isoformat()
            }
            with open(self.contracts_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving contracts: {e}")
    
    def create_contract(self, agent_id: str, task: str, priority: str = "NORMAL",
                       deadline: Optional[datetime] = None) -> str:
        """Create a new contract."""
        contract_id = f"CONTRACT_{agent_id}_{int(datetime.now().timestamp())}"
        contract = Contract(contract_id, agent_id, task, priority, deadline)
        self.contracts[contract_id] = contract
        self._save_contracts()
        logger.info(f"Created contract {contract_id} for {agent_id}")
        return contract_id
    
    def get_contract(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID."""
        return self.contracts.get(contract_id)
    
    def get_agent_contracts(self, agent_id: str) -> List[Contract]:
        """Get all contracts for an agent."""
        return [contract for contract in self.contracts.values() 
                if contract.agent_id == agent_id]
    
    def update_contract_status(self, contract_id: str, status: ContractStatus,
                              progress: float = None, notes: str = None) -> bool:
        """Update contract status."""
        contract = self.contracts.get(contract_id)
        if not contract:
            return False
        
        contract.status = status
        if progress is not None:
            contract.progress = progress
        if notes:
            contract.notes.append(f"{datetime.now().isoformat()}: {notes}")
        
        if status == ContractStatus.COMPLETED:
            contract.completed_at = datetime.now()
        
        self._save_contracts()
        logger.info(f"Updated contract {contract_id} status to {status.value}")
        return True

