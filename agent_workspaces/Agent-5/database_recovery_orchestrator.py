#!/usr/bin/env python3
"""
Database Recovery Orchestrator
==============================

Main orchestrator for database recovery operations.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .database_audit_core import DatabaseAuditCore, FileInfo, AuditResult
from .database_recovery_ops import DatabaseRecoveryOps, RecoveryAction


class DatabaseRecoveryOrchestrator:
    """Main orchestrator for database recovery operations"""
    
    def __init__(self, base_path: str = "agent_workspaces/meeting"):
        self.base_path = Path(base_path)
        self.logger = self._setup_logging()
        
        # Initialize components
        self.audit_core = DatabaseAuditCore(self.base_path)
        self.recovery_ops = DatabaseRecoveryOps(self.base_path)
        
        # Target files for recovery
        self.target_files = [
            "task_list.json",
            "task_list.backup.json", 
            "meeting.json"
        ]
        
        # Recovery results
        self.recovery_results = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the orchestrator"""
        logger = logging.getLogger("DatabaseRecoveryOrchestrator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[ORCHESTRATOR] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def execute_full_recovery_workflow(self) -> Dict[str, Any]:
        """Execute the complete database recovery workflow"""
        self.logger.info("Starting full database recovery workflow")
        
        workflow_results = {
            "workflow_id": f"recovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "start_time": datetime.now().isoformat(),
            "phases": {},
            "overall_status": "in_progress",
            "summary": {}
        }
        
        try:
            # Phase 1: Initial Assessment
            self.logger.info("Phase 1: Initial Assessment")
            assessment = self._perform_initial_assessment()
            workflow_results["phases"]["initial_assessment"] = assessment
            
            # Phase 2: File Analysis
            self.logger.info("Phase 2: File Analysis")
            file_analysis = self._analyze_target_files()
            workflow_results["phases"]["file_analysis"] = file_analysis
            
            # Phase 3: Recovery Operations
            self.logger.info("Phase 3: Recovery Operations")
            recovery_ops = self._execute_recovery_operations(file_analysis)
            workflow_results["phases"]["recovery_operations"] = recovery_ops
            
            # Phase 4: Post-Recovery Validation
            self.logger.info("Phase 4: Post-Recovery Validation")
            validation = self._validate_recovery_results()
            workflow_results["phases"]["post_recovery_validation"] = validation
            
            # Generate final summary
            workflow_results["overall_status"] = "completed"
            workflow_results["end_time"] = datetime.now().isoformat()
            workflow_results["summary"] = self._generate_workflow_summary(workflow_results)
            
            self.logger.info("Database recovery workflow completed successfully")
            
        except Exception as e:
            self.logger.error(f"Recovery workflow failed: {e}")
            workflow_results["overall_status"] = "failed"
            workflow_results["error"] = str(e)
            workflow_results["end_time"] = datetime.now().isoformat()
        
        return workflow_results
    
    def _perform_initial_assessment(self) -> Dict[str, Any]:
        """Perform initial assessment of the recovery environment"""
        try:
            assessment = {
                "timestamp": datetime.now().isoformat(),
                "base_path": str(self.base_path),
                "base_path_exists": self.base_path.exists(),
                "base_path_readable": self.base_path.is_dir(),
                "target_files": self.target_files,
                "environment_ready": True,
                "issues": []
            }
            
            if not self.base_path.exists():
                assessment["environment_ready"] = False
                assessment["issues"].append("Base path does not exist")
            
            if not self.base_path.is_dir():
                assessment["environment_ready"] = False
                assessment["issues"].append("Base path is not a directory")
            
            return assessment
            
        except Exception as e:
            self.logger.error(f"Initial assessment failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "environment_ready": False
            }
    
    def _analyze_target_files(self) -> Dict[str, Any]:
        """Analyze all target files for recovery"""
        try:
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "files_analyzed": 0,
                "file_details": {},
                "overall_health_score": 0.0,
                "critical_issues": [],
                "warnings": []
            }
            
            file_infos = []
            
            for filename in self.target_files:
                filepath = self.base_path / filename
                file_info = self.audit_core.analyze_file(filepath)
                file_infos.append(file_info)
                
                analysis_results["file_details"][filename] = {
                    "exists": file_info.exists,
                    "readable": file_info.readable,
                    "valid_json": file_info.valid_json,
                    "size_bytes": file_info.size_bytes,
                    "issues": []
                }
                
                if not file_info.exists:
                    analysis_results["critical_issues"].append(f"File {filename} does not exist")
                elif not file_info.readable:
                    analysis_results["critical_issues"].append(f"File {filename} is not readable")
                elif not file_info.valid_json:
                    analysis_results["warnings"].append(f"File {filename} contains invalid JSON")
                
                analysis_results["files_analyzed"] += 1
            
            # Calculate overall health score
            if file_infos:
                analysis_results["overall_health_score"] = self.audit_core._calculate_health_score(file_infos)
            
            return analysis_results
            
        except Exception as e:
            self.logger.error(f"File analysis failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "files_analyzed": 0
            }
    
    def _execute_recovery_operations(self, file_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Execute recovery operations based on file analysis"""
        try:
            recovery_results = {
                "timestamp": datetime.now().isoformat(),
                "operations_executed": 0,
                "operations_successful": 0,
                "operations_failed": 0,
                "operation_details": []
            }
            
            for filename, file_detail in file_analysis.get("file_details", {}).items():
                filepath = self.base_path / filename
                
                if not file_detail["exists"]:
                    # File doesn't exist - try to restore from backup
                    self.logger.info(f"Attempting to restore missing file: {filename}")
                    if self.recovery_ops.restore_from_backup(filepath):
                        recovery_results["operations_successful"] += 1
                        recovery_results["operation_details"].append({
                            "file": filename,
                            "operation": "restore_from_backup",
                            "status": "success"
                        })
                    else:
                        recovery_results["operations_failed"] += 1
                        recovery_results["operation_details"].append({
                            "file": filename,
                            "operation": "restore_from_backup",
                            "status": "failed"
                        })
                
                elif not file_detail["valid_json"]:
                    # File exists but has invalid JSON - try to repair
                    self.logger.info(f"Attempting to repair corrupted file: {filename}")
                    if self.recovery_ops.repair_json_file(filepath):
                        recovery_results["operations_successful"] += 1
                        recovery_results["operation_details"].append({
                            "file": filename,
                            "operation": "repair_json",
                            "status": "success"
                        })
                    else:
                        recovery_results["operations_failed"] += 1
                        recovery_results["operation_details"].append({
                            "file": filename,
                            "operation": "repair_json",
                            "status": "failed"
                        })
                
                recovery_results["operations_executed"] += 1
            
            return recovery_results
            
        except Exception as e:
            self.logger.error(f"Recovery operations failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "operations_executed": 0
            }
    
    def _validate_recovery_results(self) -> Dict[str, Any]:
        """Validate the results of recovery operations"""
        try:
            validation_results = {
                "timestamp": datetime.now().isoformat(),
                "files_validated": 0,
                "validation_passed": 0,
                "validation_failed": 0,
                "validation_details": {}
            }
            
            for filename in self.target_files:
                filepath = self.base_path / filename
                validation_result = self.recovery_ops.validate_file_integrity(filepath)
                
                validation_results["validation_details"][filename] = validation_result
                validation_results["files_validated"] += 1
                
                if validation_result["integrity_score"] >= 75.0:
                    validation_results["validation_passed"] += 1
                else:
                    validation_results["validation_failed"] += 1
            
            return validation_results
            
        except Exception as e:
            self.logger.error(f"Recovery validation failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "files_validated": 0
            }
    
    def _generate_workflow_summary(self, workflow_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the recovery workflow"""
        try:
            phases = workflow_results.get("phases", {})
            
            summary = {
                "workflow_duration": "calculated",
                "overall_success": workflow_results.get("overall_status") == "completed",
                "phases_completed": len(phases),
                "critical_issues_found": 0,
                "files_recovered": 0,
                "final_health_score": 0.0
            }
            
            # Count critical issues
            if "file_analysis" in phases:
                summary["critical_issues_found"] = len(
                    phases["file_analysis"].get("critical_issues", [])
                )
            
            # Count recovered files
            if "recovery_operations" in phases:
                summary["files_recovered"] = phases["recovery_operations"].get("operations_successful", 0)
            
            # Get final health score
            if "post_recovery_validation" in phases:
                validation_details = phases["post_recovery_validation"].get("validation_details", {})
                if validation_details:
                    scores = [detail.get("integrity_score", 0) for detail in validation_details.values()]
                    summary["final_health_score"] = sum(scores) / len(scores) if scores else 0.0
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Failed to generate workflow summary: {e}")
            return {
                "error": str(e),
                "overall_success": False
            }
    
    def get_recovery_status(self) -> Dict[str, Any]:
        """Get current recovery status"""
        return {
            "timestamp": datetime.now().isoformat(),
            "orchestrator_status": "active",
            "recovery_summary": self.recovery_ops.get_recovery_summary(),
            "target_files": self.target_files,
            "base_path": str(self.base_path)
        }
