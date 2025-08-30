#!/usr/bin/env python3
"""
Corruption Scanner - Emergency Database Recovery System
Provides database corruption detection and scanning functionality
"""

import json
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Set
from datetime import datetime
from ..models.integrity_issues import IntegrityIssues
from ..services.logging_service import LoggingService
from ..services.validation_service import ValidationService


class CorruptionScanner:
    """Database corruption detection and scanning system"""
    
    def __init__(self):
        self.logger = LoggingService().get_logger("CorruptionScanner")
        self.validation_service = ValidationService()
        
        # Corruption patterns to detect
        self.corruption_patterns = {
            "json_syntax": [
                r'[^\x00-\x7F]',  # Non-ASCII characters
                r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]',  # Control characters
                r'[^\x20-\x7E]',  # Non-printable characters
            ],
            "data_structure": [
                r'null\s*[^,}\]]',  # Malformed null values
                r'[^"]\s*:\s*[^"{\[\d]',  # Malformed key-value pairs
                r'[^,}\]]\s*[^,}\]]',  # Missing separators
            ],
            "file_corruption": [
                r'\x00{10,}',  # Multiple null bytes
                r'\xFF{10,}',  # Multiple 0xFF bytes
                r'[^\x00-\xFF]{10,}',  # Extended ASCII issues
            ]
        }
        
        # Critical file patterns for corruption scanning
        self.critical_patterns = {
            "status_files": r"status\.json$",
            "task_files": r"task.*\.json$",
            "contract_files": r"contract.*\.json$",
            "meeting_files": r"meeting.*\.json$"
        }
        
        # Corruption severity levels
        self.severity_levels = {
            "CRITICAL": "File completely unreadable or severely corrupted",
            "HIGH": "Major structural corruption affecting functionality",
            "MEDIUM": "Partial corruption with some data loss",
            "LOW": "Minor corruption with minimal impact"
        }
    
    def scan_for_corruption(self, target_directory: Optional[Path] = None) -> Dict[str, Any]:
        """Perform comprehensive corruption scan of database files"""
        if target_directory is None:
            target_directory = Path("agent_workspaces/meeting")
        
        self.logger.info(f"Starting corruption scan of {target_directory}")
        
        start_time = datetime.now()
        
        scan_results = {
            "timestamp": start_time.isoformat(),
            "target_directory": str(target_directory),
            "files_scanned": 0,
            "files_with_corruption": 0,
            "corruption_summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "corrupted_files": [],
            "corruption_details": {},
            "scan_duration_seconds": 0,
            "recommendations": []
        }
        
        try:
            # Find all JSON files in target directory
            json_files = list(target_directory.rglob("*.json"))
            scan_results["files_scanned"] = len(json_files)
            
            self.logger.info(f"Found {len(json_files)} JSON files to scan")
            
            # Scan each file for corruption
            for filepath in json_files:
                corruption_result = self._scan_file_for_corruption(filepath)
                
                if corruption_result["corruption_detected"]:
                    scan_results["files_with_corruption"] += 1
                    scan_results["corrupted_files"].append(str(filepath))
                    scan_results["corruption_details"][str(filepath)] = corruption_result
                    
                    # Update corruption summary
                    severity = corruption_result["severity"]
                    if severity in scan_results["corruption_summary"]:
                        scan_results["corruption_summary"][severity] += 1
            
            # Generate recommendations
            scan_results["recommendations"] = self._generate_corruption_recommendations(scan_results)
            
            # Calculate scan duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            scan_results["scan_duration_seconds"] = duration
            
            self.logger.info(
                f"Corruption scan completed in {duration:.2f}s. "
                f"Found corruption in {scan_results['files_with_corruption']} out of {scan_results['files_scanned']} files"
            )
            
        except Exception as e:
            self.logger.error(f"Corruption scan failed: {e}")
            scan_results["error"] = str(e)
        
        return scan_results
    
    def scan_specific_file(self, filepath: Path) -> Dict[str, Any]:
        """Scan a specific file for corruption"""
        self.logger.info(f"Scanning specific file for corruption: {filepath}")
        
        if not filepath.exists():
            return {
                "corruption_detected": False,
                "error": "File does not exist",
                "filepath": str(filepath)
            }
        
        return self._scan_file_for_corruption(filepath)
    
    def scan_by_pattern(self, pattern: str, target_directory: Optional[Path] = None) -> Dict[str, Any]:
        """Scan files matching a specific pattern for corruption"""
        if target_directory is None:
            target_directory = Path("agent_workspaces/meeting")
        
        self.logger.info(f"Scanning files matching pattern '{pattern}' in {target_directory}")
        
        # Find files matching pattern
        matching_files = []
        for filepath in target_directory.rglob("*.json"):
            if re.search(pattern, str(filepath)):
                matching_files.append(filepath)
        
        scan_results = {
            "timestamp": datetime.now().isoformat(),
            "pattern": pattern,
            "target_directory": str(target_directory),
            "files_matching_pattern": len(matching_files),
            "files_scanned": 0,
            "files_with_corruption": 0,
            "corruption_summary": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0
            },
            "corrupted_files": [],
            "corruption_details": {}
        }
        
        # Scan matching files
        for filepath in matching_files:
            corruption_result = self._scan_file_for_corruption(filepath)
            scan_results["files_scanned"] += 1
            
            if corruption_result["corruption_detected"]:
                scan_results["files_with_corruption"] += 1
                scan_results["corrupted_files"].append(str(filepath))
                scan_results["corruption_details"][str(filepath)] = corruption_result
                
                # Update corruption summary
                severity = corruption_result["severity"]
                if severity in scan_results["corruption_summary"]:
                    scan_results["corruption_summary"][severity] += 1
        
        return scan_results
    
    def detect_corruption_type(self, filepath: Path) -> Dict[str, Any]:
        """Detect specific type of corruption in a file"""
        self.logger.info(f"Detecting corruption type in {filepath}")
        
        if not filepath.exists():
            return {
                "corruption_type": "file_not_found",
                "severity": "CRITICAL",
                "details": "File does not exist"
            }
        
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
            
            corruption_analysis = {
                "filepath": str(filepath),
                "file_size_bytes": len(content),
                "corruption_types": [],
                "severity": "LOW",
                "details": {}
            }
            
            # Check for JSON syntax corruption
            json_corruption = self._check_json_syntax_corruption(content)
            if json_corruption:
                corruption_analysis["corruption_types"].append("json_syntax")
                corruption_analysis["details"]["json_syntax"] = json_corruption
            
            # Check for data structure corruption
            structure_corruption = self._check_data_structure_corruption(content)
            if structure_corruption:
                corruption_analysis["corruption_types"].append("data_structure")
                corruption_analysis["details"]["data_structure"] = structure_corruption
            
            # Check for file corruption
            file_corruption = self._check_file_corruption(content)
            if file_corruption:
                corruption_analysis["corruption_types"].append("file_corruption")
                corruption_analysis["details"]["file_corruption"] = file_corruption
            
            # Determine overall severity
            if "file_corruption" in corruption_analysis["corruption_types"]:
                corruption_analysis["severity"] = "CRITICAL"
            elif "json_syntax" in corruption_analysis["corruption_types"]:
                corruption_analysis["severity"] = "HIGH"
            elif "data_structure" in corruption_analysis["corruption_types"]:
                corruption_analysis["severity"] = "MEDIUM"
            
            return corruption_analysis
            
        except Exception as e:
            return {
                "corruption_type": "scan_error",
                "severity": "CRITICAL",
                "details": f"Error scanning file: {str(e)}"
            }
    
    def _scan_file_for_corruption(self, filepath: Path) -> Dict[str, Any]:
        """Scan individual file for corruption"""
        corruption_result = {
            "filepath": str(filepath),
            "corruption_detected": False,
            "severity": "LOW",
            "corruption_types": [],
            "corruption_details": {},
            "file_size_bytes": 0,
            "scan_timestamp": datetime.now().isoformat()
        }
        
        try:
            # Get file size
            stat = filepath.stat()
            corruption_result["file_size_bytes"] = stat.st_size
            
            # Check if file is empty
            if stat.st_size == 0:
                corruption_result["corruption_detected"] = True
                corruption_result["severity"] = "CRITICAL"
                corruption_result["corruption_types"].append("empty_file")
                corruption_result["corruption_details"]["empty_file"] = "File is empty (0 bytes)"
                return corruption_result
            
            # Read file content
            with open(filepath, 'rb') as f:
                content = f.read()
            
            # Check for various corruption types
            corruption_found = False
            
            # JSON syntax corruption
            json_corruption = self._check_json_syntax_corruption(content)
            if json_corruption:
                corruption_found = True
                corruption_result["corruption_types"].append("json_syntax")
                corruption_result["corruption_details"]["json_syntax"] = json_corruption
            
            # Data structure corruption
            structure_corruption = self._check_data_structure_corruption(content)
            if structure_corruption:
                corruption_found = True
                corruption_result["corruption_types"].append("data_structure")
                corruption_result["corruption_details"]["data_structure"] = structure_corruption
            
            # File corruption
            file_corruption = self._check_file_corruption(content)
            if file_corruption:
                corruption_found = True
                corruption_result["corruption_types"].append("file_corruption")
                corruption_result["corruption_details"]["file_corruption"] = file_corruption
            
            # Try to parse JSON
            try:
                json.loads(content.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                corruption_found = True
                corruption_result["corruption_types"].append("json_parse_error")
                corruption_result["corruption_details"]["json_parse_error"] = str(e)
            
            # Update result
            corruption_result["corruption_detected"] = corruption_found
            
            # Determine severity
            if "file_corruption" in corruption_result["corruption_types"]:
                corruption_result["severity"] = "CRITICAL"
            elif "json_syntax" in corruption_result["corruption_types"]:
                corruption_result["severity"] = "HIGH"
            elif "data_structure" in corruption_result["corruption_types"]:
                corruption_result["severity"] = "MEDIUM"
            
        except Exception as e:
            corruption_result["corruption_detected"] = True
            corruption_result["severity"] = "CRITICAL"
            corruption_result["corruption_types"].append("scan_error")
            corruption_result["corruption_details"]["scan_error"] = str(e)
        
        return corruption_result
    
    def _check_json_syntax_corruption(self, content: bytes) -> Optional[Dict[str, Any]]:
        """Check for JSON syntax corruption patterns"""
        corruption_info = {
            "patterns_found": [],
            "locations": [],
            "severity": "LOW"
        }
        
        try:
            content_str = content.decode('utf-8')
            
            for pattern_name, pattern in self.corruption_patterns["json_syntax"].items():
                matches = re.finditer(pattern, content_str)
                for match in matches:
                    corruption_info["patterns_found"].append(pattern_name)
                    corruption_info["locations"].append({
                        "position": match.start(),
                        "pattern": pattern_name,
                        "context": content_str[max(0, match.start()-10):match.end()+10]
                    })
            
            if corruption_info["patterns_found"]:
                corruption_info["severity"] = "HIGH"
                return corruption_info
            
        except UnicodeDecodeError:
            corruption_info["patterns_found"].append("unicode_decode_error")
            corruption_info["severity"] = "CRITICAL"
            return corruption_info
        
        return None
    
    def _check_data_structure_corruption(self, content: bytes) -> Optional[Dict[str, Any]]:
        """Check for data structure corruption patterns"""
        corruption_info = {
            "patterns_found": [],
            "locations": [],
            "severity": "MEDIUM"
        }
        
        try:
            content_str = content.decode('utf-8')
            
            for pattern_name, pattern in self.corruption_patterns["data_structure"].items():
                matches = re.finditer(pattern, content_str)
                for match in matches:
                    corruption_info["patterns_found"].append(pattern_name)
                    corruption_info["locations"].append({
                        "position": match.start(),
                        "pattern": pattern_name,
                        "context": content_str[max(0, match.start()-20):match.end()+20]
                    })
            
            if corruption_info["patterns_found"]:
                return corruption_info
            
        except UnicodeDecodeError:
            corruption_info["patterns_found"].append("unicode_decode_error")
            corruption_info["severity"] = "CRITICAL"
            return corruption_info
        
        return None
    
    def _check_file_corruption(self, content: bytes) -> Optional[Dict[str, Any]]:
        """Check for file corruption patterns"""
        corruption_info = {
            "patterns_found": [],
            "severity": "CRITICAL"
        }
        
        for pattern_name, pattern in self.corruption_patterns["file_corruption"].items():
            if re.search(pattern, content):
                corruption_info["patterns_found"].append(pattern_name)
        
        if corruption_info["patterns_found"]:
            return corruption_info
        
        return None
    
    def _generate_corruption_recommendations(self, scan_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on corruption scan results"""
        recommendations = []
        
        files_with_corruption = scan_results.get("files_with_corruption", 0)
        corruption_summary = scan_results.get("corruption_summary", {})
        
        if files_with_corruption == 0:
            recommendations.append("MAINTENANCE: Schedule regular corruption scans to maintain system health")
            recommendations.append("PREVENTION: Implement automated backup and validation procedures")
            return recommendations
        
        critical_corruption = corruption_summary.get("critical", 0)
        high_corruption = corruption_summary.get("high", 0)
        
        if critical_corruption > 0:
            recommendations.append("IMMEDIATE: Address all critical corruption issues to prevent system failure")
            recommendations.append("RECOVERY: Restore corrupted files from recent backups")
            recommendations.append("ISOLATION: Isolate severely corrupted files to prevent spread")
        
        if high_corruption > 0:
            recommendations.append("URGENT: Fix high-severity corruption to restore functionality")
            recommendations.append("VALIDATION: Validate file integrity after repairs")
        
        if files_with_corruption > 0:
            recommendations.append("ASSESSMENT: Evaluate corruption patterns to identify root causes")
            recommendations.append("PREVENTION: Implement corruption detection and prevention measures")
            recommendations.append("BACKUP: Ensure all critical files have recent, valid backups")
        
        return recommendations
