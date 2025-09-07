"""
Contract validation logic for the contract claiming system.
"""

from typing import Dict, Any
from ..models.contract import Contract
from ..models.contract_status import ContractStatus


class ContractValidator:
    """Validates contract operations and state transitions."""
    
    def validate_claim(self, contract: Contract, agent_id: str) -> Dict[str, Any]:
        """Validate contract claiming operation."""
        if not contract.is_available():
            return {
                "valid": False,
                "error": f"Contract {contract.contract_id} is not available for claiming"
            }
        
        if not agent_id or not agent_id.strip():
            return {
                "valid": False,
                "error": "Agent ID is required for claiming"
            }
        
        return {"valid": True}
    
    def validate_progress_update(self, contract: Contract, agent_id: str) -> Dict[str, Any]:
        """Validate contract progress update operation."""
        if not contract.is_claimed():
            return {
                "valid": False,
                "error": f"Contract {contract.contract_id} must be claimed before updating progress"
            }
        
        if contract.agent_id != agent_id:
            return {
                "valid": False,
                "error": f"Only agent {contract.agent_id} can update progress on contract {contract.contract_id}"
            }
        
        return {"valid": True}
    
    def validate_completion(self, contract: Contract, agent_id: str) -> Dict[str, Any]:
        """Validate contract completion operation."""
        if contract.is_completed():
            return {
                "valid": False,
                "error": f"Contract {contract.contract_id} is already completed"
            }
        
        if not contract.is_claimed() and not contract.status == ContractStatus.IN_PROGRESS:
            return {
                "valid": False,
                "error": f"Contract {contract.contract_id} must be claimed or in progress before completion"
            }
        
        if contract.agent_id != agent_id:
            return {
                "valid": False,
                "error": f"Only agent {contract.agent_id} can complete contract {contract.contract_id}"
            }
        
        return {"valid": True}
    
    def validate_contract_data(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate contract data structure."""
        required_fields = ['contract_id', 'title', 'description', 'category', 'points', 'status']
        missing_fields = []
        
        for field in required_fields:
            if field not in contract_data or contract_data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            return {
                "valid": False,
                "error": f"Missing required fields: {', '.join(missing_fields)}"
            }
        
        # Validate status
        try:
            ContractStatus.from_string(contract_data['status'])
        except ValueError:
            return {
                "valid": False,
                "error": f"Invalid status: {contract_data['status']}"
            }
        
        # Validate points
        if not isinstance(contract_data['points'], int) or contract_data['points'] <= 0:
            return {
                "valid": False,
                "error": "Points must be a positive integer"
            }
        
        return {"valid": True}
    
    def validate_agent_id(self, agent_id: str) -> Dict[str, Any]:
        """Validate agent ID format."""
        if not agent_id or not agent_id.strip():
            return {
                "valid": False,
                "error": "Agent ID cannot be empty"
            }
        
        # Basic format validation (can be extended)
        if len(agent_id.strip()) < 2:
            return {
                "valid": False,
                "error": "Agent ID must be at least 2 characters long"
            }
        
        return {"valid": True}
    
    def validate_progress_format(self, progress: str) -> Dict[str, Any]:
        """Validate progress string format."""
        if not progress or not progress.strip():
            return {
                "valid": False,
                "error": "Progress cannot be empty"
            }
        
        progress = progress.strip()
        
        # Check for percentage format
        if progress.endswith('%'):
            try:
                percentage = int(progress[:-1])
                if 0 <= percentage <= 100:
                    return {"valid": True}
                else:
                    return {
                        "valid": False,
                        "error": "Percentage must be between 0 and 100"
                    }
            except ValueError:
                return {
                    "valid": False,
                    "error": "Invalid percentage format"
                }
        
        # Check for descriptive format
        valid_descriptions = [
            "not started", "planning", "in progress", "testing", 
            "review", "complete", "completed", "done"
        ]
        
        if progress.lower() in valid_descriptions:
            return {"valid": True}
        
        return {
            "valid": False,
            "error": "Progress must be a percentage (e.g., '50%') or valid description"
        }
