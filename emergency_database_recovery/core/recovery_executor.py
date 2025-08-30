#!/usr/bin/env python3
"""
Recovery Executor - Emergency Database Recovery System
Provides database recovery execution and orchestration functionality
"""

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..models.recovery_actions import RecoveryAction, RecoveryPlan
from ..services.logging_service import LoggingService
from ..services.notification_service import NotificationService
from ..services.reporting_service import ReportingService


class RecoveryExecutor:
    """Database recovery execution and orchestration system"""

    def __init__(self):
        self.logger = LoggingService().get_logger("RecoveryExecutor")
        self.notification_service = NotificationService()
        self.reporting_service = ReportingService()

        # Recovery strategies
        self.recovery_strategies = {
            "file_restoration": self._restore_from_backup,
            "data_reconstruction": self._reconstruct_data,
            "schema_repair": self._repair_schema,
            "corruption_removal": self._remove_corruption,
        }

        # Recovery priorities
        self.recovery_priorities = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}

    def execute_recovery_plan(self, recovery_plan: RecoveryPlan) -> Dict[str, Any]:
        """Execute a comprehensive recovery plan"""
        self.logger.info(f"Executing recovery plan: {recovery_plan.plan_id}")

        start_time = datetime.now()

        execution_result = {
            "plan_id": recovery_plan.plan_id,
            "timestamp": start_time.isoformat(),
            "execution_status": "in_progress",
            "actions_executed": 0,
            "actions_successful": 0,
            "actions_failed": 0,
            "actions_in_progress": 0,
            "recovery_results": {},
            "execution_duration_seconds": 0,
            "overall_success": False,
        }

        try:
            # Sort actions by priority
            sorted_actions = sorted(
                recovery_plan.actions,
                key=lambda x: self.recovery_priorities.get(x.priority, 5),
            )

            # Execute each action
            for action in sorted_actions:
                self.logger.info(
                    f"Executing recovery action: {action.action_id} - {action.description}"
                )

                action_result = self._execute_recovery_action(action)
                execution_result["recovery_results"][action.action_id] = action_result
                execution_result["actions_executed"] += 1

                if action_result["status"] == "success":
                    execution_result["actions_successful"] += 1
                elif action_result["status"] == "failed":
                    execution_result["actions_failed"] += 1
                else:
                    execution_result["actions_in_progress"] += 1

                # Check if we should continue after critical failures
                if (
                    action_result["status"] == "failed"
                    and action.priority == "CRITICAL"
                ):
                    self.logger.error(
                        f"Critical recovery action failed: {action.action_id}"
                    )
                    execution_result["execution_status"] = "failed_critical"
                    break

            # Determine overall execution status
            if execution_result["actions_failed"] == 0:
                execution_result["execution_status"] = "completed_success"
                execution_result["overall_success"] = True
            elif (
                execution_result["actions_failed"] > 0
                and execution_result["actions_successful"] > 0
            ):
                execution_result["execution_status"] = "completed_partial"
                execution_result["overall_success"] = False
            else:
                execution_result["execution_status"] = "failed"
                execution_result["overall_success"] = False

            # Calculate execution duration
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            execution_result["execution_duration_seconds"] = duration

            # Send notifications
            self._notify_recovery_completion(execution_result)

            # Generate recovery report
            self._generate_recovery_report(execution_result)

            self.logger.info(
                f"Recovery plan execution completed in {duration:.2f}s. "
                f"Status: {execution_result['execution_status']}, "
                f"Success rate: {(execution_result['actions_successful'] / execution_result['actions_executed'] * 100):.1f}%"
            )

        except Exception as e:
            self.logger.error(f"Recovery plan execution failed: {e}")
            execution_result["error"] = str(e)
            execution_result["execution_status"] = "failed"
            execution_result["overall_success"] = False

        return execution_result

    def execute_single_recovery_action(self, action: RecoveryAction) -> Dict[str, Any]:
        """Execute a single recovery action"""
        self.logger.info(f"Executing single recovery action: {action.action_id}")

        return self._execute_recovery_action(action)

    def create_recovery_plan(
        self, issues: List[Dict[str, Any]], strategy: str = "comprehensive"
    ) -> RecoveryPlan:
        """Create a recovery plan based on identified issues"""
        self.logger.info(
            f"Creating recovery plan for {len(issues)} issues using {strategy} strategy"
        )

        plan_id = f"RECOVERY_PLAN_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        actions = []

        for issue in issues:
            action = self._create_recovery_action_for_issue(issue, strategy)
            if action:
                actions.append(action)

        recovery_plan = RecoveryPlan(
            plan_id=plan_id,
            timestamp=datetime.now().isoformat(),
            strategy=strategy,
            issues_count=len(issues),
            actions=actions,
            estimated_duration_minutes=len(actions) * 5,  # Rough estimate
            priority=self._determine_plan_priority(actions),
        )

        self.logger.info(f"Created recovery plan {plan_id} with {len(actions)} actions")
        return recovery_plan

    def validate_recovery_plan(self, recovery_plan: RecoveryPlan) -> Dict[str, Any]:
        """Validate a recovery plan before execution"""
        self.logger.info(f"Validating recovery plan: {recovery_plan.plan_id}")

        validation_result = {
            "plan_id": recovery_plan.plan_id,
            "valid": True,
            "validation_errors": [],
            "validation_warnings": [],
            "risk_assessment": "LOW",
            "recommendations": [],
        }

        # Check plan structure
        if not recovery_plan.actions:
            validation_result["valid"] = False
            validation_result["validation_errors"].append("No recovery actions defined")

        # Validate each action
        for action in recovery_plan.actions:
            action_validation = self._validate_recovery_action(action)
            if not action_validation["valid"]:
                validation_result["valid"] = False
                validation_result["validation_errors"].extend(
                    action_validation["errors"]
                )

            if action_validation["warnings"]:
                validation_result["validation_warnings"].extend(
                    action_validation["warnings"]
                )

        # Assess risk level
        critical_actions = [
            a for a in recovery_plan.actions if a.priority == "CRITICAL"
        ]
        if len(critical_actions) > 3:
            validation_result["risk_assessment"] = "HIGH"
            validation_result["recommendations"].append(
                "Consider breaking plan into smaller phases"
            )
        elif len(critical_actions) > 1:
            validation_result["risk_assessment"] = "MEDIUM"
            validation_result["recommendations"].append(
                "Monitor critical actions closely"
            )

        # Generate recommendations
        if validation_result["validation_errors"]:
            validation_result["recommendations"].append(
                "Fix all validation errors before execution"
            )

        if validation_result["validation_warnings"]:
            validation_result["recommendations"].append(
                "Review warnings and address as needed"
            )

        return validation_result

    def _execute_recovery_action(self, action: RecoveryAction) -> Dict[str, Any]:
        """Execute a single recovery action"""
        action_result = {
            "action_id": action.action_id,
            "status": "in_progress",
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_seconds": 0,
            "result": {},
            "error": None,
            "logs": [],
        }

        try:
            self.logger.info(
                f"Starting recovery action: {action.action_id} - {action.description}"
            )

            # Execute the action based on its type
            if action.action_type in self.recovery_strategies:
                result = self.recovery_strategies[action.action_type](action)
                action_result["result"] = result
                action_result["status"] = "success"
            else:
                raise ValueError(f"Unknown recovery action type: {action.action_type}")

            # Record completion time
            end_time = datetime.now()
            action_result["end_time"] = end_time.isoformat()
            action_result["duration_seconds"] = (
                end_time - datetime.fromisoformat(action_result["start_time"])
            ).total_seconds()

            self.logger.info(
                f"Recovery action completed successfully: {action.action_id}"
            )

        except Exception as e:
            self.logger.error(f"Recovery action failed: {action.action_id} - {e}")
            action_result["status"] = "failed"
            action_result["error"] = str(e)

            # Record completion time even for failed actions
            end_time = datetime.now()
            action_result["end_time"] = end_time.isoformat()
            action_result["duration_seconds"] = (
                end_time - datetime.fromisoformat(action_result["start_time"])
            ).total_seconds()

        return action_result

    def _restore_from_backup(self, action: RecoveryAction) -> Dict[str, Any]:
        """Restore file from backup"""
        source_path = Path(action.parameters.get("backup_path", ""))
        target_path = Path(action.parameters.get("target_path", ""))

        if not source_path.exists():
            raise FileNotFoundError(f"Backup file not found: {source_path}")

        # Create backup of current file if it exists
        if target_path.exists():
            backup_name = f"{target_path.name}.pre_recovery_backup"
            backup_path = target_path.parent / backup_name
            shutil.copy2(target_path, backup_path)
            self.logger.info(f"Created pre-recovery backup: {backup_path}")

        # Restore from backup
        shutil.copy2(source_path, target_path)
        self.logger.info(f"Restored {target_path} from backup {source_path}")

        return {
            "restored_file": str(target_path),
            "backup_source": str(source_path),
            "pre_recovery_backup": str(backup_path) if target_path.exists() else None,
        }

    def _reconstruct_data(self, action: RecoveryAction) -> Dict[str, Any]:
        """Reconstruct data from available sources"""
        target_file = Path(action.parameters.get("target_file", ""))
        source_files = [Path(p) for p in action.parameters.get("source_files", [])]

        reconstructed_data = {}

        # Attempt to reconstruct from source files
        for source_file in source_files:
            if source_file.exists():
                try:
                    with open(source_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        reconstructed_data.update(data)
                except Exception as e:
                    self.logger.warning(
                        f"Could not read source file {source_file}: {e}"
                    )

        # Save reconstructed data
        if reconstructed_data:
            with open(target_file, "w", encoding="utf-8") as f:
                json.dump(reconstructed_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"Reconstructed data saved to {target_file}")

        return {
            "reconstructed_file": str(target_file),
            "source_files_used": [str(f) for f in source_files if f.exists()],
            "data_fields_reconstructed": list(reconstructed_data.keys()),
        }

    def _repair_schema(self, action: RecoveryAction) -> Dict[str, Any]:
        """Repair file schema and structure"""
        target_file = Path(action.parameters.get("target_file", ""))
        schema_template = action.parameters.get("schema_template", {})

        if not target_file.exists():
            raise FileNotFoundError(f"Target file not found: {target_file}")

        # Read current file
        with open(target_file, "r", encoding="utf-8") as f:
            try:
                current_data = json.load(f)
            except json.JSONDecodeError:
                current_data = {}

        # Apply schema template
        repaired_data = self._apply_schema_template(current_data, schema_template)

        # Save repaired data
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(repaired_data, f, indent=2, ensure_ascii=False)

        self.logger.info(f"Schema repair completed for {target_file}")

        return {
            "repaired_file": str(target_file),
            "fields_added": len(repaired_data) - len(current_data),
            "schema_applied": bool(schema_template),
        }

    def _remove_corruption(self, action: RecoveryAction) -> Dict[str, Any]:
        """Remove corruption from file content"""
        target_file = Path(action.parameters.get("target_file", ""))
        corruption_patterns = action.parameters.get("corruption_patterns", [])

        if not target_file.exists():
            raise FileNotFoundError(f"Target file not found: {target_file}")

        # Read file content
        with open(target_file, "rb") as f:
            content = f.read()

        # Remove corruption patterns
        cleaned_content = content
        patterns_removed = 0

        for pattern in corruption_patterns:
            if pattern in str(content):
                cleaned_content = cleaned_content.replace(pattern.encode(), b"")
                patterns_removed += 1

        # Save cleaned content
        with open(target_file, "wb") as f:
            f.write(cleaned_content)

        self.logger.info(f"Corruption removal completed for {target_file}")

        return {
            "cleaned_file": str(target_file),
            "patterns_removed": patterns_removed,
            "original_size": len(content),
            "cleaned_size": len(cleaned_content),
        }

    def _create_recovery_action_for_issue(
        self, issue: Dict[str, Any], strategy: str
    ) -> Optional[RecoveryAction]:
        """Create a recovery action for a specific issue"""
        issue_type = issue.get("type", "unknown")
        severity = issue.get("severity", "MEDIUM")

        if issue_type == "file_missing":
            return RecoveryAction(
                action_id=f"RESTORE_{issue.get('filepath', 'unknown').replace('/', '_')}",
                action_type="file_restoration",
                description=f"Restore missing file: {issue.get('filepath', 'unknown')}",
                priority=severity,
                parameters={
                    "backup_path": issue.get("backup_path", ""),
                    "target_path": issue.get("filepath", ""),
                },
            )
        elif issue_type == "corruption_detected":
            return RecoveryAction(
                action_id=f"CLEAN_{issue.get('filepath', 'unknown').replace('/', '_')}",
                action_type="corruption_removal",
                description=f"Remove corruption from: {issue.get('filepath', 'unknown')}",
                priority=severity,
                parameters={
                    "target_file": issue.get("filepath", ""),
                    "corruption_patterns": issue.get("corruption_patterns", []),
                },
            )
        elif issue_type == "schema_invalid":
            return RecoveryAction(
                action_id=f"REPAIR_{issue.get('filepath', 'unknown').replace('/', '_')}",
                action_type="schema_repair",
                description=f"Repair schema for: {issue.get('filepath', 'unknown')}",
                priority=severity,
                parameters={
                    "target_file": issue.get("filepath", ""),
                    "schema_template": issue.get("schema_template", {}),
                },
            )

        return None

    def _determine_plan_priority(self, actions: List[RecoveryAction]) -> str:
        """Determine overall priority of recovery plan"""
        if not actions:
            return "LOW"

        priorities = [self.recovery_priorities.get(a.priority, 5) for a in actions]
        avg_priority = sum(priorities) / len(priorities)

        if avg_priority <= 1.5:
            return "CRITICAL"
        elif avg_priority <= 2.5:
            return "HIGH"
        elif avg_priority <= 3.5:
            return "MEDIUM"
        else:
            return "LOW"

    def _validate_recovery_action(self, action: RecoveryAction) -> Dict[str, Any]:
        """Validate a single recovery action"""
        validation_result = {"valid": True, "errors": [], "warnings": []}

        # Check required parameters
        if action.action_type == "file_restoration":
            if not action.parameters.get("backup_path"):
                validation_result["valid"] = False
                validation_result["errors"].append("Missing backup_path parameter")
            if not action.parameters.get("target_path"):
                validation_result["valid"] = False
                validation_result["errors"].append("Missing target_path parameter")

        elif action.action_type == "corruption_removal":
            if not action.parameters.get("target_file"):
                validation_result["valid"] = False
                validation_result["errors"].append("Missing target_file parameter")

        elif action.action_type == "schema_repair":
            if not action.parameters.get("target_file"):
                validation_result["valid"] = False
                validation_result["errors"].append("Missing target_file parameter")

        # Check action type validity
        if action.action_type not in self.recovery_strategies:
            validation_result["valid"] = False
            validation_result["errors"].append(
                f"Unknown action type: {action.action_type}"
            )

        return validation_result

    def _apply_schema_template(
        self, current_data: Dict[str, Any], schema_template: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply schema template to current data"""
        repaired_data = current_data.copy()

        for field, default_value in schema_template.items():
            if field not in repaired_data:
                repaired_data[field] = default_value

        return repaired_data

    def _notify_recovery_completion(self, execution_result: Dict[str, Any]):
        """Send notification about recovery completion"""
        try:
            success_rate = (
                (
                    execution_result["actions_successful"]
                    / execution_result["actions_executed"]
                    * 100
                )
                if execution_result["actions_executed"] > 0
                else 0
            )

            self.notification_service.notify_recovery_completion(
                recovery_summary=execution_result,
                success_rate=success_rate,
                time_taken=execution_result["execution_duration_seconds"],
            )
        except Exception as e:
            self.logger.error(f"Failed to send recovery completion notification: {e}")

    def _generate_recovery_report(self, execution_result: Dict[str, Any]):
        """Generate recovery execution report"""
        try:
            self.reporting_service.generate_recovery_action_report(
                recovery_actions=list(execution_result["recovery_results"].values()),
                status=execution_result["execution_status"],
                output_dir=Path("emergency_database_recovery/reports"),
            )
        except Exception as e:
            self.logger.error(f"Failed to generate recovery report: {e}")
