"""Task validation execution helpers."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from .base_validator import (
    BaseValidator,
    ValidationResult,
    ValidationSeverity,
    ValidationStatus,
)


def validate_task_structure(
    validator: BaseValidator, task_data: Dict[str, Any]
) -> List[ValidationResult]:
    """Validate task data structure and format."""
    results: List[ValidationResult] = []
    if not isinstance(task_data, dict):
        result = validator._create_result(
            rule_id="task_type",
            rule_name="Task Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task data must be a dictionary",
            actual_value=type(task_data).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if len(task_data) == 0:
        result = validator._create_result(
            rule_id="task_empty",
            rule_name="Task Empty Check",
            status=ValidationStatus.WARNING,
            severity=ValidationSeverity.WARNING,
            message="Task data is empty",
            actual_value=task_data,
            expected_value="non-empty task data",
        )
        results.append(result)
    return results


def validate_task_status(
    validator: BaseValidator, status: Any
) -> Optional[ValidationResult]:
    """Validate task status value."""
    if not isinstance(status, str):
        return validator._create_result(
            rule_id="status_type",
            rule_name="Status Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task status must be a string",
            field_path="status",
            actual_value=type(status).__name__,
            expected_value="str",
        )

    if status.lower() not in getattr(validator, "task_statuses", []):
        return validator._create_result(
            rule_id="status_invalid",
            rule_name="Status Invalid Value",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message=f"Invalid task status: {status}",
            field_path="status",
            actual_value=status,
            expected_value=f"one of {getattr(validator, 'task_statuses', [])}",
        )
    return None


def validate_task_priority(
    validator: BaseValidator, priority: Any
) -> Optional[ValidationResult]:
    """Validate task priority value."""
    if not isinstance(priority, str):
        return validator._create_result(
            rule_id="priority_type",
            rule_name="Priority Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task priority must be a string",
            field_path="priority",
            actual_value=type(priority).__name__,
            expected_value="str",
        )

    if priority.lower() not in getattr(validator, "task_priorities", []):
        return validator._create_result(
            rule_id="priority_invalid",
            rule_name="Priority Invalid Value",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message=f"Invalid task priority: {priority}",
            field_path="priority",
            actual_value=priority,
            expected_value=f"one of {getattr(validator, 'task_priorities', [])}",
        )
    return None


def validate_task_type(
    validator: BaseValidator, task_type: Any
) -> Optional[ValidationResult]:
    """Validate task type value."""
    if not isinstance(task_type, str):
        return validator._create_result(
            rule_id="type_type",
            rule_name="Type Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task type must be a string",
            field_path="type",
            actual_value=type(task_type).__name__,
            expected_value="str",
        )

    if task_type.lower() not in getattr(validator, "task_types", []):
        return validator._create_result(
            rule_id="type_invalid",
            rule_name="Type Invalid Value",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message=f"Invalid task type: {task_type}",
            field_path="type",
            actual_value=task_type,
            expected_value=f"one of {getattr(validator, 'task_types', [])}",
        )
    return None


def validate_task_assignment(
    validator: BaseValidator, assignment: Any
) -> List[ValidationResult]:
    """Validate task assignment data."""
    results: List[ValidationResult] = []
    if not isinstance(assignment, dict):
        result = validator._create_result(
            rule_id="assignment_type",
            rule_name="Assignment Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task assignment must be a dictionary",
            field_path="assignment",
            actual_value=type(assignment).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "assignee" in assignment:
        assignee = assignment["assignee"]
        if isinstance(assignee, str) and len(assignee) == 0:
            result = validator._create_result(
                rule_id="assignee_empty",
                rule_name="Assignee Empty Check",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task assignee cannot be empty",
                field_path="assignment.assignee",
                actual_value=assignee,
                expected_value="non-empty assignee",
            )
            results.append(result)

    if "assigned_date" in assignment:
        assigned_date = assignment["assigned_date"]
        if isinstance(assigned_date, str):
            from datetime import datetime

            try:
                datetime.fromisoformat(assigned_date.replace("Z", "+00:00"))
            except ValueError:
                result = validator._create_result(
                    rule_id="assigned_date_format",
                    rule_name="Assigned Date Format Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Invalid assigned date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)",
                    field_path="assignment.assigned_date",
                    actual_value=assigned_date,
                    expected_value="ISO format date string",
                )
                results.append(result)

    if "estimated_effort" in assignment:
        estimated_effort = assignment["estimated_effort"]
        if isinstance(estimated_effort, (int, float)) and estimated_effort <= 0:
            result = validator._create_result(
                rule_id="estimated_effort_invalid",
                rule_name="Estimated Effort Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Estimated effort must be greater than 0",
                field_path="assignment.estimated_effort",
                actual_value=estimated_effort,
                expected_value="> 0",
            )
            results.append(result)
    return results


def validate_task_dependencies(
    validator: BaseValidator, dependencies: Any
) -> List[ValidationResult]:
    """Validate task dependencies."""
    results: List[ValidationResult] = []
    if not isinstance(dependencies, list):
        result = validator._create_result(
            rule_id="dependencies_type",
            rule_name="Dependencies Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task dependencies must be a list",
            field_path="dependencies",
            actual_value=type(dependencies).__name__,
            expected_value="list",
        )
        results.append(result)
        return results

    for i, dependency in enumerate(dependencies):
        if isinstance(dependency, dict):
            if "task_id" in dependency:
                task_id = dependency["task_id"]
                if not isinstance(task_id, str) or len(task_id) == 0:
                    result = validator._create_result(
                        rule_id=f"dependency_{i}_task_id",
                        rule_name=f"Dependency {i} Task ID Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Dependency {i} task ID must be a non-empty string",
                        field_path=f"dependencies[{i}].task_id",
                        actual_value=task_id,
                        expected_value="non-empty string",
                    )
                    results.append(result)
            if "type" in dependency:
                dep_type = dependency["type"]
                valid_dep_types = ["blocks", "blocked_by", "related", "requires"]
                if (
                    isinstance(dep_type, str)
                    and dep_type.lower() not in valid_dep_types
                ):
                    result = validator._create_result(
                        rule_id=f"dependency_{i}_type_invalid",
                        rule_name=f"Dependency {i} Type Invalid Value",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Invalid dependency type: {dep_type}",
                        field_path=f"dependencies[{i}].type",
                        actual_value=dep_type,
                        expected_value=f"one of {valid_dep_types}",
                    )
                    results.append(result)
        else:
            result = validator._create_result(
                rule_id=f"dependency_{i}_type",
                rule_name=f"Dependency {i} Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Dependency {i} must be a dictionary",
                field_path=f"dependencies[{i}]",
                actual_value=type(dependency).__name__,
                expected_value="dict",
            )
            results.append(result)
    return results


def validate_task_progress(
    validator: BaseValidator, progress: Any
) -> List[ValidationResult]:
    """Validate task progress data."""
    results: List[ValidationResult] = []
    if not isinstance(progress, dict):
        result = validator._create_result(
            rule_id="progress_type",
            rule_name="Progress Type Validation",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.ERROR,
            message="Task progress must be a dictionary",
            field_path="progress",
            actual_value=type(progress).__name__,
            expected_value="dict",
        )
        results.append(result)
        return results

    if "completion_percentage" in progress:
        completion = progress["completion_percentage"]
        if isinstance(completion, (int, float)) and (
            completion < 0 or completion > 100
        ):
            result = validator._create_result(
                rule_id="completion_percentage_invalid",
                rule_name="Completion Percentage Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Completion percentage must be between 0 and 100",
                field_path="progress.completion_percentage",
                actual_value=completion,
                expected_value="0 <= completion <= 100",
            )
            results.append(result)

    if "time_spent" in progress:
        time_spent = progress["time_spent"]
        if isinstance(time_spent, (int, float)) and time_spent < 0:
            result = validator._create_result(
                rule_id="time_spent_invalid",
                rule_name="Time Spent Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Time spent cannot be negative",
                field_path="progress.time_spent",
                actual_value=time_spent,
                expected_value=">= 0",
            )
            results.append(result)

    if "milestones" in progress:
        milestones = progress["milestones"]
        if isinstance(milestones, list):
            for i, milestone in enumerate(milestones):
                if isinstance(milestone, dict):
                    if "completed" in milestone:
                        completed = milestone["completed"]
                        if not isinstance(completed, bool):
                            result = validator._create_result(
                                rule_id=f"milestone_{i}_completed_type",
                                rule_name=f"Milestone {i} Completed Type Validation",
                                status=ValidationStatus.FAILED,
                                severity=ValidationSeverity.ERROR,
                                message=f"Milestone {i} completed must be a boolean",
                                field_path=f"progress.milestones[{i}].completed",
                                actual_value=type(completed).__name__,
                                expected_value="bool",
                            )
                            results.append(result)
                else:
                    result = validator._create_result(
                        rule_id=f"milestone_{i}_type",
                        rule_name=f"Milestone {i} Type Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Milestone {i} must be a dictionary",
                        field_path=f"progress.milestones[{i}]",
                        actual_value=type(milestone).__name__,
                        expected_value="dict",
                    )
                    results.append(result)
    return results


def validate_task_consistency(
    validator: BaseValidator, task_data: Dict[str, Any]
) -> List[ValidationResult]:
    """Validate task consistency and logic."""
    results: List[ValidationResult] = []
    if "status" in task_data and "completion_date" in task_data:
        status = task_data["status"]
        completion_date = task_data["completion_date"]
        if isinstance(status, str) and isinstance(completion_date, str):
            if status.lower() == "completed" and not completion_date:
                result = validator._create_result(
                    rule_id="completion_date_missing",
                    rule_name="Completion Date Missing",
                    status=ValidationStatus.WARNING,
                    severity=ValidationSeverity.WARNING,
                    message="Completed task should have a completion date",
                    field_path="completion_date",
                    actual_value="missing",
                    expected_value="completion date for completed task",
                )
                results.append(result)

    if "estimated_effort" in task_data and "actual_effort" in task_data:
        estimated = task_data["estimated_effort"]
        actual = task_data["actual_effort"]
        if isinstance(estimated, (int, float)) and isinstance(actual, (int, float)):
            if estimated > 0 and actual > 0:
                ratio = actual / estimated
                if ratio > 3:
                    result = validator._create_result(
                        rule_id="effort_estimation_poor",
                        rule_name="Effort Estimation Poor",
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.WARNING,
                        message=(
                            f"Actual effort ({actual}) is {ratio:.1f}x estimated effort ({estimated})"
                        ),
                        field_path="effort_estimation",
                        actual_value=f"ratio: {ratio:.1f}",
                        expected_value="ratio <= 3.0",
                    )
                    results.append(result)

    if "dependencies" in task_data and "id" in task_data:
        dependencies = task_data["dependencies"]
        task_id = task_data["id"]
        if isinstance(dependencies, list) and isinstance(task_id, str):
            for dependency in dependencies:
                if isinstance(dependency, dict) and "task_id" in dependency:
                    if dependency["task_id"] == task_id:
                        result = validator._create_result(
                            rule_id="self_dependency",
                            rule_name="Self Dependency Check",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message="Task cannot depend on itself",
                            field_path="dependencies",
                            actual_value=f"self-reference: {task_id}",
                            expected_value="different task ID",
                        )
                        results.append(result)
    return results
