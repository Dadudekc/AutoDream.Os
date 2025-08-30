#!/usr/bin/env python3
"""
Database Auditor Service
Contract: EMERGENCY-RESTORE-004
Agent: Agent-5
Description: Service for auditing database structure and validation
"""

import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from ..models.audit_models import AuditResult, FileAnalysis, StructureValidation, MetadataConsistency

class DatabaseAuditor:
    """Service for auditing database structure and validation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def audit_database_structure(self, task_list_path: Path, meeting_path: Path) -> AuditResult:
        """Audit the overall structure of the contract database"""
        self.logger.info("Auditing database structure...")
        
        # File existence and accessibility check
        files_to_check = [
            ("task_list.json", task_list_path),
            ("meeting.json", meeting_path)
        ]
        
        file_analysis = {}
        critical_issues = []
        
        for filename, filepath in files_to_check:
            file_info = self._analyze_file(filepath)
            file_analysis[filename] = file_info
            
            if not file_info.exists:
                critical_issues.append(f"CRITICAL: {filename} not found!")
            elif not file_info.readable:
                critical_issues.append(f"CRITICAL: {filename} not readable!")
            elif not file_info.valid_json:
                critical_issues.append(f"CRITICAL: {filename} contains invalid JSON!")
        
        # Structure validation
        structure_validation = self._validate_task_list_structure(task_list_path)
        
        # Metadata consistency
        metadata_consistency = self._validate_metadata_consistency(files_to_check)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(critical_issues, structure_validation)
        
        return AuditResult(
            timestamp=datetime.now(),
            file_analysis=file_analysis,
            structure_validation=structure_validation,
            metadata_consistency=metadata_consistency,
            critical_issues=critical_issues,
            recommendations=recommendations
        )
    
    def _analyze_file(self, filepath: Path) -> FileAnalysis:
        """Analyze a single file for accessibility and validity"""
        file_info = FileAnalysis(
            filename=filepath.name,
            exists=filepath.exists(),
            readable=False,
            writable=False,
            valid_json=False,
            size_bytes=0
        )
        
        if not file_info.exists:
            return file_info
        
        try:
            # Check readability
            file_info.readable = filepath.is_file() and filepath.stat().st_size > 0
            
            # Check writability
            file_info.writable = filepath.is_file() and filepath.stat().st_mode & 0o200
            
            # Get file size
            file_info.size_bytes = filepath.stat().st_size
            
            # Get last modified time
            file_info.last_modified = datetime.fromtimestamp(filepath.stat().st_mtime)
            
            # Validate JSON
            if file_info.readable:
                try:
                    with open(filepath, 'r') as f:
                        json.load(f)
                    file_info.valid_json = True
                    
                    # Calculate checksum
                    with open(filepath, 'rb') as f:
                        content = f.read()
                        file_info.checksum = hashlib.md5(content).hexdigest()
                        
                except json.JSONDecodeError as e:
                    file_info.error_message = f"Invalid JSON: {e}"
                except Exception as e:
                    file_info.error_message = f"Error reading file: {e}"
                    
        except Exception as e:
            file_info.error_message = f"Error analyzing file: {e}"
        
        return file_info
    
    def _validate_task_list_structure(self, task_list_path: Path) -> StructureValidation:
        """Validate the structure of the task list"""
        if not task_list_path.exists() or not task_list_path.is_file():
            return StructureValidation(
                total_contracts=0,
                valid_contracts=0,
                invalid_contracts=0
            )
        
        try:
            with open(task_list_path, 'r') as f:
                task_list = json.load(f)
            
            total_contracts = len(task_list.get('contracts', []))
            valid_contracts = 0
            invalid_contracts = 0
            missing_required_fields = []
            duplicate_contract_ids = []
            invalid_status_values = []
            structure_errors = []
            
            # Check each contract
            contract_ids = []
            for contract in task_list.get('contracts', []):
                contract_valid = True
                
                # Check required fields
                required_fields = ['contract_id', 'title', 'status']
                for field in required_fields:
                    if field not in contract:
                        missing_required_fields.append(f"Contract missing {field}")
                        contract_valid = False
                
                # Check contract ID uniqueness
                if 'contract_id' in contract:
                    if contract['contract_id'] in contract_ids:
                        duplicate_contract_ids.append(contract['contract_id'])
                        contract_valid = False
                    else:
                        contract_ids.append(contract['contract_id'])
                
                # Check status values
                if 'status' in contract:
                    valid_statuses = ['AVAILABLE', 'CLAIMED', 'ASSIGNED', 'IN_PROGRESS', 'COMPLETED', 'FAILED']
                    if contract['status'] not in valid_statuses:
                        invalid_status_values.append(f"Invalid status: {contract['status']}")
                        contract_valid = False
                
                if contract_valid:
                    valid_contracts += 1
                else:
                    invalid_contracts += 1
            
            return StructureValidation(
                total_contracts=total_contracts,
                valid_contracts=valid_contracts,
                invalid_contracts=invalid_contracts,
                missing_required_fields=missing_required_fields,
                duplicate_contract_ids=duplicate_contract_ids,
                invalid_status_values=invalid_status_values,
                structure_errors=structure_errors
            )
            
        except Exception as e:
            self.logger.error(f"Error validating task list structure: {e}")
            return StructureValidation(
                total_contracts=0,
                valid_contracts=0,
                invalid_contracts=0,
                structure_errors=[f"Error during validation: {e}"]
            )
    
    def _validate_metadata_consistency(self, files_to_check: List[tuple]) -> MetadataConsistency:
        """Validate metadata consistency across files"""
        total_files = len(files_to_check)
        consistent_files = 0
        inconsistent_files = 0
        timestamp_discrepancies = []
        version_mismatches = []
        metadata_errors = []
        
        # Check for basic consistency
        for filename, filepath in files_to_check:
            if filepath.exists() and filepath.is_file():
                try:
                    # Basic file validation
                    if filepath.stat().st_size > 0:
                        consistent_files += 1
                    else:
                        inconsistent_files += 1
                        metadata_errors.append(f"{filename} is empty")
                except Exception as e:
                    inconsistent_files += 1
                    metadata_errors.append(f"Error checking {filename}: {e}")
            else:
                inconsistent_files += 1
                metadata_errors.append(f"{filename} does not exist")
        
        return MetadataConsistency(
            total_files=total_files,
            consistent_files=consistent_files,
            inconsistent_files=inconsistent_files,
            timestamp_discrepancies=timestamp_discrepancies,
            version_mismatches=version_mismatches,
            metadata_errors=metadata_errors
        )
    
    def _generate_recommendations(self, critical_issues: List[str], 
                                structure_validation: StructureValidation) -> List[str]:
        """Generate recommendations based on audit results"""
        recommendations = []
        
        if critical_issues:
            recommendations.append("Immediate action required to resolve critical issues")
            recommendations.append("Verify file permissions and accessibility")
            recommendations.append("Check for file corruption or system issues")
        
        if structure_validation.invalid_contracts > 0:
            recommendations.append("Review and fix invalid contract structures")
            recommendations.append("Implement contract validation rules")
        
        if structure_validation.duplicate_contract_ids:
            recommendations.append("Resolve duplicate contract IDs")
            recommendations.append("Implement unique constraint validation")
        
        if structure_validation.invalid_status_values:
            recommendations.append("Standardize contract status values")
            recommendations.append("Update status validation rules")
        
        if not recommendations:
            recommendations.append("Database structure appears healthy")
            recommendations.append("Continue with regular maintenance")
        
        return recommendations
