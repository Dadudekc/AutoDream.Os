"""
Contract Repository - Data Access Layer
========================================

Handles all contract-related data operations including contract retrieval,
availability checking, and contract claiming.

Author: Agent-7 - Repository Cloning Specialist
Mission: Quarantine Fix Phase 3 (Repository Pattern)
Date: 2025-10-16
Points: 300 pts
V2 Compliant: ≤400 lines, single responsibility

Architecture:
- Follows repository pattern (data access abstraction)
- No business logic (data operations only)
- Type hints for all methods
- Comprehensive error handling

Usage:
    from src.repositories import ContractRepository
    
    repo = ContractRepository()
    contract = repo.get_contract("contract_123")
    available = repo.get_available_contracts("Agent-7")
    repo.claim_contract("contract_123", "Agent-7")
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ContractRepository:
    """
    Repository for contract data operations.
    
    Provides data access methods for contracts, availability checking,
    and contract claiming operations.
    """
    
    def __init__(self, contracts_dir: str = "contracts"):
        """
        Initialize contract repository.
        
        Args:
            contracts_dir: Directory containing contract files
        """
        self.contracts_dir = Path(contracts_dir)
    
    def get_contract(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """
        Get contract by ID.
        
        Args:
            contract_id: Contract identifier
            
        Returns:
            Contract data dictionary or None if not found
        """
        try:
            # Try multiple potential file formats
            potential_files = [
                self.contracts_dir / f"{contract_id}.json",
                self.contracts_dir / f"{contract_id}.md",
                self.contracts_dir / contract_id,
            ]
            
            for contract_file in potential_files:
                if contract_file.exists():
                    if contract_file.suffix == '.json':
                        with open(contract_file, 'r', encoding='utf-8') as f:
                            return json.load(f)
                    else:
                        with open(contract_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            return {
                                "contract_id": contract_id,
                                "content": content,
                                "file": str(contract_file)
                            }
            
            logger.warning(f"Contract {contract_id} not found")
            return None
            
        except Exception as e:
            logger.error(f"Error reading contract {contract_id}: {e}")
            return None
    
    def get_all_contracts(self) -> List[Dict[str, Any]]:
        """
        Get all contracts.
        
        Returns:
            List of contract data dictionaries
        """
        contracts = []
        
        try:
            if not self.contracts_dir.exists():
                logger.warning("Contracts directory does not exist")
                return []
            
            # Read all contract files
            for contract_file in self.contracts_dir.iterdir():
                if contract_file.is_file():
                    contract_id = contract_file.stem
                    contract_data = self.get_contract(contract_id)
                    if contract_data:
                        contracts.append(contract_data)
            
            return contracts
            
        except Exception as e:
            logger.error(f"Error reading contracts: {e}")
            return []
    
    def get_available_contracts(
        self, 
        agent_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get available contracts for agent.
        
        Args:
            agent_id: Agent identifier (optional filter)
            
        Returns:
            List of available contract data dictionaries
        """
        all_contracts = self.get_all_contracts()
        
        # Filter for unclaimed contracts
        available = [
            contract for contract in all_contracts
            if contract.get('status') != 'claimed' and
            contract.get('claimed_by') is None
        ]
        
        # Optional: filter by agent specialization
        if agent_id:
            available = [
                contract for contract in available
                if self._matches_agent_specialty(contract, agent_id)
            ]
        
        return available
    
    def claim_contract(
        self, 
        contract_id: str, 
        agent_id: str
    ) -> bool:
        """
        Claim contract for agent.
        
        Args:
            contract_id: Contract identifier
            agent_id: Agent identifier
            
        Returns:
            True if successfully claimed, False otherwise
        """
        try:
            contract = self.get_contract(contract_id)
            
            if not contract:
                logger.error(f"Contract {contract_id} not found")
                return False
            
            # Check if already claimed
            if contract.get('claimed_by'):
                logger.warning(
                    f"Contract {contract_id} already claimed by "
                    f"{contract.get('claimed_by')}"
                )
                return False
            
            # Update contract with claim information
            contract['claimed_by'] = agent_id
            contract['claimed_at'] = datetime.now().isoformat()
            contract['status'] = 'claimed'
            
            # Save updated contract
            contract_file = self.contracts_dir / f"{contract_id}.json"
            with open(contract_file, 'w', encoding='utf-8') as f:
                json.dump(contract, f, indent=2)
            
            logger.info(f"Contract {contract_id} claimed by {agent_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error claiming contract {contract_id}: {e}")
            return False
    
    def release_contract(self, contract_id: str) -> bool:
        """
        Release a claimed contract.
        
        Args:
            contract_id: Contract identifier
            
        Returns:
            True if successfully released, False otherwise
        """
        try:
            contract = self.get_contract(contract_id)
            
            if not contract:
                return False
            
            contract['claimed_by'] = None
            contract['claimed_at'] = None
            contract['status'] = 'available'
            contract['released_at'] = datetime.now().isoformat()
            
            contract_file = self.contracts_dir / f"{contract_id}.json"
            with open(contract_file, 'w', encoding='utf-8') as f:
                json.dump(contract, f, indent=2)
            
            logger.info(f"Contract {contract_id} released")
            return True
            
        except Exception as e:
            logger.error(f"Error releasing contract {contract_id}: {e}")
            return False
    
    def get_agent_contracts(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all contracts claimed by agent.
        
        Args:
            agent_id: Agent identifier
            
        Returns:
            List of contract data dictionaries
        """
        all_contracts = self.get_all_contracts()
        
        agent_contracts = [
            contract for contract in all_contracts
            if contract.get('claimed_by') == agent_id
        ]
        
        return agent_contracts
    
    def _matches_agent_specialty(
        self, 
        contract: Dict[str, Any], 
        agent_id: str
    ) -> bool:
        """
        Check if contract matches agent specialty.
        
        Args:
            contract: Contract data dictionary
            agent_id: Agent identifier
            
        Returns:
            True if matches, False otherwise
        """
        # Simplified specialty matching
        # Can be enhanced with agent specialty lookup
        
        specialty_map = {
            "Agent-1": ["integration", "core"],
            "Agent-2": ["architecture", "design"],
            "Agent-3": ["infrastructure", "devops"],
            "Agent-5": ["business", "intelligence"],
            "Agent-6": ["coordination", "communication"],
            "Agent-7": ["web", "development", "repository"],
            "Agent-8": ["ssot", "integration"],
        }
        
        agent_specialties = specialty_map.get(agent_id, [])
        contract_type = contract.get('type', '').lower()
        
        # Match if any specialty keyword in contract type
        return any(
            specialty in contract_type 
            for specialty in agent_specialties
        )

