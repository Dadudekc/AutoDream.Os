"""
Core contract management functionality for the contract claiming system.
"""

from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime

# Try absolute imports first, fallback to relative
try:
    from contract import Contract
    from contract_status import ContractStatus
    from contract_validator import ContractValidator
    from contract_persistence import ContractPersistence
except ImportError:
    from ..models.contract import Contract
    from ..models.contract_status import ContractStatus
    from .contract_validator import ContractValidator
    from .contract_persistence import ContractPersistence


class ContractManager:
    """Core contract management operations."""
    
    def __init__(self, task_list_path: str):
        self.persistence = ContractPersistence(task_list_path)
        self.validator = ContractValidator()
        self.contracts = self.persistence.load_contracts()
    
    def get_all_contracts(self) -> Dict[str, Any]:
        """Get all contracts from the system."""
        return self.contracts
    
    def find_contract(self, contract_id: str) -> Optional[Tuple[Contract, str, int]]:
        """
        Find a contract by ID.
        
        Returns:
            Tuple of (contract, contract_type, index) or None if not found
        """
        contracts_section = self.contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for i, contract_dict in enumerate(contracts_list):
                        if isinstance(contract_dict, dict) and contract_dict.get('contract_id') == contract_id:
                            try:
                                contract = Contract.from_dict(contract_dict)
                                return contract, contract_type, i
                            except Exception:
                                continue
            elif isinstance(contract_data, list):
                for i, contract_dict in enumerate(contract_data):
                    if isinstance(contract_dict, dict) and contract_dict.get('contract_id') == contract_id:
                        try:
                            contract = Contract.from_dict(contract_dict)
                            return contract, contract_type, i
                        except Exception:
                            continue
        
        return None
    
    def claim_contract(self, contract_id: str, agent_id: str) -> Dict[str, Any]:
        """Claim a contract for an agent."""
        result = self.find_contract(contract_id)
        if not result:
            return {"success": False, "error": "Contract not found"}
        
        contract, contract_type, index = result
        
        # Validate claim operation
        validation_result = self.validator.validate_claim(contract, agent_id)
        if not validation_result["valid"]:
            return {"success": False, "error": validation_result["error"]}
        
        # Update contract
        contract.agent_id = agent_id
        contract.status = ContractStatus.CLAIMED
        contract.claimed_at = datetime.now()
        contract.updated_at = datetime.now()
        
        # Save changes
        if self._update_contract_in_storage(contract, contract_type, index):
            self.persistence.save_contracts(self.contracts)
            return {
                "success": True,
                "contract": contract.to_dict(),
                "message": f"Contract {contract_id} claimed by {agent_id}"
            }
        else:
            return {"success": False, "error": "Failed to update contract storage"}
    
    def update_contract_progress(self, contract_id: str, agent_id: str, progress: str) -> Dict[str, Any]:
        """Update contract progress."""
        result = self.find_contract(contract_id)
        if not result:
            return {"success": False, "error": "Contract not found"}
        
        contract, contract_type, index = result
        
        # Validate update operation
        validation_result = self.validator.validate_progress_update(contract, agent_id)
        if not validation_result["valid"]:
            return {"success": False, "error": validation_result["error"]}
        
        # Update contract
        contract.update_progress(progress)
        if progress == "100%":
            contract.status = ContractStatus.IN_PROGRESS
        
        # Save changes
        if self._update_contract_in_storage(contract, contract_type, index):
            self.persistence.save_contracts(self.contracts)
            return {
                "success": True,
                "contract": contract.to_dict(),
                "message": f"Progress updated to {progress}"
            }
        else:
            return {"success": False, "error": "Failed to update contract storage"}
    
    def complete_contract(self, contract_id: str, agent_id: str, deliverables: str) -> Dict[str, Any]:
        """Complete a contract with deliverables."""
        result = self.find_contract(contract_id)
        if not result:
            return {"success": False, "error": "Contract not found"}
        
        contract, contract_type, index = result
        
        # Validate completion operation
        validation_result = self.validator.validate_completion(contract, agent_id)
        if not validation_result["valid"]:
            return {"success": False, "error": validation_result["error"]}
        
        # Update contract
        contract.status = ContractStatus.COMPLETED
        contract.progress = "100%"
        contract.updated_at = datetime.now()
        
        # Parse deliverables
        if deliverables:
            deliverable_list = [d.strip() for d in deliverables.split(",")]
            for deliverable in deliverable_list:
                contract.add_deliverable(deliverable)
        
        # Save changes
        if self._update_contract_in_storage(contract, contract_type, index):
            self.persistence.save_contracts(self.contracts)
            return {
                "success": True,
                "contract": contract.to_dict(),
                "message": f"Contract {contract_id} completed by {agent_id}"
            }
        else:
            return {"success": False, "error": "Failed to update contract storage"}
    
    def _update_contract_in_storage(self, contract: Contract, contract_type: str, index: int) -> bool:
        """Update contract in the storage structure."""
        try:
            contracts_section = self.contracts.get("contracts", {})
            contract_data = contracts_section.get(contract_type, {})
            
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list) and 0 <= index < len(contracts_list):
                    contracts_list[index] = contract.to_dict()
                    return True
            elif isinstance(contract_data, list) and 0 <= index < len(contract_data):
                contract_data[index] = contract.to_dict()
                return True
            
            return False
        except Exception:
            return False
    
    def get_contract_statistics(self) -> Dict[str, Any]:
        """Get statistics about contracts in the system."""
        total_contracts = 0
        available_contracts = 0
        claimed_contracts = 0
        completed_contracts = 0
        
        contracts_section = self.contracts.get("contracts", {})
        
        for contract_type, contract_data in contracts_section.items():
            if isinstance(contract_data, dict) and 'contracts' in contract_data:
                contracts_list = contract_data.get('contracts', [])
                if isinstance(contracts_list, list):
                    for contract_dict in contracts_list:
                        if isinstance(contract_dict, dict):
                            total_contracts += 1
                            status = contract_dict.get('status', 'AVAILABLE')
                            if status == 'AVAILABLE':
                                available_contracts += 1
                            elif status == 'CLAIMED':
                                claimed_contracts += 1
                            elif status == 'COMPLETED':
                                completed_contracts += 1
            elif isinstance(contract_data, list):
                for contract_dict in contract_data:
                    if isinstance(contract_dict, dict):
                        total_contracts += 1
                        status = contract_dict.get('status', 'AVAILABLE')
                        if status == 'AVAILABLE':
                            available_contracts += 1
                        elif status == 'CLAIMED':
                            claimed_contracts += 1
                        elif status == 'COMPLETED':
                            completed_contracts += 1
        
        return {
            "total_contracts": total_contracts,
            "available_contracts": available_contracts,
            "claimed_contracts": claimed_contracts,
            "completed_contracts": completed_contracts,
            "completion_rate": (completed_contracts / total_contracts * 100) if total_contracts > 0 else 0
        }
