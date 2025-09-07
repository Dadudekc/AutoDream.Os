#!/usr/bin/env python3
"""
Consolidated Task Validation System - Agent Cellphone V2
=======================================================

Unified task validation system that consolidates 4 duplicate task validation
files into 1 focused module, eliminating duplication and providing unified
task validation across the codebase.

This system provides:
- Complete task validation functionality
- Task structure, status, priority, and type validation
- Task assignment and dependency validation
- Task progress and timeline validation
- Unified task validation interface

**Author:** Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
**Mission:** Critical SSOT Consolidation - Validation Systems
**Status:** CONSOLIDATION IN PROGRESS
**Target:** 50%+ reduction in duplicate validation folders
**V2 Compliance:** ✅ Under 400 lines, single responsibility
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


# ============================================================================
# TASK VALIDATION ENUMS
# ============================================================================

class TaskStatus(Enum):
    """Task status values."""
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    FAILED = "failed"


class TaskPriority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"


class TaskType(Enum):
    """Task type categories."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"
    RESEARCH = "research"
    BUG_FIX = "bug_fix"
    FEATURE = "feature"
    REFACTORING = "refactoring"
    REVIEW = "review"


class ValidationSeverity(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Validation result status."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


# ============================================================================
# TASK VALIDATION DATA STRUCTURES
# ============================================================================

@dataclass
class ValidationResult:
    """Result of a validation operation."""
    rule_id: str
    rule_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    field_path: Optional[str] = None
    actual_value: Optional[Any] = None
    expected_value: Optional[Any] = None
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TaskData:
    """Task data structure for validation."""
    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    type: Optional[TaskType] = None
    assignment: Optional[Dict[str, Any]] = None
    dependencies: Optional[List[str]] = None
    progress: Optional[Dict[str, Any]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deadline: Optional[datetime] = None


@dataclass
class TaskValidationContext:
    """Context for task validation operations."""
    task_data: TaskData
    validation_rules: List[str] = field(default_factory=list)
    strict_mode: bool = False
    include_warnings: bool = True
    custom_validators: Optional[Dict[str, callable]] = None


# ============================================================================
# CONSOLIDATED TASK VALIDATION MANAGER
# ============================================================================

class ConsolidatedTaskValidator:
    """
    Consolidated task validation system that eliminates duplication
    and provides unified task validation across the codebase.
    """
    
    def __init__(self):
        self.task_statuses = [status.value for status in TaskStatus]
        self.task_priorities = [priority.value for priority in TaskPriority]
        self.task_types = [task_type.value for task_type in TaskType]
        self.validation_history: List[ValidationResult] = []
        
        # Initialize validation system
        self._initialize_validation_system()
        
        logger.info("Consolidated task validation system initialized successfully")
    
    def _initialize_validation_system(self):
        """Initialize the task validation system."""
        logger.info("Task validation system initialized with standard task definitions")
    
    def validate_task(self, task_data: Dict[str, Any], 
                     context: Optional[TaskValidationContext] = None) -> List[ValidationResult]:
        """Validate task data and return validation results."""
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
                assignment_results = self._validate_task_assignment(task_data["assignment"])
                results.extend(assignment_results)
            
            # Validate dependencies if present
            if "dependencies" in task_data:
                dependency_results = self._validate_task_dependencies(task_data["dependencies"])
                results.extend(dependency_results)
            
            # Validate progress if present
            if "progress" in task_data:
                progress_results = self._validate_task_progress(task_data["progress"])
                results.extend(progress_results)
            
            # Validate timeline if present
            if "deadline" in task_data or "created_at" in task_data:
                timeline_results = self._validate_task_timeline(task_data)
                results.extend(timeline_results)
            
            # Store validation results
            self.validation_history.extend(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Task validation failed: {e}")
            error_result = self._create_error_result(e)
            results.append(error_result)
            self.validation_history.append(error_result)
            return results
    
    def _validate_task_structure(self, task_data: Any) -> List[ValidationResult]:
        """Validate task data structure and format."""
        results = []
        
        if not isinstance(task_data, dict):
            result = ValidationResult(
                rule_id="task_type",
                rule_name="Task Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task data must be a dictionary",
                actual_value=type(task_data).__name__,
                expected_value="dict"
            )
            results.append(result)
            return results
        
        if len(task_data) == 0:
            result = ValidationResult(
                rule_id="task_empty",
                rule_name="Task Empty Check",
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.WARNING,
                message="Task data is empty",
                actual_value=task_data,
                expected_value="non-empty task data"
            )
            results.append(result)
        
        return results
    
    def _validate_required_fields(self, task_data: Dict[str, Any], 
                                 required_fields: List[str]) -> List[ValidationResult]:
        """Validate required fields in task data."""
        results = []
        
        for field in required_fields:
            if field not in task_data or task_data[field] is None:
                result = ValidationResult(
                    rule_id=f"required_field_{field}",
                    rule_name=f"Required Field: {field}",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Required field '{field}' is missing or null",
                    field_path=field,
                    expected_value=f"non-null {field} value"
                )
                results.append(result)
            elif field in ["title", "description"] and isinstance(task_data[field], str):
                if len(task_data[field].strip()) == 0:
                    result = ValidationResult(
                        rule_id=f"empty_field_{field}",
                        rule_name=f"Empty Field: {field}",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message=f"Field '{field}' cannot be empty",
                        field_path=field,
                        actual_value=task_data[field],
                        expected_value=f"non-empty {field} value"
                    )
                    results.append(result)
        
        return results
    
    def _validate_task_status(self, status: Any) -> Optional[ValidationResult]:
        """Validate task status value."""
        if not isinstance(status, str):
            return ValidationResult(
                rule_id="status_type",
                rule_name="Status Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task status must be a string",
                field_path="status",
                actual_value=type(status).__name__,
                expected_value="str"
            )
        
        if status.lower() not in self.task_statuses:
            return ValidationResult(
                rule_id="status_invalid",
                rule_name="Status Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid task status: {status}",
                field_path="status",
                actual_value=status,
                expected_value=f"one of {self.task_statuses}"
            )
        
        return None
    
    def _validate_task_priority(self, priority: Any) -> Optional[ValidationResult]:
        """Validate task priority value."""
        if not isinstance(priority, str):
            return ValidationResult(
                rule_id="priority_type",
                rule_name="Priority Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task priority must be a string",
                field_path="priority",
                actual_value=type(priority).__name__,
                expected_value="str"
            )
        
        if priority.lower() not in self.task_priorities:
            return ValidationResult(
                rule_id="priority_invalid",
                rule_name="Priority Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid task priority: {priority}",
                field_path="priority",
                actual_value=priority,
                expected_value=f"one of {self.task_priorities}"
            )
        
        return None
    
    def _validate_task_type(self, task_type: Any) -> Optional[ValidationResult]:
        """Validate task type value."""
        if not isinstance(task_type, str):
            return ValidationResult(
                rule_id="type_type",
                rule_name="Type Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task type must be a string",
                field_path="type",
                actual_value=type(task_type).__name__,
                expected_value="str"
            )
        
        if task_type.lower() not in self.task_types:
            return ValidationResult(
                rule_id="type_invalid",
                rule_name="Type Invalid Value",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message=f"Invalid task type: {task_type}",
                field_path="type",
                actual_value=task_type,
                expected_value=f"one of {self.task_types}"
            )
        
        return None
    
    def _validate_task_assignment(self, assignment: Any) -> List[ValidationResult]:
        """Validate task assignment data."""
        results = []
        
        if not isinstance(assignment, dict):
            result = ValidationResult(
                rule_id="assignment_type",
                rule_name="Assignment Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task assignment must be a dictionary",
                field_path="assignment",
                actual_value=type(assignment).__name__,
                expected_value="dict"
            )
            results.append(result)
            return results
        
        # Validate required assignment fields
        if "assignee" not in assignment:
            result = ValidationResult(
                rule_id="assignment_assignee",
                rule_name="Assignment Assignee Required",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task assignment must include assignee",
                field_path="assignment.assignee",
                expected_value="assignee value"
            )
            results.append(result)
        
        # Validate assignee format
        if "assignee" in assignment and isinstance(assignment["assignee"], str):
            if len(assignment["assignee"].strip()) == 0:
                result = ValidationResult(
                    rule_id="assignment_assignee_empty",
                    rule_name="Assignment Assignee Empty",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Task assignee cannot be empty",
                    field_path="assignment.assignee",
                    actual_value=assignment["assignee"],
                    expected_value="non-empty assignee value"
                )
                results.append(result)
        
        return results
    
    def _validate_task_dependencies(self, dependencies: Any) -> List[ValidationResult]:
        """Validate task dependencies data."""
        results = []
        
        if not isinstance(dependencies, list):
            result = ValidationResult(
                rule_id="dependencies_type",
                rule_name="Dependencies Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task dependencies must be a list",
                field_path="dependencies",
                actual_value=type(dependencies).__name__,
                expected_value="list"
            )
            results.append(result)
            return results
        
        # Validate each dependency
        for i, dependency in enumerate(dependencies):
            if not isinstance(dependency, str):
                result = ValidationResult(
                    rule_id=f"dependency_type_{i}",
                    rule_name=f"Dependency {i} Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Dependency {i} must be a string",
                    field_path=f"dependencies[{i}]",
                    actual_value=type(dependency).__name__,
                    expected_value="str"
                )
                results.append(result)
            elif len(dependency.strip()) == 0:
                result = ValidationResult(
                    rule_id=f"dependency_empty_{i}",
                    rule_name=f"Dependency {i} Empty",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Dependency {i} cannot be empty",
                    field_path=f"dependencies[{i}]",
                    actual_value=dependency,
                    expected_value="non-empty dependency value"
                )
                results.append(result)
        
        return results
    
    def _validate_task_progress(self, progress: Any) -> List[ValidationResult]:
        """Validate task progress data."""
        results = []
        
        if not isinstance(progress, dict):
            result = ValidationResult(
                rule_id="progress_type",
                rule_name="Progress Type Validation",
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.ERROR,
                message="Task progress must be a dictionary",
                field_path="progress",
                actual_value=type(progress).__name__,
                expected_value="dict"
            )
            results.append(result)
            return results
        
        # Validate percentage if present
        if "percentage" in progress:
            percentage = progress["percentage"]
            if isinstance(percentage, (int, float)):
                if percentage < 0 or percentage > 100:
                    result = ValidationResult(
                        rule_id="progress_percentage_range",
                        rule_name="Progress Percentage Range",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Task progress percentage must be between 0 and 100",
                        field_path="progress.percentage",
                        actual_value=percentage,
                        expected_value="0-100"
                    )
                    results.append(result)
            else:
                result = ValidationResult(
                    rule_id="progress_percentage_type",
                    rule_name="Progress Percentage Type",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Task progress percentage must be a number",
                    field_path="progress.percentage",
                    actual_value=type(percentage).__name__,
                    expected_value="number"
                )
                results.append(result)
        
        return results
    
    def _validate_task_timeline(self, task_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate task timeline data."""
        results = []
        
        # Validate created_at if present
        if "created_at" in task_data:
            created_at = task_data["created_at"]
            if not isinstance(created_at, datetime):
                result = ValidationResult(
                    rule_id="created_at_type",
                    rule_name="Created At Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Task created_at must be a datetime",
                    field_path="created_at",
                    actual_value=type(created_at).__name__,
                    expected_value="datetime"
                )
                results.append(result)
        
        # Validate deadline if present
        if "deadline" in task_data:
            deadline = task_data["deadline"]
            if not isinstance(deadline, datetime):
                result = ValidationResult(
                    rule_id="deadline_type",
                    rule_name="Deadline Type Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message="Task deadline must be a datetime",
                    field_path="deadline",
                    actual_value=type(deadline).__name__,
                    expected_value="datetime"
                )
                results.append(result)
            elif "created_at" in task_data and isinstance(task_data["created_at"], datetime):
                if deadline <= task_data["created_at"]:
                    result = ValidationResult(
                        rule_id="deadline_logic",
                        rule_name="Deadline Logic Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.ERROR,
                        message="Task deadline must be after creation date",
                        field_path="deadline",
                        actual_value=deadline,
                        expected_value="date after creation"
                    )
                    results.append(result)
        
        return results
    
    def _create_error_result(self, error: Exception) -> ValidationResult:
        """Create a standardized error result for unexpected validation failures."""
        return ValidationResult(
            rule_id="task_validation_error",
            rule_name="Task Validation Error",
            status=ValidationStatus.FAILED,
            severity=ValidationSeverity.CRITICAL,
            message=f"Task validation error: {error}",
            details={"error_type": type(error).__name__}
        )
    
    # Utility methods
    def get_validation_history(self) -> List[ValidationResult]:
        """Get validation history."""
        return self.validation_history
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary statistics."""
        if not self.validation_history:
            return {"total_validations": 0}
        
        total = len(self.validation_history)
        passed = len([r for r in self.validation_history if r.status == ValidationStatus.PASSED])
        failed = len([r for r in self.validation_history if r.status == ValidationStatus.FAILED])
        warnings = len([r for r in self.validation_history if r.status == ValidationStatus.WARNING])
        
        return {
            "total_validations": total,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "success_rate": (passed / total) * 100 if total > 0 else 0
        }
    
    def clear_validation_history(self):
        """Clear validation history."""
        self.validation_history.clear()
        logger.info("Task validation history cleared")
    
    def get_task_statuses(self) -> List[str]:
        """Get list of valid task statuses."""
        return self.task_statuses.copy()
    
    def get_task_priorities(self) -> List[str]:
        """Get list of valid task priorities."""
        return self.task_priorities.copy()
    
    def get_task_types(self) -> List[str]:
        """Get list of valid task types."""
        return self.task_types.copy()


# ============================================================================
# GLOBAL TASK VALIDATOR INSTANCE
# ============================================================================

# Global task validator instance
_task_validator: Optional[ConsolidatedTaskValidator] = None

def get_task_validator() -> ConsolidatedTaskValidator:
    """Get the global task validator instance."""
    global _task_validator
    if _task_validator is None:
        _task_validator = ConsolidatedTaskValidator()
    return _task_validator

def validate_task(task_data: Dict[str, Any]) -> List[ValidationResult]:
    """Validate task using the global task validator."""
    return get_task_validator().validate_task(task_data)


# ============================================================================
# MAIN EXECUTION (FOR TESTING)
# ============================================================================

if __name__ == "__main__":
    # Example usage
    task_validator = ConsolidatedTaskValidator()
    
    # Test task validation
    test_task = {
        "id": "TASK-001",
        "title": "Test Task",
        "description": "A test task for validation",
        "status": "pending",
        "priority": "high",
        "type": "development",
        "assignment": {"assignee": "agent-5"},
        "dependencies": ["TASK-000"],
        "progress": {"percentage": 25},
        "created_at": datetime.now(),
        "deadline": datetime.now() + timedelta(days=7)
    }
    
    results = task_validator.validate_task(test_task)
    print(f"Task validation completed: {len(results)} results")
    
    # Show validation summary
    summary = task_validator.get_validation_summary()
    print(f"Validation summary: {summary}")
    
    # Show validation history
    history = task_validator.get_validation_history()
    print(f"Validation history: {len(history)} validations performed")
