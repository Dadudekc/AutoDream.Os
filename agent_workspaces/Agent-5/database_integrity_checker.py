#!/usr/bin/env python3
"""
Database Integrity Checker - EMERGENCY-RESTORE-004 Mission
=========================================================

This system provides ongoing database integrity monitoring and validation.
Part of the emergency system restoration mission for Agent-5.
"""

import json
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from src.database.integrity_tools import setup_logging, iter_contracts

@dataclass
class IntegrityCheck:
    """Represents a single integrity check"""
    check_id: str
    check_name: str
    status: str  # PASSED, FAILED, WARNING
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    details: Dict[str, Any]
    timestamp: str

@dataclass
class IntegrityReport:
    """Complete integrity check report"""
    report_id: str
    timestamp: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    warning_checks: int
    overall_status: str
    checks: List[IntegrityCheck]
    recommendations: List[str]

class DatabaseIntegrityChecker:
    """Monitors and validates contract database integrity"""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.task_list_path = Path(task_list_path)
        self.contracts = {}
        self.logger = setup_logging("DatabaseIntegrityChecker")
        
    def load_contracts(self) -> bool:
        """Load contracts from the task list file"""
        try:
            if not self.task_list_path.exists():
                self.logger.error(f"Task list file not found: {self.task_list_path}")
                return False
                
            with open(self.task_list_path, 'r') as f:
                self.contracts = json.load(f)
                
            self.logger.info(f"Loaded {self.contracts.get('total_contracts', 0)} contracts")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load contracts: {e}")
            return False
            
    def check_contract_counts(self) -> IntegrityCheck:
        """Check contract count consistency"""
        total_claimed = self.contracts.get("claimed_contracts", 0)
        total_completed = self.contracts.get("completed_contracts", 0)
        total_available = self.contracts.get("available_contracts", 0)
        total_contracts = self.contracts.get("total_contracts", 0)
        
        # Count actual contracts in the data
        actual_total = sum(1 for _ in iter_contracts(self.contracts))
        
        calculated_total = total_claimed + total_completed + total_available
        
        # Check both consistency checks
        header_consistent = calculated_total == total_contracts
        data_consistent = actual_total == total_contracts
        
        if header_consistent and data_consistent:
            return IntegrityCheck(
                check_id="COUNT_CONSISTENCY",
                check_name="Contract Count Consistency",
                status="PASSED",
                severity="CRITICAL",
                message="Contract counts are consistent",
                details={
                    "total_contracts": total_contracts,
                    "claimed": total_claimed,
                    "completed": total_completed,
                    "available": total_available,
                    "actual_count": actual_total
                },
                timestamp=datetime.datetime.now().isoformat()
            )
        else:
            return IntegrityCheck(
                check_id="COUNT_CONSISTENCY",
                check_name="Contract Count Consistency",
                status="FAILED",
                severity="CRITICAL",
                message=f"Contract count mismatch: header={calculated_total}, data={actual_total}, declared={total_contracts}",
                details={
                    "total_contracts": total_contracts,
                    "claimed": total_claimed,
                    "completed": total_completed,
                    "available": total_available,
                    "calculated_total": calculated_total,
                    "actual_count": actual_total
                },
                timestamp=datetime.datetime.now().isoformat()
            )
            
    def check_required_fields(self) -> List[IntegrityCheck]:
        """Check for missing required fields in contracts"""
        checks = []
        
        if "contracts" not in self.contracts:
            checks.append(IntegrityCheck(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="FAILED",
                severity="CRITICAL",
                message="No contracts section found",
                details={},
                timestamp=datetime.datetime.now().isoformat()
            ))
            return checks
            
        required_fields = [
            "title", "description", "difficulty", "extra_credit_points",
            "requirements", "deliverables", "status"
        ]
        
        missing_field_contracts = []

        for _, contract in iter_contracts(self.contracts):
            contract_id = contract.get("contract_id", "UNKNOWN")
            missing_fields = [field for field in required_fields if field not in contract]

            if missing_fields:
                missing_field_contracts.append({
                    "contract_id": contract_id,
                    "missing_fields": missing_fields,
                })
                    
        if missing_field_contracts:
            checks.append(IntegrityCheck(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(missing_field_contracts)} contracts with missing required fields",
                details={"missing_field_contracts": missing_field_contracts},
                timestamp=datetime.datetime.now().isoformat()
            ))
        else:
            checks.append(IntegrityCheck(
                check_id="REQUIRED_FIELDS",
                check_name="Required Fields Check",
                status="PASSED",
                severity="HIGH",
                message="All contracts have required fields",
                details={},
                timestamp=datetime.datetime.now().isoformat()
            ))
            
        return checks
        
    def check_status_consistency(self) -> List[IntegrityCheck]:
        """Check contract status consistency"""
        checks = []
        
        if "contracts" not in self.contracts:
            return checks
            
        status_issues = []
        
        for _, contract in iter_contracts(self.contracts):
            contract_id = contract.get("contract_id", "UNKNOWN")
            status = contract.get("status")
            claimed_by = contract.get("claimed_by")
            claimed_at = contract.get("claimed_at")
            completed_at = contract.get("completed_at")

            # Check CLAIMED status consistency
            if status == "CLAIMED":
                if not claimed_by:
                    status_issues.append({
                        "contract_id": contract_id,
                        "issue": "CLAIMED status without agent assignment"
                    })
                if not claimed_at:
                    status_issues.append({
                        "contract_id": contract_id,
                        "issue": "CLAIMED status without claim timestamp"
                    })

            # Check COMPLETED status consistency
            elif status == "COMPLETED":
                if not completed_at:
                    status_issues.append({
                        "contract_id": contract_id,
                        "issue": "COMPLETED status without completion timestamp"
                    })
                        
        if status_issues:
            checks.append(IntegrityCheck(
                check_id="STATUS_CONSISTENCY",
                check_name="Contract Status Consistency",
                status="FAILED",
                severity="HIGH",
                message=f"Found {len(status_issues)} status consistency issues",
                details={"status_issues": status_issues},
                timestamp=datetime.datetime.now().isoformat()
            ))
        else:
            checks.append(IntegrityCheck(
                check_id="STATUS_CONSISTENCY",
                check_name="Contract Status Consistency",
                status="PASSED",
                severity="HIGH",
                message="All contract statuses are consistent",
                details={},
                timestamp=datetime.datetime.now().isoformat()
            ))
            
        return checks
        
    def check_timestamp_validity(self) -> List[IntegrityCheck]:
        """Check timestamp validity and format"""
        checks = []
        
        if "contracts" not in self.contracts:
            return checks
            
        timestamp_issues = []
        
        for _, contract in iter_contracts(self.contracts):
            contract_id = contract.get("contract_id", "UNKNOWN")

            # Check claimed_at timestamp
            if "claimed_at" in contract and contract["claimed_at"]:
                try:
                    claimed_time = datetime.datetime.fromisoformat(
                        contract["claimed_at"].replace('Z', '+00:00')
                    )
                    current_dt = datetime.datetime.now(claimed_time.tzinfo)
                    if claimed_time > current_dt:
                        timestamp_issues.append({
                            "contract_id": contract_id,
                            "issue": "Future claim timestamp",
                            "timestamp": contract["claimed_at"]
                        })
                except ValueError:
                    timestamp_issues.append({
                        "contract_id": contract_id,
                        "issue": "Invalid claim timestamp format",
                        "timestamp": contract["claimed_at"]
                    })

            # Check completed_at timestamp
            if "completed_at" in contract and contract["completed_at"]:
                try:
                    completed_time = datetime.datetime.fromisoformat(
                        contract["completed_at"].replace('Z', '+00:00')
                    )
                    current_dt = datetime.datetime.now(completed_time.tzinfo)
                    if completed_time > current_dt:
                        timestamp_issues.append({
                            "contract_id": contract_id,
                            "issue": "Future completion timestamp",
                            "timestamp": contract["completed_at"]
                        })
                except ValueError:
                    timestamp_issues.append({
                        "contract_id": contract_id,
                        "issue": "Invalid completion timestamp format",
                        "timestamp": contract["completed_at"]
                    })
                        
        if timestamp_issues:
            checks.append(IntegrityCheck(
                check_id="TIMESTAMP_VALIDITY",
                check_name="Timestamp Validity",
                status="FAILED",
                severity="MEDIUM",
                message=f"Found {len(timestamp_issues)} timestamp issues",
                details={"timestamp_issues": timestamp_issues},
                timestamp=datetime.datetime.now().isoformat()
            ))
        else:
            checks.append(IntegrityCheck(
                check_id="TIMESTAMP_VALIDITY",
                check_name="Timestamp Validity",
                status="PASSED",
                severity="MEDIUM",
                message="All timestamps are valid",
                details={},
                timestamp=datetime.datetime.now().isoformat()
            ))
            
        return checks
        
    def check_data_types(self) -> List[IntegrityCheck]:
        """Check data type consistency"""
        checks = []
        
        if "contracts" not in self.contracts:
            return checks

        type_issues = []

        for _, contract in iter_contracts(self.contracts):
            contract_id = contract.get("contract_id", "UNKNOWN")

            # Check extra_credit_points is numeric
            if "extra_credit_points" in contract:
                if not isinstance(contract["extra_credit_points"], (int, float)):
                    type_issues.append({
                        "contract_id": contract_id,
                        "issue": "extra_credit_points is not numeric",
                        "value": contract["extra_credit_points"],
                    })

            # Check requirements and deliverables are lists
            for field in ["requirements", "deliverables"]:
                if field in contract and not isinstance(contract[field], list):
                    type_issues.append({
                        "contract_id": contract_id,
                        "issue": f"{field} is not a list",
                        "value": contract[field],
                    })
                        
        if type_issues:
            checks.append(IntegrityCheck(
                check_id="DATA_TYPES",
                check_name="Data Type Consistency",
                status="FAILED",
                severity="MEDIUM",
                message=f"Found {len(type_issues)} data type issues",
                details={"type_issues": type_issues},
                timestamp=datetime.datetime.now().isoformat()
            ))
        else:
            checks.append(IntegrityCheck(
                check_id="DATA_TYPES",
                check_name="Data Type Consistency",
                status="PASSED",
                severity="MEDIUM",
                message="All data types are consistent",
                details={},
                timestamp=datetime.datetime.now().isoformat()
            ))
            
        return checks
        
    def run_integrity_checks(self) -> IntegrityReport:
        """Run all integrity checks"""
        self.logger.info("Starting database integrity checks...")
        
        if not self.load_contracts():
            return IntegrityReport(
                report_id="failed_load",
                timestamp=datetime.datetime.now().isoformat(),
                total_checks=0,
                passed_checks=0,
                failed_checks=0,
                warning_checks=0,
                overall_status="FAILED",
                checks=[],
                recommendations=["Failed to load contracts"]
            )
            
        # Run all checks
        all_checks = []
        
        # Basic checks
        all_checks.append(self.check_contract_counts())
        
        # Detailed checks
        all_checks.extend(self.check_required_fields())
        all_checks.extend(self.check_status_consistency())
        all_checks.extend(self.check_timestamp_validity())
        all_checks.extend(self.check_data_types())
        
        # Calculate statistics
        total_checks = len(all_checks)
        passed_checks = sum(1 for c in all_checks if c.status == "PASSED")
        failed_checks = sum(1 for c in all_checks if c.status == "FAILED")
        warning_checks = sum(1 for c in all_checks if c.status == "WARNING")
        
        # Determine overall status
        if failed_checks > 0:
            overall_status = "FAILED"
        elif warning_checks > 0:
            overall_status = "WARNING"
        else:
            overall_status = "PASSED"
            
        # Generate recommendations
        recommendations = []
        if failed_checks > 0:
            recommendations.append("Immediate action required to fix failed checks")
        if warning_checks > 0:
            recommendations.append("Review warnings and address as needed")
        if overall_status == "PASSED":
            recommendations.append("Database integrity is good - continue monitoring")
            
        report = IntegrityReport(
            report_id=f"integrity_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}",
            timestamp=datetime.datetime.now().isoformat(),
            total_checks=total_checks,
            passed_checks=passed_checks,
            failed_checks=failed_checks,
            warning_checks=warning_checks,
            overall_status=overall_status,
            checks=all_checks,
            recommendations=recommendations
        )
        
        self.logger.info(f"Integrity checks complete: {passed_checks}/{total_checks} passed")
        return report
        
    def save_integrity_report(self, report: IntegrityReport, output_path: str = None) -> bool:
        """Save integrity report to file"""
        if not output_path:
            output_path = f"database_integrity_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        try:
            report_data = {
                "report_id": report.report_id,
                "timestamp": report.timestamp,
                "summary": {
                    "total_checks": report.total_checks,
                    "passed_checks": report.passed_checks,
                    "failed_checks": report.failed_checks,
                    "warning_checks": report.warning_checks,
                    "overall_status": report.overall_status
                },
                "checks": [
                    {
                        "check_id": check.check_id,
                        "check_name": check.check_name,
                        "status": check.status,
                        "severity": check.severity,
                        "message": check.message,
                        "details": check.details,
                        "timestamp": check.timestamp
                    }
                    for check in report.checks
                ],
                "recommendations": report.recommendations
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
                
            self.logger.info(f"Integrity report saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save integrity report: {e}")
            return False

def main():
    """Main function for command-line execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Database Integrity Checker - EMERGENCY-RESTORE-004 Mission"
    )
    parser.add_argument(
        "--task-list", 
        default="agent_workspaces/meeting/task_list.json",
        help="Path to task list file"
    )
    parser.add_argument(
        "--output", 
        help="Output path for integrity report"
    )
    
    args = parser.parse_args()
    
    # Initialize integrity checker
    checker = DatabaseIntegrityChecker(args.task_list)
    
    # Run integrity checks
    report = checker.run_integrity_checks()
    
    # Display results
    print(f"\n{'='*80}")
    print(f"DATABASE INTEGRITY REPORT")
    print(f"{'='*80}")
    print(f"Report ID: {report.report_id}")
    print(f"Timestamp: {report.timestamp}")
    print(f"Overall Status: {report.overall_status}")
    print(f"Total Checks: {report.total_checks}")
    print(f"Passed: {report.passed_checks}")
    print(f"Failed: {report.failed_checks}")
    print(f"Warnings: {report.warning_checks}")
    
    if report.checks:
        print(f"\n{'='*80}")
        print(f"INTEGRITY CHECK RESULTS")
        print(f"{'='*80}")
        for check in report.checks:
            status_icon = "✅" if check.status == "PASSED" else "❌" if check.status == "FAILED" else "⚠️"
            print(f"\n{status_icon} {check.check_name} - {check.status}")
            print(f"   Severity: {check.severity}")
            print(f"   Message: {check.message}")
            
    if report.recommendations:
        print(f"\n{'='*80}")
        print(f"RECOMMENDATIONS")
        print(f"{'='*80}")
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")
            
    # Save report
    if args.output:
        checker.save_integrity_report(report, args.output)
    else:
        checker.save_integrity_report(report)
        
    print(f"\n{'='*80}")
    print(f"Integrity check complete. Report saved.")
    print(f"{'='*80}")
    
    return report.overall_status != "FAILED"

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
