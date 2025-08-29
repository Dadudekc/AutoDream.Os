#!/usr/bin/env python3
"""Contract system manager for centralized contract operations."""

import sys
import os
import logging
from typing import Optional, Dict, Any, List
from .path_utils import PathUtils


class ContractSystemManager:
    """Centralized contract system management to eliminate duplication."""
    
    def __init__(self):
        self._system = None
        self._task_list_path = None
        self._initialized = False
        self.logger = logging.getLogger(f"{__name__}.ContractSystemManager")
    
    def initialize(self) -> bool:
        """Initialize contract system once to eliminate duplicate imports."""
        if self._initialized:
            return True
            
        try:
            # Add meeting path to sys.path
            meeting_path = PathUtils.get_contract_system_path()
            if meeting_path not in sys.path:
                sys.path.append(meeting_path)
            
            # Import contract system
            from contract_claiming_system import ContractClaimingSystem
            
            # Set up paths
            self._task_list_path = PathUtils.get_task_list_path()
            
            # Initialize system
            self._system = ContractClaimingSystem(self._task_list_path)
            
            self._initialized = True
            self.logger.info("Contract system initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize contract system: {e}")
            return False
    
    def get_system(self):
        """Get initialized contract system."""
        if not self.initialize():
            raise RuntimeError("Failed to initialize contract system")
        return self._system
    
    def get_task_list_path(self) -> str:
        """Get task list path."""
        if not self.initialize():
            raise RuntimeError("Failed to initialize contract system")
        return self._task_list_path
    
    def claim_contract(self, contract_id: str, agent_id: str) -> Dict[str, Any]:
        """Claim a contract using centralized system."""
        try:
            system = self.get_system()
            return system.claim_contract(contract_id, agent_id)
        except Exception as e:
            self.logger.error(f"Contract claiming failed: {e}")
            return {"success": False, "message": f"Contract claiming failed: {e}"}
    
    def complete_contract(self, contract_id: str, agent_id: str, deliverables: List[str]) -> Dict[str, Any]:
        """Complete a contract using centralized system."""
        try:
            system = self.get_system()
            return system.complete_contract(contract_id, agent_id, deliverables)
        except Exception as e:
            self.logger.error(f"Contract completion failed: {e}")
            return {"success": False, "message": f"Contract completion failed: {e}"}
    
    def list_available_contracts(self) -> List[Dict[str, Any]]:
        """List available contracts using centralized system."""
        try:
            system = self.get_system()
            return system.list_available_contracts()
        except Exception as e:
            self.logger.error(f"Failed to list contracts: {e}")
            return []
    
    def get_contract_statistics(self) -> Dict[str, Any]:
        """Get contract statistics using centralized system."""
        try:
            system = self.get_system()
            return system.get_contract_statistics()
        except Exception as e:
            self.logger.error(f"Failed to get contract statistics: {e}")
            return {"total_contracts": 0, "available_contracts": 0}
    
    def get_contract_details(self, contract_id: str) -> Optional[Dict[str, Any]]:
        """Get contract details using centralized system."""
        try:
            system = self.get_system()
            contracts = system.load_contracts()
            
            for category_name, category_data in contracts.get("contracts", {}).items():
                for contract in category_data.get("contracts", []):
                    if contract.get("contract_id") == contract_id:
                        return contract
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get contract details: {e}")
            return None
