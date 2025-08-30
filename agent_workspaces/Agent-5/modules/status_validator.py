#!/usr/bin/env python3
"""
Status Validator Module
Extracted from EMERGENCY_RESTORE_004_DATABASE_AUDIT.py
Handles contract status validation and consistency checks
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class StatusValidator:
    """Contract status validator for database integrity"""
    
    def __init__(self, task_list_path: Path):
        self.task_list_path = task_list_path
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for status validator"""
        logger = logging.getLogger("StatusValidator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[VALIDATOR] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def validate_contract_status_accuracy(self) -> Dict[str, Any]:
        """Validate the accuracy of contract statuses"""
        self.logger.info("Validating contract status accuracy...")
        
        validation_results = {
            "timestamp": datetime.now().isoformat(),
            "status_validation": {},
            "status_issues": [],
            "recommendations": []
        }
        
        try:
            with open(self.task_list_path, 'r') as f:
                task_list = json.load(f)
                
            if "contracts" in task_list:
                for category, category_data in task_list["contracts"].items():
                    if "contracts" in category_data and isinstance(category_data["contracts"], list):
                        for contract in category_data["contracts"]:
                            contract_id = contract.get("contract_id", "UNKNOWN")
                            status = contract.get("status", "MISSING_STATUS")
                            
                            # Validate status field
                            if status not in ["AVAILABLE", "CLAIMED", "COMPLETED"]:
                                validation_results["status_issues"].append(
                                    f"Invalid status '{status}' for contract {contract_id}"
                                )
                                
                            # Check for missing required fields based on status
                            if status == "CLAIMED":
                                if "claimed_by" not in contract:
                                    validation_results["status_issues"].append(
                                        f"Missing 'claimed_by' for claimed contract {contract_id}"
                                    )
                                if "claimed_at" not in contract:
                                    validation_results["status_issues"].append(
                                        f"Missing 'claimed_at' for claimed contract {contract_id}"
                                    )
                                    
                            elif status == "COMPLETED":
                                if "completed_at" not in contract:
                                    validation_results["status_issues"].append(
                                        f"Missing 'completed_at' for completed contract {contract_id}"
                                    )
                                if "final_deliverables" not in contract:
                                    validation_results["status_issues"].append(
                                        f"Missing 'final_deliverables' for completed contract {contract_id}"
                                    )
                                    
                            # Check for logical inconsistencies
                            if status == "COMPLETED" and "claimed_by" not in contract:
                                validation_results["status_issues"].append(
                                    f"Completed contract {contract_id} missing 'claimed_by' field"
                                )
                                
                            if status == "AVAILABLE" and "claimed_by" in contract:
                                validation_results["status_issues"].append(
                                    f"Available contract {contract_id} has 'claimed_by' field (should be removed)"
                                )
                                
        except Exception as e:
            validation_results["status_issues"].append(f"Failed to validate contract statuses: {e}")
            
        # Generate recommendations
        if validation_results["status_issues"]:
            validation_results["recommendations"].append(
                "Implement automated status validation to prevent future inconsistencies"
            )
            validation_results["recommendations"].append(
                "Add status transition validation rules"
            )
            validation_results["recommendations"].append(
                "Implement contract state machine with validation"
            )
            
        return validation_results
