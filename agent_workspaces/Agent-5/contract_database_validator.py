#!/usr/bin/env python3
"""
Contract Database Validator - EMERGENCY-RESTORE-004 Mission
==========================================================

This system validates contract database integrity and recovers corrupted contracts.
Part of the emergency system restoration mission for Agent-5.
"""

import json
import datetime
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass

@dataclass
class ValidationIssue:
    """Represents a validation issue found in the contract database"""
    contract_id: str
    issue_type: str
    severity: str
    description: str
    current_value: Any
    expected_value: Any
    recovery_action: str

@dataclass
class ValidationResult:
    """Result of contract database validation"""
    total_contracts: int
    valid_contracts: int
    corrupted_contracts: int
    issues_found: List[ValidationIssue]
    recovery_actions: List[str]
    validation_timestamp: str

class ContractDatabaseValidator:
    """Validates and recovers contract database integrity"""
    
    def __init__(self, task_list_path: str = "agent_workspaces/meeting/task_list.json"):
        self.task_list_path = Path(task_list_path)
        self.contracts = {}
        self.issues = []
        self.recovery_actions = []
        self.logger = self._setup_logging()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for validation operations"""
        logger = logging.getLogger("ContractDatabaseValidator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
        
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
            
    def validate_contract_structure(self) -> List[ValidationIssue]:
        """Validate the overall structure of the contract database"""
        issues = []
        
        # Check required top-level fields
        required_fields = [
            "task_list_id", "timestamp", "total_contracts", 
            "available_contracts", "claimed_contracts", "completed_contracts"
        ]
        
        for field in required_fields:
            if field not in self.contracts:
                issues.append(ValidationIssue(
                    contract_id="SYSTEM",
                    issue_type="MISSING_FIELD",
                    severity="CRITICAL",
                    description=f"Missing required field: {field}",
                    current_value=None,
                    expected_value="Required field",
                    recovery_action=f"Add missing field: {field}"
                ))
                
        # Validate contract count consistency
        total_claimed = self.contracts.get("claimed_contracts", 0)
        total_completed = self.contracts.get("completed_contracts", 0)
        total_available = self.contracts.get("available_contracts", 0)
        total_contracts = self.contracts.get("total_contracts", 0)
        
        calculated_total = total_claimed + total_completed + total_available
        
        if calculated_total != total_contracts:
            issues.append(ValidationIssue(
                contract_id="SYSTEM",
                issue_type="COUNT_MISMATCH",
                severity="CRITICAL",
                description="Contract count mismatch",
                current_value=f"Claimed: {total_claimed}, Completed: {total_completed}, Available: {total_available}",
                expected_value=f"Total: {total_contracts}",
                recovery_action="Recalculate and fix contract counts"
            ))
            
        return issues
        
    def validate_individual_contracts(self) -> List[ValidationIssue]:
        """Validate individual contract entries"""
        issues = []
        
        if "contracts" not in self.contracts:
            return issues
            
        for category_name, category_data in self.contracts["contracts"].items():
            if "contracts" not in category_data:
                continue
                
            for contract in category_data["contracts"]:
                contract_issues = self._validate_single_contract(contract, category_name)
                issues.extend(contract_issues)
                
        return issues
        
    def _validate_single_contract(self, contract: Dict[str, Any], category: str) -> List[ValidationIssue]:
        """Validate a single contract entry"""
        issues = []
        contract_id = contract.get("contract_id", "UNKNOWN")
        
        # Check required fields
        required_fields = [
            "title", "description", "difficulty", "extra_credit_points",
            "requirements", "deliverables", "status"
        ]
        
        for field in required_fields:
            if field not in contract:
                issues.append(ValidationIssue(
                    contract_id=contract_id,
                    issue_type="MISSING_FIELD",
                    severity="HIGH",
                    description=f"Missing required field: {field}",
                    current_value=None,
                    expected_value="Required field",
                    recovery_action=f"Add missing field: {field} to contract {contract_id}"
                ))
                
        # Validate status consistency
        status = contract.get("status")
        claimed_by = contract.get("claimed_by")
        claimed_at = contract.get("claimed_at")
        completed_at = contract.get("completed_at")
        
        if status == "CLAIMED":
            if not claimed_by:
                issues.append(ValidationIssue(
                    contract_id=contract_id,
                    issue_type="STATUS_INCONSISTENCY",
                    severity="HIGH",
                    description="Contract marked as CLAIMED but no agent assigned",
                    current_value=f"Status: {status}, Claimed by: {claimed_by}",
                    expected_value="CLAIMED status requires claimed_by field",
                    recovery_action=f"Fix contract {contract_id} status or assign agent"
                ))
                
            if not claimed_at:
                issues.append(ValidationIssue(
                    contract_id=contract_id,
                    issue_type="STATUS_INCONSISTENCY",
                    severity="MEDIUM",
                    description="Contract marked as CLAIMED but no claim timestamp",
                    current_value=f"Status: {status}, Claimed at: {claimed_at}",
                    expected_value="CLAIMED status requires claimed_at timestamp",
                    recovery_action=f"Add claim timestamp to contract {contract_id}"
                ))
                
        elif status == "COMPLETED":
            if not completed_at:
                issues.append(ValidationIssue(
                    contract_id=contract_id,
                    issue_type="STATUS_INCONSISTENCY",
                    severity="HIGH",
                    description="Contract marked as COMPLETED but no completion timestamp",
                    current_value=f"Status: {status}, Completed at: {completed_at}",
                    expected_value="COMPLETED status requires completed_at timestamp",
                    recovery_action=f"Add completion timestamp to contract {contract_id}"
                ))
                
        # Validate timestamp format
        if claimed_at:
            try:
                datetime.datetime.fromisoformat(claimed_at.replace('Z', '+00:00'))
            except ValueError:
                issues.append(ValidationIssue(
                    contract_id=contract_id,
                    issue_type="INVALID_TIMESTAMP",
                    severity="MEDIUM",
                    description="Invalid claim timestamp format",
                    current_value=claimed_at,
                    expected_value="ISO 8601 format timestamp",
                    recovery_action=f"Fix timestamp format for contract {contract_id}"
                ))
                
        if completed_at:
            try:
                datetime.datetime.fromisoformat(completed_at.replace('Z', '+00:00'))
            except ValueError:
                issues.append(ValidationIssue(
                    contract_id=contract_id,
                    issue_type="INVALID_TIMESTAMP",
                    severity="MEDIUM",
                    description="Invalid completion timestamp format",
                    current_value=completed_at,
                    expected_value="ISO 8601 format timestamp",
                    recovery_action=f"Fix timestamp format for contract {contract_id}"
                ))
                
        return issues
        
    def generate_recovery_actions(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate recovery actions based on validation issues"""
        actions = []
        
        # Group issues by type for efficient recovery
        missing_fields = [i for i in issues if i.issue_type == "MISSING_FIELD"]
        status_issues = [i for i in issues if i.issue_type == "STATUS_INCONSISTENCY"]
        timestamp_issues = [i for i in issues if i.issue_type == "INVALID_TIMESTAMP"]
        count_issues = [i for i in issues if i.issue_type == "COUNT_MISMATCH"]
        
        if count_issues:
            actions.append("Recalculate contract counts and update database")
            
        if missing_fields:
            actions.append(f"Add {len(missing_fields)} missing required fields")
            
        if status_issues:
            actions.append(f"Fix {len(status_issues)} status inconsistencies")
            
        if timestamp_issues:
            actions.append(f"Fix {len(timestamp_issues)} timestamp format issues")
            
        return actions
        
    def validate_database(self) -> ValidationResult:
        """Perform comprehensive database validation"""
        self.logger.info("Starting contract database validation...")
        
        if not self.load_contracts():
            return ValidationResult(
                total_contracts=0,
                valid_contracts=0,
                corrupted_contracts=0,
                issues_found=[],
                recovery_actions=["Failed to load contracts"],
                validation_timestamp=datetime.datetime.now().isoformat()
            )
            
        # Perform validations
        structure_issues = self.validate_contract_structure()
        contract_issues = self.validate_individual_contracts()
        
        all_issues = structure_issues + contract_issues
        
        # Generate recovery actions
        recovery_actions = self.generate_recovery_actions(all_issues)
        
        # Calculate statistics
        total_contracts = self.contracts.get("total_contracts", 0)
        corrupted_contracts = len(all_issues)
        valid_contracts = total_contracts - corrupted_contracts
        
        result = ValidationResult(
            total_contracts=total_contracts,
            valid_contracts=valid_contracts,
            corrupted_contracts=corrupted_contracts,
            issues_found=all_issues,
            recovery_actions=recovery_actions,
            validation_timestamp=datetime.datetime.now().isoformat()
        )
        
        self.logger.info(f"Validation complete: {valid_contracts}/{total_contracts} contracts valid")
        return result
        
    def save_validation_report(self, result: ValidationResult, output_path: str = None) -> bool:
        """Save validation report to file"""
        if not output_path:
            output_path = f"contract_validation_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        try:
            report_data = {
                "validation_timestamp": result.validation_timestamp,
                "summary": {
                    "total_contracts": result.total_contracts,
                    "valid_contracts": result.valid_contracts,
                    "corrupted_contracts": result.corrupted_contracts,
                    "integrity_percentage": round((result.valid_contracts / result.total_contracts) * 100, 2) if result.total_contracts > 0 else 0
                },
                "issues": [
                    {
                        "contract_id": issue.contract_id,
                        "issue_type": issue.issue_type,
                        "severity": issue.severity,
                        "description": issue.description,
                        "current_value": str(issue.current_value),
                        "expected_value": str(issue.expected_value),
                        "recovery_action": issue.recovery_action
                    }
                    for issue in result.issues_found
                ],
                "recovery_actions": result.recovery_actions
            }
            
            with open(output_path, 'w') as f:
                json.dump(report_data, f, indent=2)
                
            self.logger.info(f"Validation report saved to: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save validation report: {e}")
            return False

