#!/usr/bin/env python3
"""
Database Audit Core Module
==========================

Core functionality for database auditing operations.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Tuple
from datetime import datetime
from dataclasses import dataclass


@dataclass
class AuditResult:
    """Container for audit results"""
    timestamp: str
    file_analysis: Dict[str, Any]
    structure_validation: Dict[str, Any]
    metadata_consistency: Dict[str, Any]
    critical_issues: List[str]
    warnings: List[str]
    recommendations: List[str]


@dataclass
class FileInfo:
    """Container for file analysis information"""
    exists: bool
    readable: bool
    valid_json: bool
    size_bytes: int
    last_modified: str
    content_hash: str
    json_structure: Dict[str, Any]


class DatabaseAuditCore:
    """Core database auditing functionality"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for database audit operations"""
        logger = logging.getLogger("DatabaseAuditCore")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[AUDIT] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def analyze_file(self, filepath: Path) -> FileInfo:
        """Analyze a single file for audit purposes"""
        try:
            file_info = FileInfo(
                exists=filepath.exists(),
                readable=False,
                valid_json=False,
                size_bytes=0,
                last_modified="",
                content_hash="",
                json_structure={}
            )
            
            if not file_info.exists:
                return file_info
            
            # Check readability
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    file_info.readable = True
                    file_info.size_bytes = len(content.encode('utf-8'))
                    file_info.content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            except Exception as e:
                self.logger.warning(f"File {filepath} not readable: {e}")
                return file_info
            
            # Check JSON validity
            try:
                json_data = json.loads(content)
                file_info.valid_json = True
                file_info.json_structure = self._analyze_json_structure(json_data)
            except json.JSONDecodeError as e:
                self.logger.warning(f"File {filepath} contains invalid JSON: {e}")
            
            # Get file metadata
            try:
                stat = filepath.stat()
                file_info.last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
            except Exception as e:
                self.logger.warning(f"Could not get metadata for {filepath}: {e}")
            
            return file_info
            
        except Exception as e:
            self.logger.error(f"Error analyzing file {filepath}: {e}")
            return FileInfo(
                exists=False,
                readable=False,
                valid_json=False,
                size_bytes=0,
                last_modified="",
                content_hash="",
                json_structure={}
            )
    
    def _analyze_json_structure(self, data: Any, max_depth: int = 3, current_depth: int = 0) -> Dict[str, Any]:
        """Analyze JSON structure recursively"""
        if current_depth >= max_depth:
            return {"type": type(data).__name__, "truncated": True}
        
        if isinstance(data, dict):
            return {
                "type": "dict",
                "keys": list(data.keys()),
                "key_count": len(data),
                "sample_values": {k: self._analyze_json_structure(v, max_depth, current_depth + 1) 
                                for k, v in list(data.items())[:5]}
            }
        elif isinstance(data, list):
            return {
                "type": "list",
                "length": len(data),
                "sample_items": [self._analyze_json_structure(item, max_depth, current_depth + 1) 
                               for item in data[:3]]
            }
        else:
            return {
                "type": type(data).__name__,
                "value": str(data)[:100] if data is not None else None
            }
    
    def validate_json_schema(self, data: Any, expected_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate JSON data against expected schema"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "missing_fields": [],
            "extra_fields": []
        }
        
        if not isinstance(data, dict):
            validation_result["valid"] = False
            validation_result["errors"].append("Root data is not a dictionary")
            return validation_result
        
        # Check required fields
        for field, field_info in expected_schema.items():
            if field_info.get("required", False) and field not in data:
                validation_result["valid"] = False
                validation_result["missing_fields"].append(field)
            elif field in data:
                # Type validation
                expected_type = field_info.get("type")
                if expected_type and not isinstance(data[field], expected_type):
                    validation_result["valid"] = False
                    validation_result["errors"].append(
                        f"Field '{field}' expected type {expected_type}, got {type(data[field])}"
                    )
        
        # Check for extra fields
        for field in data:
            if field not in expected_schema:
                validation_result["warnings"].append(f"Unexpected field: {field}")
                validation_result["extra_fields"].append(field)
        
        return validation_result
    
    def generate_audit_summary(self, audit_results: List[FileInfo]) -> Dict[str, Any]:
        """Generate summary of audit results"""
        total_files = len(audit_results)
        existing_files = sum(1 for f in audit_results if f.exists)
        readable_files = sum(1 for f in audit_results if f.readable)
        valid_json_files = sum(1 for f in audit_results if f.valid_json)
        
        total_size = sum(f.size_bytes for f in audit_results if f.exists)
        
        return {
            "summary": {
                "total_files": total_files,
                "existing_files": existing_files,
                "readable_files": readable_files,
                "valid_json_files": valid_json_files,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2)
            },
            "health_score": self._calculate_health_score(audit_results),
            "recommendations": self._generate_recommendations(audit_results)
        }
    
    def _calculate_health_score(self, audit_results: List[FileInfo]) -> float:
        """Calculate overall health score (0-100)"""
        if not audit_results:
            return 0.0
        
        scores = []
        for file_info in audit_results:
            score = 0.0
            if file_info.exists:
                score += 25.0
            if file_info.readable:
                score += 25.0
            if file_info.valid_json:
                score += 50.0
            scores.append(score)
        
        return sum(scores) / len(scores)
    
    def _generate_recommendations(self, audit_results: List[FileInfo]) -> List[str]:
        """Generate recommendations based on audit results"""
        recommendations = []
        
        missing_files = [f for f in audit_results if not f.exists]
        if missing_files:
            recommendations.append(f"Restore {len(missing_files)} missing files")
        
        unreadable_files = [f for f in audit_results if f.exists and not f.readable]
        if unreadable_files:
            recommendations.append(f"Fix permissions for {len(unreadable_files)} unreadable files")
        
        invalid_json_files = [f for f in audit_results if f.readable and not f.valid_json]
        if invalid_json_files:
            recommendations.append(f"Repair {len(invalid_json_files)} files with invalid JSON")
        
        if not recommendations:
            recommendations.append("All files are healthy - no action required")
        
        return recommendations
