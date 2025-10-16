"""
Contract Repository - Data Access Layer
=======================================

Handles all contract-related data operations following the repository pattern.
This repository provides data access abstraction for contract storage, retrieval,
and status management.

Author: Agent-7 (Quarantine Mission Phase 3)
Date: 2025-10-16
Points: 300
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime


class ContractRepository:
    """
    Repository for contract data operations.
    
    Provides data access layer for contract management including
    retrieval, claiming, completion, and status tracking.
    No business logic - pure data operations.
    
    Attributes:
        contracts_file: Path to contracts JSON file
    """
    
    def __init__(self, contracts_file: str = "data/contracts.json"):
        """
        Initialize contract repository.
        
        Args:
            contracts_file: Path to contracts storage file
        """
        self.contracts_file = Path(contracts_file)
        self._ensure_contracts_file()
        
    def _ensure_contracts_file(self) -> None:
        """Ensure contracts file exists with proper structure."""
        if not self.contracts_file.exists():
            self.contracts_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_contracts({'contracts': [], 'metadata': {'version': '1.0'}})
    
    def _load_contracts(self) -> Dict[str, Any]:
        """
        Load contracts from file.
        
        Returns:
            Contracts data dictionary
        """
        try:
            with open(self.contracts_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {'contracts': [], 'metadata': {'version': '1.0'}}
    
    def _save_contracts(self, data: Dict[str, Any]) -> bool:
        """
        Save contracts to file.
        
        Args:
            data: Contracts data dictionary
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            with open(self.contracts_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except IOError:
            return False
    
    def get_contract(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """
        Get contract by ID.
        
        Args:
            contract_id: Contract identifier
            
        Returns:
            Contract data dictionary if found, None otherwise
        """
        data = self._load_contracts()
        
        for contract in data.get('contracts', []):
            if contract.get('contract_id') == contract_id:
                return contract
                
        return None
    
    def get_all_contracts(self) -> List[Dict[str, Any]]:
        """
        Get all contracts.
        
        Returns:
            List of all contract data dictionaries
        """
        data = self._load_contracts()
        return data.get('contracts', [])
    
    def get_available_contracts(self, agent_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get available contracts (unclaimed or for specific agent).
        
        Args:
            agent_id: Optional agent identifier to filter contracts
            
        Returns:
            List of available contract data dictionaries
        """
        data = self._load_contracts()
        contracts = data.get('contracts', [])
        
        available = []
        for contract in contracts:
            status = contract.get('status', 'available')
            assigned_agent = contract.get('assigned_agent')
            
            # Include if unclaimed or assigned to specific agent
            if status == 'available' or (agent_id and assigned_agent == agent_id):
                available.append(contract)
                
        return available
    
    def claim_contract(self, contract_id: str, agent_id: str) -> bool:
        """
        Claim contract for agent.
        
        Args:
            contract_id: Contract identifier
            agent_id: Agent identifier claiming the contract
            
        Returns:
            True if claim successful, False otherwise
        """
        data = self._load_contracts()
        contracts = data.get('contracts', [])
        
        for contract in contracts:
            if contract.get('contract_id') == contract_id:
                contract['status'] = 'claimed'
                contract['assigned_agent'] = agent_id
                contract['claimed_at'] = datetime.now().isoformat()
                return self._save_contracts(data)
                
        return False
    
    def complete_contract(self, contract_id: str) -> bool:
        """
        Mark contract as completed.
        
        Args:
            contract_id: Contract identifier
            
        Returns:
            True if completion successful, False otherwise
        """
        data = self._load_contracts()
        contracts = data.get('contracts', [])
        
        for contract in contracts:
            if contract.get('contract_id') == contract_id:
                contract['status'] = 'completed'
                contract['completed_at'] = datetime.now().isoformat()
                return self._save_contracts(data)
                
        return False
    
    def add_contract(self, contract_data: Dict[str, Any]) -> bool:
        """
        Add new contract to storage.
        
        Args:
            contract_data: Contract data dictionary
            
        Returns:
            True if addition successful, False otherwise
        """
        data = self._load_contracts()
        contracts = data.get('contracts', [])
        
        # Add timestamp if not present
        if 'created_at' not in contract_data:
            contract_data['created_at'] = datetime.now().isoformat()
            
        contracts.append(contract_data)
        data['contracts'] = contracts
        
        return self._save_contracts(data)
    
    def get_contracts_by_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all contracts assigned to specific agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of contract data dictionaries
        """
        data = self._load_contracts()
        contracts = data.get('contracts', [])
        
        agent_contracts = [
            c for c in contracts 
            if c.get('assigned_agent') == agent_id
        ]
        
        return agent_contracts
    
    def update_contract_status(self, contract_id: str, status: str) -> bool:
        """
        Update contract status.
        
        Args:
            contract_id: Contract identifier
            status: New status value
            
        Returns:
            True if update successful, False otherwise
        """
        data = self._load_contracts()
        contracts = data.get('contracts', [])
        
        for contract in contracts:
            if contract.get('contract_id') == contract_id:
                contract['status'] = status
                contract['status_updated_at'] = datetime.now().isoformat()
                return self._save_contracts(data)
                
        return False
