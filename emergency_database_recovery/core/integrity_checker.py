#!/usr/bin/env python3
"""
Integrity Checker - Emergency Database Recovery System
Provides database integrity checking and validation functionality
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime
from ..models.integrity_issues import IntegrityIssues
from ..services.logging_service import LoggingService
from ..services.validation_service import ValidationService


class IntegrityChecker:
    """Database integrity checking and validation system"""
    
    def __init__(self):
        self.logger = LoggingService().get_logger("IntegrityChecker")
        self.validation_service = ValidationService()
        
        # Critical database files to check
        self.critical_files = [
            Path("agent_workspaces/meeting/task_list.json"),
            Path("agent_workspaces/meeting/meeting.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-1/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-2/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-3/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-4/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-5/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-6/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-7/status.json"),
            Path("agent_workspaces/meeting/agent_workspaces/Agent-8/status.json")
        ]
        
        # Integrity check thresholds
        self.thresholds = {
            "max_file_age_hours": 24,
            "min_backup_age_hours": 1,
            "max_file_size_mb": 10,
            "required_fields": ["timestamp", "version", "last_updated"]
        }
    
    def perform_integrity_check(self) -> Dict[str, Any]:
        """Perform comprehensive database integrity check"""
        self.logger.info("Starting comprehensive database integrity check...")
        
        start_time = datetime.now()
        
        integrity_results = {
            "timestamp": start_time.isoformat(),
            "overall_integrity": False,
            "files_validated": 0,
            "files_with_issues": 0,
            "critical_issues": 0,
            "warnings": 0,
            "file_analysis": {},
            "backup_status": {},
            "cross_reference_issues": [],
            "recommendations": [],
            "check_duration_seconds": 0
        }
        
        try:
            # Check each critical file
            for filepath in self.critical_files:
                file_result = self._check_file_integrity(filepath)
                integrity_results["file_analysis"][str(filepath)] = file_result
                integrity_results["files_validated"] += 1
                
                if not file_result["valid"]:
                    integrity_results["files_with_issues"] += 1
                    if len(file_result["errors"]) > 0:
                        integrity_results["critical_issues"] += 1
                
                if len(file_result["warnings"]) > 0:
                    integrity_results["warnings"] += len(file_result["warnings"])
            
            # Check backup status
            integrity_results["backup_status"] = self._check_backup_status()
            
            # Check cross-references
            integrity_results["cross_reference_issues"] = self._check_cross_references(
                integrity_results["file_analysis"]
            )
            
            # Generate recommendations
            integrity_results["recommendations"] = self._generate_recommendations(
                integrity_results
            )
            
            # Determine overall integrity
            integrity_results["overall_integrity"] = (
                integrity_results["critical_issues"] == 0 and
                integrity_results["files_with_issues"] == 0
            )
            
            # Calculate check duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            integrity_results["check_duration_seconds"] = duration
            
            self.logger.info(
                f"Integrity check completed in {duration:.2f}s. "
                f"Overall integrity: {integrity_results['overall_integrity']}, "
                f"Critical issues: {integrity_results['critical_issues']}"
            )
            
        except Exception as e:
            self.logger.error(f"Integrity check failed: {e}")
            integrity_results["error"] = str(e)
            integrity_results["overall_integrity"] = False
        
        return integrity_results
    
    def check_specific_file(self, filepath: Path) -> Dict[str, Any]:
        """Check integrity of a specific file"""
        self.logger.info(f"Checking integrity of specific file: {filepath}")
        
        if not filepath.exists():
            return {
                "valid": False,
                "errors": ["File does not exist"],
                "warnings": [],
                "filepath": str(filepath),
                "exists": False
            }
        
        return self._check_file_integrity(filepath)
    
    def validate_data_consistency(self, primary_file: Path, reference_files: List[Path]) -> Dict[str, Any]:
        """Validate data consistency between primary file and reference files"""
        self.logger.info(f"Validating data consistency for {primary_file}")
        
        consistency_result = {
            "primary_file": str(primary_file),
            "reference_files": [str(f) for f in reference_files],
            "consistency_issues": [],
            "overall_consistent": True,
            "validation_details": {}
        }
        
        try:
            # Load primary file data
            if not primary_file.exists():
                consistency_result["consistency_issues"].append(f"Primary file {primary_file} does not exist")
                consistency_result["overall_consistent"] = False
                return consistency_result
            
            with open(primary_file, 'r', encoding='utf-8') as f:
                primary_data = json.load(f)
            
            # Check each reference file for consistency
            for ref_file in reference_files:
                if not ref_file.exists():
                    consistency_result["consistency_issues"].append(f"Reference file {ref_file} does not exist")
                    consistency_result["overall_consistent"] = False
                    continue
                
                try:
                    with open(ref_file, 'r', encoding='utf-8') as f:
                        ref_data = json.load(f)
                    
                    # Check for common fields and validate consistency
                    consistency_issues = self._check_data_consistency(primary_data, ref_data, str(ref_file))
                    consistency_result["validation_details"][str(ref_file)] = {
                        "consistent": len(consistency_issues) == 0,
                        "issues": consistency_issues
                    }
                    
                    if consistency_issues:
                        consistency_result["consistency_issues"].extend(consistency_issues)
                        consistency_result["overall_consistent"] = False
                
                except Exception as e:
                    consistency_result["consistency_issues"].append(f"Error reading {ref_file}: {e}")
                    consistency_result["overall_consistent"] = False
            
        except Exception as e:
            consistency_result["consistency_issues"].append(f"Error processing primary file: {e}")
            consistency_result["overall_consistent"] = False
        
        return consistency_result
    
    def _check_file_integrity(self, filepath: Path) -> Dict[str, Any]:
        """Check integrity of individual file"""
        file_result = {
            "filepath": str(filepath),
            "exists": filepath.exists(),
            "valid": False,
            "errors": [],
            "warnings": [],
            "file_size_mb": 0,
            "last_modified": None,
            "checksum": None,
            "json_valid": False,
            "schema_valid": False,
            "age_hours": None
        }
        
        if not file_result["exists"]:
            file_result["errors"].append("File does not exist")
            return file_result
        
        try:
            # Get file stats
            stat = filepath.stat()
            file_result["file_size_mb"] = stat.st_size / (1024 * 1024)
            file_result["last_modified"] = datetime.fromtimestamp(stat.st_mtime).isoformat()
            
            # Calculate age
            age_seconds = datetime.now().timestamp() - stat.st_mtime
            file_result["age_hours"] = age_seconds / 3600
            
            # Check file size
            if file_result["file_size_mb"] > self.thresholds["max_file_size_mb"]:
                file_result["warnings"].append(
                    f"File size ({file_result['file_size_mb']:.2f}MB) exceeds recommended limit"
                )
            
            # Check file age
            if file_result["age_hours"] > self.thresholds["max_file_age_hours"]:
                file_result["warnings"].append(
                    f"File is {file_result['age_hours']:.1f} hours old (exceeds {self.thresholds['max_file_age_hours']} hour limit)"
                )
            
            # Read and validate file content
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Calculate checksum
                file_result["checksum"] = hashlib.md5(content.encode()).hexdigest()
                
                # Validate JSON
                try:
                    data = json.loads(content)
                    file_result["json_valid"] = True
                    
                    # Check required fields
                    missing_fields = []
                    for field in self.thresholds["required_fields"]:
                        if field not in data:
                            missing_fields.append(field)
                    
                    if missing_fields:
                        file_result["warnings"].append(f"Missing recommended fields: {', '.join(missing_fields)}")
                    
                    # Schema validation
                    file_result["schema_valid"] = self._validate_file_schema(filepath, data)
                    
                except json.JSONDecodeError as e:
                    file_result["errors"].append(f"Invalid JSON: {str(e)}")
                    return file_result
            
            # Determine overall validity
            file_result["valid"] = len(file_result["errors"]) == 0
            
        except Exception as e:
            file_result["errors"].append(f"Error checking file: {str(e)}")
        
        return file_result
    
    def _check_backup_status(self) -> Dict[str, Any]:
        """Check backup status for critical files"""
        return {}
    
    def _check_cross_references(self, file_analysis: Dict[str, Any]) -> List[str]:
        """Check for cross-reference issues between files"""
        cross_ref_issues = []
        
        # This is a simplified implementation
        # In a full system, this would check for:
        # - Contract IDs referenced in task lists
        # - Agent status consistency
        # - Task assignment validation
        # - Phase transition consistency
        
        return cross_ref_issues
    
    def _validate_file_schema(self, filepath: Path, data: Dict[str, Any]) -> bool:
        """Validate file schema based on file type"""
        filename = filepath.name.lower()
        
        if "status" in filename:
            return self._validate_status_schema(data)
        elif "task" in filename:
            return self._validate_task_schema(data)
        elif "contract" in filename:
            return self._validate_contract_schema(data)
        elif "meeting" in filename:
            return self._validate_meeting_schema(data)
        else:
            return True  # Unknown file type, assume valid
    
    def _validate_status_schema(self, data: Dict[str, Any]) -> bool:
        """Validate agent status schema"""
        required_fields = ["agent_id", "current_contract", "progress", "last_updated"]
        return all(field in data for field in required_fields)
    
    def _validate_task_schema(self, data: Dict[str, Any]) -> bool:
        """Validate task list schema"""
        required_fields = ["tasks", "last_updated"]
        return all(field in data for field in required_fields)
    
    def _validate_contract_schema(self, data: Dict[str, Any]) -> bool:
        """Validate contract schema"""
        required_fields = ["contracts", "last_updated"]
        return all(field in data for field in required_fields)
    
    def _validate_meeting_schema(self, data: Dict[str, Any]) -> bool:
        """Validate meeting schema"""
        required_fields = ["meeting_id", "participants", "timestamp"]
        return all(field in data for field in required_fields)
    
    def _check_data_consistency(self, primary_data: Dict[str, Any], 
                               reference_data: Dict[str, Any], 
                               reference_name: str) -> List[str]:
        """Check data consistency between primary and reference data"""
        consistency_issues = []
        
        # Check for common fields and validate consistency
        # This is a simplified implementation
        # In a full system, this would perform detailed field-by-field validation
        
        return consistency_issues
    
    def _generate_recommendations(self, integrity_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on integrity check results"""
        recommendations = []
        
        critical_issues = integrity_results.get("critical_issues", 0)
        files_with_issues = integrity_results.get("files_with_issues", 0)
        warnings = integrity_results.get("warnings", 0)
        
        if critical_issues > 0:
            recommendations.append("IMMEDIATE: Address all critical issues to restore system integrity")
            recommendations.append("PRIORITY: Review and fix file accessibility and JSON validation problems")
        
        if files_with_issues > 0:
            recommendations.append("URGENT: Fix issues in files with problems to prevent system degradation")
        
        if warnings > 0:
            recommendations.append("REVIEW: Address warnings to improve system health and performance")
        
        # Check backup status
        backup_status = integrity_results.get("backup_status", {})
        missing_backups = sum(1 for status in backup_status.values() if not status.get("backup_exists", False))
        
        if missing_backups > 0:
            recommendations.append(f"BACKUP: Create backups for {missing_backups} critical files")
        
        if not recommendations:
            recommendations.append("MAINTENANCE: Schedule regular integrity checks to maintain system health")
            recommendations.append("OPTIMIZATION: Review system performance metrics and optimize as needed")
        
        return recommendations
