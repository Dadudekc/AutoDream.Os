#!/usr/bin/env python3
"""
Database Audit Module
Extracted from EMERGENCY_RESTORE_004_DATABASE_AUDIT.py
Handles database structure analysis and validation
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class DatabaseAuditor:
    """Database structure auditor for contract database"""

    def __init__(self, task_list_path: Path, meeting_path: Path):
        self.task_list_path = task_list_path
        self.meeting_path = meeting_path
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for database auditor"""
        logger = logging.getLogger("DatabaseAuditor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[AUDIT] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
        
    def audit_database_structure(self) -> Dict[str, Any]:
        """Audit the overall structure of the contract database"""
        self.logger.info("Auditing database structure...")
        
        audit_results = {
            "timestamp": datetime.now().isoformat(),
            "file_analysis": {},
            "structure_validation": {},
            "metadata_consistency": {},
            "critical_issues": []
        }
        
        # File existence and accessibility check
        files_to_check = [
            ("task_list.json", self.task_list_path),
            ("meeting.json", self.meeting_path)
        ]
        
        for filename, filepath in files_to_check:
            file_info = self._analyze_file(filepath)
            audit_results["file_analysis"][filename] = file_info
            
            if not file_info["exists"]:
                audit_results["critical_issues"].append(f"CRITICAL: {filename} not found!")
            elif not file_info["readable"]:
                audit_results["critical_issues"].append(f"CRITICAL: {filename} not readable!")
            elif not file_info["valid_json"]:
                audit_results["critical_issues"].append(f"CRITICAL: {filename} contains invalid JSON!")
                
        # Structure validation
        if self.task_list_path.exists() and self.task_list_path.is_file():
            try:
                with open(self.task_list_path, 'r') as f:
                    task_list = json.load(f)
                    
                audit_results["structure_validation"] = self._validate_task_list_structure(task_list)
                
            except Exception as e:
                audit_results["critical_issues"].append(f"CRITICAL: Failed to parse task_list.json: {e}")
                
        # Metadata consistency check
        audit_results["metadata_consistency"] = self._check_metadata_consistency()
        
        return audit_results
        
    def _analyze_file(self, filepath: Path) -> Dict[str, Any]:
        """Analyze a single file for existence, readability, and JSON validity"""
        file_info = {
            "exists": filepath.exists(),
            "readable": False,
            "valid_json": False,
            "size_bytes": 0,
            "last_modified": None,
            "hash": None
        }
        
        if filepath.exists():
            file_info["size_bytes"] = filepath.stat().st_size
            file_info["last_modified"] = datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
            
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                    file_info["readable"] = True
                    
                    # Validate JSON
                    json.loads(content)
                    file_info["valid_json"] = True
                    
                    # Calculate hash for integrity
                    file_info["hash"] = hashlib.md5(content.encode()).hexdigest()
                    
            except Exception as e:
                file_info["readable"] = False
                file_info["valid_json"] = False
                
        return file_info
        
    def _validate_task_list_structure(self, task_list: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the structure of the task list"""
        validation = {
            "required_fields": {},
            "contract_counts": {},
            "status_distribution": {},
            "structural_issues": []
        }
        
        # Check required fields
        required_fields = [
            "task_list_id", "timestamp", "created_by", "session_type",
            "contract_status", "total_contracts", "available_contracts",
            "claimed_contracts", "completed_contracts", "contracts"
        ]
        
        for field in required_fields:
            validation["required_fields"][field] = field in task_list
            
        # Validate contract counts
        if "total_contracts" in task_list:
            validation["contract_counts"]["declared_total"] = task_list["total_contracts"]
            
        # Count actual contracts
        actual_contracts = 0
        available_count = 0
        claimed_count = 0
        completed_count = 0
        
        if "contracts" in task_list:
            for category, category_data in task_list["contracts"].items():
                if "contracts" in category_data and isinstance(category_data["contracts"], list):
                    for contract in category_data["contracts"]:
                        actual_contracts += 1
                        
                        if "status" in contract:
                            status = contract["status"]
                            if status == "AVAILABLE":
                                available_count += 1
                            elif status == "CLAIMED":
                                claimed_count += 1
                            elif status == "COMPLETED":
                                completed_count += 1
                                
        validation["contract_counts"]["actual_total"] = actual_contracts
        validation["contract_counts"]["actual_available"] = available_count
        validation["contract_counts"]["actual_claimed"] = claimed_count
        validation["contract_counts"]["actual_completed"] = completed_count
        
        # Check for count discrepancies
        if "total_contracts" in task_list:
            if task_list["total_contracts"] != actual_contracts:
                validation["structural_issues"].append(
                    f"Contract count mismatch: declared {task_list['total_contracts']}, actual {actual_contracts}"
                )
                
        if "available_contracts" in task_list:
            if task_list["available_contracts"] != available_count:
                validation["structural_issues"].append(
                    f"Available count mismatch: declared {task_list['available_contracts']}, actual {available_count}"
                )
                
        if "claimed_contracts" in task_list:
            if task_list["claimed_contracts"] != claimed_count:
                validation["structural_issues"].append(
                    f"Claimed count mismatch: declared {task_list['claimed_contracts']}, actual {claimed_count}"
                )
                
        if "completed_contracts" in task_list:
            if task_list["completed_contracts"] != completed_count:
                validation["structural_issues"].append(
                    f"Completed count mismatch: declared {task_list['completed_contracts']}, actual {completed_count}"
                )
                
        return validation
        
    def _check_metadata_consistency(self) -> Dict[str, Any]:
        """Check metadata consistency across files"""
        metadata_check = {
            "timestamp_consistency": {},
            "contract_count_consistency": {},
            "status_consistency": {},
            "inconsistencies": []
        }
        
        try:
            # Load task list
            with open(self.task_list_path, 'r') as f:
                task_list = json.load(f)
                
            # Load meeting data
            with open(self.meeting_path, 'r') as f:
                meeting_data = json.load(f)
                
            # Check contract counts
            if "contract_system_status" in meeting_data:
                meeting_counts = meeting_data["contract_system_status"]
                
                # Compare counts
                if "total_contracts" in meeting_counts and "total_contracts" in task_list:
                    if meeting_counts["total_contracts"] != task_list["total_contracts"]:
                        metadata_check["inconsistencies"].append(
                            f"Total contract count mismatch: meeting.json shows {meeting_counts['total_contracts']}, "
                            f"task_list.json shows {task_list['total_contracts']}"
                        )
                        
                if "available" in meeting_counts and "available_contracts" in task_list:
                    if meeting_counts["available"] != task_list["available_contracts"]:
                        metadata_check["inconsistencies"].append(
                            f"Available contract count mismatch: meeting.json shows {meeting_counts['available']}, "
                            f"task_list.json shows {task_list['available_contracts']}"
                        )
                        
                if "claimed" in meeting_counts and "claimed_contracts" in task_list:
                    if meeting_counts["claimed"] != task_list["claimed_contracts"]:
                        metadata_check["inconsistencies"].append(
                            f"Claimed contract count mismatch: meeting.json shows {meeting_counts['claimed']}, "
                            f"task_list.json shows {task_list['claimed_contracts']}"
                        )
                        
                if "completed" in meeting_counts and "completed_contracts" in task_list:
                    if meeting_counts["completed"] != task_list["completed_contracts"]:
                        metadata_check["inconsistencies"].append(
                            f"Completed contract count mismatch: meeting.json shows {meeting_counts['completed']}, "
                            f"task_list.json shows {task_list['completed_contracts']}"
                        )
                        
        except Exception as e:
            metadata_check["inconsistencies"].append(f"Failed to check metadata consistency: {e}")
            
        return metadata_check
