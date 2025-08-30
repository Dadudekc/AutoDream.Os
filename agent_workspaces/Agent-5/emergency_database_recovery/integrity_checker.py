"""
Integrity Checker - Contract validation and integrity checks.

This module handles contract validation, integrity checking, and status accuracy validation.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .models import ContractValidation, IntegrityCheckResult


class IntegrityChecker:
    """Handles contract validation and integrity checking."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def validate_contract_status_accuracy(self, task_list_path: Path) -> ContractValidation:
        """Validate the accuracy of contract status information."""
        self.logger.info("Validating contract status accuracy...")
        
        try:
            with open(task_list_path, 'r') as f:
                task_list = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load task list: {e}")
            return ContractValidation(
                total_contracts=0,
                valid_contracts=0,
                corrupted_contracts=0,
                missing_contracts=0,
                validation_errors=[f"Failed to load task list: {str(e)}"],
                corruption_details=[]
            )
        
        contracts = task_list.get("contracts", [])
        total_contracts = len(contracts)
        valid_contracts = 0
        corrupted_contracts = 0
        missing_contracts = 0
        validation_errors = []
        corruption_details = []
        
        for i, contract in enumerate(contracts):
            try:
                # Check required fields
                required_fields = ["id", "title", "status", "agent"]
                missing_fields = [field for field in required_fields if field not in contract]
                
                if missing_fields:
                    corrupted_contracts += 1
                    corruption_details.append({
                        "contract_index": i,
                        "contract_id": contract.get("id", "UNKNOWN"),
                        "missing_fields": missing_fields,
                        "error_type": "missing_required_fields"
                    })
                    validation_errors.append(f"Contract {i} missing fields: {missing_fields}")
                    continue
                
                # Validate status values
                status = contract.get("status")
                valid_statuses = {"PENDING", "ACTIVE", "COMPLETED", "FAILED", "CANCELLED"}
                if status not in valid_statuses:
                    corrupted_contracts += 1
                    corruption_details.append({
                        "contract_index": i,
                        "contract_id": contract.get("id"),
                        "invalid_status": status,
                        "error_type": "invalid_status"
                    })
                    validation_errors.append(f"Contract {i} has invalid status: {status}")
                    continue
                
                # Check for logical inconsistencies
                if self._has_logical_inconsistencies(contract):
                    corrupted_contracts += 1
                    corruption_details.append({
                        "contract_index": i,
                        "contract_id": contract.get("id"),
                        "error_type": "logical_inconsistency",
                        "details": "Contract has logical inconsistencies"
                    })
                    validation_errors.append(f"Contract {i} has logical inconsistencies")
                    continue
                
                valid_contracts += 1
                
            except Exception as e:
                corrupted_contracts += 1
                corruption_details.append({
                    "contract_index": i,
                    "contract_id": contract.get("id", "UNKNOWN") if isinstance(contract, dict) else "UNKNOWN",
                    "error_type": "validation_exception",
                    "exception": str(e)
                })
                validation_errors.append(f"Contract {i} validation failed: {str(e)}")
        
        return ContractValidation(
            total_contracts=total_contracts,
            valid_contracts=valid_contracts,
            corrupted_contracts=corrupted_contracts,
            missing_contracts=missing_contracts,
            validation_errors=validation_errors,
            corruption_details=corruption_details
        )
    
    def _has_logical_inconsistencies(self, contract: Dict[str, Any]) -> bool:
        """Check for logical inconsistencies in a contract."""
        # Check completion time vs status
        if contract.get("status") == "COMPLETED":
            completion_time = contract.get("completion_time")
            if completion_time:
                try:
                    if isinstance(completion_time, str):
                        completion_dt = datetime.fromisoformat(completion_time.replace('Z', '+00:00'))
                    else:
                        completion_dt = completion_time
                    
                    # Check if completion time is in the future
                    if completion_dt > datetime.now():
                        return True
                except Exception:
                    return True
        
        # Check for negative values in numeric fields
        numeric_fields = ["points", "estimated_hours", "actual_hours"]
        for field in numeric_fields:
            value = contract.get(field)
            if isinstance(value, (int, float)) and value < 0:
                return True
        
        # Check for empty required string fields
        string_fields = ["title", "description"]
        for field in string_fields:
            value = contract.get(field)
            if value is not None and isinstance(value, str) and not value.strip():
                return True
        
        return False
    
    def run_integrity_check(self, task_list_path: Path) -> IntegrityCheckResult:
        """Run comprehensive integrity checks on the database."""
        self.logger.info("Running integrity checks...")
        
        checks_performed = 0
        checks_passed = 0
        checks_failed = 0
        critical_failures = 0
        warnings = 0
        recommendations = []
        next_actions = []
        
        try:
            # Check 1: File accessibility
            checks_performed += 1
            if task_list_path.exists() and task_list_path.is_file():
                checks_passed += 1
            else:
                checks_failed += 1
                critical_failures += 1
                recommendations.append("Ensure task_list.json file exists and is accessible")
                next_actions.append("Verify file path and permissions")
            
            # Check 2: JSON validity
            checks_performed += 1
            try:
                with open(task_list_path, 'r') as f:
                    json.load(f)
                checks_passed += 1
            except json.JSONDecodeError:
                checks_failed += 1
                critical_failures += 1
                recommendations.append("Fix JSON syntax errors in task_list.json")
                next_actions.append("Validate JSON format and fix syntax errors")
            
            # Check 3: Contract validation
            checks_performed += 1
            contract_validation = self.validate_contract_status_accuracy(task_list_path)
            
            if contract_validation.corrupted_contracts == 0:
                checks_passed += 1
            elif contract_validation.corrupted_contracts < 5:
                checks_passed += 1
                warnings += 1
                recommendations.append(f"Found {contract_validation.corrupted_contracts} corrupted contracts")
                next_actions.append("Review and fix corrupted contracts")
            else:
                checks_failed += 1
                critical_failures += 1
                recommendations.append(f"Critical: {contract_validation.corrupted_contracts} corrupted contracts found")
                next_actions.append("Immediate contract repair required")
            
            # Check 4: Data consistency
            checks_performed += 1
            try:
                with open(task_list_path, 'r') as f:
                    task_list = json.load(f)
                
                contracts = task_list.get("contracts", [])
                metadata = task_list.get("metadata", {})
                
                expected_count = metadata.get("total_contracts", 0)
                actual_count = len(contracts)
                
                if expected_count == actual_count or expected_count == 0:
                    checks_passed += 1
                else:
                    checks_failed += 1
                    warnings += 1
                    recommendations.append(f"Contract count mismatch: expected {expected_count}, got {actual_count}")
                    next_actions.append("Update metadata to match actual contract count")
                    
            except Exception as e:
                checks_failed += 1
                warnings += 1
                recommendations.append(f"Data consistency check failed: {str(e)}")
                next_actions.append("Investigate data loading issues")
            
        except Exception as e:
            checks_failed += 1
            critical_failures += 1
            recommendations.append(f"Integrity check system error: {str(e)}")
            next_actions.append("Check system logs and restart integrity checker")
        
        # Generate overall recommendations
        if critical_failures > 0:
            recommendations.insert(0, "CRITICAL: System integrity compromised - immediate action required")
            next_actions.insert(0, "Stop all operations and initiate emergency recovery")
        elif warnings > 0:
            recommendations.insert(0, "WARNING: System has integrity issues that need attention")
            next_actions.insert(0, "Schedule maintenance to address integrity issues")
        else:
            recommendations.insert(0, "System integrity verified - all checks passed")
            next_actions.insert(0, "Continue normal operations")
        
        return IntegrityCheckResult(
            checks_performed=checks_performed,
            checks_passed=checks_passed,
            checks_failed=checks_failed,
            critical_failures=critical_failures,
            warnings=warnings,
            recommendations=recommendations,
            next_actions=next_actions
        )