def main():
    """Main function for command-line execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Contract Database Validator - EMERGENCY-RESTORE-004 Mission"
    )
    parser.add_argument(
        "--task-list", 
        default="agent_workspaces/meeting/task_list.json",
        help="Path to task list file"
    )
    parser.add_argument(
        "--output", 
        help="Output path for validation report"
    )
    
    args = parser.parse_args()
    
    # Initialize validator
    validator = ContractDatabaseValidator(args.task_list)
    
    # Perform validation
    result = validator.validate_database()
    
    # Display results
    print(f"\n{'='*80}")
    print(f"CONTRACT DATABASE VALIDATION REPORT")
    print(f"{'='*80}")
    print(f"Total Contracts: {result.total_contracts}")
    print(f"Valid Contracts: {result.valid_contracts}")
    print(f"Corrupted Contracts: {result.corrupted_contracts}")
    print(f"Integrity: {round((result.valid_contracts / result.total_contracts) * 100, 2)}%")
    print(f"Issues Found: {len(result.issues_found)}")
    print(f"Recovery Actions: {len(result.recovery_actions)}")
    
    if result.issues_found:
        print(f"\n{'='*80}")
        print(f"VALIDATION ISSUES")
        print(f"{'='*80}")
        for issue in result.issues_found:
            print(f"\n🔴 {issue.issue_type} - {issue.severity}")
            print(f"   Contract: {issue.contract_id}")
            print(f"   Description: {issue.description}")
            print(f"   Recovery: {issue.recovery_action}")
            
    if result.recovery_actions:
        print(f"\n{'='*80}")
        print(f"RECOVERY ACTIONS REQUIRED")
        print(f"{'='*80}")
        for i, action in enumerate(result.recovery_actions, 1):
            print(f"{i}. {action}")
            
    # Save report
    if args.output:
        validator.save_validation_report(result, args.output)
    else:
        validator.save_validation_report(result)
        
    print(f"\n{'='*80}")
    print(f"Validation complete. Report saved.")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
