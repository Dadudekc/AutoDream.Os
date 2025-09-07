#!/usr/bin/env python3
"""
Database Integrity Orchestrator - Main Coordination Module
========================================================

This module contains the main orchestrator that coordinates all database
integrity checking operations. It serves as the primary interface for
the modularized database integrity checker system.

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Contract:** V2-COMPLIANCE-005 - Database Audit System Modularization
**Status:** MODULARIZATION IN PROGRESS
**Target:** ≤250 lines per module, single responsibility principle
**V2 Compliance:** ✅ Under 250 lines, focused responsibility
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from database_integrity_models import IntegrityCheck, IntegrityReport
from database_integrity_checks import DatabaseIntegrityChecks
from database_integrity_reporting import DatabaseIntegrityReporting


class DatabaseIntegrityOrchestrator:
    """Main orchestrator for database integrity checking operations"""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.task_list_path = Path(task_list_path)
        self.contracts = {}
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.integrity_checks = DatabaseIntegrityChecks(self.logger)
        self.reporting = DatabaseIntegrityReporting(self.logger)
    
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
    
    def run_integrity_checks(self) -> IntegrityReport:
        """Run all integrity checks and generate a comprehensive report"""
        self.logger.info("Starting database integrity checks")
        
        # Ensure contracts are loaded
        if not self.contracts:
            if not self.load_contracts():
                raise RuntimeError("Failed to load contracts for integrity checking")
        
        # Run all integrity checks
        all_checks = []
        
        # Contract count consistency check
        count_check = self.integrity_checks.check_contract_counts(self.contracts)
        all_checks.append(count_check)
        
        # Required fields check
        required_fields_checks = self.integrity_checks.check_required_fields(self.contracts)
        all_checks.extend(required_fields_checks)
        
        # Status consistency check
        status_checks = self.integrity_checks.check_status_consistency(self.contracts)
        all_checks.extend(status_checks)
        
        # Timestamp validity check
        timestamp_checks = self.integrity_checks.check_timestamp_validity(self.contracts)
        all_checks.extend(timestamp_checks)
        
        # Generate comprehensive report
        report = self.reporting.generate_report(all_checks)
        
        self.logger.info(f"Integrity checks complete: {report.passed_checks}/{report.total_checks} passed")
        return report
    
    def save_integrity_report(self, report: IntegrityReport, 
                             output_path: Optional[str] = None) -> bool:
        """Save integrity report to file"""
        return self.reporting.save_report_to_file(report, output_path)
    
    def save_markdown_report(self, report: IntegrityReport, 
                            output_path: Optional[str] = None) -> bool:
        """Save integrity report as markdown file"""
        return self.reporting.save_report_as_markdown(report, output_path)
    
    def display_report(self, report: IntegrityReport) -> None:
        """Display the integrity report in console format"""
        formatted_report = self.reporting.format_report_for_display(report)
        print(formatted_report)
    
    def get_contracts_summary(self) -> Dict[str, Any]:
        """Get a summary of the loaded contracts"""
        if not self.contracts:
            return {"error": "No contracts loaded"}
        
        return {
            "total_contracts": self.contracts.get("total_contracts", 0),
            "claimed_contracts": self.contracts.get("claimed_contracts", 0),
            "completed_contracts": self.contracts.get("completed_contracts", 0),
            "available_contracts": self.contracts.get("available_contracts", 0),
            "file_path": str(self.task_list_path)
        }
    
    def validate_single_contract(self, contract_id: str) -> Optional[IntegrityCheck]:
        """Validate a single contract by ID"""
        if "contracts" not in self.contracts:
            return None
        
        contract = self.contracts["contracts"].get(contract_id)
        if not contract:
            return None
        
        # Create a minimal contracts data structure for single contract validation
        single_contract_data = {
            "contracts": {contract_id: contract},
            "total_contracts": 1
        }
        
        # Run required fields check on this single contract
        checks = self.integrity_checks.check_required_fields(single_contract_data)
        return checks[0] if checks else None
    
    def get_integrity_status(self) -> str:
        """Get the overall integrity status"""
        if not self.contracts:
            return "UNKNOWN"
        
        try:
            report = self.run_integrity_checks()
            return report.overall_status
        except Exception as e:
            self.logger.error(f"Failed to get integrity status: {e}")
            return "ERROR"
    
    def run_quick_check(self) -> bool:
        """Run a quick integrity check and return pass/fail status"""
        try:
            report = self.run_integrity_checks()
            return report.overall_status == "PASSED"
        except Exception as e:
            self.logger.error(f"Quick check failed: {e}")
            return False


def main():
    """Main function for command-line execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Database Integrity Checker - V2 Compliance Modularized Version"
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
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Save report as markdown format"
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Run quick check and exit with status code"
    )
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = DatabaseIntegrityOrchestrator(args.task_list)
    
    # Run integrity checks
    try:
        report = orchestrator.run_integrity_checks()
        
        # Display results
        orchestrator.display_report(report)
        
        # Save report if requested
        if args.output:
            if args.markdown:
                orchestrator.save_markdown_report(report, args.output)
            else:
                orchestrator.save_integrity_report(report, args.output)
        else:
            # Save default report
            orchestrator.save_integrity_report(report)
        
        # Exit with appropriate code
        if args.quick:
            exit(0 if report.overall_status == "PASSED" else 1)
        else:
            exit(0 if report.overall_status != "FAILED" else 1)
            
    except Exception as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
