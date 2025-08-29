"""Task validation rule definitions and shared constants."""

from typing import List

from .base_validator import ValidationRule, ValidationSeverity

# Task status values recognised by the validation system.
TASK_STATUSES: List[str] = [
    "pending",
    "assigned",
    "in_progress",
    "review",
    "completed",
    "cancelled",
    "failed",
]

# Supported priority levels for tasks.
TASK_PRIORITIES: List[str] = ["low", "medium", "high", "critical", "urgent"]

# Supported task type categories.
TASK_TYPES: List[str] = [
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

# Default rules applied by ``TaskValidator``.
DEFAULT_TASK_RULES: List[ValidationRule] = [
    ValidationRule(
        rule_id="task_structure",
        rule_name="Task Structure",
        rule_type="task",
        description="Validate task data structure and format",
        severity=ValidationSeverity.ERROR,
    ),
    ValidationRule(
        rule_id="task_assignment_validation",
        rule_name="Task Assignment Validation",
        rule_type="task",
        description="Validate task assignment and ownership",
        severity=ValidationSeverity.ERROR,
    ),
    ValidationRule(
        rule_id="task_dependencies_validation",
        rule_name="Task Dependencies Validation",
        rule_type="task",
        description="Validate task dependencies and relationships",
        severity=ValidationSeverity.WARNING,
    ),
    ValidationRule(
        rule_id="task_progress_validation",
        rule_name="Task Progress Validation",
        rule_type="task",
        description="Validate task progress and timeline",
        severity=ValidationSeverity.WARNING,
    ),
]
