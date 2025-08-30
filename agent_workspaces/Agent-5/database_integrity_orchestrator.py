#!/usr/bin/env python3
"""
Database Integrity Orchestrator - EMERGENCY-RESTORE-004 Mission
===============================================================

Main orchestrator for database integrity checking system.
Part of the emergency system restoration mission for Agent-5.
"""

import logging
from typing import Dict, List, Any, Optional
from .database_integrity_models import IntegrityReport, IntegrityValidator
from .database_integrity_operations import DatabaseOperations
from .database_integrity_core import IntegrityChecker
from .database_integrity_reporting import IntegrityReporter


class DatabaseIntegrityOrchestrator:
    """Main orchestrator for database integrity checking"""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.task_list_path = task_list_path
        self.db_ops = DatabaseOperations(task_list_path)
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the orchestrator"""
        logger = logging.getLogger("DatabaseIntegrityOrchestrator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def run_integrity_checks(self) -> IntegrityReport:
        """Run complete integrity checking process"""
        try:
            self.logger.info("Starting database integrity checks")
            
            # Load contracts
            if not self.db_ops.load_contracts():
                self.logger.error("Failed to load contracts")
                return self._create_error_report("Failed to load contracts")
            
            # Get contracts data
            contracts_data = self.db_ops.get_contracts_data()
            
            # Run integrity checks
            checker = IntegrityChecker(contracts_data)
            checks = checker.run_all_checks()
            
            # Generate recommendations
            recommendations = self._generate_recommendations(checks)
            
            # Create report
            report = IntegrityValidator.create_report(checks, recommendations)
            
            self.logger.info(f"Integrity checks completed: {report.overall_status}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error during integrity checks: {e}")
            return self._create_error_report(f"Error during integrity checks: {e}")
    
    def _generate_recommendations(self, checks: List[Any]) -> List[str]:
        """Generate recommendations based on check results"""
        recommendations = []
        
        failed_checks = [check for check in checks if check.status == "FAILED"]
        warning_checks = [check for check in checks if check.status == "WARNING"]
        
        if failed_checks:
            recommendations.append("Review and fix failed integrity checks")
            recommendations.append("Update contract data to resolve inconsistencies")
            recommendations.append("Verify contract count calculations")
        
        if warning_checks:
            recommendations.append("Address warning-level issues to improve data quality")
            recommendations.append("Review contract status assignments")
        
        if not failed_checks and not warning_checks:
            recommendations.append("All integrity checks passed - database is healthy")
        
        return recommendations
    
    def _create_error_report(self, error_message: str) -> IntegrityReport:
        """Create an error report when something goes wrong"""
        error_check = IntegrityValidator.create_check(
            check_id="SYSTEM_ERROR",
            check_name="System Error",
            status="FAILED",
            severity="CRITICAL",
            message=error_message,
            details={"error": error_message}
        )
        
        return IntegrityValidator.create_report(
            [error_check],
            ["Fix the system error and re-run integrity checks"]
        )
    
    def validate_file_structure(self) -> Dict[str, Any]:
        """Validate the basic file structure"""
        return self.db_ops.validate_file_structure()
    
    def get_file_info(self) -> Dict[str, Any]:
        """Get information about the contracts file"""
        return self.db_ops.get_file_info()
    
    def create_backup(self, backup_path: Optional[str] = None) -> bool:
        """Create a backup of the contracts file"""
        return self.db_ops.backup_contracts(backup_path)
    
    def restore_from_backup(self, backup_path: str) -> bool:
        """Restore contracts from backup"""
        return self.db_ops.restore_contracts(backup_path)
    
    def generate_report(self, format_type: str = "text", output_file: Optional[str] = None) -> str:
        """Generate and optionally save a report"""
        # Run integrity checks
        report = self.run_integrity_checks()
        
        # Setup reporter
        reporter = IntegrityReporter()
        reporter.set_output_format(format_type)
        
        # Generate formatted report
        formatted_report = reporter.generate_report(report)
        
        # Save to file if specified
        if output_file:
            reporter.save_report(report, output_file)
        
        return formatted_report


def main():
    """Main entry point for the orchestrator"""
    import sys
    
    # Check if running as script
    if len(sys.argv) > 1:
        # Use CLI interface
        from .database_integrity_reporting import CLIInterface
        cli = CLIInterface()
        cli.run()
    else:
        # Use orchestrator directly
        orchestrator = DatabaseIntegrityOrchestrator()
        report = orchestrator.run_integrity_checks()
        
        # Print report
        reporter = IntegrityReporter()
        reporter.print_report(report)
        
        # Exit with appropriate code
        if report.overall_status == "FAILED":
            sys.exit(1)
        elif report.overall_status == "WARNING":
            sys.exit(2)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()
