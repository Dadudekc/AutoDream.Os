"""
Task Validator - Unified Validation Framework

This module provides task validation functionality, inheriting from BaseValidator
and following the unified validation framework patterns.
"""

from typing import Dict, List, Any, Optional
from .base_validator import (
    BaseValidator,
    ValidationSeverity,
    ValidationStatus,
    ValidationResult,
)


class TaskValidator(BaseValidator):
    """Validates task data and assignments using unified validation framework"""

    def __init__(self):
        """Initialize task validator"""
        super().__init__("TaskValidator")
        self.task_statuses = [
            "pending",
            "assigned",
            "in_progress",
            "review",
            "completed",
            "cancelled",
            "failed",
        ]
        self.task_priorities = ["low", "medium", "high", "critical", "urgent"]
        self.task_types = [
            "development",
            "testing",
            "documentation",
            "deployment",
            "maintenance",
            "research",
            "bug_fix",
            "feature",
            "refactoring",
            "review",
        ]

    def validate(self, task_data: Dict[str, Any], **kwargs) -> List[ValidationResult]:
        """Validate task data and return validation results.

        Returns:
            List[ValidationResult]: Validation results produced during task
            validation.
        """
        results = []

        try:
            # Validate task data structure
            structure_results = self._validate_task_structure(task_data)
            results.extend(structure_results)

            # Validate required fields
            required_fields = ["id", "title", "description", "status", "priority"]
            field_results = self._validate_required_fields(task_data, required_fields)
            results.extend(field_results)

            # Validate task status if present
            if "status" in task_data:
                status_result = self._validate_task_status(task_data["status"])
                if status_result:
                    results.append(status_result)

            # Validate task priority if present
            if "priority" in task_data:
                priority_result = self._validate_task_priority(task_data["priority"])
                if priority_result:
                    results.append(priority_result)

            # Validate task type if present
            if "type" in task_data:
                type_result = self._validate_task_type(task_data["type"])
                if type_result:
                    results.append(type_result)

            # Validate assignment if present
            if "assignment" in task_data:
                assignment_results = self._validate_task_assignment(
                    task_data["assignment"]
                )
                results.extend(assignment_results)

            # Validate dependencies if present
            if "dependencies" in task_data:
                dependency_results = self._validate_task_dependencies(
                    task_data["dependencies"]
                )
                results.extend(dependency_results)

            # Validate progress if present
            if "progress" in task_data:
                progress_results = self._validate_task_progress(task_data["progress"])
                results.extend(progress_results)

            # Check task consistency
            consistency_results = self._validate_task_consistency(task_data)
            results.extend(consistency_results)

            # Add overall success result if no critical errors
            if not any(r.severity == ValidationSeverity.ERROR for r in results):
                success_result = self._create_result(
                    rule_id="overall_task_validation",
                    rule_name="Overall Task Validation",
                    status=ValidationStatus.PASSED,
                    severity=ValidationSeverity.INFO,
                    message="Task validation passed successfully",
                    details={"total_checks": len(results)},
                )
                results.append(success_result)

        except Exception as e:
            error_result = self._create_result(
                rule_id="task_validation_error",
                rule_name="Task Validation Error",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.CRITICAL,
                message=f"Task validation error: {str(e)}",
                details={"error_type": type(e).__name__},
            )
            results.append(error_result)

        return results

    def _validate_task_structure(
        self, task_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate task data structure and format"""
        results = []

        if not isinstance(task_data, dict):
            result = self._create_result(
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
            result = self._create_result(
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

    def _validate_task_status(self, status: Any) -> Optional[ValidationResult]:
        """Validate task status value"""
        if not isinstance(status, str):
            return self._create_result(
                rule_id="status_type",
                rule_name="Status Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task status must be a string",
                field_path="status",
                actual_value=type(status).__name__,
                expected_value="str",
            )

        if status.lower() not in self.task_statuses:
            return self._create_result(
                rule_id="status_invalid",
                rule_name="Status Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid task status: {status}",
                field_path="status",
                actual_value=status,
                expected_value=f"one of {self.task_statuses}",
            )

        return None

    def _validate_task_priority(self, priority: Any) -> Optional[ValidationResult]:
        """Validate task priority value"""
        if not isinstance(priority, str):
            return self._create_result(
                rule_id="priority_type",
                rule_name="Priority Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task priority must be a string",
                field_path="priority",
                actual_value=type(priority).__name__,
                expected_value="str",
            )

        if priority.lower() not in self.task_priorities:
            return self._create_result(
                rule_id="priority_invalid",
                rule_name="Priority Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid task priority: {priority}",
                field_path="priority",
                actual_value=priority,
                expected_value=f"one of {self.task_priorities}",
            )

        return None

    def _validate_task_type(self, task_type: Any) -> Optional[ValidationResult]:
        """Validate task type value"""
        if not isinstance(task_type, str):
            return self._create_result(
                rule_id="type_type",
                rule_name="Type Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task type must be a string",
                field_path="type",
                actual_value=type(task_type).__name__,
                expected_value="str",
            )

        if task_type.lower() not in self.task_types:
            return self._create_result(
                rule_id="type_invalid",
                rule_name="Type Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid task type: {task_type}",
                field_path="type",
                actual_value=task_type,
                expected_value=f"one of {self.task_types}",
            )

        return None

    def _validate_task_assignment(self, assignment: Any) -> List[ValidationResult]:
        """Validate task assignment data"""
        results = []

        if not isinstance(assignment, dict):
            result = self._create_result(
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

        # Validate assignee if present
        if "assignee" in assignment:
            assignee = assignment["assignee"]
            if isinstance(assignee, str):
                if len(assignee) == 0:
                    result = self._create_result(
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

        # Validate assignment date if present
        if "assigned_date" in assignment:
            assigned_date = assignment["assigned_date"]
            if isinstance(assigned_date, str):
                try:
                    from datetime import datetime

                    datetime.fromisoformat(assigned_date.replace("Z", "+00:00"))
                except ValueError:
                    result = self._create_result(
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

        # Validate estimated effort if present
        if "estimated_effort" in assignment:
            estimated_effort = assignment["estimated_effort"]
            if isinstance(estimated_effort, (int, float)):
                if estimated_effort <= 0:
                    result = self._create_result(
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

    def _validate_task_dependencies(self, dependencies: Any) -> List[ValidationResult]:
        """Validate task dependencies"""
        results = []

        if not isinstance(dependencies, list):
            result = self._create_result(
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

        # Validate each dependency
        for i, dependency in enumerate(dependencies):
            if isinstance(dependency, dict):
                # Validate dependency ID
                if "task_id" in dependency:
                    task_id = dependency["task_id"]
                    if not isinstance(task_id, str) or len(task_id) == 0:
                        result = self._create_result(
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

                # Validate dependency type if present
                if "type" in dependency:
                    dep_type = dependency["type"]
                    valid_dep_types = ["blocks", "blocked_by", "related", "requires"]

                    if isinstance(dep_type, str):
                        if dep_type.lower() not in valid_dep_types:
                            result = self._create_result(
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
                result = self._create_result(
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

    def _validate_task_progress(self, progress: Any) -> List[ValidationResult]:
        """Validate task progress data"""
        results = []

        if not isinstance(progress, dict):
            result = self._create_result(
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

        # Validate completion percentage if present
        if "completion_percentage" in progress:
            completion = progress["completion_percentage"]
            if isinstance(completion, (int, float)):
                if completion < 0 or completion > 100:
                    result = self._create_result(
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

        # Validate time spent if present
        if "time_spent" in progress:
            time_spent = progress["time_spent"]
            if isinstance(time_spent, (int, float)):
                if time_spent < 0:
                    result = self._create_result(
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

        # Validate milestones if present
        if "milestones" in progress:
            milestones = progress["milestones"]
            if isinstance(milestones, list):
                for i, milestone in enumerate(milestones):
                    if isinstance(milestone, dict):
                        # Validate milestone completion
                        if "completed" in milestone:
                            completed = milestone["completed"]
                            if not isinstance(completed, bool):
                                result = self._create_result(
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
                        result = self._create_result(
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

    def _validate_task_consistency(
        self, task_data: Dict[str, Any]
    ) -> List[ValidationResult]:
        """Validate task consistency and logic"""
        results = []

        # Check if completed tasks have completion date
        if "status" in task_data and "completion_date" in task_data:
            status = task_data["status"]
            completion_date = task_data["completion_date"]

            if isinstance(status, str) and isinstance(completion_date, str):
                if status.lower() == "completed" and not completion_date:
                    result = self._create_result(
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

        # Check if estimated effort is reasonable compared to actual effort
        if "estimated_effort" in task_data and "actual_effort" in task_data:
            estimated = task_data["estimated_effort"]
            actual = task_data["actual_effort"]

            if isinstance(estimated, (int, float)) and isinstance(actual, (int, float)):
                if estimated > 0 and actual > 0:
                    ratio = actual / estimated
                    if ratio > 3:  # Actual effort is 3x estimated
                        result = self._create_result(
                            rule_id="effort_estimation_poor",
                            rule_name="Effort Estimation Poor",
                            status=ValidationStatus.WARNING,
                            severity=ValidationSeverity.WARNING,
                            message=f"Actual effort ({actual}) is {ratio:.1f}x estimated effort ({estimated})",
                            field_path="effort_estimation",
                            actual_value=f"ratio: {ratio:.1f}",
                            expected_value="ratio <= 3.0",
                        )
                        results.append(result)

        # Check if task dependencies are valid
        if "dependencies" in task_data and "id" in task_data:
            dependencies = task_data["dependencies"]
            task_id = task_data["id"]

            if isinstance(dependencies, list) and isinstance(task_id, str):
                # Check for self-referencing dependencies
                for dependency in dependencies:
                    if isinstance(dependency, dict) and "task_id" in dependency:
                        if dependency["task_id"] == task_id:
                            result = self._create_result(
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

    def add_task_status(self, status: str) -> bool:
        """Add a custom task status"""
        try:
            if status not in self.task_statuses:
                self.task_statuses.append(status)
                self.logger.info(f"Task status added: {status}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add task status: {e}")
            return False

    def add_task_priority(self, priority: str) -> bool:
        """Add a custom task priority"""
        try:
            if priority not in self.task_priorities:
                self.task_priorities.append(priority)
                self.logger.info(f"Task priority added: {priority}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add task priority: {e}")
            return False

    def add_task_type(self, task_type: str) -> bool:
        """Add a custom task type"""
        try:
            if task_type not in self.task_types:
                self.task_types.append(task_type)
                self.logger.info(f"Task type added: {task_type}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to add task type: {e}")
            return False
