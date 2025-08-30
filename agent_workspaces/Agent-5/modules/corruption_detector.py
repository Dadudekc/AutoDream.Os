#!/usr/bin/env python3
"""
Corruption Detector Module
Extracted from EMERGENCY_RESTORE_004_DATABASE_AUDIT.py
Handles corruption detection and data integrity scanning
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class CorruptionDetector:
    """Contract corruption detector for database integrity"""
    
    def __init__(self, task_list_path: Path):
        self.task_list_path = task_list_path
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for corruption detector"""
        logger = logging.getLogger("CorruptionDetector")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[CORRUPTION] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def scan_for_corruption(self) -> Dict[str, Any]:
        """Scan for corrupted or missing contracts"""
        self.logger.info("Scanning for corruption and missing contracts...")
        
        corruption_scan = {
            "timestamp": datetime.now().isoformat(),
            "corruption_indicators": [],
            "missing_contracts": [],
            "duplicate_contracts": [],
            "data_integrity_issues": [],
            "recovery_actions": []
        }
        
        try:
            with open(self.task_list_path, 'r') as f:
                task_list = json.load(f)
                
            if "contracts" in task_list:
                contract_ids = set()
                
                for category, category_data in task_list["contracts"].items():
                    if "contracts" in category_data and isinstance(category_data["contracts"], list):
                        for contract in category_data["contracts"]:
                            contract_id = contract.get("contract_id")
                            
                            if not contract_id:
                                corruption_scan["corruption_indicators"].append(
                                    f"Contract missing ID in category {category}"
                                )
                                continue
                                
                            # Check for duplicates
                            if contract_id in contract_ids:
                                corruption_scan["duplicate_contracts"].append(contract_id)
                            else:
                                contract_ids.add(contract_id)
                                
                            # Check for data corruption indicators
                            if self._is_contract_corrupted(contract):
                                corruption_scan["data_integrity_issues"].append({
                                    "contract_id": contract_id,
                                    "issues": self._identify_corruption_issues(contract)
                                })
                                
        except Exception as e:
            corruption_scan["corruption_indicators"].append(f"Failed to scan for corruption: {e}")
            
        # Generate recovery actions
        if corruption_scan["corruption_indicators"]:
            corruption_scan["recovery_actions"].append(
                "Implement automated corruption detection system"
            )
            corruption_scan["recovery_actions"].append(
                "Add data validation on contract creation/modification"
            )
            corruption_scan["recovery_actions"].append(
                "Implement contract backup and restore procedures"
            )
            
        return corruption_scan
        
    def _is_contract_corrupted(self, contract: Dict[str, Any]) -> bool:
        """Check if a contract appears to be corrupted"""
        corruption_indicators = [
            not contract.get("contract_id"),
            not contract.get("title"),
            not contract.get("description"),
            not contract.get("status"),
            contract.get("extra_credit_points", 0) < 0,
            contract.get("estimated_time") == "INVALID_TIME"
        ]
        
        return any(corruption_indicators)
        
    def _identify_corruption_issues(self, contract: Dict[str, Any]) -> List[str]:
        """Identify specific corruption issues in a contract"""
        issues = []
        
        if not contract.get("contract_id"):
            issues.append("Missing contract ID")
        if not contract.get("title"):
            issues.append("Missing title")
        if not contract.get("description"):
            issues.append("Missing description")
        if not contract.get("status"):
            issues.append("Missing status")
        if contract.get("extra_credit_points", 0) < 0:
            issues.append("Invalid extra credit points")
        if contract.get("estimated_time") == "INVALID_TIME":
            issues.append("Invalid estimated time")
            
        return issues
