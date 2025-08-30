"""
Corruption Scanner - Database corruption detection and scanning.

This module handles scanning for corrupted or missing contracts and data.
"""

import json
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

from .models import IntegrityIssue, RecoveryAction


class CorruptionScanner:
    """Handles scanning for database corruption and data issues."""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
    
    def scan_for_corruption(self, task_list_path: Path) -> Dict[str, Any]:
        """Scan for corrupted or missing contracts."""
        self.logger.info("Scanning for corruption...")
        
        try:
            with open(task_list_path, 'r') as f:
                task_list = json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load task list for corruption scan: {e}")
            return {
                "corruption_detected": True,
                "critical_error": f"Failed to load task list: {str(e)}",
                "integrity_issues": [],
                "recovery_actions": []
            }
        
        contracts = task_list.get("contracts", [])
        integrity_issues = []
        recovery_actions = []
        
        # Scan for various types of corruption
        integrity_issues.extend(self._scan_for_missing_contracts(contracts))
        integrity_issues.extend(self._scan_for_corrupted_data(contracts))
        integrity_issues.extend(self._scan_for_orphaned_references(contracts))
        integrity_issues.extend(self._scan_for_data_integrity_violations(contracts))
        
        # Generate recovery actions based on issues found
        recovery_actions.extend(self._generate_recovery_actions(integrity_issues))
        
        corruption_detected = len(integrity_issues) > 0
        
        return {
            "corruption_detected": corruption_detected,
            "total_issues": len(integrity_issues),
            "critical_issues": len([i for i in integrity_issues if i.severity == "CRITICAL"]),
            "high_priority_issues": len([i for i in integrity_issues if i.severity == "HIGH"]),
            "integrity_issues": integrity_issues,
            "recovery_actions": recovery_actions
        }
    
    def _scan_for_missing_contracts(self, contracts: List[Dict[str, Any]]) -> List[IntegrityIssue]:
        """Scan for missing or incomplete contracts."""
        issues = []
        
        for i, contract in enumerate(contracts):
            # Check for missing required fields
            required_fields = ["id", "title", "status", "agent"]
            missing_fields = [field for field in required_fields if field not in contract]
            
            if missing_fields:
                issues.append(IntegrityIssue(
                    issue_id=f"missing_fields_{i}",
                    severity="HIGH",
                    description=f"Contract {i} missing required fields: {missing_fields}",
                    affected_contracts=[contract.get("id", f"index_{i}")],
                    suggested_fix=f"Add missing fields: {missing_fields}"
                ))
            
            # Check for empty or null values in critical fields
            critical_fields = ["title", "description"]
            for field in critical_fields:
                value = contract.get(field)
                if value is not None and isinstance(value, str) and not value.strip():
                    issues.append(IntegrityIssue(
                        issue_id=f"empty_field_{i}_{field}",
                        severity="MEDIUM",
                        description=f"Contract {i} has empty {field} field",
                        affected_contracts=[contract.get("id", f"index_{i}")],
                        suggested_fix=f"Provide valid content for {field} field"
                    ))
        
        return issues
    
    def _scan_for_corrupted_data(self, contracts: List[Dict[str, Any]]) -> List[IntegrityIssue]:
        """Scan for corrupted or invalid data in contracts."""
        issues = []
        
        for i, contract in enumerate(contracts):
            # Check for invalid status values
            status = contract.get("status")
            valid_statuses = {"PENDING", "ACTIVE", "COMPLETED", "FAILED", "CANCELLED"}
            if status and status not in valid_statuses:
                issues.append(IntegrityIssue(
                    issue_id=f"invalid_status_{i}",
                    severity="HIGH",
                    description=f"Contract {i} has invalid status: {status}",
                    affected_contracts=[contract.get("id", f"index_{i}")],
                    suggested_fix=f"Update status to one of: {', '.join(valid_statuses)}"
                ))
            
            # Check for invalid numeric values
            numeric_fields = ["points", "estimated_hours", "actual_hours"]
            for field in numeric_fields:
                value = contract.get(field)
                if value is not None:
                    if not isinstance(value, (int, float)):
                        issues.append(IntegrityIssue(
                            issue_id=f"invalid_numeric_{i}_{field}",
                            severity="MEDIUM",
                            description=f"Contract {i} has invalid {field}: {value} (expected number)",
                            affected_contracts=[contract.get("id", f"index_{i}")],
                            suggested_fix=f"Fix {field} to be a valid number"
                        ))
                    elif value < 0:
                        issues.append(IntegrityIssue(
                            issue_id=f"negative_value_{i}_{field}",
                            severity="MEDIUM",
                            description=f"Contract {i} has negative {field}: {value}",
                            affected_contracts=[contract.get("id", f"index_{i}")],
                            suggested_fix=f"Fix {field} to be non-negative"
                        ))
            
            # Check for invalid timestamps
            timestamp_fields = ["created_at", "updated_at", "completion_time", "deadline"]
            for field in timestamp_fields:
                value = contract.get(field)
                if value:
                    try:
                        if isinstance(value, str):
                            datetime.fromisoformat(value.replace('Z', '+00:00'))
                        elif not isinstance(value, datetime):
                            issues.append(IntegrityIssue(
                                issue_id=f"invalid_timestamp_{i}_{field}",
                                severity="MEDIUM",
                                description=f"Contract {i} has invalid {field} format: {value}",
                                affected_contracts=[contract.get("id", f"index_{i}")],
                                suggested_fix=f"Fix {field} to be a valid ISO timestamp"
                            ))
                    except ValueError:
                        issues.append(IntegrityIssue(
                            issue_id=f"invalid_timestamp_{i}_{field}",
                            severity="MEDIUM",
                            description=f"Contract {i} has invalid {field} format: {value}",
                            affected_contracts=[contract.get("id", f"index_{i}")],
                            suggested_fix=f"Fix {field} to be a valid ISO timestamp"
                        ))
        
        return issues
    
    def _scan_for_orphaned_references(self, contracts: List[Dict[str, Any]]) -> List[IntegrityIssue]:
        """Scan for orphaned references and broken links."""
        issues = []
        
        # Check for duplicate contract IDs
        contract_ids = {}
        for i, contract in enumerate(contracts):
            contract_id = contract.get("id")
            if contract_id:
                if contract_id in contract_ids:
                    issues.append(IntegrityIssue(
                        issue_id=f"duplicate_id_{contract_id}",
                        severity="CRITICAL",
                        description=f"Duplicate contract ID found: {contract_id}",
                        affected_contracts=[contract_id],
                        suggested_fix="Ensure all contract IDs are unique"
                    ))
                else:
                    contract_ids[contract_id] = i
        
        # Check for references to non-existent agents
        # This would require access to agent registry
        # For now, we'll just check for empty agent references
        for i, contract in enumerate(contracts):
            agent = contract.get("agent")
            if not agent or (isinstance(agent, str) and not agent.strip()):
                issues.append(IntegrityIssue(
                    issue_id=f"missing_agent_{i}",
                    severity="HIGH",
                    description=f"Contract {i} has no assigned agent",
                    affected_contracts=[contract.get("id", f"index_{i}")],
                    suggested_fix="Assign a valid agent to the contract"
                ))
        
        return issues
    
    def _scan_for_data_integrity_violations(self, contracts: List[Dict[str, Any]]) -> List[IntegrityIssue]:
        """Scan for data integrity violations and logical inconsistencies."""
        issues = []
        
        for i, contract in enumerate(contracts):
            # Check for logical inconsistencies in status and timing
            status = contract.get("status")
            completion_time = contract.get("completion_time")
            deadline = contract.get("deadline")
            
            if status == "COMPLETED" and completion_time:
                try:
                    if isinstance(completion_time, str):
                        completion_dt = datetime.fromisoformat(completion_time.replace('Z', '+00:00'))
                    else:
                        completion_dt = completion_time
                    
                    # Check if completion time is in the future
                    if completion_dt > datetime.now():
                        issues.append(IntegrityIssue(
                            issue_id=f"future_completion_{i}",
                            severity="HIGH",
                            description=f"Contract {i} marked as completed with future completion time",
                            affected_contracts=[contract.get("id", f"index_{i}")],
                            suggested_fix="Fix completion time to be in the past"
                        ))
                except Exception:
                    pass
            
            # Check for deadline violations
            if status == "ACTIVE" and deadline:
                try:
                    if isinstance(deadline, str):
                        deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
                    else:
                        deadline_dt = deadline
                    
                    # Check if deadline has passed but status is still active
                    if deadline_dt < datetime.now():
                        issues.append(IntegrityIssue(
                            issue_id=f"overdue_deadline_{i}",
                            severity="MEDIUM",
                            description=f"Contract {i} is overdue (deadline: {deadline})",
                            affected_contracts=[contract.get("id", f"index_{i}")],
                            suggested_fix="Update contract status or extend deadline"
                        ))
                except Exception:
                    pass
        
        return issues
    
    def _generate_recovery_actions(self, integrity_issues: List[IntegrityIssue]) -> List[RecoveryAction]:
        """Generate recovery actions based on integrity issues found."""
        actions = []
        
        # Group issues by severity
        critical_issues = [i for i in integrity_issues if i.severity == "CRITICAL"]
        high_priority_issues = [i for i in integrity_issues if i.severity == "HIGH"]
        medium_priority_issues = [i for i in integrity_issues if i.severity == "MEDIUM"]
        
        # Critical issues - immediate action required
        if critical_issues:
            actions.append(RecoveryAction(
                action_id="emergency_recovery",
                priority=1,
                description="Emergency recovery for critical integrity issues",
                affected_components=[i.affected_contracts[0] for i in critical_issues[:3]],
                estimated_time=30,
                status="PENDING"
            ))
        
        # High priority issues - urgent action required
        if high_priority_issues:
            actions.append(RecoveryAction(
                action_id="urgent_repair",
                priority=2,
                description="Urgent repair for high priority integrity issues",
                affected_components=[i.affected_contracts[0] for i in high_priority_issues[:5]],
                estimated_time=60,
                status="PENDING"
            ))
        
        # Medium priority issues - scheduled maintenance
        if medium_priority_issues:
            actions.append(RecoveryAction(
                action_id="scheduled_maintenance",
                priority=3,
                description="Scheduled maintenance for medium priority issues",
                affected_components=[i.affected_contracts[0] for i in medium_priority_issues[:10]],
                estimated_time=120,
                status="PENDING"
            ))
        
        # General recovery action
        if integrity_issues:
            actions.append(RecoveryAction(
                action_id="comprehensive_audit",
                priority=4,
                description="Comprehensive database audit and cleanup",
                affected_components=["database"],
                estimated_time=240,
                status="PENDING"
            ))
        
        return actions
