"""
Database Auditor - Database structure analysis and validation.

This module handles database structure auditing, file analysis, and validation.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .models import FileInfo, StructureValidation, MetadataConsistency


class DatabaseAuditor:
    """Handles database structure auditing and validation."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def analyze_file(self, filepath: Path) -> FileInfo:
        """Analyze a file for existence, readability, and JSON validity."""
        try:
            exists = filepath.exists()
            if not exists:
                return FileInfo(
                    exists=False,
                    readable=False,
                    valid_json=False,
                    size=0,
                    last_modified=None,
                    error_message="File does not exist"
                )
            
            # Check readability
            try:
                with open(filepath, 'r') as f:
                    content = f.read()
                readable = True
                size = len(content)
            except Exception as e:
                return FileInfo(
                    exists=True,
                    readable=False,
                    valid_json=False,
                    size=0,
                    last_modified=None,
                    error_message=f"File not readable: {str(e)}"
                )
            
            # Check JSON validity
            try:
                json.loads(content)
                valid_json = True
                error_message = None
            except json.JSONDecodeError as e:
                valid_json = False
                error_message = f"Invalid JSON: {str(e)}"
            
            # Get last modified time
            try:
                last_modified = datetime.fromtimestamp(filepath.stat().st_mtime)
            except Exception:
                last_modified = None
            
            return FileInfo(
                exists=True,
                readable=readable,
                valid_json=valid_json,
                size=size,
                last_modified=last_modified,
                error_message=error_message
            )
            
        except Exception as e:
            return FileInfo(
                exists=False,
                readable=False,
                valid_json=False,
                size=0,
                last_modified=None,
                error_message=f"Analysis failed: {str(e)}"
            )
    
    def validate_task_list_structure(self, task_list: Dict[str, Any]) -> StructureValidation:
        """Validate the structure of the task list."""
        validation_errors = []
        missing_fields = []
        data_type_errors = []
        
        if not isinstance(task_list, dict):
            validation_errors.append("Task list is not a dictionary")
            return StructureValidation(
                total_contracts=0,
                valid_contracts=0,
                invalid_contracts=0,
                missing_fields=missing_fields,
                data_type_errors=data_type_errors,
                validation_errors=validation_errors
            )
        
        # Check for required top-level fields
        required_fields = ["contracts", "metadata", "version"]
        for field in required_fields:
            if field not in task_list:
                missing_fields.append(f"Missing required field: {field}")
        
        # Validate contracts array
        contracts = task_list.get("contracts", [])
        if not isinstance(contracts, list):
            data_type_errors.append("Contracts field is not a list")
            contracts = []
        
        total_contracts = len(contracts)
        valid_contracts = 0
        invalid_contracts = 0
        
        # Validate individual contracts
        for i, contract in enumerate(contracts):
            if not isinstance(contract, dict):
                invalid_contracts += 1
                validation_errors.append(f"Contract {i} is not a dictionary")
                continue
            
            # Check required contract fields
            contract_required_fields = ["id", "title", "status", "agent"]
            for field in contract_required_fields:
                if field not in contract:
                    missing_fields.append(f"Contract {i} missing field: {field}")
                    invalid_contracts += 1
                    break
            else:
                valid_contracts += 1
        
        return StructureValidation(
            total_contracts=total_contracts,
            valid_contracts=valid_contracts,
            invalid_contracts=invalid_contracts,
            missing_fields=missing_fields,
            data_type_errors=data_type_errors,
            validation_errors=validation_errors
        )
    
    def check_metadata_consistency(self, task_list: Dict[str, Any]) -> MetadataConsistency:
        """Check metadata consistency across the database."""
        inconsistencies = []
        
        # Check contract count consistency
        contracts = task_list.get("contracts", [])
        metadata = task_list.get("metadata", {})
        
        actual_count = len(contracts)
        expected_count = metadata.get("total_contracts", 0)
        contract_count_matches = actual_count == expected_count
        
        if not contract_count_matches:
            inconsistencies.append(f"Contract count mismatch: expected {expected_count}, got {actual_count}")
        
        # Check ID consistency
        id_consistency = True
        contract_ids = set()
        for contract in contracts:
            contract_id = contract.get("id")
            if contract_id in contract_ids:
                id_consistency = False
                inconsistencies.append(f"Duplicate contract ID: {contract_id}")
            contract_ids.add(contract_id)
        
        # Check status consistency
        status_consistency = True
        valid_statuses = {"PENDING", "ACTIVE", "COMPLETED", "FAILED", "CANCELLED"}
        for contract in contracts:
            status = contract.get("status")
            if status not in valid_statuses:
                status_consistency = False
                inconsistencies.append(f"Invalid status '{status}' for contract {contract.get('id')}")
        
        # Check timestamp consistency
        timestamp_consistency = True
        current_time = datetime.now()
        for contract in contracts:
            created_time = contract.get("created_at")
            if created_time:
                try:
                    if isinstance(created_time, str):
                        created_dt = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
                    else:
                        created_dt = created_time
                    
                    if created_dt > current_time:
                        timestamp_consistency = False
                        inconsistencies.append(f"Future timestamp for contract {contract.get('id')}")
                except Exception:
                    timestamp_consistency = False
                    inconsistencies.append(f"Invalid timestamp format for contract {contract.get('id')}")
        
        return MetadataConsistency(
            contract_count_matches=contract_count_matches,
            id_consistency=id_consistency,
            status_consistency=status_consistency,
            timestamp_consistency=timestamp_consistency,
            inconsistencies=inconsistencies
        )
    
    def audit_database_structure(self, task_list_path: Path, meeting_path: Path) -> Dict[str, Any]:
        """Perform comprehensive database structure audit."""
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
            ("task_list.json", task_list_path),
            ("meeting.json", meeting_path)
        ]
        
        for filename, filepath in files_to_check:
            file_info = self.analyze_file(filepath)
            audit_results["file_analysis"][filename] = file_info.__dict__
            
            if not file_info.exists:
                audit_results["critical_issues"].append(f"CRITICAL: {filename} not found!")
            elif not file_info.readable:
                audit_results["critical_issues"].append(f"CRITICAL: {filename} not readable!")
            elif not file_info.valid_json:
                audit_results["critical_issues"].append(f"CRITICAL: {filename} contains invalid JSON!")
        
        # Structure validation
        if task_list_path.exists() and task_list_path.is_file():
            try:
                with open(task_list_path, 'r') as f:
                    task_list = json.load(f)
                
                structure_validation = self.validate_task_list_structure(task_list)
                audit_results["structure_validation"] = structure_validation.__dict__
                
                metadata_consistency = self.check_metadata_consistency(task_list)
                audit_results["metadata_consistency"] = metadata_consistency.__dict__
                
            except Exception as e:
                audit_results["critical_issues"].append(f"CRITICAL: Failed to load task list: {str(e)}")
        
        return audit_results
