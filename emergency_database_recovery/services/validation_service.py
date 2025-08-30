#!/usr/bin/env python3
"""
Validation Service - Emergency Database Recovery System
Provides data validation and integrity checking functionality
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime


class ValidationService:
    """Data validation and integrity checking service"""
    
    def __init__(self):
        self.validation_rules = {
            "json_files": {
                "required_fields": ["timestamp", "version"],
                "max_file_size_mb": 10,
                "encoding": "utf-8"
            },
            "database_files": {
                "required_structure": ["contracts", "tasks", "status"],
                "backup_required": True,
                "integrity_checks": ["checksum", "schema_validation"]
            }
        }
    
    def validate_json_file(self, filepath: Path) -> Dict[str, Any]:
        """Validate JSON file for structure, content, and integrity"""
        validation_result = {
            "valid": False,
            "errors": [],
            "warnings": [],
            "file_size_mb": 0,
            "checksum": None,
            "schema_valid": False,
            "content_valid": False
        }
        
        try:
            # Check file existence and size
            if not filepath.exists():
                validation_result["errors"].append("File does not exist")
                return validation_result
            
            file_size = filepath.stat().st_size
            validation_result["file_size_mb"] = file_size / (1024 * 1024)
            
            if validation_result["file_size_mb"] > self.validation_rules["json_files"]["max_file_size_mb"]:
                validation_result["warnings"].append(
                    f"File size ({validation_result['file_size_mb']:.2f}MB) exceeds recommended limit"
                )
            
            # Read and parse JSON
            with open(filepath, 'r', encoding=self.validation_rules["json_files"]["encoding"]) as f:
                content = f.read()
                
                # Calculate checksum
                validation_result["checksum"] = hashlib.md5(content.encode()).hexdigest()
                
                # Parse JSON
                try:
                    data = json.loads(content)
                    validation_result["content_valid"] = True
                except json.JSONDecodeError as e:
                    validation_result["errors"].append(f"Invalid JSON: {str(e)}")
                    return validation_result
                
                # Validate required fields
                for field in self.validation_rules["json_files"]["required_fields"]:
                    if field not in data:
                        validation_result["warnings"].append(f"Missing recommended field: {field}")
                
                # Schema validation for specific file types
                if "contracts" in str(filepath).lower():
                    validation_result["schema_valid"] = self._validate_contract_schema(data)
                elif "task" in str(filepath).lower():
                    validation_result["schema_valid"] = self._validate_task_schema(data)
                elif "status" in str(filepath).lower():
                    validation_result["schema_valid"] = self._validate_status_schema(data)
                
                validation_result["valid"] = len(validation_result["errors"]) == 0
                
        except Exception as e:
            validation_result["errors"].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    def validate_database_integrity(self, database_files: List[Path]) -> Dict[str, Any]:
        """Validate overall database integrity across multiple files"""
        integrity_result = {
            "overall_integrity": False,
            "files_validated": 0,
            "files_with_issues": 0,
            "critical_issues": 0,
            "cross_reference_issues": [],
            "backup_status": {},
            "recommendations": []
        }
        
        validation_results = {}
        
        # Validate each file individually
        for filepath in database_files:
            if filepath.suffix == '.json':
                result = self.validate_json_file(filepath)
                validation_results[str(filepath)] = result
                integrity_result["files_validated"] += 1
                
                if not result["valid"]:
                    integrity_result["files_with_issues"] += 1
                    if len(result["errors"]) > 0:
                        integrity_result["critical_issues"] += 1
        
        # Check cross-references between files
        integrity_result["cross_reference_issues"] = self._check_cross_references(validation_results)
        
        # Check backup status
        integrity_result["backup_status"] = self._check_backup_status(database_files)
        
        # Generate recommendations
        integrity_result["recommendations"] = self._generate_recommendations(validation_results)
        
        # Overall integrity assessment
        integrity_result["overall_integrity"] = (
            integrity_result["critical_issues"] == 0 and
            integrity_result["files_with_issues"] == 0
        )
        
        return integrity_result
    
    def _validate_contract_schema(self, data: Dict[str, Any]) -> bool:
        """Validate contract data schema"""
        required_fields = ["contract_id", "title", "category", "difficulty"]
        return all(field in data for field in required_fields)
    
    def _validate_task_schema(self, data: Dict[str, Any]) -> bool:
        """Validate task data schema"""
        required_fields = ["task_id", "title", "status", "assigned_to"]
        return all(field in data for field in required_fields)
    
    def _validate_status_schema(self, data: Dict[str, Any]) -> bool:
        """Validate status data schema"""
        required_fields = ["agent_id", "current_contract", "progress", "last_updated"]
        return all(field in data for field in required_fields)
    
    def _check_cross_references(self, validation_results: Dict[str, Any]) -> List[str]:
        """Check for cross-reference issues between files"""
        issues = []
        # Implementation for cross-reference validation
        # This would check for consistency between related files
        return issues
    
    def _check_backup_status(self, database_files: List[Path]) -> Dict[str, Any]:
        """Check backup status for database files"""
        return {}
    
    def _generate_recommendations(self, validation_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        for filepath, result in validation_results.items():
            if not result["valid"]:
                recommendations.append(f"Fix critical issues in {filepath}")
            elif len(result["warnings"]) > 0:
                recommendations.append(f"Address warnings in {filepath}")
        
        return recommendations
