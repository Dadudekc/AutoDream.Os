"""
Contract persistence layer for the contract claiming system.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any


class ContractPersistence:
    """Handles loading and saving of contract data."""
    
    def __init__(self, task_list_path: str):
        self.task_list_path = Path(task_list_path)
    
    def load_contracts(self) -> Dict[str, Any]:
        """Load contracts from the task list file."""
        try:
            if self.task_list_path.exists():
                with open(self.task_list_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"❌ Task list not found: {self.task_list_path}")
                return {"contracts": {}}
        except Exception as e:
            print(f"❌ Error loading contracts: {e}")
            return {"contracts": {}}
    
    def save_contracts(self, contracts: Dict[str, Any]) -> bool:
        """Save contracts to the task list file."""
        try:
            # Ensure directory exists
            self.task_list_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.task_list_path, 'w', encoding='utf-8') as f:
                json.dump(contracts, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error saving contracts: {e}")
            return False
    
    def backup_contracts(self, contracts: Dict[str, Any], backup_suffix: str = None) -> bool:
        """Create a backup of the current contracts."""
        try:
            if backup_suffix is None:
                from datetime import datetime
                backup_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            backup_path = self.task_list_path.with_suffix(f".backup_{backup_suffix}.json")
            
            with open(backup_path, 'w', encoding='utf-8') as f:
                json.dump(contracts, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Backup created: {backup_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def validate_file_structure(self, contracts: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the structure of the contracts file."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        if not isinstance(contracts, dict):
            validation_result["valid"] = False
            validation_result["errors"].append("Root must be a dictionary")
            return validation_result
        
        if "contracts" not in contracts:
            validation_result["valid"] = False
            validation_result["errors"].append("Missing 'contracts' key")
            return validation_result
        
        contracts_section = contracts.get("contracts", {})
        if not isinstance(contracts_section, dict):
            validation_result["valid"] = False
            validation_result["errors"].append("'contracts' section must be a dictionary")
            return validation_result
        
        # Check each contract category
        for category, category_data in contracts_section.items():
            if isinstance(category_data, dict):
                if 'contracts' in category_data:
                    contracts_list = category_data.get('contracts', [])
                    if not isinstance(contracts_list, list):
                        validation_result["warnings"].append(f"Category '{category}' contracts should be a list")
                    else:
                        for i, contract in enumerate(contracts_list):
                            if not isinstance(contract, dict):
                                validation_result["warnings"].append(f"Contract {i} in category '{category}' should be a dictionary")
                            elif 'contract_id' not in contract:
                                validation_result["warnings"].append(f"Contract {i} in category '{category}' missing contract_id")
            elif isinstance(category_data, list):
                for i, contract in enumerate(category_data):
                    if not isinstance(contract, dict):
                        validation_result["warnings"].append(f"Contract {i} in category '{category}' should be a dictionary")
                    elif 'contract_id' not in contract:
                        validation_result["warnings"].append(f"Contract {i} in category '{category}' missing contract_id")
            else:
                validation_result["warnings"].append(f"Category '{category}' should be a dictionary or list")
        
        return validation_result
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about the contracts file."""
        try:
            if not self.task_list_path.exists():
                return {
                    "exists": False,
                    "size": 0,
                    "last_modified": None,
                    "path": str(self.task_list_path)
                }
            
            stat = self.task_list_path.stat()
            return {
                "exists": True,
                "size": stat.st_size,
                "last_modified": stat.st_mtime,
                "path": str(self.task_list_path),
                "readable": os.access(self.task_list_path, os.R_OK),
                "writable": os.access(self.task_list_path, os.W_OK)
            }
        except Exception as e:
            return {
                "exists": False,
                "size": 0,
                "last_modified": None,
                "path": str(self.task_list_path),
                "error": str(e)
            }
    
    def create_sample_contracts(self) -> Dict[str, Any]:
        """Create a sample contracts structure for testing."""
        sample_contracts = {
            "contracts": {
                "Modularization": {
                    "category": "Modularization",
                    "manager": "Agent-1",
                    "contracts": [
                        {
                            "contract_id": "MODULAR-001",
                            "title": "Monolithic File Modularization",
                            "description": "Modularize files over 500 lines",
                            "category": "Modularization",
                            "points": 500,
                            "status": "AVAILABLE"
                        }
                    ]
                }
            }
        }
        
        if self.save_contracts(sample_contracts):
            return {"success": True, "message": "Sample contracts created"}
        else:
            return {"success": False, "error": "Failed to create sample contracts"}
