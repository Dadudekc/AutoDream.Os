"""
Core Emergency Database Recovery System

This module orchestrates the emergency database recovery process using modular components.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .models import AuditResult, RecoveryReport
from .database_auditor import DatabaseAuditor
from .integrity_checker import IntegrityChecker
from .corruption_scanner import CorruptionScanner
from .recovery_executor import RecoveryExecutor


class EmergencyContractDatabaseRecovery:
    """EMERGENCY-RESTORE-004: Contract Database Recovery System"""
    
    def __init__(self):
        self.task_list_path = Path("agent_workspaces/meeting/task_list.json")
        self.meeting_path = Path("agent_workspaces/meeting/meeting.json")
        
        # Initialize logging
        self.logger = self._setup_logging()
        
        # Initialize modular components
        self.database_auditor = DatabaseAuditor(self.logger)
        self.integrity_checker = IntegrityChecker(self.logger)
        self.corruption_scanner = CorruptionScanner(self.logger)
        self.recovery_executor = RecoveryExecutor(self.logger)
        
        self.logger.info("🚨 EMERGENCY-RESTORE-004: Contract Database Recovery System initialized")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup emergency logging system."""
        logger = logging.getLogger("EMERGENCY_RESTORE_004")
        logger.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            "[EMERGENCY] %(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Create file handler
        file_handler = logging.FileHandler("emergency_database_recovery.log")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def execute_emergency_recovery(self) -> RecoveryReport:
        """Execute EMERGENCY-RESTORE-004 immediately"""
        self.logger.info("EXECUTING EMERGENCY-RESTORE-004: Contract Database Recovery")
        self.logger.info("TASK: Audit contract database structure and implement integrity checks")
        
        try:
            # Step 1: Audit contract database structure
            self.logger.info("STEP 1: Auditing contract database structure...")
            audit_results = self.audit_database_structure()
            
            # Step 2: Validate contract status accuracy
            self.logger.info("STEP 2: Validating contract status accuracy...")
            contract_validation = self.validate_contract_status_accuracy()
            
            # Step 3: Look for corrupted or missing contracts
            self.logger.info("STEP 3: Scanning for corrupted or missing contracts...")
            corruption_scan = self.scan_for_corruption()
            
            # Step 4: Implement database integrity checks
            self.logger.info("STEP 4: Implementing database integrity checks...")
            integrity_checks = self.implement_integrity_checks()
            
            # Step 5: Generate comprehensive report
            self.logger.info("STEP 5: Generating comprehensive recovery report...")
            recovery_report = self.generate_recovery_report(
                audit_results, contract_validation, corruption_scan, integrity_checks
            )
            
            self.logger.info("✅ EMERGENCY-RESTORE-004 completed successfully")
            return recovery_report
            
        except Exception as e:
            self.logger.error(f"❌ EMERGENCY-RESTORE-004 failed: {e}")
            # Return error report
            return RecoveryReport(
                timestamp=datetime.now(),
                audit_results=AuditResult(
                    timestamp=datetime.now(),
                    file_analysis={},
                    structure_validation=None,
                    metadata_consistency=None,
                    critical_issues=[f"Emergency recovery failed: {str(e)}"],
                    integrity_issues=[],
                    recovery_actions=[],
                    overall_status="FAILED"
                ),
                integrity_check_results=None,
                recovery_actions_taken=[],
                system_status="FAILED",
                recommendations=[f"Emergency recovery failed: {str(e)}"],
                next_steps=["Check system logs", "Verify file permissions", "Restart recovery system"]
            )
    
    def audit_database_structure(self) -> Dict[str, Any]:
        """Audit the overall structure of the contract database."""
        return self.database_auditor.audit_database_structure(
            self.task_list_path, self.meeting_path
        )
    
    def validate_contract_status_accuracy(self) -> Dict[str, Any]:
        """Validate the accuracy of contract status information."""
        return self.integrity_checker.validate_contract_status_accuracy(self.task_list_path)
    
    def scan_for_corruption(self) -> Dict[str, Any]:
        """Scan for corrupted or missing contracts."""
        return self.corruption_scanner.scan_for_corruption(self.task_list_path)
    
    def implement_integrity_checks(self) -> Dict[str, Any]:
        """Implement database integrity checks."""
        return self.recovery_executor.implement_integrity_checks(self.task_list_path)
    
    def generate_recovery_report(self, audit_results: Dict[str, Any],
                               contract_validation: Dict[str, Any],
                               corruption_scan: Dict[str, Any],
                               integrity_checks: Dict[str, Any]) -> RecoveryReport:
        """Generate comprehensive recovery report."""
        self.logger.info("Generating comprehensive recovery report...")
        
        # Determine overall system status
        system_status = self._determine_system_status(
            audit_results, contract_validation, corruption_scan, integrity_checks
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            audit_results, contract_validation, corruption_scan, integrity_checks
        )
        
        # Generate next steps
        next_steps = self._generate_next_steps(
            audit_results, contract_validation, corruption_scan, integrity_checks
        )
        
        # Create recovery actions list
        recovery_actions = []
        if corruption_scan.get("recovery_actions"):
            recovery_actions.extend(corruption_scan["recovery_actions"])
        if integrity_checks.get("recovery_actions"):
            recovery_actions.extend(integrity_checks["recovery_actions"])
        
        # Create audit results object
        audit_result = AuditResult(
            timestamp=datetime.now(),
            file_analysis=audit_results.get("file_analysis", {}),
            structure_validation=None,  # Would need to convert from dict
            metadata_consistency=None,  # Would need to convert from dict
            critical_issues=audit_results.get("critical_issues", []),
            integrity_issues=corruption_scan.get("integrity_issues", []),
            recovery_actions=recovery_actions,
            overall_status=system_status
        )
        
        # Create integrity check results object
        integrity_check_results = None
        if integrity_checks.get("integrity_results"):
            # Would need to convert from dict to IntegrityCheckResult
            pass
        
        return RecoveryReport(
            timestamp=datetime.now(),
            audit_results=audit_result,
            integrity_check_results=integrity_check_results,
            recovery_actions_taken=recovery_actions,
            system_status=system_status,
            recommendations=recommendations,
            next_steps=next_steps
        )
    
    def _determine_system_status(self, audit_results: Dict[str, Any],
                                contract_validation: Dict[str, Any],
                                corruption_scan: Dict[str, Any],
                                integrity_checks: Dict[str, Any]) -> str:
        """Determine overall system status based on all checks."""
        # Check for critical issues
        critical_issues = audit_results.get("critical_issues", [])
        if critical_issues:
            return "CRITICAL"
        
        # Check for corruption
        if corruption_scan.get("corruption_detected", False):
            critical_corruption = corruption_scan.get("critical_issues", 0)
            if critical_corruption > 0:
                return "CRITICAL"
            else:
                return "WARNING"
        
        # Check contract validation
        corrupted_contracts = contract_validation.get("corrupted_contracts", 0)
        if corrupted_contracts > 10:
            return "CRITICAL"
        elif corrupted_contracts > 5:
            return "WARNING"
        elif corrupted_contracts > 0:
            return "ATTENTION"
        
        # Check integrity checks
        if not integrity_checks.get("integrity_checks_implemented", False):
            return "WARNING"
        
        return "HEALTHY"
    
    def _generate_recommendations(self, audit_results: Dict[str, Any],
                                contract_validation: Dict[str, Any],
                                corruption_scan: Dict[str, Any],
                                integrity_checks: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on all check results."""
        recommendations = []
        
        # Critical issues recommendations
        critical_issues = audit_results.get("critical_issues", [])
        if critical_issues:
            recommendations.append("CRITICAL: Immediate action required to fix critical database issues")
            recommendations.append("Stop all database operations until critical issues are resolved")
        
        # Corruption recommendations
        if corruption_scan.get("corruption_detected", False):
            total_issues = corruption_scan.get("total_issues", 0)
            recommendations.append(f"Database corruption detected: {total_issues} issues found")
            recommendations.append("Run comprehensive corruption scan and repair procedures")
        
        # Contract validation recommendations
        corrupted_contracts = contract_validation.get("corrupted_contracts", 0)
        if corrupted_contracts > 0:
            recommendations.append(f"Contract validation issues: {corrupted_contracts} corrupted contracts")
            recommendations.append("Review and fix corrupted contracts to restore data integrity")
        
        # Integrity check recommendations
        if not integrity_checks.get("integrity_checks_implemented", False):
            recommendations.append("Implement regular database integrity checks")
            recommendations.append("Set up automated monitoring for database health")
        
        # General recommendations
        if not recommendations:
            recommendations.append("Database is healthy - maintain current monitoring practices")
            recommendations.append("Schedule regular integrity checks and maintenance")
        
        return recommendations
    
    def _generate_next_steps(self, audit_results: Dict[str, Any],
                            contract_validation: Dict[str, Any],
                            corruption_scan: Dict[str, Any],
                            integrity_checks: Dict[str, Any]) -> List[str]:
        """Generate next steps based on all check results."""
        next_steps = []
        
        # Immediate actions for critical issues
        critical_issues = audit_results.get("critical_issues", [])
        if critical_issues:
            next_steps.append("IMMEDIATE: Stop all database operations")
            next_steps.append("IMMEDIATE: Create emergency backup of current state")
            next_steps.append("IMMEDIATE: Contact database administrator")
        
        # Corruption recovery steps
        if corruption_scan.get("corruption_detected", False):
            next_steps.append("Run automated corruption repair procedures")
            next_steps.append("Validate repair results with integrity checks")
            next_steps.append("Schedule manual review of repaired data")
        
        # Contract repair steps
        corrupted_contracts = contract_validation.get("corrupted_contracts", 0)
        if corrupted_contracts > 0:
            next_steps.append("Review corrupted contracts manually")
            next_steps.append("Apply automated fixes where possible")
            next_steps.append("Validate contract data after repairs")
        
        # Preventive measures
        next_steps.append("Implement regular backup procedures")
        next_steps.append("Set up automated integrity monitoring")
        next_steps.append("Schedule periodic database maintenance")
        
        return next_steps
    
    def run_quick_health_check(self) -> Dict[str, Any]:
        """Run a quick health check of the database."""
        self.logger.info("Running quick health check...")
        
        try:
            # Basic file existence check
            files_exist = self.task_list_path.exists() and self.meeting_path.exists()
            
            # Basic JSON validity check
            json_valid = False
            if self.task_list_path.exists():
                try:
                    with open(self.task_list_path, 'r') as f:
                        json.load(f)
                    json_valid = True
                except Exception:
                    pass
            
            # Basic contract count check
            contract_count = 0
            if json_valid:
                try:
                    with open(self.task_list_path, 'r') as f:
                        task_list = json.load(f)
                    contract_count = len(task_list.get("contracts", []))
                except Exception:
                    pass
            
            return {
                "timestamp": datetime.now().isoformat(),
                "files_exist": files_exist,
                "json_valid": json_valid,
                "contract_count": contract_count,
                "status": "HEALTHY" if (files_exist and json_valid) else "ISSUES_DETECTED"
            }
            
        except Exception as e:
            self.logger.error(f"Quick health check failed: {e}")
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "status": "ERROR"
            }
